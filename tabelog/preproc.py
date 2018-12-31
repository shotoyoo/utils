# python: encoding utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pdb
def extract_item(df, col):
    try:
        df[col] = df[col].str.split("'", expand=True).loc[:,7]
    except Exception:
        pass
    return df
def convert_bool(df, cols):
    for col in cols:
        sr = df[col]
        sr[sr==tfs[0]] = 1
        sr[sr==tfs[1]] = 0
        df[col] = sr
    return df

if __name__=="__main__":
    df = pd.read_csv("test.csv", encoding="cp932")
    cols = []
    bools = []
    for col in df.columns:
        if isinstance(df[col][0], str) and df[col][0].startswith("Order"):
            df = extract_item(df, col)
        if isinstance(df[col][0], str) and df[col].str[:2].unique().shape[0]==2:
            df[col] = df[col].str[:2]
    df = extract_item(df, cols)
    # サブジャンルのnan
    df["sub_genre"] = df["sub_genre"].fillna("なし")
    # 平均予算のna
    df = df.iloc[np.where(~df.budget.isna())[0], :]
    # b = df["budget"].str.split("～", expand=True)
    # b.iloc[:,1] = b.iloc[:,1].str[:-1]
    # df["budget"] = np.array(b, dtype=float).mean(axis=1)
    # df["budget"] = df["budget"].fillna(df["budget"].mean())
    # capacityのnan
    df["capacity"] = df["capacity"].fillna(df["capacity"].mean())
    # 禁煙席
    no = df["non_smoking"].str.contains("禁煙席なし")
    df["non_smoking"][no] = "禁煙席なし"
    partial = df["non_smoking"].str.contains("一部禁煙")
    df["non_smoking"][partial] = "一部禁煙"
    total = df["non_smoking"].str.contains("全面禁煙")
    df["non_smoking"][total] = "全面禁煙"
    df["non_smoking"][~(no|partial|total)] = "禁煙席なし"
    # 貸切
    ka = df["charter"].str.contains("貸切可")
    huka = df["charter"].str.contains("貸切不可")
    df["charter"][ka] = "あり"
    df["charter"][huka] = "なし"
    df.to_csv("test2.csv", encoding="cp932", index=False)
    # 深夜営業
    ka = df["midnight"].str.contains("している")
    huka = df["midnight"].str.contains("していない")
    df["midnight"][ka] = "あり"
    df["midnight"][huka] = "なし"
    # バンド
    huka = df["band"].str.contains("不可")
    ka = ~huka
    df["band"][ka] = "あり"
    df["band"][huka] = "なし"
    # カード
    huka = df["card"].str.contains("利用不可")
    ka = ~huka
    df["card"][ka] = "あり"
    df["card"][huka] = "なし"
    # 必要カラム
    columns = ["name", "id", "middle_area", "genre", "sub_genre", "budget", "capacity",
          "free_drink", "free_food", "private_room", "horigotatsu", 
           "tatami", "card", "non_smoking", "charter", "parking", 
          "barrier_free", "show", "karaoke", "band", "tv", "english",
          "pet", "lunch", "midnight", "score"]

    df[columns].to_csv("test3.csv", encoding="cp932", index=False)

"""large_service_area
service_area
large_area
middle_area
small_area
lat
lng
genre
sub_genre
budget
budget_memo
catch
capacity
access
mobile_access
urls
open
close
party_capacity
wifi
other_memo
shop_detail_memo
wedding
free_drink
free_food
private_room
horigotatsu
tatami
card
non_smoking
charter
parking
barrier_free
show
karaoke
band
tv
english
pet
child
coupon_urls
course
photo
"""