## win_probability.R ##
## polls ESPN win probablity data for current NBA games ##
# This script polls ESPN win probability data for current NBA games at specified intervals # 
# poll_espn_win_probability: poll win probability for current games #
# create dir for win probability if it doesn't exist #
# print games we'll be tracking #
# get the list of ESPN game IDs #
# check if games are still active # 
# get win prob for each game # 

library(hoopR)
library(dplyr)

# Function to poll win probability for current games
poll_espn_win_probability <- function(interval_seconds = 30) {
 
  if (!file.exists("current_espn_nba_games.rds")) {
    stop("No current games file found. Run get_current_espn_games.R first.")
  }
  
  current_games <- readRDS("current_espn_nba_games.rds")
  
  if (is.null(current_games) || nrow(current_games) == 0) {
    stop("No current games to poll.")
  }
  
  if (!dir.exists("win_probability_data")) {
    dir.create("win_probability_data")
  }
  
  cat("Tracking win probability for the following games:\n")
  for (i in 1:nrow(current_games)) {
    cat(sprintf("%s vs %s (Game ID: %s)\n", 
                current_games$away_team_name[i],
                current_games$home_team_name[i],
                current_games$game_id[i]))
  }

  game_ids <- current_games$game_id
  
  tracking_data <- list()
  for (game_id in game_ids) {
    tracking_data[[as.character(game_id)]] <- list(
      polls = 0,
      latest_data = NULL
    )
  }
  
  cat(sprintf("\nStarting to poll win probability every %d seconds...\n", 
              interval_seconds))
  cat("Press Ctrl+C to stop polling at any time.\n\n")
  
  poll_count <- 0
  
  while (TRUE) {
    poll_count <- poll_count + 1
    current_time <- format(Sys.time(), "%Y-%m-%d %H:%M:%S")
    cat(sprintf("Poll #%d at %s\n", poll_count, current_time))
    
    current_date <- format(Sys.Date(), "%Y%m%d")
    updated_games <- tryCatch({
      espn_nba_scoreboard(current_date)
    }, error = function(e) {
      cat("Error fetching updated scoreboard:", conditionMessage(e), "\n")
      return(NULL)
    })
    
    if (!is.null(updated_games)) {
      active_games <- sum(updated_games$game_id %in% game_ids & 
                         updated_games$status_type_description == "In Progress")
      if (active_games == 0) {
        cat("All tracked games have ended. Stopping polling.\n")
        break
      }
    }
    
    for (game_id in game_ids) {

      if (!is.null(updated_games)) {
        game_row <- updated_games[updated_games$game_id == game_id, ]
        if (nrow(game_row) > 0 && game_row$status_type_description != "In Progress") {
          cat(sprintf("Game ID %s is no longer active. Skipping.\n", game_id))
          next
        }
      }
      
      tryCatch({
        wp_data <- espn_nba_wp(game_id = game_id)
        
        if (!is.null(wp_data) && nrow(wp_data) > 0) {
 
          tracking_data[[as.character(game_id)]]$polls <- tracking_data[[as.character(game_id)]]$polls + 1
          tracking_data[[as.character(game_id)]]$latest_data <- wp_data
          
          timestamp <- format(Sys.time(), "%Y%m%d_%H%M%S")
          filename <- sprintf("win_probability_data/game_%s_%s.rds", game_id, timestamp)
          saveRDS(wp_data, file = filename)
          
          latest_record <- tail(wp_data, 1)
          if (nrow(latest_record) > 0) {
            cat(sprintf("Game ID %s: Home %s%% - Away %s%% (Period: %s, Clock: %s)\n", 
                        game_id, 
                        round(latest_record$home_win_percentage * 100, 1),
                        round(latest_record$away_win_percentage * 100, 1),
                        latest_record$period_display_value,
                        latest_record$clock_display_value))
          }
        } else {
          cat(sprintf("No win probability data available for Game ID %s\n", game_id))
        }
      }, error = function(e) {
        cat(sprintf("Error fetching win probability for Game ID %s: %s\n", 
                   game_id, conditionMessage(e)))
      })
    }
    
    
    cat(sprintf("Waiting %d seconds until next poll...\n\n", interval_seconds))
    Sys.sleep(interval_seconds)
  }
  
  cat("\nPolling complete. Summary:\n")
  for (game_id in game_ids) {
    polls <- tracking_data[[as.character(game_id)]]$polls
    cat(sprintf("Game ID %s: Polled %d times\n", game_id, polls))
  }
}

interval_seconds <- 30  

args <- commandArgs(trailingOnly = TRUE)
if (length(args) >= 1) interval_seconds <- as.numeric(args[1])

if (!interactive()) {
  poll_espn_win_probability(interval_seconds)
}