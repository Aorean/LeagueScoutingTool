import psycopg2

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
        query = f'SELECT "{selection}" FROM "{schema}"."{table}"'
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
    query_select_player = get_query("select", "puuid", "playerdata", "player")
    select_player = execute_query(db_connection, query_select_player)
    # getting a list with all puuids in the sql database already
    list_select_player = []
    for player in select_player:
        str_player = "".join(player)
        list_select_player.append(str_player)
    return list_select_player

def SELECT_PK_MATCH(db_connection):
    # get match table from database
    query_select_match = get_query("select", "PUUID_MATCHID", "playerdata", "match")
    select_match = execute_query(db_connection, query_select_match)

    # list with str datatypes of primary key
    list_select_match = []
    for match in select_match:
        str_match = "".join(match)
        list_select_match.append(str_match)
    return list_select_match

def SELECT_PK_PLAYERSTATS(db_connection):
    # get playerstats table from database
    query_select_playerstats = get_query("select", "PUUID_MATCHID", "playerdata", "playerstats")
    select_playerstats = execute_query(db_connection, query_select_playerstats)

    list_select_playerstats = []
    # list with str datatypes of primary key
    for playerstats in select_playerstats:
        str_playerstats = "".join(playerstats)
        list_select_playerstats.append(str_playerstats)
    return list_select_playerstats

def SELECT_PK_OBJECTIVES(db_connection):
    # get objectives table from database
    query_select_objectives = get_query("select", "MATCHID_TEAMID", "playerdata", "objectives")
    select_objectives = execute_query(db_connection, query_select_objectives)

    list_select_objectives = []
    # list with str datatypes of primary key
    for playerstats in select_objectives:
        str_objectives = "".join(playerstats)
        list_select_objectives.append(str_objectives)
    return list_select_objectives