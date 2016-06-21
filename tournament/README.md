
# Tournament
A [swiss tournament](https://en.wikipedia.org/wiki/Swiss-system_tournament) database built upon PostgreSQL corresponding python db-api.

* tournament.sql : contain database schema and necessary view
* tournament.py ­ ​:
this file is used to provide access to your database via a library of
functions which can add, delete or query data in your database to another python
program (a client program).

### tounament.py includes:

##### registerPlayer(name)
Adds a player to the tournament by putting an entry in the database. The database should assign an ID number to the player. Different players may have the same names but will receive different ID numbers.

##### countPlayers()
Returns the number of currently registered players. This function should not use the Python len() function; it should have the database count the players.

##### deletePlayers()
Clear out all the player records from the database.

##### reportMatch(winner, loser)
Stores the outcome of a single match between two players in the database.

##### deleteMatches()
Clear out all the match records from the database.

##### playerStandings()
Returns a list of (id, name, wins, matches) for each player, sorted by the number of wins each player has.

##### swissPairings()
Given the existing set of registered players and the matches they have played, generates and returns a list of pairings according to the Swiss system. Each pairing is a tuple (id1, name1, id2, name2), giving the ID and name of the paired players. For instance, if there are eight registered players, this function should return four pairings. This function should use playerStandings to find the ranking of players.

## Quick Run
To test the implementation please navigate to vagrant/tournament
and to setup the database schema use:

```psql - f tournament.sql```

to run the test script:

```python tournament_test.py```


## Using the Vagrant Virtual Machine  
  This project is run in vagrant VM, please follow the below instruction to setup the working enviroment:

 The Vagrant VM has PostgreSQL installed and configured, as well as the psql
command line interface (CLI)​
 , so that you don't have to install or configure them on your
local machine.
To use the Vagrant virtual machine, navigate to the
vagrant/tournament directory in the terminal, then ​
 use the command

```vagrant up ​```
(powers on the virtual machine)
followed by

```vagrant ​ssh ​```
 (logs into the
virtual machine)​  

once you have executed the ​
 vagrant ssh ​
 command, you will want to cd
 ​
/vagrant ​
 to change directory to the ​
 synced folders​

The Vagrant VM provided in the already has PostgreSQL server installed,
as well as the psql command line interface (CLI).
