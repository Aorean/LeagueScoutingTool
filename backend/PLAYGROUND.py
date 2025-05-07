from functions.sql_functions import filter_matchhistory
from config_data import db_connection


matchhistory = []

with open("matchhistory.txt", "r") as f:
    for line in f:
        matchid = line.strip()
        matchhistory.append(matchid)

test = filter_matchhistory(db_connection, matchhistory)

print(test)