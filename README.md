# Project: Impact of Weather & Other Factors on Premier League Goals

## Overview
This project aims to analyze whether external factors such as weather conditions, crowd attendance, referee decisions, and the introduction of VAR have had a measurable impact on goal-scoring patterns in the Premier League. While it's known that tactics, player forms and team managers play a big role in the amount of goals scored, external conditions could also influence how many goals are scored in a game.

I will be specifically focusing on teams based in London (Arsenal, Chelsea, Tottenham, etc.) and Manchester (Man City, Man United). These two cities house 8 teams,5 of which of are from the known "Big 6" which are the best and most dominant teams in the league. By analyzing historical match data and weather reports, I aim to determine whether factors like temperature, rain, wind speed, and humidity correlate with changes in goal frequency.

Additionally, i will investigate whether higher crowd attendance is correlated to the amount of goals scored, if certain referees influence game outcomes, and whether the introduction of VAR in 2019/20 has significantly impacted how many goals are scored per match.

## Motivation
Ever since i was a kid i've heard the quote *"but can he do it on a cold rainy night in Stoke"* which is a quote said as a joke when comparing top players, but after this project I hopefully will be able to know whether cold, rainy, or night affect anything.

If any of these factors turn out to have a significant effect on the number of goals scored, this information could be valuable for bettors looking to improve their predictions. By identifying factors that affect goal-scoring, bettors could make more accurate betting decisions. Understanding these trends might give them an edge in predicting total goals scored per game, potentially increasing their betting success.

## Data Sources
- **Match Data**: [Premier League dataset on Kaggle]([https://www.kaggle.com/datasets](https://www.kaggle.com/datasets/saife245/english-premier-league)) (includes attendance data)
- **Weather Data**: Collected from [Visual Crossing]([https://www.visualcrossing.com/](https://www.visualcrossing.com/weather-query-builder/)) (dataset not directly on website, had to request and download)
- **VAR Impact Analysis**: Comparing goal trends before (early 2000s) and after the introduction of VAR (post-2020).

## Tools Used
- **Python**: The main language for data processing.
- **Pandas**: Data cleaning, merging, and analysis.
- **NumPy**: Statistical calculations (trendlines, correlations, averages).
- **Matplotlib**: Data visualization (scatter plots, bar charts).
- **Excel**: Initial manual data inspection.

## Key Questions Explored
- **Weather & Goals**: Does temperature impact the number of goals scored? Do rain, humidity, or wind play a role?
- **Crowd Influence**: Does higher attendance lead to more goals, or does pressure make teams more defensive?
- **Referee Impact**: Are some referees more penalty- or red-card-happy than others?
- **VAR Changes**: Has the introduction of VAR changed the frequency of goals? More penalties, fewer offside goals?
- **Time of Day**: Are evening matches more goal-heavy than afternoon or morning games?

## Expected Results
- **Cold or Rainy Weather = Fewer Goals?** If the data supports the "cold, rainy night in Stoke" theory, we might see fewer goals in bad weather.
- **Higher Attendance = More Goals?** A loud crowd might push teams forward, but might also pressure unexperienced players causing them to play worse.
- **Referee Bias Exists?** Some referees might consistently give more penalties or red cards, which might change a teams whole play-style, causing them to score less.
- **VAR = Fewer Open Play Goals?** If VAR rules out more marginal goals (offsides, handballs), the data may show fewer open play goals, but this can in fact increase goals-scored since penalties hardly go unnoticed with VAR.
- **Evening Games = More Goals?** Does the sunlight affect how players play, or are they more tired playing not long after they wake up, or not too long before they sleep?

## Conclusion
Football is more than just skill—external factors like weather, referees, and fan presence can influence the game. In this project i aim to use data to uncover hidden patterns in goal-scoring trends, particularly focusing on how conditions impact teams from London and Manchester.  

If this research proves that these external factors have an effect on goal-scoring, then football fans finally have the data to back up the famous stoke quote . If not, then maybe er should all retire this phrase.
