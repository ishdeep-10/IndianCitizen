"""
Simulating results
==================

We now use a Poisson regression to fit a model to the Premier League
and then we use the estimated values to simulate results between
two teams.

This code is adapted from
https://dashee87.github.io/football/python/predicting-football-results-with-statistical-modelling/
"""

# importing the tools required for the Poisson regression model
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn
from scipy.stats import poisson,skellam

###################################################
# Import data
# -----------
# Here we use football-data.co.uk

epl = pd.read_csv("C:/Users/acer/Desktop/Soccermatics/LESSON - 5/2023-24.csv")
epl = epl[['HomeTeam','AwayTeam','FTHG','FTAG']]
epl_2324 = epl.rename(columns={'FTHG': 'HomeGoals', 'FTAG': 'AwayGoals'})
epl_2324.head()

#epl = epl[:-10]

epl_2324[['HomeGoals','AwayGoals']].mean()


# construct Poisson  for each mean goals value
poisson_pred = np.column_stack([[poisson.pmf(i, epl_2324[['HomeGoals','AwayGoals']].mean()[j]) for i in range(8)] for j in range(2)])

# plot histogram of actual goals

plt.hist(epl_2324[['HomeGoals', 'AwayGoals']].values, range(9), 
         alpha=0.7, label=['Home', 'Away'],density=True, color=["#FF0000", "#0000FF"])

# add lines for the Poisson distributions
pois1, = plt.plot([i-0.5 for i in range(1,9)], poisson_pred[:,0],
                  linestyle='-', marker='o',label="Home", color = '#FF0000')
pois2, = plt.plot([i-0.5 for i in range(1,9)], poisson_pred[:,1],
                  linestyle='-', marker='o',label="Away", color = '#0000FF')

leg=plt.legend(loc='upper right', fontsize=13, ncol=2)
leg.set_title("Poisson           Actual        ", prop = {'size':'14', 'weight':'bold'})

plt.xticks([i-0.5 for i in range(1,10)],[i for i in range(9)])
plt.xlabel("Goals per Match",size=13)
plt.ylabel("Proportion of Matches",size=13)
plt.title("Number of Goals per Match (EPL 2023/24 Season)",size=14,fontweight='bold')
plt.ylim([-0.004, 0.4])
plt.tight_layout()
plt.grid(True)
plt.show()

# probability of draw between home and away team
skellam.pmf(0.0,  epl_2324[['HomeGoals','AwayGoals']].mean()[0],  epl_2324[['HomeGoals','AwayGoals']].mean()[1])

# probability of home team winning by one goal
skellam.pmf(1,  epl_2324[['HomeGoals','AwayGoals']].mean()[0],  epl_2324[['HomeGoals','AwayGoals']].mean()[1])


skellam_pred = [skellam.pmf(i,  epl_2324[['HomeGoals','AwayGoals']].mean()[0],  
                            epl_2324[['HomeGoals','AwayGoals']].mean()[1]) for i in range(-6,9)]

plt.hist(epl_2324[['HomeGoals']].values - epl_2324[['AwayGoals']].values, range(-6,9), 
         alpha=0.7, label='Actual',density=True)
plt.plot([i+0.5 for i in range(-6,9)], skellam_pred,
                  linestyle='-', marker='o',label="Skellam", color = '#CD5C5C')
plt.legend(loc='upper right', fontsize=13)
plt.xticks([i+0.5 for i in range(-6,9)],[i for i in range(-6,9)])
plt.xlabel("Home Goals - Away Goals",size=13)
plt.ylabel("Proportion of Matches",size=13)
plt.title("Difference in Goals Scored (Home Team vs Away Team)",size=14,fontweight='bold')
plt.ylim([-0.004, 0.26])
plt.tight_layout()
plt.grid(True)
plt.show()



fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

# Selecting data for Liverpool's home matches and counting the goals
liv_home_data = epl_2324[epl_2324['HomeTeam'] == 'Liverpool']['HomeGoals']
liv_home_goal_counts = liv_home_data.value_counts(normalize=True).sort_index()
# Calculating the Poisson distribution for Liverpool's home goals
liv_home_pois = [poisson.pmf(i,np.sum(np.multiply(liv_home_goal_counts.values,liv_home_goal_counts.index))) for i in range(8)]

