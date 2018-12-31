# encoding: utf-8
import urllib.request
import requests
import pdb
import xmltodict
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

KEY = "1fa61c56392e94a6"
COUNT = 100
# グルメサーチAPI
H_API = "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/" #?key=sample&large_area=Z011
# google検索
G_SEARCH = "https://www.google.co.jp/search?num=5&q="

def hotpepper_search(keywords, start=1):
    """
    keywords : list of str
    d : dict
    """
    keys = {
        "key": KEY,
        "genre": " ".join(keywords),
        "large_area": "Z011", # 東京
        "start": start,
        "count": COUNT
    }
    url = "{}?{}".format(H_API, urllib.parse.urlencode(keys))
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as res:
            body = res.read()
        d = xmltodict.parse(body)
        return d
    except Exception as e:
        print(e)
        pdb.set_trace()

def google_search(keys):
    """
    keys : list or str
    url : 検索結果最上位のurl
    """
    url = G_SEARCH + " ".join(keys)
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        for el in soup.select("h3.r a"):
            title = el.get_text()
            print(title)
            url = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(el.get("href")).query))["q"]
            break
        return url
    except Exception as e:
        print(e)
        return ""

def tabelog_search(url):
    if "tabelog" not in url:
        print("not found tabelog page!")
        return None
    try:
        sleep(3)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        score = float(soup.find_all("span", class_="rdheader-rating__score-val-dtl")[0].string)
        print("score : {}".format(score))
        return score
    except Exception as e:
        print(e)
        print("not found tabelog score")
        return None
if __name__=="__main__":
    df = pd.read_csv("test.csv", encoding="cp932", header=0).set_index("name")
    shop_ids = set(df["id"])
    keys = ["G004"]
    # keys = ["バル"]
    # keys = ["居酒屋"]
    out = hotpepper_search(keys)
    num = int(out["results"]["results_available"])
    print("{} shops available in hotpepper".format(num))
    shops = []
    scores = []
    ind = 0
    try:
        for ind in range(0,num,COUNT):
            print("{} / {}".format(ind, num))
            out = hotpepper_search(keys, start=ind)
            tmp_shops = []
            scores = []
            for shop in out["results"]["shop"]:
                try:
                    if shop["id"] in shop_ids:
                        print("{} already in data".format(shop["name"]))
                        continue
                    url = google_search(["食べログ", shop["name"]])
                    score = tabelog_search(url)
                    if score is not None:
                        tmp_shops.append(shop)
                        scores.append(score)
                except Exception:
                    pass
            if tmp_shops:
                df2 = pd.DataFrame(tmp_shops)
                df2["score"] = scores
                df2 = df2.set_index("name")
                df = pd.concat((df, df2))
                df.to_csv("test.csv", encoding="cp932")
            
    # out2 = google_search(["信濃町", "煉瓦"])
    except KeyboardInterrupt:
        pass
    df2 = pd.DataFrame(shops)
    df2["score"] = scores
    df2 = df2.set_index("name")
    df3 = pd.concat((df, df2))
    df3.to_csv("test.csv", encoding="cp932")
    pdb.set_trace()
