import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

#data= pd.read_csv("1238752.csv")

#names= pd.read_csv("people.csv")
import requests
from bs4 import BeautifulSoup

#print(id.e)
bowlers = {}
batsmen = {}


"""
for k in range(len(names.identifier[:20])):
    cricinfo = str(int(names.key_cricinfo[k]))
    print(cricinfo)
    url = 'https://www.espncricinfo.com/player/' + 's-' + cricinfo
    r = requests.get(url)
    soup = BeautifulSoup(r.text ,"lxml")

    hi = soup.find_all('h5',class_='player-card-description gray-900')

    try:
        names.Batting[k] = hi[3].get_text()
    except:
        print('wrong')
    try:
        names.Bowling[k] = hi[4].get_text()
    except:
        print('wrong')

names.to_csv('check.csv')
"""

# Batsman total runs
# Summarizing match data
# Performance vs a certain bowler type
# Cumulative Complex Batting rating. Take each game and find the batter runs against bowlers given their average at that point (cumulative statsguru)
# Cumulative Complex Batting Rating 2. Take each game and find the batter runs compared to how flat the pitch is.
# How flat the pitch is. Take the Cumulative batting averages of the batsmen and find the the expected score. Find the actual score.
# Expected score. 
## Player information. Pulls dataframe from player information csv. Then edits it with the list of players provided
## Match info: 
## Cumulative Complex Batting and Bowling averages. Creates new info file which contains the batters and bowlers with their complex averages
## at the start of each match

def PlayerInformation(PlayerList):
    """ 
    Pulls the Player Information CSV. Crawls the web for information aabout the players provided (given with registry number). 
    Adds info to CSV. 
    """
    newlist = pd.read_csv("PlayerInfo.csv")
    registry = pd.read_csv("people.csv")
    a = len(newlist.Registry)
    print(len(PlayerList))
    # should first check if they are already in playerlist
    ind  = 0
    while ind < len(PlayerList)-1:
        if PlayerList[ind] in newlist.Registry.values:
            del PlayerList[ind]
            print('deleted',PlayerList[ind])
        else:
            ind = ind + 1
        print(ind)
    
    print(PlayerList)
    #for k in range(len(PlayerList)):
    for k in range(len(registry.identifier)):
        average = '-'
        baverage = '-'
        if registry.identifier[k] in PlayerList:
            print(registry.identifier[k])
            df2 = {}
            newlist = newlist.append(df2, ignore_index=True)
            newlist.Registry[a] = registry.identifier[k]
            newlist.Name[a] = registry.name[k]
            newlist.Cricinfo_ID[a] = str(int(registry.key_cricinfo[k]))
            cricinfo = str(int(registry.key_cricinfo[k]))

            print(cricinfo)
            # Hand
            url = 'https://www.espncricinfo.com/player/' + 's-' + cricinfo
            r = requests.get(url)
            soup = BeautifulSoup(r.text ,"lxml")
            hi = soup.find_all('h5',class_='player-card-description gray-900')
            for i in range(len(hi)):
                if 'Left' in hi[i].get_text() or 'Right' in hi[i].get_text():
                    if 'bat' in hi[i].get_text():
                        newlist.Batting_Hand[a] = hi[i].get_text()
                    else:
                        newlist.Bowling_Hand[a] = hi[i].get_text()

            # Average
            url = 'https://stats.espncricinfo.com/ci/engine/player/' + cricinfo + '.html?class=1;template=results;type=allround;view=cumulative'
            r = requests.get(url)
            soup = BeautifulSoup(r.text ,"lxml")

            hi = soup.find_all('tr',class_='data1')
            for i in range(len(hi)-5):
                if int(hi[i+2].get_text().split('Test # ')[1]) > 1780:
                    average = (hi[i+2].get_text().split('\n'))[4]
                    baverage = (hi[i+2].get_text().split('\n'))[8]
                    break
            newlist.Bat_Average[a] = average
            newlist.Bowl_Average[a] = baverage
            a = a + 1
    print(newlist)
    newlist.to_csv('PlayerInfo.csv', index=False)
    

Plist = []
for file_name in glob.glob('/Users/sraza/Downloads/Test/'+'*_info.csv'):
    id = pd.read_csv(file_name, names = ['a','b','c','d','e'])
    for i in range(len(id.a)):
        if len(str(id.e[i])) > 4:
            Plist.append(id.e[i])


Plist = list(dict.fromkeys(Plist))
#print(Plist)
#PlayerInformation(Plist)

def PlayerRuns(PlayerName):
    """ 
    Pulls the Player Information CSV. Crawls the web for information aabout the players provided (given with registry number). 
    Adds info to CSV. 
    """
    Runs = 0
    for file_name in glob.glob('/Users/sraza/Downloads/Test/'+'*.csv'):
        if 'info' not in file_name and 'Player' not in file_name and 'people' not in file_name:
            matchdata = pd.read_csv(file_name)
            for i in range(len(matchdata.striker)):
                if PlayerName in matchdata.striker[i]:
                    Runs = Runs + matchdata.runs_off_bat[i]
                    print(Runs)