city_home_data = epl_2324[epl_2324['HomeTeam'] == 'Man City']['HomeGoals']
city_home_goal_counts = city_home_data.value_counts(normalize=True).sort_index()
city_home_pois = [poisson.pmf(i,np.sum(np.multiply(city_home_goal_counts.values,city_home_goal_counts.index))) for i in range(8)]

liv_away_data = epl_2324[epl_2324['AwayTeam'] == 'Liverpool']['AwayGoals']
liv_away_goal_counts = liv_away_data.value_counts(normalize=True).sort_index()
liv_away_pois = [poisson.pmf(i,np.sum(np.multiply(liv_away_goal_counts.values,liv_away_goal_counts.index))) for i in range(8)]

city_away_data = epl_2324[epl_2324['AwayTeam'] == 'Man City']['AwayGoals']
city_away_goal_counts = city_away_data.value_counts(normalize=True).sort_index()
city_away_pois = [poisson.pmf(i,np.sum(np.multiply(city_away_goal_counts.values,city_away_goal_counts.index))) for i in range(8)]

ax1.bar(liv_home_goal_counts.index-0.4,liv_home_goal_counts.values,width=0.4,color="#034694",label="Liverpool")
ax1.bar(city_home_goal_counts.index,city_home_goal_counts.values,width=0.4,color="#EB172B",label="Man City")
pois1, = ax1.plot([i for i in range(8)], liv_home_pois,
                  linestyle='-', marker='o',label="Liverpool", color = "#0a7bff")
pois2, = ax1.plot([i for i in range(8)], city_home_pois,
                  linestyle='-', marker='o',label="Man City", color = "#ff7c89")
leg=ax1.legend(loc='upper right', fontsize=12, ncol=2)
leg.set_title("Poisson                 Actual                ", prop = {'size':'14', 'weight':'bold'})
ax1.set_xlim([-0.5,7.5])
ax1.set_ylim([-0.01,0.65])
ax1.set_xticklabels([])
# mimicing the facet plots in ggplot2 with a bit of a hack
ax1.text(7.8, 0, '                Home                ', rotation=-90,
        bbox={'facecolor':'#ffbcf6', 'alpha':0.5, 'pad':5})
ax2.text(7.8, 0, '                Away                ', rotation=-90,
        bbox={'facecolor':'#ffbcf6', 'alpha':0.5, 'pad':5})

ax1.grid(True)

ax2.bar(liv_away_goal_counts.index-0.4,liv_away_goal_counts.values,width=0.4,color="#034694",label="Liverpool")
ax2.bar(city_away_goal_counts.index,city_away_goal_counts.values,width=0.4,color="#EB172B",label="Man City")
pois1, = ax2.plot([i for i in range(8)], liv_away_pois,
                  linestyle='-', marker='o',label="Liverpool", color = "#0a7bff")
pois2, = ax2.plot([i for i in range(8)], city_away_pois,
                  linestyle='-', marker='o',label="Man City", color = "#ff7c89")
ax2.set_xlim([-0.5,7.5])
ax2.set_ylim([-0.01,0.65])
ax1.set_title("Number of Goals per Match (EPL 2023/24 Season)",size=14,fontweight='bold')
ax2.set_xlabel("Goals per Match",size=13)
ax2.text(-1.15, 0.3, 'Proportion of Matches', rotation=90, size=13)
ax2.grid(True)
#plt.tight_layout()
plt.show()



###################################################
# Perform the regression
# -----------
# In the fit, we include a parameter for home advantage.
# Team and opponent are fixed effects.

goal_model_data = pd.concat([epl_2324[['HomeTeam','AwayTeam','HomeGoals']].assign(home=1).rename(
            columns={'HomeTeam':'team', 'AwayTeam':'opponent','HomeGoals':'goals'}),
           epl_2324[['AwayTeam','HomeTeam','AwayGoals']].assign(home=0).rename(
            columns={'AwayTeam':'team', 'HomeTeam':'opponent','AwayGoals':'goals'})])

