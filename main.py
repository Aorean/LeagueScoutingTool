#Using processdata in main, minimalistic code, just running the functions
#and getting the values/classes I need.
#add "google sheet export" Boolean in user_input

#SQL imports
import psycopg2
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker, declarative_base


#my stuff
from process_data import classes_player, dict_matches
from sql_tables import PLAYER, MATCH, PLAYERSTATS, OBJECTIVES, Base
from sql_functions import *

#dotenv
from dotenv import load_dotenv
import os

load_dotenv()

#Login for Database
db_username = os.environ.get("db_username")
db_host = os.environ.get("db_host")
db_port = os.environ.get("db_port")
db_name = os.environ.get("db_name")
db_password = os.environ.get("db_password")

db_connection = [
                    db_name,
                    db_username,
                    db_password,
                    db_host,
                    db_port
                 ]


#connection to postgrsql
conn_url = create_db_connection_string(db_username, db_password, db_host, db_port, db_name)
db_engine = create_engine(conn_url)

#table classes
DB_PLAYER = PLAYER
DB_MATCH = MATCH
DB_PLAYERSTATS = PLAYERSTATS
DB_OBJECTIVES = OBJECTIVES
print(Base.metadata.tables.keys())
#create tables if not in sql
Base.metadata.create_all(db_engine)

#def session
SessionLocal = sessionmaker(bind=db_engine, autocommit=False, autoflush=False)
session = SessionLocal()

#getting list of classes
classes_player = classes_player
#getting dict of classes
dict_matches = dict_matches


#SELECT to check if UPDATE or INSERT

#MATCH
list_select_match = SELECT_PK_MATCH(db_connection)
#PLAYERSTATS
list_select_playerstats = SELECT_PK_PLAYERSTATS(db_connection)
#OBJECTIVES
list_select_objectives = SELECT_PK_OBJECTIVES(db_connection)



insert_or_update_PLAYER(db_connection, classes_player)

# upload match
# look for sql injections!!!!!!!!!!!! ("?" instead of fstring)

# iteration from last 20 matches, insert the ones that are new, update the ones that are old
for key in dict_matches:
    #dependencies
    match = dict_matches[key]

    class_match = match[0]

    # create sql class
    new_match = MATCH.from_match(class_match)
    participants_sql = get_participants_sql(new_match)


    # does the class already exist?:
    # YES it exists
    # UPDATE the SQL Table with new content
    if new_match.PUUID_MATCHID in list_select_match:
        # variables for get_query
        columns_and_values = f'"puuid" = \'{new_match.puuid}\', "matchid" = \'{new_match.matchid}\', "participants" = \'{participants_sql}\', "gamestart" = {new_match.gamestart}, "gameend" = {new_match.gameend}, "gameduration" = {new_match.gameduration}, "tournamentcode" = \'{new_match.tournamentcode}\', "gamemode" = \'{new_match.gamemode}\''
        query_update = get_query("update", table='"playerdata"."match"', columns_and_values=columns_and_values, key='"PUUID_MATCHID"', keyvalue=new_match.PUUID_MATCHID)
        do_i_need_equal = execute_query(db_connection, query_update)

    # NO it does not exist
    # INSERT the new data
    elif new_match.PUUID_MATCHID not in list_select_match:
        # variables for get_query
        tablename = \
            (
                '"playerdata"."match"'
                '("PUUID_MATCHID", "puuid", "matchid", "participants", "gamestart", "gameend", '
                '"gameduration", "tournamentcode", "gamemode")'
             )
        values = (
            f"'{new_match.PUUID_MATCHID}', '{new_match.puuid}', '{new_match.matchid}', "
                  f"'{participants_sql}', {new_match.gamestart}, {new_match.gameend}, "
                  f"{new_match.gameduration}, '{new_match.tournamentcode}', "
                  f"'{new_match.gamemode}'"
        )
        query_insert = get_query("insert", tablename=tablename, values=values)
        list_select_match.append(new_match.PUUID_MATCHID)
        do_i_need_equal = execute_query(db_connection, query_insert)

