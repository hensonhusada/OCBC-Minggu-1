from apps.helper import Log
from apps.schemas import BaseResponse, SchemaScrap
from main import PARAMS
from apps.helper import ScrapingHelper
from sqlalchemy import create_engine as cce
from apps.models import db as conn
from apps.models.LoanModel import PsychologyArticle

from bs4 import BeautifulSoup
import pandas as pd
import requests, re, hashlib

SALT = PARAMS.SALT.salt

class ScrapingController(object): 
    headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,id;q=0.8,ms;q=0.7,ja;q=0.6,ko;q=0.5"
        }  
    # Get all articles urls for one page of psychologytoday.com
    @classmethod
    def get_articles_urls(cls, page_number=1):
        response = BaseResponse()
        base_url = "https://www.psychologytoday.com"
        url = base_url + "/intl/blog-posts?page=" + str(page_number-1)
        Log.info(url)
        list_of_urls = []
        response.status = 404
        response.message = "Error during get request"
        try:
            soup = ScrapingHelper.get_bs4_containers(url, cls.headers, 'html.parser', 'div', 'blog_entry__text')        
            if not soup: return response
            for can in soup:
                list_of_urls.append(base_url + can.select('a')[1]['href'])                    
            # response.data = list_of_urls
            response.data = SchemaScrap.ResponseScrapURL(**{'url_list': list_of_urls})
            response.status = 200
            response.message = "Success"
        except Exception as e:
            Log.error(e)            
            response.message = "Error: " + str(e)

        return response

    # Get the detail of one article of psychologytoday.com
    # Fetch detail from db if exist, if not then insert to db
    @classmethod
    def get_article_detail(cls, url: str):
        response = BaseResponse()
        index = hashlib.md5(url.encode()).hexdigest()

        # Check if entry is available in database
        exist_in_db = ScrapingHelper.check_entry_in_db(index)
        if exist_in_db:            
            response.status = 200
            response.message = "Success"            
            # response.data = exist_in_db._original
            response.data = SchemaScrap.ResponseScrapDetail(**exist_in_db._original)
            return response

        response.status = 404
        response.message = "Error during get request"
        # If entry doesn't exist, proceed to scraping & insert to db        
        try:
            data = requests.get(url, headers=cls.headers, verify=False)
            if data.status_code == 200:
                soup = BeautifulSoup(data.text, 'html.parser')
            elif data.status_code == 404:
                response.message = "URL not found"
                return response
            else:
                return response
            # Processing for date entry
            date = soup.select('p.blog-entry__date--full')[0].get_text()
            date = re.findall(
                r'([A-Za-z]\w+ [0-9]\d{0,1}, [0-9]\d{3})',
                date
            )[0].replace(',', '')
            date = pd.to_datetime(date)        
            # Processing for paragraph entry
            huge_text = soup.select('div.blog-entry--body-second p')
            article_text = ""
            for i in huge_text:            
                article_text += i.text

            entry = {
                'index': index,
                'title': soup.select('h1.blog-entry__title--full')[0].get_text(' ', strip=True),
                'author': soup.select('h3.profile-card__profile-name a')[0].get_text(' ', strip=True),
                'magazine': soup.select('div.profile_card__blog-title a')[0].get_text(),
                'publishdate': date,
                'url': url,
                'paragraph': article_text
            }
            # Insert into db
            ScrapingHelper.input_entry_to_db(entry)
            response.status = 200
            response.message = "Success"
            response.data = SchemaScrap.ResponseScrapDetail(**entry)
        except Exception as e:
            Log.error(e)            
            response.message = "Error: " + str(e)

        return response

    @classmethod
    def get_some_articles(cls, number=5):
        results = []
        response = BaseResponse()
        try:
            temp = conn.table('psychologyarticle_detail').select('*').order_by('publishdate', 'desc').limit(number).get()
            for i in temp:
                results.append({                    
                    "title": i[1],
                    "author": i[2],
                    "magazine": i[3],
                    "publishdate": i[4],
                    "url": i[5]                
                })
            response.status = 200
            response.message = "Success"
            response.data = results
        except Exception as e:
            Log.error(e)
            response.status = 404
            response.message = "Error: " + str(e)

        return response
        


    # Get one page of articles from psychologytoday.com
    # @classmethod
    # def get_articles(cls, page_num):
    #     response = ScrapingHelper.get_one_page_psycho(page_num)
    #     return response

    # # Insert entries of articles into psychologyarticle database
    # @classmethod
    # def to_db(cls, data):
    #     cs = 'postgresql://postgres:admin@localhost/your_database'
    #     response = BaseResponse()
    #     datas = pd.DataFrame(data)
    #     Log.info(type(datas))
    #     try:
    #         db = cce(cs)
    #         with db.begin() as conn:
    #             conn.execute("""
    #                 CREATE TABLE NewArticles (
    #                     title text,
    #                     genre text,
    #                     publisher text,
    #                     publishdate timestamp without time zone,
    #                     magazine text,
    #                     url text,
    #                     summary text
    #                 )
    #             """)
    #             sql_insert_articles = f"INSERT INTO NewArticles VALUES (?,?,?,?,?,?,?)"
    #             conn.execute(sql_insert_articles, datas.values.tolist())

    #             sql_merge = """
    #                 MERGE psychologyarticle AS Target
    #                 USING #NewArticles AS Source
    #                     ON Source.title=Target.title
    #                 WHEN NOT MATCHED BY Target THEN
    #                     INSERT (title, genre, publisher, publishdate, magazine, url, summary)
    #                     VALUES (source.title, source.genre, source.publisher, source.publishdate, source.magazine, source.url, source.summary)
    #                 WHEN MATCHED THEN
    #                     UPDATE SET
    #                     Target.title = Source.title
    #                 WHEN NOT MATCHED BY Source THEN
    #                     DELETE
    #                 ;
    #             """
    #             conn.execute(sql_merge)                
    #         # Export to db using dataframe
    #         # db = cce(cs)
    #         # db_conn = db.connect()            
            
    #         # datas.to_sql('psychologyarticle', db_conn, if_exists='append', index=False, method='multi')
    #         # db_conn.close()

    #         response.message = "Success"
    #         response.status = 200
    #         response.data = len(data)
    #     except Exception as e:
    #         Log.error(e)
    #         response.status = 404
    #         response.message = "Error: "+ str(e)
    #     return response

    # # Get five most recent articles from database
    # @classmethod
    # def get_some_articles(cls, number=5):
    #     results = []
    #     response = BaseResponse()
    #     try:
    #         temp = conn.table('psychologyarticle').select('*').order_by('publishdate', 'desc').limit(number).get()
    #         for i in temp:
    #             results.append({
    #                 "title": i[0],
    #                 "genre": i[1],
    #                 "publisher": i[2],
    #                 "publishdate": i[3],
    #                 "magazine": i[4],
    #                 "url": i[5],
    #                 "summary": i[6]
    #             })
    #         response.status = 200
    #         response.message = "Success"
    #         response.data = results
    #     except Exception as e:
    #         Log.error(e)
    #         response.status = 404
    #         response.message = "Error: " + str(e)

    #     return response