# PlayerRuns('Kohli')

def running_mean(x, N):
    cumsum = numpy.cumsum(numpy.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

def AverageRuns():
    """ 
    Pulls the Player Information CSV. Crawls the web for information aabout the players provided (given with registry number). 
    Adds info to CSV. 
    """
    AvgRuns = []
    MovingAvg = [38*100]
    Runs = 0
    Wickets = 0
    
    for file_name in sorted(glob.glob(f'{os.getcwd()}/*.csv'), key=lambda x: int(os.path.splitext(os.path.basename(x))[0])):
        if 'info' not in file_name and 'Player' not in file_name and 'people' not in file_name:
            print(file_name)
            matchdata = pd.read_csv(file_name)
            for i in range(len(matchdata.match_id)):
                Runs = Runs + matchdata.runs_off_bat[i]
                if str(matchdata.wicket_type[i]) != 'nan':
                    Wickets = Wickets + 1
            AvgRuns.append(Runs/Wickets)
    print(AvgRuns)
    plt.plot(AvgRuns)
    plt.show()

AverageRuns()

def complexbattingrating1(Player1):
    """ 
    Doesn't take into account things like pitch conditions and so on.
    The bowling rating is calculated as such
    """   
            
    

    

#data.noballs.fillna(0, inplace=True)
#data.wides.fillna(0, inplace=True)

"""
for i in range(len(data.bowler)):
    if not(data.bowler[i] in bowlers.keys()):
        bowlers[data.bowler[i]] = []
        bowlers[data.bowler[i]].append(1) ## overs
        bowlers[data.bowler[i]].append(data.runs_off_bat[i])
        if len(str(data.wicket_type[i])) > 3:
            bowlers[data.bowler[i]].append(1)
        bowlers[data.bowler[i]].append(0) ## wickets
    else:
        bowlers[data.bowler[i]][1] = bowlers[data.bowler[i]][1] + data.runs_off_bat[i]
        if (data.wides[i]) > 0 or (data.noballs[i]) > 0:
            bowlers[data.bowler[i]][1] = bowlers[data.bowler[i]][1] + data.wides[i] + data.noballs[i]
        else:
            bowlers[data.bowler[i]][0] = bowlers[data.bowler[i]][0] + 1
        if len(str(data.wicket_type[i])) > 3:
            bowlers[data.bowler[i]][2] = bowlers[data.bowler[i]][2] + 1

for i in range(len(data.striker)):
    if not(data.striker[i] in batsmen.keys()):
        for j in range(len(id.a[43:])):
            if data.striker[i] == id.d[j+43]:
                reg = id.e[j+43]
                for k in range(len(names.identifier)):
                    if names.identifier[k] == reg:
                        cricinfo = str(int(names.key_cricinfo[k]))
                        print(cricinfo)
                        url = 'https://www.espncricinfo.com/player/' + 's-' + cricinfo
                        r = requests.get(url)
                        soup = BeautifulSoup(r.text ,"lxml")

                        hi = soup.find_all('h5',class_='player-card-description gray-900')
                        print(hi[3].get_text())
        batsmen[data.striker[i]] = {}
        batsmen[data.striker[i]][data.bowler[i]] = []
        if (data.wides[i]) == 0 or (data.noballs[i]) == 0:
            batsmen[data.striker[i]][data.bowler[i]].append(1) ## overs
        else:
            batsmen[data.striker[i]][data.bowler[i]].append(0) ## overs
        batsmen[data.striker[i]][data.bowler[i]].append(data.runs_off_bat[i])
        batsmen[data.striker[i]][data.bowler[i]].append(0) ## wickets
    else:
        if not (data.bowler[i] in batsmen[data.striker[i]].keys()):
            batsmen[data.striker[i]][data.bowler[i]] = []
            if (data.wides[i]) == 0 or (data.noballs[i]) == 0:
                batsmen[data.striker[i]][data.bowler[i]].append(1) ## overs
            else:
                batsmen[data.striker[i]][data.bowler[i]].append(0) ## overs
            batsmen[data.striker[i]][data.bowler[i]].append(data.runs_off_bat[i])
            batsmen[data.striker[i]][data.bowler[i]].append(0) ## wickets
        else:
            if (data.wides[i]) == 0 or (data.noballs[i]) == 0:
                batsmen[data.striker[i]][data.bowler[i]][0] = batsmen[data.striker[i]][data.bowler[i]][0] + 1
            batsmen[data.striker[i]][data.bowler[i]][1] = batsmen[data.striker[i]][data.bowler[i]][1] + data.runs_off_bat[i]
            if len(str(data.wicket_type[i])) > 3:
                batsmen[data.striker[i]][data.bowler[i]][2] = batsmen[data.striker[i]][data.bowler[i]][2] + 1


#for item in mydict.items():
#    item[1][0] /= 6
"""