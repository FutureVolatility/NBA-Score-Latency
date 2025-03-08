from nba_api.live.nba.endpoints import scoreboard
import json
from datetime import datetime

## get_current_game() ##
## get list of current games & returns id / other data ##
# get today scoreboard & games date # 
# store all game ids for today #
# check if game data, if so print each #
# print team info, score info, game status, game time, 
# current period #
def get_current_games():

    games = scoreboard.ScoreBoard()
    
    data = games.get_dict()
    
    game_date = data['scoreboard']['gameDate']
    formatted_date = datetime.strptime(game_date, "%Y-%m-%d").strftime("%B %d, %Y")
    
    print(f"\n===== NBA GAMES FOR {formatted_date} =====\n")
    
    game_ids = []
    
    if not data['scoreboard']['games']:
        print("No games scheduled for today.")
        return game_ids
    
    for game in data['scoreboard']['games']:
        game_id = game['gameId']
        game_ids.append(game_id)
        
        away_team = f"{game['awayTeam']['teamCity']} {game['awayTeam']['teamName']}"
        home_team = f"{game['homeTeam']['teamCity']} {game['homeTeam']['teamName']}"
        away_record = f"({game['awayTeam']['wins']}-{game['awayTeam']['losses']})"
        home_record = f"({game['homeTeam']['wins']}-{game['homeTeam']['losses']})"
        
        away_score = game['awayTeam']['score']
        home_score = game['homeTeam']['score']
        
        status = game['gameStatusText']
        
        game_time = game['gameEt'] if status == "Scheduled" else ""
        
        period = f"Q{game['period']}" if game['period'] > 0 else ""
        clock = game['gameClock'] if game['gameClock'] else ""
        
        time_display = f" - {game_time}" if game_time else f" - {period} {clock}".strip()
        
        print(f"Game ID: {game_id}")
        print(f"{away_team} {away_record} @ {home_team} {home_record}")
        print(f"Score: {away_score}-{home_score}")
        print(f"Status: {status}{time_display}")
        
        if game['gameStatus'] >= 2:  
            try:
                away_leader = game['gameLeaders']['awayLeaders']
                home_leader = game['gameLeaders']['homeLeaders']
                
                print("\nGame Leaders:")
                print(f"  {away_team}: {away_leader['name']} - {away_leader['points']}pts, {away_leader['rebounds']}reb, {away_leader['assists']}ast")
                print(f"  {home_team}: {home_leader['name']} - {home_leader['points']}pts, {home_leader['rebounds']}reb, {home_leader['assists']}ast")
            except (KeyError, TypeError):
                print("Game leader stats not available yet")
        
        print("\n" + "-" * 50 + "\n")
    
    print(f"Found {len(game_ids)} games.")
    print("Game IDs for use in polling script:")
    print(', '.join(game_ids))
    
    return game_ids

if __name__ == "__main__":
    get_current_games()

# example data of repsone based on format # 
"""
{
    "meta": {"version": 1, "request": "", "time": "", "code": 200},
    "scoreboard": {
        "gameDate": "2025-03-08",
        "leagueId": "00",
        "leagueName": "National Basketball Association",
        "games": [
            {
                "gameId": "0022400123",
                "gameCode": "20250308/LALBOS",
                "gameStatus": 2,
                "gameStatusText": "In Progress",
                "period": 3,
                "gameClock": "6:24",
                "gameTimeUTC": "2025-03-08T20:00:00Z",
                "gameEt": "3:00 PM ET",
                "regulationPeriods": 4,
                "homeTeam": {
                    "teamId": 1610612738,
                    "teamName": "Celtics",
                    "teamCity": "Boston",
                    "teamTricode": "BOS",
                    "wins": 41,
                    "losses": 12,
                    "score": 78,
                    "inBonus": "1",
                    "timeoutsRemaining": 4,
                    "periods": [
                        {"period": 1, "periodType": "REGULAR", "score": 28},
                        {"period": 2, "periodType": "REGULAR", "score": 26},
                        {"period": 3, "periodType": "REGULAR", "score": 24}
                    ]
                },
                "awayTeam": {
                    "teamId": 1610612747,
                    "teamName": "Lakers",
                    "teamCity": "Los Angeles",
                    "teamTricode": "LAL",
                    "wins": 35,
                    "losses": 26,
                    "score": 72,
                    "inBonus": "1",
                    "timeoutsRemaining": 3,
                    "periods": [
                        {"period": 1, "periodType": "REGULAR", "score": 23},
                        {"period": 2, "periodType": "REGULAR", "score": 25},
                        {"period": 3, "periodType": "REGULAR", "score": 24}
                    ]
                },
                "gameLeaders": {
                    "homeLeaders": {
                        "personId": 1628369,
                        "name": "J. Tatum",
                        "jerseyNum": "0",
                        "position": "F",
                        "teamTricode": "BOS",
                        "points": 24,
                        "rebounds": 8,
                        "assists": 5
                    },
                    "awayLeaders": {
                        "personId": 2544,
                        "name": "L. James",
                        "jerseyNum": "23",
                        "position": "F",
                        "teamTricode": "LAL",
                        "points": 26,
                        "rebounds": 7,
                        "assists": 9
                    }
                }
            }
            // More games would be listed here
        ]
    }
}
"""