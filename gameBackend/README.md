# Concentration Game backend


## Set-Up Instructions:
1.  Update the value of application in app.yaml to the app ID you have registered
 in the App Engine admin console and would like to use to host your instance of this sample.
1.  Run the app with the devserver using dev_appserver.py DIR, and ensure it's
 running by visiting the API Explorer - by default localhost:8080/_ah/api/explorer.
1.  Application is deployed at [here](https://game-backend-wc.appspot.com)


##Game Description:

Concentration is a simple guessing game. Each game begins with a random 'target'
string array with at least length of 4, and a maximum number of 'attempts'(currently equals to the length of the array).

'Guesses' are sent to the `make_move` endpoint providing the guess indexes for a pair in the string array, then replies with the guessed string and the current state of the array(correct guesses are visible to user, non correct guess is "")

Each game can be retrieved or played by using the path parameter
`urlsafe_game_key`.

User can get the leaderboard by with api 'get_high_scores' , and get oneself's
ranking with 'get_user_rankings'

##Files Included:
 - api.py: Contains endpoints and game playing logic.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.(send unfinished games to user every day)
 - main.py: Handler for taskqueue handler.
 - models.py: Entity and message definitions including helper methods.
 - utils.py: Helper function for retrieving ndb.Models by urlsafe Key string.

##Endpoints Included:
 - **create_user**
    - Path: 'user'
    - Method: POST
    - Parameters: user_name, email (optional)
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. user_name provided must be unique. Will
    raise a ConflictException if a User with that user_name already exists.

 - **new_game**
    - Path: 'game'
    - Method: POST
    - Parameters: user_name, min, max, attempts
    - Returns: GameForm with initial game state.
    - Description: Creates a new Game. user_name provided must correspond to an
    existing user - will raise a NotFoundException if not. Min must be less than
    max. Also adds a task to a task queue to update the average moves remaining
    for active games.

 - **get_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: GameForm with current game state.
    - Description: Returns the current state of a game.

 - **make_move**
    - Path: 'game/{urlsafe_game_key}'
    - Method: PUT
    - Parameters: urlsafe_game_key, guess
    - Returns: GameForm with new game state.
    - Description: Accepts a 'guess' and returns the updated state of the game.
    If this causes a game to end, a corresponding Score entity will be created.

 - **get_scores**
    - Path: 'scores'
    - Method: GET
    - Parameters: None
    - Returns: ScoreForms.
    - Description: Returns all Scores in the database (unordered).

  - **get_high_scores**
     - Path: 'scores/leaderboard'
     - Method: GET
     - Parameters: top_k
     - Returns: UserScoreForms.
     - Description: Generate a leader-board (high scores in descending order).
        Accept an optional parameter number_of_results that limits
        the number of results returned.

  - **get_user_rankings**
     - Path: 'rank'
     - Method: GET
     - Parameters: user_name, email
     - Returns: UserRankForm.
     - Description: rank user by how many games won, each won game worth 1 point
        on the leaderboard, get and set rank/score info in memcache
        for fast retriving.

 - **get_user_scores**
    - Path: 'scores/user/{user_name}'
    - Method: GET
    - Parameters: user_name
    - Returns: ScoreForms.
    - Description: Returns all Scores recorded by the provided player (unordered).
    Will raise a NotFoundException if the User does not exist.

 - **get_average_attempts**
    - Path: 'games/average_attempts'
    - Method: GET
    - Parameters: user_name,email
    - Returns: GameForms
    - Description: Get the cached average moves remaining.

- **get_user_games**
   - Path: 'game/user/{user_name}'
   - Method: GET
   - Parameters: user_name,email
   - Returns: StringMessage
   - Description: Return all of a User's active games.

- **cancel_game**
  - Path: 'user/game/{urlsafe_game_key}'
  - Method: GET
  - Parameters: user_name,urlsafe_game_key
  - Returns: StringMessage
  - Description: allows users to cancel a game in progress.

- **get_game_history**
  - Path: 'game/history/{urlsafe_game_key}'
  - Method: GET
  - Parameters:urlsafe_game_key
  - Returns: GameHistoryForm
  - Description: retrieve game history for each round


##Models Included:
 - **User**
    - Stores unique user_name and (optional) email address.

 - **Game**
    - Stores unique game states. Associated with User model via KeyProperty.

 - **Score**
    - Records completed games. Associated with Users model via KeyProperty.

##Forms Included:
 - **GameStateForm**
   - Representation of a Game's state for history Representation(guessed_strings, current_state,  message, attempts_remaining, game_over flag).

 - **GameHistoryForm**
   - Representation of a Game's history.Built on GameStateForm.
   - Multiple GameStateForm container.

 - **GameForm**
    - Representation of a Game's state (urlsafe_key, attempts_remaining,
    game_over flag, message, user_name, current_state, guessed_strings).

 - **NewGameForm**
    - Used to create a new game (user_name, min, max, attempts)
    -
 - **MakeMoveForm**
    - Inbound make move form (guess).

- **UserRankForm**
   - Representation of a user's rank (user_name, rank).

- **UserScoreForm**
    - Representation of a completed user Score (user_name, score).

- **UserScoreForms**
   - Representation of a completed users Score .
   - Multiple UserScoreForm container.

- **ScoreForm**
    - Representation of a completed game's Score (user_name, date, won flag,
    guesses).

 - **ScoreForms**
    - Multiple ScoreForm container.

 - **StringMessage**
    - General purpose String container.
