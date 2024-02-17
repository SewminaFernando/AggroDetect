import pandas as pd
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from pyarrow import null


# def datastore(name, phone_number, phone_number2=null, router_status=null,phone_status=null,Instrument_status=null):
#
#
#     if os.path.isfile("user_data.xlsx"):
#
#         df=pd.read_excel("user_data.xlsx")
#
#         df.append([name,phone_number, phone_number2, router_status, phone_status, Instrument_status])
#         df.to_excel("user_data.xlsx",index=False)
#
#     else:
#         df=pd.DataFrame([name,phone_number, phone_number2, router_status, phone_status, Instrument_status],columns=["name","phone_number", "phone_number2", "router_status", "phone_status", "Instrument_status"])
#         df.to_excel("user_data.xlsx", index=False)

# def datastore(name, phone_number, phone_number2=null, router_status=null, phone_status=null, Instrument_status=null):
#
#     data = {
#         "name": [name],
#         "phone_number": [phone_number],
#         "phone_number2": [phone_number2],
#         "router_status": [router_status],
#         "phone_status": [phone_status],
#         "Instrument_status": [Instrument_status]
#     }
#
#     if os.path.isfile("user_data.xlsx"):
#         df = pd.read_excel("user_data.xlsx")
#         df = df.append(pd.DataFrame(data))
#     else:
#         df = pd.DataFrame(data)
#
#     df.to_excel("user_data.xlsx", index=False)


def datastore(name, phone_number, phone_number2=null, router_status=null, phone_status=null, Instrument_status=null):

    data = {
        "name": [name],
        "phone_number": [phone_number],
        "phone_number2": [phone_number2],
        "router_status": [router_status],
        "phone_status": [phone_status],
        "Instrument_status": [Instrument_status]
    }

    if os.path.isfile("user_data.xlsx"):
        df = pd.read_excel("user_data.xlsx")
        df = pd.concat([df, pd.DataFrame(data)])
    else:
        df = pd.DataFrame(data)

    df.to_excel("user_data.xlsx", index=False)



def firebase_datastore(username, convesation):
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('interface/aggrodetectdb-firebase-adminsdk-g7mwx-5a58418db8.json')

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