poisson_model = smf.glm(formula="goals ~ home + team + opponent", data=goal_model_data,
                        family=sm.families.Poisson()).fit()
poisson_model.summary()


###################################################
# Simulating a game
# -----------------
# Let's now simulate a match between City and Liverpool

# Set teams here
home_team='Liverpool'
away_team='Man City'

#Predict for Liverpool vs. Manchester City
home_score_rate=poisson_model.predict(pd.DataFrame(data={'team': home_team, 'opponent': away_team,
                                       'home':1},index=[1]))
away_score_rate=poisson_model.predict(pd.DataFrame(data={'team': away_team, 'opponent': home_team,
                                       'home':0},index=[1]))
print(home_team + ' against ' + away_team + ' expect to score: ' + str(home_score_rate))
print(away_team + ' against ' + home_team + ' expect to score: ' + str(away_score_rate))

#Lets just get a result
home_goals=np.random.poisson(home_score_rate)
away_goals=np.random.poisson(away_score_rate)
print(home_team + ': ' + str(home_goals[0]))
print(away_team + ': '  + str(away_goals[0]))

def simulate_match(foot_model, homeTeam, awayTeam, max_goals=10):
    home_goals_avg = foot_model.predict(pd.DataFrame(data={'team': homeTeam, 
                                                            'opponent': awayTeam,'home':1},
                                                      index=[1])).values[0]
    away_goals_avg = foot_model.predict(pd.DataFrame(data={'team': awayTeam, 
                                                            'opponent': homeTeam,'home':0},
                                                      index=[1])).values[0]
    team_pred = [[poisson.pmf(i, team_avg) for i in range(0, max_goals+1)] for team_avg in [home_goals_avg, away_goals_avg]]
    return(np.outer(np.array(team_pred[0]), np.array(team_pred[1])))
simulate_match(poisson_model, 'Liverpool', 'Man City', max_goals=3)

liv_city = simulate_match(poisson_model, "Liverpool", "Man City", max_goals=10)
# liv win
np.sum(np.tril(liv_city, -1))

# draw
np.sum(np.diag(liv_city))

# city win
np.sum(np.triu(liv_city, 1))

###################################################
# Two-dimensional histogram of scores
# -----------------------------------
# This gives the probability of different score lines.


# Code to caluclate the goals for the match.
def simulate_match(foot_model, homeTeam, awayTeam, max_goals=10):
    home_goals_avg = foot_model.predict(pd.DataFrame(data={'team': homeTeam,
                                                           'opponent': awayTeam, 'home': 1},
                                                     index=[1])).values[0]
    away_goals_avg = foot_model.predict(pd.DataFrame(data={'team': awayTeam,
                                                           'opponent': homeTeam, 'home': 0},
                                                     index=[1])).values[0]
    team_pred = [[poisson.pmf(i, team_avg) for i in range(0, max_goals + 1)] for team_avg in
                 [home_goals_avg, away_goals_avg]]
    return (np.outer(np.array(team_pred[0]), np.array(team_pred[1])))

#Fill in the matrix
max_goals=5
score_matrix=simulate_match(poisson_model, home_team, away_team,max_goals)

fig=plt.figure()
ax=fig.add_subplot(1,1,1)
pos=ax.imshow(score_matrix, extent=[-0.5,max_goals+0.5,-0.5,max_goals+0.5], aspect='auto',cmap=plt.cm.Reds)
fig.colorbar(pos, ax=ax)
ax.set_title('Probability of outcome')
plt.xlim((-0.5,5.5))
plt.ylim((-0.5,5.5))
plt.tight_layout()
ax.set_xlabel('Goals scored by ' + away_team)
ax.set_ylabel('Goals scored by ' + home_team)
plt.show()

#Home, draw, away probabilities
homewin=np.sum(np.tril(score_matrix, -1))
draw=np.sum(np.diag(score_matrix))
awaywin=np.sum(np.triu(score_matrix, 1))


