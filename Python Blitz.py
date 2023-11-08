import requests
import sys
import json
import pandas as pd
import warnings
import time
warnings.simplefilter(action='ignore', category=FutureWarning)

# Accept Summoner name and print it back out
api_key = 'RGAPI-610f9abe-9f29-49fb-b6fa-739668ceb387'
summoner_names_list = []
input_arguments = sys.argv
friend_df = pd.DataFrame(columns=['SummonerName','Surrender Vote Percentage'])
for arg in input_arguments[1:]:
    url_ready_name = arg.replace(" ", "%20")
    summoner_names_list.append(url_ready_name)

for name in summoner_names_list:
    friend_df = friend_df.append({'SummonerName': name},ignore_index=True)


#Create a list of puuids of each friend
puuid_list = []
for summoner_name in summoner_names_list:
    api_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name + "?api_key=" + api_key
    api_request = requests.get(api_url)
    playerinfo = api_request.json()
    puuid = playerinfo['puuid']
    puuid_list.append(puuid)

#Win and loss list function
def get_win_list(id):
    match_info_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/' + id + '?api_key=' + api_key
    match_response = requests.get(match_info_url)
    match_response_json = match_response.json()
    Win = str(match_response_json['info']['participants'][0]['win'])
    if Win == "True":
        game_result = "Win"
    else:
        game_result = "Loss"   
    Win_list.append(game_result)
#Surrender list function
def get_surrenders(id):
    match_info_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/' + id + '?api_key=' + api_key
    match_response = requests.get(match_info_url)
    match_response_json = match_response.json()
    Surrender = str(match_response_json['info']['participants'][0]['gameEndedInSurrender'])
    if Surrender == "True":
        surrender_result = "Yes"
    else:
        surrender_result ="No"
    Surrender_list.append(surrender_result)

def get_ff_percentage(ff,df):    
    ff_percent = (len(ff)/len(df))
    return(ff_percent)

#Get list of match IDs, then iterate through the list and create a win list and surrender list
ff_list = []
for puuid in puuid_list:
    matchid_api_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/' + puuid + '/ids?start=0&count=23&api_key=' + api_key
    match_id_info = requests.get(matchid_api_url)
    match_id_list = match_id_info.json()
    Win_list = []
    Surrender_list= []
    for id in match_id_list:
        get_win_list(id)
        get_surrenders(id)
    match_results = {}
    for id, game_result, surrender_result in zip(match_id_list, Win_list, Surrender_list):
        match_results[id] = (game_result, surrender_result)
    df = pd.DataFrame.from_dict(match_results,orient='index')
    df.columns =['Win/Loss','EndedinSurrender']
    ff = df.loc[(df['Win/Loss'] == 'Loss') & (df['EndedinSurrender'] == 'Yes')]
    ff_percent = (len(ff)/len(df))
    ff_list.append(ff_percent)
    time.sleep(120)
friend_df.loc[:len(summoner_names_list), 'Surrender Vote Percentage'] = ff_list


highest_surrender_percentage_df = friend_df.sort_values(by=['Surrender Vote Percentage'],ascending=[False]).head(1)
highest_surrender_percentage = highest_surrender_percentage_df['Surrender Vote Percentage'].values[0]
Top_summoner_name = str(highest_surrender_percentage_df['SummonerName'].values[0])
Message = "The player who surrenders and loses the most is " + Top_summoner_name + " with a surrender rate of ... {:.0%}"
print(Message.format(highest_surrender_percentage))

'''
Possible ideas:
Highest count of games above 40 minutes
Highest time spent dead
Highest time played
'''