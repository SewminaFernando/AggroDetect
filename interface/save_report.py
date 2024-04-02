import pandas as pd
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from pyarrow import null
import re


def datastore(name, phoneNumber, issue):
    data = {
        "name": [name],
        "phoneNumber": [phoneNumber],
        "issue": [issue],

    }

    if os.path.isfile("user_data.xlsx"):
        df = pd.read_excel("user_data.xlsx")
        df = pd.concat([df, pd.DataFrame(data)])
    else:
        df = pd.DataFrame(data)

    df.to_excel("user_data.xlsx", index=False)

def extract_number(string):
    number_string = ''.join(filter(str.isdigit, string))
    if number_string:
        return int(number_string)
    else:
        return 0


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


def firebase_datastore(username, convesation, department):

    db_reference = db.reference('users/')
    db_get = db_reference.get()

    convesation["Department"] = department

    if username == "":
        usernames = list(db_get.keys())
        max_number = max(extract_number(un) for un in usernames if extract_number(un) > 0)
        username = "unknown_"+str(max_number+1)

        db_reference.child(username).set(convesation)
        print(f"'{username}' your conversation has been uploaded to database as a new user...")

def read_users_data_from_firebase():
    users_ref = db.reference('users')

    # Get all users' data from the database
    users_data = users_ref.get()

    # Dictionary to store all users' data
    all_users_data = {}
    all_users_ids = []

    # Iterate over each user and their data
    for user_id, user_data in users_data.items():
        all_users_ids.append(user_id)
        # Store user data in the dictionary
        all_users_data[user_id] = user_data

    return all_users_data, all_users_ids


def separate_aggressive_levels(sentence):
    # Define the pattern to match the aggressive levels
    pattern = r'\(aggressive level by voice: (\w+)\) \(aggressive level by text: (\w+)\)'

    # Find all matches of the pattern in the sentence
    matches = re.findall(pattern, sentence)

    # If matches are found, separate the aggressive levels and the remaining sentence
    if matches:
        remaining_sentence = re.sub(pattern, '', sentence)
        return remaining_sentence.strip(), matches
    else:
        return sentence.strip(), []


# Function to convert the dictionary into the desired format
def convert_to_conversation_dict(original_dict):
    conversation_dict = {}
    for key, value in original_dict.items():
        var = {"department": value["Department"].lower(), "department_text": value["Department"] + " Department"}
        sender = "Chatbot"
        conversation = []
        for i in range(len(value["resp"])):
            if i < len(value["user_message"]):
                if i != 0:
                    remaining_sentence, aggressive_levels = separate_aggressive_levels(value["user_message"][i])
                    agg_levels = f"(aggressive level by voice: {aggressive_levels[0][0]}) \n(aggressive level by text: {aggressive_levels[0][1]})"
                    conversation.append({
                        "sender": "User",
                        "message": remaining_sentence,
                        "time": agg_levels
                    })
            conversation.append({
                "sender": sender,
                "message": value["resp"][i],
                "time": ""
            })

        conversation_dict[key] = var, conversation
    return conversation_dict
