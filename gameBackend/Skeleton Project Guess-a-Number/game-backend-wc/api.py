# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""


import logging
import endpoints
from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue
from collections import Counter

from models import User, Game, Score
from models import StringMessage, NewGameForm, GameForm, GameForms,\
    MakeMoveForm, ScoreForms, UserScoreForm, UserScoreForms, UserRankForm,\
    GameHistoryForm
from utils import get_by_urlsafe

import json


NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)

GET_GAME_REQUEST = endpoints.ResourceContainer(
        urlsafe_game_key=messages.StringField(1),)

CANCEL_GAME_REQUEST = endpoints.ResourceContainer(
        urlsafe_game_key=messages.StringField(1),
        user_name=messages.StringField(2))

MAKE_MOVE_REQUEST = endpoints.ResourceContainer(
    MakeMoveForm,
    urlsafe_game_key=messages.StringField(1),)
USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1,required=True),
                                           email=messages.StringField(2))

LEADERBOARD_REQUEST = endpoints.ResourceContainer(
        top_k=messages.IntegerField(1,default=10),)

MEMCACHE_MOVES_REMAINING = 'MOVES_REMAINING'
MEMCACHE_LEADERBOARD = 'LEADERBOARD'

@endpoints.api(name='concentration', version='v1')
class ConcentrationApi(remote.Service):
    """Game API"""
    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                    'A User with that name already exists!')

        if User.query(User.email == request.email).get():
            raise endpoints.ConflictException(
                    'A User with that email already exists!')

        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(message='User {} created!'.format(
                request.user_name))

    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      path='game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Creates new game"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        try:
            game = Game.new_game(user.key, request.min,
                                 request.max, request.attempts)
        except ValueError:
            raise endpoints.BadRequestException('Maximum must be greater '
                                                'than minimum!')

        # Use a task queue to update the average attempts remaining.
        # This operation is not needed to complete the creation of a new game
        # so it is performed out of sequence.
        taskqueue.add(url='/tasks/cache_average_attempts')
        return game.to_form('Good luck pairing all the random strings!!')

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, request):
        """Return the current game state."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return game.to_form('Time to make a move!')
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=MAKE_MOVE_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='make_move',
                      http_method='PUT')
    def make_move(self, request):
        """Makes a move. Returns a game state with message"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game.game_over:
            return game.to_form('Game already over!')

        if len(request.guess) != 2:
            return game.to_form("Please give a pair you think match!")

        if request.guess[0] >= len(game.target) or\
            request.guess[1] >= len(game.target):
            return game.to_form("You enter an index that is"
                                " not exist for this game")

        if game.current_state[request.guess[0]] or\
            game.current_state[request.guess[1]]:
            return game.to_form("Aren't you already got part of the result?")

        if game.target[request.guess[0]] == game.target[request.guess[1]]:
            msg = 'You got one pair!'
            game.current_state[request.guess[0]] = game.target[request.guess[0]]
            game.current_state[request.guess[1]] = game.target[request.guess[1]]
        else:
            msg = 'sorry, it\'s not a match'

        game.attempts_remaining -= 1
        if game.current_state == game.target:
            game.end_game(True)
            return game.to_form('You win!')

        #keep game history
        game.history.append(json.dumps({"guess":[game.target[request.guess[0]],
                                      game.target[request.guess[1]]],
                             "state":game.current_state,
                             "message":msg,
                             "attempts_remaining":game.attempts_remaining,
                             "game_over":game.game_over}))

        if game.attempts_remaining < 1:
            game.end_game(False)
            game.put()
            return game.to_form(msg + ' Game over!')
        else:
            game.put()
            return game.to_form_with_current_guessed_result(msg,
                [game.target[request.guess[0]], game.target[request.guess[1]]])

    @endpoints.method(response_message=ScoreForms,
                      path='scores',
                      name='get_scores',
                      http_method='GET')
    def get_scores(self, request):
        """Return all scores"""
        return ScoreForms(items=[score.to_form() for score in Score.query()])

    @endpoints.method(request_message=LEADERBOARD_REQUEST,
                      response_message=UserScoreForms,
                      path='scores/leaderboard',
                      name='get_high_scores',
                      http_method='GET')
    def get_high_scores(self, request):
        """
        Generate a leader-board (high scores in descending order).
        Accept an optional parameter number_of_results that limits
        the number of results returned.
        """
        k = request.top_k
        filtered_ct = memcache.get(MEMCACHE_LEADERBOARD)

        if filtered_ct is not None:
            data = UserScoreForms(items=[UserScoreForm(
                    user_name=item[0], score=item[1])
                    for item in filtered_ct.most_common(int(k))])
        else:
            filtered_ct, _ = self.calculateLeaderBoardAndRank()
            data = UserScoreForms(items=[UserScoreForm(
                    user_name=item[0], score=item[1])
                    for item in filtered_ct.most_common(int(k))])
        return data

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=UserRankForm,
                      path='rank',
                      name='get_user_rankings',
                      http_method='GET')
    def get_user_rankings(self, request):
        """
        rank user by how many games won, each won game worth 1 point
        on the leaderboard, get and set rank/score info in memcache
        for fast retriving.
        """
        user_rank = memcache.get(request.user_name)
        if user_rank is not None:
            data = UserRankForm(user_name=request.user_name, rank=user_rank)
        else:
            _, rank_dict = self.calculateLeaderBoardAndRank()
            data = UserRankForm(user_name=request.user_name,
                            rank=rank_dict[request.user_name])
        return data

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=ScoreForms,
                      path='scores/user/{user_name}',
                      name='get_user_scores',
                      http_method='GET')
    def get_user_scores(self, request):
        """
        Returns all of an individual User's scores
        get and set rank/score info in memcache
        for fast retriving
        """
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        scores = Score.query(Score.user == user.key)
        return ScoreForms(items=[score.to_form() for score in scores])

    @endpoints.method(response_message=StringMessage,
                      path='games/average_attempts',
                      name='get_average_attempts_remaining',
                      http_method='GET')
    def get_average_attempts(self, request):
        """Get the cached average moves remaining"""
        return StringMessage(message=memcache.get(MEMCACHE_MOVES_REMAINING) or '')

    @endpoints.method(request_message=USER_REQUEST,#need to change
                      response_message=GameForms,
                      path='game/user/{user_name}',
                      name='get_user_games',
                      http_method='GET')
    def get_user_games(self, request):
        """Return all of a User's active games."""
        user = User.query(User.name == request.user_name).get()
        games = Game.query(Game.game_over == False, Game.user == user.key)

        items = [game.to_form_raw() for game in games]
        return GameForms(items=[game.to_form_raw() for game in games])

    @endpoints.method(request_message=CANCEL_GAME_REQUEST,
                      response_message=StringMessage,
                      path='user/game/{urlsafe_game_key}',
                      name='cancel_game',
                      http_method='GET')
    def cancel_game(self, request):
        """
        allows users to cancel a game in progress.
        """
        msg = StringMessage()
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        user = User.query(User.name == request.user_name).get()
        if game.user!= user.key:
            msg.message = "You are not allowed to cancel other's game"
        else:
            if game.game_over:
                msg.message = "Game was already over, you can't cancel it"
            else:
                game.key.delete()
                msg.message = "Game canceled."
        return msg

    @endpoints.method(request_message=GET_GAME_REQUEST,#need to change
                      response_message=GameHistoryForm,
                      path='game/history/{urlsafe_game_key}',
                      name='get_game_history',
                      http_method='GET')
    def get_game_history(self, request):
        """
        retrieve game history for each round
        """
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return game.to_form_history()
        else:
            raise endpoints.NotFoundException('Game not found!')

    @staticmethod
    def calculateLeaderBoardAndRank():
        """given score, calculate leaderboard and user rank and set them to memcache"""
        #it's a simple score, won count 1
        items = [score.to_form() for score in Score.query()]
        rank_dict = {item.user_name:0 for item in items}
        leaderboard_dict = {item.user_name:0 for item in items}
        for item in items:
            if item.won == True:
                leaderboard_dict[item.user_name] += 1
        filtered_ct = Counter(leaderboard_dict)
        temp_rank = filtered_ct.most_common(len(filtered_ct))
        for j, item in enumerate(temp_rank):
            rank_dict[item[0]] = j+1

        memcache.set_multi(
            rank_dict,
            time=1200
        )
        memcache.add(key=MEMCACHE_LEADERBOARD, value=filtered_ct, time=1200)

        return filtered_ct,rank_dict

    @staticmethod
    def gameReminderhelper():
        """
        for each user, return a dictionalry with email as key,corresponding
        game keys in a list as value
        """
        #it's a simple score, won count 1
        users_with_email = User.query(User.email != None)
        rest = {}
        for user_with_email in users_with_email:
            user = User.query(User.name == user_with_email.name).get()
            games = Game.query(Game.game_over == False,  Game.user == user.key)
            rest[user.email] = []
            for game in games:
                if game.user == user.key:
                    rest[user.email].append(game.key.urlsafe())
        return rest

    @staticmethod
    def _cache_average_attempts():
        """Populates memcache with the average moves remaining of Games"""
        games = Game.query(Game.game_over == False).fetch()
        if games:
            count = len(games)
            total_attempts_remaining = sum([game.attempts_remaining
                                        for game in games])
            average = float(total_attempts_remaining)/count
            memcache.set(MEMCACHE_MOVES_REMAINING,
                         'The average moves remaining is {:.2f}'.format(average))

api = endpoints.api_server([ConcentrationApi])
