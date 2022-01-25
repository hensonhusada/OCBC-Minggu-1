from apps.helper import Log
from apps.schemas import BaseResponse
from main import PARAMS
from apps.helper import ScrapingHelper
from sqlalchemy import create_engine as cce
from apps.models import db as conn
import pandas as pd

SALT = PARAMS.SALT.salt

class ScrapingController(object):   
    # Get one page of articles from psychologytoday.com
    @classmethod
    def get_articles(cls, page_num):
        response = ScrapingHelper.get_one_page_psycho(page_num)
        return response        

    # Insert entries of articles into psychologyarticle database
    @classmethod
    def to_db(cls, data):
        cs = 'postgresql://postgres:admin@localhost/your_database'
        response = BaseResponse()
        datas = pd.DataFrame(data)
        try:
            # Export to db using dataframe
            db = cce(cs)
            db_conn = db.connect()            
            
            datas.to_sql('psychologyarticle', db_conn, if_exists='append', index=False, method='multi')
            db_conn.close()

            response.message = "Success"
            response.status = 200
            response.data = len(data)
        except Exception as e:
            Log.error(e)
            response.status = 404
            response.message = "Error: "+ str(e)
        return response

    # Get five most recent articles from database
    @classmethod
    def get_some_articles(cls, number=5):
        results = []
        response = BaseResponse()
        try:
            temp = conn.table('psychologyarticle').select('*').order_by('publishdate', 'desc').limit(number).get()
            for i in temp:
                results.append({
                    "title": i[0],
                    "genre": i[1],
                    "publisher": i[2],
                    "publishdate": i[3],
                    "magazine": i[4],
                    "url": i[5],
                    "summary": i[6]
                })
            response.status = 200
            response.message = "Success"
            response.data = results
        except Exception as e:
            Log.error(e)
            response.status = 404
            response.message = "Error: " + str(e)

        return response