#upload participants
for key in dict_matches:
    # dependencies
    match = dict_matches[key]

    class_match = match[0]
    list_class_participants = match[1]
    list_class_objectives = match[2]

    for participant in list_class_participants:
        new_participant = PLAYERSTATS.from_playerstats(participant)

        if new_participant.PUUID_MATCHID in list_select_playerstats:
            columns_and_values = \
                                (
                                  f'"puuid" = \'{new_participant.puuid}\', '
                                  f'"matchid" = \'{new_participant.matchid}\', '
                                  f'"gamertag" = \'{new_participant.gamertag}\', '
                                  f'"tagline" = \'{new_participant.tagline}\', '
                                  f'"team" = {new_participant.team}, '
                                  f'"champ" = \'{new_participant.champ}\', '
                                  f'"role" = \'{new_participant.role}\', '
                                  f'"kills" = {new_participant.kills}, '
                                  f'"deaths" = {new_participant.deaths}, '
                                  f'"assists" = {new_participant.assists}, '
                                  f'"cs" = {new_participant.cs}, '
                                  f'"level" = {new_participant.level}, '
                                  f'"exp" = {new_participant.exp}, '
                                  f'"gold" = {new_participant.gold}, '
                                  f'"visionscore" = {new_participant.visionscore}, '
                                  f'"summonerspell1" = \'{new_participant.summonerspell1}\', '
                                  f'"summonerspell2" = \'{new_participant.summonerspell2}\', '
                                  f'"item1" = \'{new_participant.item1}\', '
                                  f'"item2" = \'{new_participant.item2}\', '
                                  f'"item3" = \'{new_participant.item3}\', '
                                  f'"item4" = \'{new_participant.item4}\', '
                                  f'"item5" = \'{new_participant.item5}\', '
                                  f'"item6" = \'{new_participant.item6}\', '
                                  f'"keyrune" = \'{new_participant.keyrune}\', '
                                  f'"win" = {new_participant.win}'
                                )
            query_update = get_query("update",
                                     table='"playerdata"."playerstats"',
                                     columns_and_values=columns_and_values,
                                     key='"PUUID_MATCHID"',
                                     keyvalue=new_participant.PUUID_MATCHID
                                     )

            again_do_i_need_equal = execute_query(db_connection,query_update)

        elif new_participant.PUUID_MATCHID not in list_select_playerstats:
            tablename = '"playerdata"."playerstats"("PUUID_MATCHID","puuid","matchid","gamertag","tagline","team","champ","role","kills","deaths","assists","cs","level","exp","gold","visionscore","summonerspell1","summonerspell2","item1","item2","item3","item4","item5","item6","keyrune","win")'

            values = f'\'{new_participant.PUUID_MATCHID}\', \'{new_participant.puuid}\', \'{new_participant.matchid}\', \'{new_participant.gamertag}\', \'{new_participant.tagline}\', {new_participant.team}, \'{new_participant.champ}\', \'{new_participant.role}\', {new_participant.kills}, {new_participant.deaths}, {new_participant.assists}, {new_participant.cs}, {new_participant.level}, {new_participant.exp}, {new_participant.gold}, {new_participant.visionscore}, \'{new_participant.summonerspell1}\', \'{new_participant.summonerspell2}\', \'{new_participant.item1}\', \'{new_participant.item2}\', \'{new_participant.item3}\', \'{new_participant.item4}\', \'{new_participant.item5}\', \'{new_participant.item6}\', \'{new_participant.keyrune}\', {new_participant.win}'

            query_insert = get_query("insert", tablename=tablename, values=values)

            list_select_playerstats.append(new_participant.PUUID_MATCHID)
            again_do_i_need_equal = execute_query(db_connection, query_insert)




#upload objectives
for key in dict_matches:
    # dependencies
    match = dict_matches[key]

    list_class_objectives = match[2]

    for team in list_class_objectives:
        objectives = list_class_objectives[team]
        new_team = OBJECTIVES.from_objectives(objectives)
        # check for conflict

        if new_team.MATCHID_TEAMID in list_select_objectives:
            columns_and_values = \
                                (
                                  f'"matchid" = \'{new_team.matchid}\', '
                                  f'"teamid" = {new_team.teamid}, '
                                  f'"baronfirst" = {new_team.baronfirst}, '
                                  f'"baronkills" = {new_team.baronkills}, '
                                  f'"atakhanfirst" = {new_team.atakhanfirst}, '
                                  f'"atakhankills" = {new_team.atakhankills}, '
                                  f'"grubsfirst" = {new_team.grubsfirst}, '
                                  f'"grubskills" = {new_team.grubskills}, '
                                  f'"dragonfirst" = {new_team.dragonfirst}, '
                                  f'"dragonkills" = {new_team.dragonkills}, '
                                  f'"riftheraldfirst" = {new_team.riftheraldfirst}, '
                                  f'"riftheraldkills" = {new_team.riftheraldkills}, '
                                  f'"towerfirst" = {new_team.towerfirst}, '
                                  f'"towerkills" = {new_team.towerkills}, '
                                  f'"inhibfirst" = {new_team.inhibfirst}, '
                                  f'"inhibkills" = {new_team.inhibkills}'
                                )
            query_update = get_query("update",
                                     table='"playerdata"."objectives"',
                                     columns_and_values=columns_and_values,
                                     key='"MATCHID_TEAMID"',
                                     keyvalue=new_team.MATCHID_TEAMID)
            again_do_i_need_equal_2 = execute_query(db_connection, query_update)

        elif new_team.MATCHID_TEAMID not in list_select_objectives:
            tablename = '"playerdata"."objectives"("MATCHID_TEAMID","matchid","teamid","baronfirst","baronkills","atakhanfirst","atakhankills","grubsfirst","grubskills","dragonfirst","dragonkills","riftheraldfirst","riftheraldkills","towerfirst","towerkills","inhibfirst","inhibkills")'
            values = f'\'{new_team.MATCHID_TEAMID}\', \'{new_team.matchid}\', {new_team.teamid}, {new_team.baronfirst}, {new_team.baronkills}, {new_team.atakhanfirst}, {new_team.atakhankills}, {new_team.grubsfirst}, {new_team.grubskills}, {new_team.dragonfirst}, {new_team.dragonkills}, {new_team.riftheraldfirst}, {new_team.riftheraldkills}, {new_team.towerfirst}, {new_team.towerkills}, {new_team.inhibfirst}, {new_team.inhibkills}'

            query_insert = get_query("insert", tablename=tablename, values=values)

            list_select_objectives.append(new_team.MATCHID_TEAMID)
            again_do_i_need_equal_2 = execute_query(db_connection, query_insert)



session.close()
