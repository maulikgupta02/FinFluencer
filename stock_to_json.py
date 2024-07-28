import json
import os
import pandas as pd

files=os.listdir("stock_dataset")
# print(files)

data=[]
counter=1

for stock in files:
    d={"data":[]}
    df=pd.read_csv(f"stock_dataset/{stock}")
    name=stock.split(".")[0]
    d["name"]=name
    d["id"]=counter
    for ID,VALUE in df.iterrows():
        d['data'].append({"date":VALUE["Unnamed: 0"],"value":VALUE.Close})
    counter+=1
    data.append(d)
        
stocks_data=json.dumps(data,indent=2)

with open("Market_Stocks_Data", "w") as json_file:
    json_file.write(stocks_data)

print(f"JSON data has been saved to Market_Stocks_Data")