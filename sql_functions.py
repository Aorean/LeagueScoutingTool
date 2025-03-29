import psycopg2
from sql_tables import PLAYER, MATCH, PLAYERSTATS, OBJECTIVES, Base

def create_db_connection_string(db_username, db_password, db_host, db_port, db_name):
    connection_url = "postgresql+psycopg2://" + db_username + ":" + db_password + "@" + db_host + ":" + db_port + "/" + db_name
    return connection_url

def get_query(querytype,
          selection=None,
          schema=None,
          table = None,
          tablename=None,
          values=None,
          columns_and_values=None,
          key=None,
          keyvalue=None
              ):
    #querytypes = select, insert, update
    if querytype == "select":
        query = f'SELECT {selection} FROM "{schema}"."{table}"'
        # selection = column name (alternatively "*" for all
        # schema = sql schema (here playerdata for the most part)
        # table = sql tablename
    elif querytype == "insert":
        query = f'INSERT INTO {tablename}\nVALUES ({values})'
        # tablename = sql tablename(columns) = tablename(columnname1, columnname2, columnname3, ...)
        # values = ('value1', value2, value3, ...)
    elif querytype == "update":
        query = f"UPDATE {table}\nSET {columns_and_values}\nWHERE {key} = '{keyvalue}'"
        # table = sql tablename
        # columns_and_values = column1 = "value1", column2 = "value2", ...
        # key = name of the primarykey column
        # keyvalue = value of the primary key column that should be updated
    else:
        print("ERROR: Wrong querytype")
        query = None

    return query

def execute_query(db_connection, query):
    # curser
    conn = psycopg2.connect(dbname=db_connection[0],
                            user=db_connection[1],
                            password=db_connection[2],
                            host=db_connection[3],
                            port=db_connection[4])
    cur = conn.cursor()
    #f string for whole query, to minimize diff functions, use query for every SQL method
    print("trying query: " , query)
    try:
        cur.execute(f'{query}')

        if query.strip().startswith("SELECT"):
            rows = cur.fetchall()
            return rows
        else:
            conn.commit()

    except psycopg2.ProgrammingError as e:
        print(f"ProgrammingError: Query couldnt be executed")
        #print(psycopg2.ProgrammingError)
    except psycopg2.DatabaseError as e:
        print(f"DatabaseError: Query couldnt be executed")
    except Exception as e:
        print(f"UnexpectedError: Query couldnt be executed")

    conn.close()
    cur.close()

def get_participants_sql(new_match):
    participants_sql = ""
    for participant in new_match.participants:
        participants_sql += '"'
        participants_sql += participant
        participants_sql += '"'
        participants_sql += ","
    participants_sql = participants_sql[:len(participants_sql) - 1]
    return participants_sql

def SELECT_PK_PLAYER(db_connection):
    # get player table from database
    query_select_player = get_query("select", '"puuid"', "playerdata", "player")
    select_player = execute_query(db_connection, query_select_player)
    # getting a list with all puuids in the sql database already
    list_select_player = []
    for player in select_player:
        str_player = "".join(player)
        list_select_player.append(str_player)
    return list_select_player

def SELECT_PK_MATCH(db_connection):
    # get match table from database
    query_select_match = get_query("select", '"PUUID_MATCHID"', "playerdata", "match")
    select_match = execute_query(db_connection, query_select_match)

    # list with str datatypes of primary key
    list_select_match = []
    for match in select_match:
        str_match = "".join(match)
        list_select_match.append(str_match)
    return list_select_match

def SELECT_PK_PLAYERSTATS(db_connection):
    # get playerstats table from database
    query_select_playerstats = get_query("select", '"PUUID_MATCHID"', "playerdata", "playerstats")
    select_playerstats = execute_query(db_connection, query_select_playerstats)

    list_select_playerstats = []
    # list with str datatypes of primary key
    for playerstats in select_playerstats:
        str_playerstats = "".join(playerstats)
        list_select_playerstats.append(str_playerstats)
    return list_select_playerstats

def SELECT_PK_OBJECTIVES(db_connection):
    # get objectives table from database
    query_select_objectives = get_query("select", '"MATCHID_TEAMID"', "playerdata", "objectives")
    select_objectives = execute_query(db_connection, query_select_objectives)

    list_select_objectives = []
    # list with str datatypes of primary key
    for playerstats in select_objectives:
        str_objectives = "".join(playerstats)
        list_select_objectives.append(str_objectives)
    return list_select_objectives

def insert_or_update_player(input_type, db_connection, classes_player = None, dict_matches = None):
    if input_type == "player":
        # SELECT to check if UPDATE or INSERT
        list_select_player = SELECT_PK_PLAYER(db_connection)
        for class_player in classes_player:
            # create sql class
            new_player = PLAYER.from_player(class_player)

            # does the class already exist?:
            # YES it exists
            # UPDATE the SQL Table with new content
            if new_player.puuid in list_select_player:
                # variables for get query
                columns_and_values = f'"gamertag" = \'{new_player.gamertag}\', "tagline" = \'{new_player.tagline}\''
                # get query
                query_update = get_query("update",
                                         table='"playerdata"."player"',
                                         columns_and_values=columns_and_values,
                                         key='"puuid"',
                                         keyvalue=new_player.puuid)
                # execute query (UPDATE)
                rows = execute_query(db_connection, query_update)

            # NO it does not exist
            # INSERT the new data
            elif new_player.puuid not in list_select_player:
                # variables for get query
                tablename = '"playerdata"."player"("puuid", "gamertag", "tagline")'
                values = f"'{new_player.puuid}', '{new_player.gamertag}', '{new_player.tagline}'"
                # get query
                query_insert = get_query("insert",
                                         tablename=tablename,
                                         values=values)
                # append the primary key to the list of primary keys to prevent double input
                list_select_player.append(new_player.puuid)
                # execute query (INSERT)
                rows = execute_query(db_connection, query_insert)

    if input_type == "match":
        # MATCH
        list_select_match = SELECT_PK_MATCH(db_connection)
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

    if input_type == "playerstats":
        # PLAYERSTATS
        list_select_playerstats = SELECT_PK_PLAYERSTATS(db_connection)
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



    if input_type == "objectives":
        # OBJECTIVES
        list_select_objectives = SELECT_PK_OBJECTIVES(db_connection)
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






