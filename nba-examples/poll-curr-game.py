from nba_api.live.nba.endpoints import scoreboard
import time
import json
from datetime import datetime


## poll_game_updates() ##
## poll updates for updating scoreboard quickly ##
## args: game_id(game we are monitoring), polling_interval(poll freq in terms of secs) ##
# find specific game from main #
# get current game info #
# check for updates on x interval #
# only print if something changes #
# save values for next iteration #
def poll_game_updates(game_id, polling_interval=30, max_polls=None):
    """
    Polls for updates on a specific NBA game.
    
    Args:
        game_id (str): The NBA game ID to monitor
        polling_interval (int): Seconds to wait between polls (default: 30)
        max_polls (int, optional): Maximum number of polls before stopping (None = unlimited)
    """
    poll_count = 0
    last_score = {'home': None, 'away': None}
    last_period = None
    last_status = None
    
    print(f"Starting to poll for game ID: {game_id}")
    print(f"Press Ctrl+C to stop polling\n")
    
    try:

        while max_polls is None or poll_count < max_polls:
          
            games = scoreboard.ScoreBoard()
            data = games.get_dict()
            
            game = None
            for g in data['scoreboard']['games']:
                if g['gameId'] == game_id:
                    game = g
                    break
            
            if not game:
                print(f"Game ID {game_id} not found in today's schedule.")
                break  
            
            current_time = datetime.now().strftime("%H:%M:%S")
            
            away_team = f"{game['awayTeam']['teamCity']} {game['awayTeam']['teamName']}"
            home_team = f"{game['homeTeam']['teamCity']} {game['homeTeam']['teamName']}"
            away_score = game['awayTeam']['score']
            home_score = game['homeTeam']['score']
            status = game['gameStatusText']
            period = game['period']
            clock = game['gameClock']
            
            score_changed = (last_score['home'] != home_score or last_score['away'] != away_score)
            period_changed = last_period != period
            status_changed = last_status != status
            
            if poll_count == 0 or score_changed or period_changed or status_changed:
                print(f"[{current_time}] {away_team} {away_score} - {home_score} {home_team}")
                print(f"Status: {status} | Period: {period} | Clock: {clock}")
                
                if poll_count > 0:
                    changes = []
                    if score_changed:
                        score_diff = ""
                        if last_score['home'] is not None and last_score['away'] is not None:
                            home_diff = home_score - last_score['home']
                            away_diff = away_score - last_score['away']
                            if home_diff > 0:
                                score_diff += f" {home_team} +{home_diff}"
                            if away_diff > 0:
                                score_diff += f" {away_team} +{away_diff}"
                        changes.append(f"Score changed:{score_diff}")
                    if period_changed:
                        changes.append(f"Period changed: {last_period} → {period}")
                    if status_changed:
                        changes.append(f"Status changed: {last_status} → {status}")
                    
                    print("UPDATES: " + ", ".join(changes))
                print("-" * 50)
            
            last_score['home'] = home_score
            last_score['away'] = away_score
            last_period = period
            last_status = status
            
            if status.lower() in ["final", "game over", "finished"]:
                print(f"\nGame has ended. Final score: {away_team} {away_score} - {home_score} {home_team}")
                break  
            
            poll_count += 1
            
            time.sleep(polling_interval)
            
    except KeyboardInterrupt:
        print("\nPolling stopped by user.")
    except Exception as e:
        print(f"\nError occurred: {e}")
    
    print(f"\nCompleted {poll_count} polls for game ID: {game_id}")

if __name__ == "__main__":

    EXAMPLE_GAME_ID = "1234567"  
    
    poll_game_updates(EXAMPLE_GAME_ID, polling_interval=30)
