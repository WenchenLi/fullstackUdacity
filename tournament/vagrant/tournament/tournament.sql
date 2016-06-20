-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE player ( player_id SERIAL primary key,
                       player_name TEXT
                      );

CREATE TABLE match ( match_id SERIAL primary key,
                       winner integer REFERENCES player (player_id),
                       loser integer REFERENCES player (player_id)
                      );

CREATE VIEW player_standings AS
	SELECT
		player.player_id,
		player.player_name,
		count(match.winner) as wins,
		(select count(*) from match where player.player_id = match.winner or player.player_id = match.loser) as matches
	from
		player
	left join --player exist before match
		match on
	 		player.player_id = match.winner
	group by player.player_id
	order by wins desc;
