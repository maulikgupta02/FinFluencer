import pandas as pd
import json

preds=pd.read_csv("refined_predictions.csv")

def CRED_SCORE(preds2):    

    from datetime import date, timedelta
    from sklearn.metrics import mean_absolute_percentage_error

    PREDICTIONS=[]
    ACTUAL=[]
    predictions=[]
    for ID, DATA in preds2.iterrows():

        if (date.today() - DATA['datetime']) > timedelta(days=30):
            name=DATA.source

            df = pd.read_csv(f"stock_dataset/{DATA['stock']}.csv")
            df.index = pd.to_datetime(df["Unnamed: 0"])
            df.index=df.index.date

            start_date = DATA['datetime']
            end_date = start_date + timedelta(days=30)

            df = df[(df.index >= start_date) & (df.index <= end_date)]

            if DATA['advice'] == "Buy":
                change = float(max(df['Close'])-df[df.index==DATA.datetime]['Close'])
                PREDICTIONS.append(change)
                ACTUAL.append(DATA.target)
            else:
                change = float(-min(df['Close'])+df[df.index==DATA.datetime]['Close'])
                PREDICTIONS.append(change)
                ACTUAL.append(DATA.target)

        if  (date.today() - DATA['datetime']) < timedelta(days=60):
            d2={ "stockInfo": DATA.stock_info,
            "date": DATA.datetime.strftime('%Y-%m-%d'),
            "targetValue": DATA.target,
            "advice": DATA.advice}
            predictions.append(d2)
            
    credibility=abs(mean_absolute_percentage_error(ACTUAL,PREDICTIONS))*100

    return {"score":credibility,"predictions":predictions}

counter=0
json_file=[]

for person in preds["source"].unique():
    
    d={}

    preds2=preds[preds["source"]==person]
    preds2.datetime=pd.to_datetime(preds2.datetime)
    preds2.datetime=preds2.datetime.dt.date
    
    d["id"]= counter
    d["name"]= preds2.iloc[0].source
    d["description"]="ma_chuda"
    d["imageURL"]="naughty"

    d2=CRED_SCORE(preds2)
    d["credibilityScore"]=d2["score"]
    d["predictions"]=d2["predictions"]

    json_file.append(d)

    counter+=1

# print(json_file)

json_file=json.dumps(json_file,indent=2)

with open("Market_Predictions", "w") as js_file:
    js_file.write(json_file)

print(f"JSON data has been saved to Market_Predictions")