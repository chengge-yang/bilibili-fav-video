
import json
import time
import os.path
import pandas
import requests
import pymysql
from flask import Flask,render_template
class Clear:
    def __init__(self,headers,cookies,params):
        self.headers = self.clear(headers)
        self.cookies = self.clear(cookies)
        self.params = self.clear(params)
    def clear(self,data):
        clear_data={str(key).replace("^",""):str(value).replace("^","") for key,value in data.items()}
        return clear_data


class MysqlDB:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "123456"
        self.database = "bilibili_data"
        self.charset = "utf8mb4"

    def save_data(self, data):
        conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset=self.charset
        )
        cursor = conn.cursor()
        sql = """
            INSERT IGNORE INTO soucang (title,author,headshot,views,video_id)
            VALUES (%s,%s,%s,%s,%s)
        """
        try:
            for item in data:
                cursor.execute(sql, (
                    item["视频标题"],
                    item["作者名字"],
                    item["头像链接"],
                    item["播放量"],
                    item["视频ID"]
                ))
            conn.commit()
            print("数据存入MySQL成功")
        except Exception as e:
            print("数据存入失败", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


    def get_data(self):
        conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset=self.charset
        )
        cursor = conn.cursor()
        cursor.execute("SELECT title,author,headshot,views,video_id FROM soucang")
        data = cursor.fetchall()

        cursor.close()
        conn.close()
        return data


class BiliSpider:
    def __init__(self, url, headers, cookies, params):

        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.params = params

        #调用Clear清洗^
        self.clean_obj = Clear(self.headers, self.cookies, self.params)

        self.req_headers = self.clean_obj.headers
        self.req_cookies = self.clean_obj.cookies
        self.req_params = self.clean_obj.params

        self.db = MysqlDB()

    def demo1(self):
        res = requests.get(
            self.url,
            headers=self.req_headers,
            cookies=self.req_cookies,
            params=self.req_params,
            timeout=5
        )
        print(res.status_code)
        print(json.dumps(res.json(), indent=4, ensure_ascii=False))
        time.sleep(2)

    def run_spider(self):
        try:
            res = requests.get(
                self.url,
                headers=self.req_headers,
                cookies=self.req_cookies,
                params=self.req_params,
                timeout=5
            )
            res.raise_for_status()
            data_json=res.json()
        except requests.exceptions.RequestException as e:
            print(f"网络请求失败:{e}")
            return False
        except ValueError as e:
            print(f"JSON解析失败:{e}")
            return False
        try:
            #print(res.status_code)
            aim_mv = data_json['data']['medias']
        except (KeyError,TypeError):
            print("响应异常,未找到'[data][medias]'")
            return False
        data = []
        for video in aim_mv:
            data.append({
                "视频ID":video["id"],
                "视频标题": video["title"],
                "作者名字": video["upper"]["name"],
                "头像链接": video["upper"]["face"],
                "播放量": video["cnt_info"]["view_text_1"]
            })

        try:
            df = pandas.DataFrame(data)
            df.to_excel("bilibili.xlsx", index=False)
            print(f"Excel路径: {os.path.abspath('bilibili.xlsx')}")
        except Exception as e:
            print(f"Excel保存失败{e}")

        try:
            self.db.save_data(data)
        except Exception as e:
            print(f"数据库保存失败:{e}")
            return False

        return True
#Flask网页
class FlaskWeb:
    def __init__(self):
        self.app = Flask(__name__)
        self.db = MysqlDB()
        self.register_route()
    def register_route(self):
        @self.app.route('/')
        def index():
            videos = self.db.get_data()
            return render_template("index.html", videos=videos)

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    headers = {}
    cookies = {}
    params = {}

    url = ""
    p1=BiliSpider(url,headers,cookies,params)

    # check=p1.demo1()

    s1=p1.run_spider()
    if not s1:
        print(f"爬虫运行失败:{s1},将直接展示数据")
    Web_html=FlaskWeb()
    Web_html.run()


