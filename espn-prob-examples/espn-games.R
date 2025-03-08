## get_current_espn_games.R ##
## fets all games from ESPN for today & filters for those in progress ##
# get_current_espn_games: get all current games from ESPN #
# get date in YYYYMMDD format #
# get NBA scoreboard for today #
# filter for games currently in progress ("in" means the game is in progress) #
# if no games, return no games in progress #
# select: game_id + others #
# print summary of current games #
# save current game to rds for polling script # 
# execute #

library(hoopR)

get_current_espn_games <- function() {
  current_date <- format(Sys.Date(), "%Y%m%d")
  
  espn_games <- espn_nba_scoreboard(current_date)
  

  current_games <- espn_games[espn_games$status_type_description == "In Progress", ]
  
  if(nrow(current_games) == 0) {
    message("No NBA games currently in progress.")
    return(NULL)
  }
  
  current_games_info <- current_games[, c("game_id", "status_type_description", 
                                         "home_team_name", "home_team_score", 
                                         "away_team_name", "away_team_score", 
                                         "period", "clock")]
  
  message(paste0(nrow(current_games_info), " NBA games currently in progress."))
  print(current_games_info)
  
  saveRDS(current_games, file = "current_espn_nba_games.rds")
  
  return(current_games)
}

if (!interactive()) {
  get_current_espn_games()
}