## MatchScore

## 1. Description
MatchScore project is a complete solution designed to simplify the organization and management of sports events, mainly serving tournaments and matches. The system offers a range of features which support sports competitions, including both one-off matches and structured tournaments in knockout or league formats.The main purpose of the application to register events with participants on certain dates and adding results of played matches.
We use the FASTAPI swagger for the project.
- `To go to the swagger after you've ran main.py`:http://127.0.0.1:8001/docs
- `Link to  Repo`: https://github.com/MatchScore-TeamProject/MatchScore-TeamProject
 
## 2. Application features
 
 
### User Section
- `POST /users/register`  Register User
- `POST /users/login`  Sign In With credentials
- `GET /users/{id}`   Show User Info 
- `POST /users/link-request`  Create User-Player Request
- `PUT /users/link-request/approve/{link_request_id}` Approve User-Player Request
- `PUT /users/link-request/deny/{link_request_id}` Deny User-Player Request
- `POST /users/promote-request` Create Promote Request
- `PUT /users/promote-request/approve/{promote_request_id}` Approve Promote Request
- `PUT /users/promote-request/deny/{promote_request_id}` Deny Promote Request
- `PUT/users/edit/{id}` Edit User Info
- `DELETE/users/delete/{id}` Delete User
 
 
### Player Profile Section
- `POST /players/create`  Create Player Profile 
- `GET/players/view-player/{nickname}`  View Player
- `PUT /players/edit/{player_profile_id}` Edit Player Profile 
- `DELETE/players/delete`  Delete Player Profile
 
### Matches Section
- `POST/matches/` Create Match
- `GET/matches/` Get All Matches
- `PUT/matches/update/{id}`  Update Match By Id
- `DELETE/matches/delete/{id}` Delete Match
 
### Tournaments Section
- `POST/tournaments/create` Create
- `GET/tournaments/` Get All
- `GET/tournaments/{tournament_name}` Get Tournament By Name
- `GET/tournaments/standings/{league_name}` Get League Standings
- `PUT/tournaments/{tournament_id}/update_match_winner`Updates Match Winner By Tournament ID
- `DELETE/tournaments/delete/{tournament_id}`Delete Tournament 
 
### Database Tables
 
 <div style="text-align:left; margin: 20px;">
    <img src="https://cdn.discordapp.com/attachments/1171044849240264768/1182020805907980369/EER_DIAGRADM.png" alt="Database Diagram" width="600px" />
    <p style="margin-top: 10px;">Database Structure for MatchScore Application</p>
</div>
 
****
Team:
D. TOTIN,
G. DODEKOV,
R. SLAVOV
****