from bs4 import BeautifulSoup
from apps.schemas import BaseResponse, ScrapResponse
from apps.helper import Log
from apps.models.LoanModel import PsychologyArticleDetail as pad
from orator.exceptions.query import QueryException
from sqlalchemy import create_engine

from main import PARAMS
import requests, re
import datetime
import pandas as pd
import hashlib

# Fetch website & return its text/content
def get_web_content(url, headers):    
    cap_data = requests.get(url, headers=headers, verify=False)
    return cap_data

# Return resultset of desired tags & class in texts with BeautifulSoup parser
def get_bs4_containers(url, headers, parser: str, tag:str, class_: str):
    cap_data = get_web_content(url, headers)
    if cap_data.status_code != 200: return None
    soup = BeautifulSoup(cap_data.text, parser)
    containers = soup.find_all(tag, class_=class_)
    return containers

# Check entry in psychologytoday_article table by index
def check_entry_in_db(index: str):
    try:
        data = pad.find(index)        
    except QueryException as e:
        Log.error(e)
        return False
    return data

database = PARAMS.DATABASE
conn_string = "postgresql://{}:{}@{}/{}".format(database.username, database.password, database.host, database.db)

# Insert psychologytoday article to psychologyarticle_detail table in db
def input_entry_to_db(entry, conn=conn_string):
    try:
        db = create_engine(conn)
        db_conn = db.connect()
        entry = pd.DataFrame(entry, index=[entry['index']])
        entry.to_sql('psychologyarticle_detail', db_conn, if_exists='append', index=False)        
        db_conn.close()
        Log.info("Done inserting entry {}".format(entry.index))
    except Exception as e:
        Log.error(e)
        raise Exception(str(e))