# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 16:16:08 2020

Reads scoretables from livetulokset.com for KHL and Liiga and sorts the tables by point averages.

@author: soderdahl
"""


from selenium import webdriver


# reads data from website and processes it
def get_data(browser, xpath):
    table = browser.find_elements_by_xpath(xpath)
    teams, games, points = split_table(table)
    p_avgs = calculate_point_avg(teams, games, points)
    data = combine_lists(teams, games, points, p_avgs)
    
    return data


# makes teams, games and points tables
def split_table(table):
    table = table[0].text
    table = table.split(".") # splits from "."
    rivit = []
    for i in table:
        rivi = i.split() # splits from whitespaces
        rivit.append(rivi)
    rivit.pop(0) # removes the first one, which is unwanted    
    
    teams = []
    games = []
    points = []
    for rivi in rivit:
        team = rivi[0]
        
        game_index = 1
        
        # checks how many words in team name, so correct index for games column is found
        try:
            int(rivi[1])
        except:
            team = team + " " + rivi[1]
            game_index = 2
        try:
            int(rivi[2])
        except:
            team = team + " " + rivi[2]
            game_index = 3
            
        point_index = -1
        for i in rivi:
            # points column is one before "?"
            if i != "?":
                point_index = point_index + 1
            else:
                break
        
        teams.append(team)        
        games.append(rivi[game_index])
        points.append(rivi[point_index])
        
    return teams, games, points
        

# calculates point_average
def point_average(games, points):
    avg = int(points)/int(games)
    return float("{:.3f}".format(avg))


# calculates point averages for all teams
def calculate_point_avg(teams, games, points):
    i = 0
    p_avgs = []
    while i < len(teams):
        p_avg = point_average(games[i], points[i])
        p_avgs.append(p_avg)
        i = i + 1

    return p_avgs
        

# combines lists and sorts the result by point average
def combine_lists(teams, games, points, p_avgs):
    i = 0
    data = []
    while i < len(teams):
        team_data = [teams[i], games[i], points[i], p_avgs[i]]
        data.append(team_data)
        i = i + 1
        
    data.sort(key = get_avg, reverse = True)
    
    return data
    

def get_avg(element):
    return element[3]


def add_to_league_table(data):
    for i in data:
        league.append(i)
        
    league.sort(key = get_avg, reverse = True)
    
    return league


def print_table(conf, data):
    print("")
    print(conf)
    
    d = {}
    pos = 1
    for i in data:
        d.update({pos:data[pos-1]})
        pos = pos + 1
    
    print ("{:<6} {:<25} {:<6} {:<7} {:<10}".format('Pos','Team','Games','Points','Average'))
    for k, v in d.items():
        team, games, points, average = v
        print ("{:<6} {:<25} {:<6} {:<7} {:<10}".format(k, team, games, points, average))
    


path = "C:/Users/soder/Downloads/chromedriver_win32/chromedriver"

# asks what league table to show from user
# asked_table = input("KHL(1) or Liiga(2)? ")
asked_table = 1

# if user wants KHL
if asked_table == "1":
    url = 'https://www.livetulokset.com/sarjataulukko/IyLo2UXp/h6c6SHor/#table/overall'
    browser = webdriver.Chrome(executable_path=path)
    browser.get(url)
    
    xpath = '//*[@id="tournament-table-tabs-and-content"]/div[3]/div[1]/div[2]/div/div[2]'
    data = get_data(browser, xpath)
    league = []
    league = add_to_league_table(data)
    print_table("LÄNTINEN KONFERENSSI", data)
    
    xpath = '//*[@id="tournament-table-tabs-and-content"]/div[3]/div[1]/div[3]/div/div[2]'
    data = get_data(browser, xpath)
    league = add_to_league_table(data)
    print_table("ITÄINEN KONFERENSSI", data)
    
    print_table("KHL", league)
    
    browser.quit()
   
# if user wants liiga
elif asked_table == "2":
    url = 'https://www.livetulokset.com/sarjataulukko/S2lOZ6l1/0v9WSkNu/#table/overall'
    browser = webdriver.Chrome(executable_path=path)
    browser.get(url)
    
    xpath = '//*[@id="tournament-table-tabs-and-content"]/div[3]/div[1]/div/div/div[2]'
    data = get_data(browser, xpath)
    print_table("LIIGA", data)   
    
    browser.quit()

# loops if wrong input                
else:
    while True:
        asked_table = input("Write 1 for KHL or 2 for Liiga: ")
        if asked_table == "1":
                url = 'https://www.livetulokset.com/sarjataulukko/IyLo2UXp/h6c6SHor/#table/overall'
                browser = webdriver.Chrome(executable_path=path)
                browser.get(url)
                
                xpath = '//*[@id="tournament-table-tabs-and-content"]/div[3]/div[1]/div[2]/div/div[2]'
                data = get_data(browser, xpath)
                league = []
                league = add_to_league_table(data)
                print_table("LÄNTINEN KONFERENSSI", data)
                
                xpath = '//*[@id="tournament-table-tabs-and-content"]/div[3]/div[1]/div[3]/div/div[2]'
                data = get_data(browser, xpath)
                league = add_to_league_table(data)
                print_table("ITÄINEN KONFERENSSI", data)
                
                print_table("KHL", league)
                
                browser.quit()
                
                break
                
        elif asked_table == "2":
            url = 'https://www.livetulokset.com/sarjataulukko/S2lOZ6l1/0v9WSkNu/#table/overall'
            browser = webdriver.Chrome(executable_path=path)
            browser.get(url)
            
            xpath = '//*[@id="tournament-table-tabs-and-content"]/div[3]/div[1]/div/div/div[2]'
            data = get_data(browser, xpath)
            print_table("LIIGA", data)   
            
            browser.quit()
            break
