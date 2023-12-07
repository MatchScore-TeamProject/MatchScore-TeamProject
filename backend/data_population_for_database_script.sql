

-- Insert users into users table. Password for everyone is 1234
INSERT INTO match_score_project.users (id, email, password, user_type) VALUES (1, 'admin@email.bg', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'admin');
INSERT INTO match_score_project.users (id, email, password, user_type) VALUES (2, 'rado@email.bg', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'user');
INSERT INTO match_score_project.users (id, email, password, user_type) VALUES (3, 'georgi@email.bg', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'user');
INSERT INTO match_score_project.users (id, email, password, user_type) VALUES (4, 'deyan@email.bg', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'user');
INSERT INTO match_score_project.users (id, email, password, user_type) VALUES (5, 'petur@email.bg', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'user');
INSERT INTO match_score_project.users (id, email, password, user_type) VALUES (6, 'ivan@email.bg', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'director');

-- Insert player_profiles into player_profile table
INSERT INTO match_score_project.player_profile (id, nickname, full_name, country, users_id) VALUES (1, 'rado', 'Radoslav Slavov Nedelkov', 'Bulgaria', NULL);
INSERT INTO match_score_project.player_profile (id, nickname, full_name, country, users_id) VALUES (2, 'georgi', 'Georgi Dodekov Ivanov', 'Bulgaria', NULL);
INSERT INTO match_score_project.player_profile (id, nickname, full_name, country, users_id) VALUES (3, 'deyan', 'Deyan Ivanov Petrov', 'Bulgaria', NULL);
INSERT INTO match_score_project.player_profile (id, nickname, full_name, country, users_id) VALUES (4, 'ivan', 'Ivan Petrov Ivanov', 'Bulgaria', NULL);
INSERT INTO match_score_project.player_profile (id, nickname, full_name, country, users_id) VALUES (5, 'Nedelko', 'Nedelko Ivanov Ivanov', 'Bulgaria', NULL);
INSERT INTO match_score_project.player_profile (id, nickname, full_name, country, users_id) VALUES (6, 'Petur', 'Petur Ivanov Ivanov', 'Bulgaria', NULL);

-- Insert matches into matches table. 1 finished and 1 with no results
INSERT INTO match_score_project.matches (date, format, tournament_id, player_profile_id1, player_profile_id2, score_1, score_2, winner, stage, order_num) VALUES ('2023-12-07', 'score', NULL, 2, 3, 1, 2, "georgi", 0, NULL);

INSERT INTO match_score_project.matches (date, format, tournament_id, player_profile_id1, player_profile_id2, score_1, score_2, winner, stage, order_num) VALUES ('2023-12-10', 'score', NULL, 4, 3, NULL, NULL, NULL, 0, NULL);

-- Insert a tournament into tournaments table
INSERT INTO match_score_project.tournaments(id, title, date, tournament_format, match_format,prize )VALUES (1, "World Cup 2024", "2024-10-11", "knockout", "score", 100000);

-- Insert the player_profiles ids into tournament_has_player_profile
INSERT INTO match_score_project.tournaments_has_player_profile (tournaments_id, player_profile_id) VALUES (1, 2);
INSERT INTO match_score_project.tournaments_has_player_profile (tournaments_id, player_profile_id) VALUES (1, 3);
INSERT INTO match_score_project.tournaments_has_player_profile (tournaments_id, player_profile_id) VALUES (1, 4);
INSERT INTO match_score_project.tournaments_has_player_profile (tournaments_id, player_profile_id) VALUES (1, 5);

-- Insert the matches for the tournament in matches table.
INSERT INTO match_score_project.matches (date, format, tournament_id, score_1, score_2, player_profile_id1, player_profile_id2, winner, stage, order_num) VALUES ("2024-10-11", "score", 1, NULL, NULL, 2, 3, NULL, 1, 1);
INSERT INTO match_score_project.matches (date, format, tournament_id, score_1, score_2, player_profile_id1, player_profile_id2, winner, stage, order_num) VALUES ("2024-10-11", "score", 1, NULL, NULL, 4, 5, NULL, 1, 2);
INSERT INTO match_score_project.matches (date, format, tournament_id, score_1, score_2, player_profile_id1, player_profile_id2, winner, stage, order_num) VALUES ("2024-10-11", "score", 1, NULL, NULL, NULL, NULL, NULL, 2, 3);



