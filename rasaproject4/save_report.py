import pandas as pd
import os

def Datastore(name,mobile_number, email, occupation):


    if os.path.isfile("user_data.xlsx"):

        df=pd.read_excel("user_data.xlsx")

        df.append([name,mobile_number, email, occupation])
        df.to_excel("user_data.xlsx",index=False)

    else:
        df=pd.DataFrame([name,mobile_number, email, occupation],columns=["name","mobile_number","email","occupation"])
        df.to_excel("user_data.xlsx", index=False)
