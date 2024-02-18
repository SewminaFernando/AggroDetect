import pandas as pd
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from pyarrow import null
import re


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

# datastore("John", "1234567890", phone_number2="0987654321", router_status="Online", phone_status="Active", Instrument_status="Working")

def firebase_datastore(username, convesation):
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate(cert={
        "type": "service_account",
        "project_id": "customerdialogue-31e3d",
        "private_key_id": "0866c8bc00bf0c672009cb86d97680ab87c8496a",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDFL/aNosYAb/LT\nfmhojc6rFq7VCASMMeuc/w0F1C7EqXju8vHwAq4EN5O9RYHOAwO8StsFhCsPITyz\ns+t7fM6JuvgFYphmrgisoQUFfelyC1/KzAyDF6k4b4cLpJbeIhSyRn1I5pI/QQD/\nkuVjX+vIr6dF/GrfkXa2LlZsi8QuBVyxd0cdIulD+BfShyDZNqee5YRWAD8juI+V\nWiLJjgbu/sNSNwl+VJ6oAEKgUfmE/+GHnw2S5BEPyuJVpYOoJuMTcI0YVVOREh09\nXazVvi/bjyeyIO9GRm4BvT+P/fzPHVQL/tlzaL/40qDML92+Qh8fIl5ajqiBqPpS\ntLOmpxofAgMBAAECggEAW9hOyULnYd3C52KqBAUFHaiHj39YCurXmT0tFilyDTT4\nuKedLBM7dYhjfpXI86lwzHu7T3Lz0WzERtmHVfHYi8tz6aI2ZSErtiib26Z9nRqS\nKDXpoAfd0IUWDETB5r5OEImHonSO6vp+mgwUXziW7NdwHMeJChBJkGq943ooStxv\npsGv6XKIZpLoYXYBy4CoOClgjh4RRJnSrdzZ5lSUU4myvA0COzbfMUrYwxIModt0\n+IzMG8O4SegrZVdq9/VC954yfFn8zw5iLwsD9fKMEPUadZ7y3OV+pyIKdSxSBxBm\ntmMPnzfZFJ/updeX8lxcLXJuhVDyHNrnx5vGzl0gcQKBgQDxwdnPDUHJE0WYiGXN\nLlgERLl6MOjCqsW6K3EdVCespOhuqO3Ck7SPUXKuQgDw0dvpTJ+kX8elWqjSVQ4W\n5pgEaeZEcxXDauh6ashFqN7Nitoky5t9TunObkehhjUl4AVxWiOpoRN8Eh+8D8JQ\n/KUyCsY0TWfNH0vDKAG92ficTwKBgQDQzepkYdPvZrlodFTmtw45m/eK/nrGLew8\nQUTzgHDTdsYs0+zNOj7B0zvZYY0UQc43NEC00/XDVhgcBi/TG/yurRYUnIoJlY/r\nS2e+OgwwPWZsO29FhyGv8fxIHP3G+b2PtFPxZRZk05cYKd1Yz6Y43XleyqOn8p50\n5AwO7aUhMQKBgCG8FCGhTvG4/7gmKFZ2Rg/qaxtS4dfwLoEo+LLIAHVF2a0/Y1YI\neGSbT+5jBXCVSCOI7qnoN5qqSO54seueJ85N3LTmfj3zmBck+WdHBjgWTRRfWQYm\nUdfdaZ9vc9EiLoA/vMQ51tc0TDtY05urdX3DJR89QePMnyzPU1bjqJ5fAoGAeAJR\nvF4ptEgDOlDaVzxQ9bV5wi5fHDZat4r/+UASGMgEQNGRIadfWIFyvY7+yezEfCAR\nLJ1CfIGoG7tGk3xbb33V2gTapYWLkT3mo4Oza6puirhiTMDNENXxHPVkuo7hb43C\nTVS/WTXvepjdOmUmcTqBvoSTKT0d66sCbzYRGZECgYBQDcDUfKguB3OgkURBaTx4\ntHUqAaoJwiYV3AMLUPeSUeMG7VNTekfYkXz5gSC8kjbLaH3Rv9gwzVJFB9kidIEf\nQJnUsjmvUHC8O1QT6Mlw90YxL7FfxP5Hy9XUKa0Vn2r5wrZwNSlAcsbJGUsgLZJG\nO388vfB74FG/jU7eg/itJw==\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-y801i@customerdialogue-31e3d.iam.gserviceaccount.com",
        "client_id": "112878831213774022434",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-y801i%40customerdialogue-31e3d.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    })
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://customerdialogue-31e3d-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })
    user_exist = False

    if username in db.reference('users/').get():
        user_exist = True
    last_number = 0
    if user_exist:
        db_ref = db.reference("users/"+username+"/conversation").get()

        last_number = int(re.search(r'\d+$', list(db_ref.keys())[-1]).group())


    # firebase_admin.get_app("aggrodetectdb")
    # As an admin, the app has access to read and write all data, regradless of Security Rules
    ref = db.reference('users')
    conv_no = 'conv_'+str(last_number+1)
    child_name = username  # username
    child_data = {
        "conversation": {conv_no: convesation},
        "aggresion_level": "Angry"
    }

    ref.child(child_name).set(child_data)
    print("Saved to database")
