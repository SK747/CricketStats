import glob

def PlayerTotalRuns(PlayerName):
    """ 
    Pulls the Player Information CSV. Crawls the web for information aabout the players provided (given with registry number). 
    Adds info to CSV. 
    """
    for file_name in glob.glob('/Users/sraza/Downloads/Test/'+'*.csv'):
        if 'info' not in file_name:
            print(file_name)

PlayerTotalRuns('hi')