-- The password for the users is 1234.

INSERT INTO match_score_project.tournaments(id, title, date, tournament_format, match_format,prize )VALUES (1, "World Cup 2024", "2024-10-11", "knockout", "score", 100000);

INSERT INTO match_score_project.tournaments_has_player_profile(tournaments_id, player_profile_id) VALUES (1, 1);
INSERT INTO match_score_project.tournaments_has_player_profile(tournaments_id, player_profile_id) VALUES (1, 2);
INSERT INTO match_score_project.tournaments_has_player_profile(tournaments_id, player_profile_id) VALUES (1, 3);
INSERT INTO match_score_project.tournaments_has_player_profile(tournaments_id, player_profile_id) VALUES (1, 4);

INSERT INTO match_score_project.matches(id, date, format, tournament_id, score_1, score_2, player_profile_id1, player_profile_id2, winner, stage, order_num) VALUES (1, "2024-10-11", "score", 1, NULL, NULL, 1, 2, NULL, 1, 1);
INSERT INTO match_score_project.matches(id, date, format, tournament_id, score_1, score_2, player_profile_id1, player_profile_id2, winner, stage, order_num) VALUES (2, "2024-10-11", "score", 1, NULL, NULL, 3, 4, NULL, 1, 2);
INSERT INTO match_score_project.matches(id, date, format, tournament_id, score_1, score_2, player_profile_id1, player_profile_id2, winner, stage, order_num) VALUES (3, "2024-10-11", "score", 1, NULL, NULL, NULL, NULL, NULL, 2, 3);