import pandas as pd
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


def datastore(name, mobile_number, email, occupation):


    if os.path.isfile("user_data.xlsx"):

        df=pd.read_excel("user_data.xlsx")

        df.append([name,mobile_number, email, occupation])
        df.to_excel("user_data.xlsx",index=False)

    else:
        df=pd.DataFrame([name,mobile_number, email, occupation],columns=["name","mobile_number","email","occupation"])
        df.to_excel("user_data.xlsx", index=False)


def firebase_datastore(username, convesation):
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('aggrodetectdb-firebase-adminsdk-g7mwx-5a58418db8.json')

    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://aggrodetectdb-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

    # As an admin, the app has access to read and write all data, regradless of Security Rules
    ref = db.reference('users')


    child_name = username # username
    child_data = {
        "conversation": convesation,
        "aggresion_level": "Angry"
    }

    ref.child(child_name).set(child_data)
