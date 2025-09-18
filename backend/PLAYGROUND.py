from backend.config import db_engine, db_connection
from backend.db_base import Base

#SQL imports
from sqlalchemy.orm import sessionmaker

import json

#psql
from backend.functions.psql import insert_or_update_player, get_query, execute_query
from backend.def_classes.sql_tables import *

#process data
from backend.config import db_connection
from backend.functions.general import get_playerclass, get_matchhistoriesclass

import os
from dotenv import load_dotenv
from backend.functions.process import process_input

from backend.process_data.avrg_stats import *

from backend.process_data.playerinfo import get_playerinfo_classes
from backend.main import json_champpool, json_mastery, json_player, run_main
#from backend.main import run_main

from backend.functions.general import create_dashboard_json
from backend.def_classes.summoners_rift import Match, Objectives, Playerstats, Champpool
from backend.process_data.c_dragon import *
from backend.functions.api import get_match
import dotenv
import os
api_key = os.environ.get("api_key")

#userinput = "https://op.gg/lol/multisearch/euw?summoners=Aorean%231311%2CQaQ%2300000%2CMoris%23RIVEN%2Cihatethisnerd%23euw%2Ci+is+pidgeon%23EUW"
userinput = "https://op.gg/lol/multisearch/euw?summoners=Aorean%231311%2CQaQ%2300000"
puuids = [
"bO5blHOm9YeY2MXm15I3DiHVtQPb8PuQov9J-wJ4X3CBuhjScuFDdaEM7VMFtciIC5htsuFYT43ytw",
"auom9H6uf9iN4yPls9QidJQWB1Mz2n4UIhfap9aQoITqA5gtRU0RE0ojafStbkIYrQzKtqxWmQr_jg"
        ]


#test = create_dashboard_json(puuids, db_connection)

test=run_main(user_input=userinput, api_key=api_key, db_connection=db_connection)



