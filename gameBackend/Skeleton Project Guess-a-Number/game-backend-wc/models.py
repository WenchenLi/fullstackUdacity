"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

import random, string
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb
import json

class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email =ndb.StringProperty()


class Game(ndb.Model):
    """Game object"""
    target = ndb.StringProperty(repeated=True)
    attempts_allowed = ndb.IntegerProperty(required=True)
    attempts_remaining = ndb.IntegerProperty(required=True, default=5)
    game_over = ndb.BooleanProperty(required=True, default=False)
    user = ndb.KeyProperty(required=True, kind='User')

    #current correct guess in the same format of target
    current_state = ndb.StringProperty(repeated=True)
    current_message = ndb.StringProperty()
    current_guessed_strings = ndb.StringProperty(repeated=True)
    history = ndb.JsonProperty(repeated=True)

    @classmethod
    def new_game(cls, user, min, max, attempts):
        """Creates and returns a new game"""

        def content_generator(pair_count):
            """
            generate target repeated string property aka,
            the string array for user to play with
            """
            def randomword(length):
                return ''.join(random.choice(string.lowercase) for i in range(length))

            res = []
            for i in xrange(pair_count):
                res.append(randomword(random.randint(1, 10)))#be a variable
            res += res
            random.shuffle(res)
            return res

        if max < min:
            raise ValueError('Maximum must be greater than minimum')
        pair_count = random.choice(range(2, max + 1))
        game = Game(user=user,
                    target=content_generator(pair_count),
                    current_state = ['']*(pair_count*2),
                    attempts_allowed=pair_count*2,
                    attempts_remaining=pair_count*2,
                    game_over=False,
                    parent=user,
                    current_message="",
                    current_guessed_strings=["",""])
        game.put()
        return game

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.attempts_remaining = self.attempts_remaining
        form.game_over = self.game_over
        form.message = message
        form.current_state = self.current_state

        self.current_message = message
        return form

    def to_form_with_current_guessed_result(self, message, guessed_strings):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.attempts_remaining = self.attempts_remaining
        form.game_over = self.game_over
        form.message = message
        form.current_state = self.current_state
        form.guessed_strings = guessed_strings

        self.current_guessed_strings = guessed_strings
        self.current_message = message
        return form

    def to_form_raw(self):
        """
        Returns a GameForm representation of the Game including current message
        and current guessed strings
        """
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.attempts_remaining = self.attempts_remaining
        form.game_over = self.game_over
        form.message = self.current_message
        form.user_name = self.user.get().name
        form.current_state = self.current_state
        form.guessed_strings = self.current_guessed_strings

        return form

    def to_form_history(self):
        """
        Returns a GameHistoryForm representation of the Game
        """

        states = [json.loads(state) for state in self.history]
        print states
        return GameHistoryForm(items=[
                GameStateForm(guessed_strings=state["guess"],
                            current_state=state["state"],
                            message=state["message"],
                            attempts_remaining=state["attempts_remaining"],
                            game_over=state["game_over"]
                            ) for state in states])

    def end_game(self, won=False):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True
        self.put()
        # Add the game to the score 'board'
        score = Score(user=self.user, date=date.today(), won=won,
                      guesses=self.attempts_allowed - self.attempts_remaining)
        score.put()


class Score(ndb.Model):
    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    guesses = ndb.IntegerProperty(required=True)

    def to_form(self):
        return ScoreForm(user_name=self.user.get().name, won=self.won,
                         date=str(self.date), guesses=self.guesses)

class GameStateForm(messages.Message):
    """GameStateForm for outbound game state information"""
    guessed_strings = messages.StringField(1, repeated=True)
    current_state = messages.StringField(2, repeated=True)
    message = messages.StringField(3, required=True)
    attempts_remaining = messages.IntegerField(4, required=True)
    game_over = messages.BooleanField(5, required=True)


class GameHistoryForm(messages.Message):
    """GameHistoryForm for outbound game state information"""
    items = messages.MessageField(GameStateForm, 1, repeated=True)

class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    attempts_remaining = messages.IntegerField(2, required=True)
    game_over = messages.BooleanField(3, required=True)
    message = messages.StringField(4, required=True)
    user_name = messages.StringField(5, required=True)
    current_state = messages.StringField(6,repeated=True)
    guessed_strings = messages.StringField(7,repeated=True)

class GameForms(messages.Message):
    """GameForms for outbound game state information"""
    items = messages.MessageField(GameForm, 1, repeated=True)

class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_name = messages.StringField(1, required=True)
    min = messages.IntegerField(2, default=1)
    max = messages.IntegerField(3, default=10)
    attempts = messages.IntegerField(4, default=5)

class MakeMoveForm(messages.Message):
    """Used to make a move in an existing game"""
    guess = messages.IntegerField(1, repeated=True)

class UserRankForm(messages.Message):
    """UserScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    rank = messages.IntegerField(2, required=True)

class UserScoreForm(messages.Message):
    """UserScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    score = messages.IntegerField(2, required=True)

class UserScoreForms(messages.Message):
    """UserScoreForms for all outbound Score information"""
    items = messages.MessageField(UserScoreForm, 1, repeated=True)

class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    guesses = messages.IntegerField(4, required=True)


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
