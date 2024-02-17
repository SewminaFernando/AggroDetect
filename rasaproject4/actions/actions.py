import subprocess
from tkinter import EventType
from typing import Any, Text, Dict, List, Union
from rasa.core.actions.forms import FormAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from save_report import firebase_datastore
from save_report import datastore
import pickle

class ActionSaveReportFull(Action):

    def name(self) -> Text:
        return "action_save_Report_full"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        datastore([tracker.get_slot("name"), tracker.get_slot("phone_number"), tracker.get_slot("phone_number2"), tracker.get_slot("router_status"), tracker.get_slot("phone_status"), tracker.get_slot("Instrument_status")])
        dispatcher.utter_message(text="your complain recorded successfully!")

        return []

class ActionSaveReportPhone(Action):

    def name(self) -> Text:
        return "action_save_Report_phone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        datastore([tracker.get_slot("name"), tracker.get_slot("phone_number"), tracker.get_slot("phone_number2"), "_", tracker.get_slot("phone_status"), tracker.get_slot("Instrument_status")])
        dispatcher.utter_message(text="your complain recorded successfully!")

        return []

class ActionSaveReportInternet(Action):

    def name(self) -> Text:
        return "action_save_Report_internet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        datastore([tracker.get_slot("name"), tracker.get_slot("phone_number"), "_", tracker.get_slot("router_status"), tracker.get_slot("phone_status"), tracker.get_slot("Instrument_status")])
        dispatcher.utter_message(text="your complain recorded successfully!")

        return []


class ActionUtterGoodbye(Action):
    def name(self) -> Text:
        return "action_utter_goodbye"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Send the custom JSON response
        dispatcher.utter_message(text="thank you for calling us. have a nice day!")
        print("hi")
        # with open('interface\old_conv.pkl', 'rb') as f:
        #     old_conv = pickle.load(f)
        # firebase_datastore('chuula6', old_conv) # 'chuula' is a dummy username

        # rasa_server_process = subprocess.Popen(['pkill', '-f', 'rasa', '-e'])
        # rasa_server_process.wait()  # Wait for the process to finish
        # # Terminate the action server
        # action_server_process = subprocess.Popen(['pkill', '-f', 'rasa_sdk', '-e'])
        # action_server_process.wait()
        return []





