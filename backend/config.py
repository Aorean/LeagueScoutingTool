import os
from dotenv import load_dotenv
from backend.functions.psql import *
import pygsheets
from backend.db_base import create_db_engine


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

conn_url = create_db_connection_string(db_username, db_password, db_host, db_port, db_name)
db_engine = create_db_engine(conn_url)



#google sheets data
service_acc = pygsheets.authorize(service_account_file="C:\\Users\\joels\\Desktop\\LeagueScoutingTool\\backend\\json\\spreadsheet-automator-449612-b3a5d5ca0942.json")

sheet = service_acc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1iHweQST_7PNmN-PbfCDlZFUAhQzesQLrw60-WgrNK1I/edit?usp=sharing")

