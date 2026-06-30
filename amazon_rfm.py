import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.4f' % x)

df_ = pd.read_csv("/Users/gurse/Desktop/Datasetler ve Projeler/Amazon/Amazon.csv")
df = df_.copy()
df.head()
df.info()
df.isnull().sum()
df.groupby("OrderStatus")["OrderID"].count()
df = df[df["OrderStatus"] == "Delivered"]
df["OrderDate"] = pd.to_datetime(df["OrderDate"])

df.describe().T

df["CustomerID"].nunique()
df.groupby("CustomerID").agg({"TotalAmount": "sum"}).sort_values("TotalAmount", ascending=False)

df["OrderDate"].max() #29.12.2024
df["OrderDate"].min() #01.01.2020
analys_date = dt.datetime(2024,12,30)

rfm = pd.DataFrame()

rfm = df.groupby('CustomerID').agg({'OrderDate': lambda OrderDate: (analys_date - OrderDate.max()).days,
                                     'OrderID': lambda OrderID: OrderID.nunique(),
                                     'TotalAmount': lambda TotalAmount: TotalAmount.sum()})
rfm.columns = ['recency', 'frequency', 'monetary']
rfm.head()

rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) +
                   rfm['frequency_score'].astype(str))

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)
rfm.head()

new_df = pd.DataFrame()
new_df["segment"] = rfm["segment"]
new_df.head()
new_df.to_csv("segment_list.csv")





