# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from tkinter import EventType
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union
from rasa.core.actions.forms import FormAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from save_report import firebase_datastore
from save_report import datastore
from interface.app import dict_to_pickle
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
        datastore([tracker.get_slot("name"), tracker.get_slot("phone_number"), tracker.get_slot("phone_number2"), tracker.get_slot("phone_status"), tracker.get_slot("Instrument_status")])
        dispatcher.utter_message(text="your complain recorded successfully!")

        return []

class ActionSaveReportInternet(Action):

    def name(self) -> Text:
        return "action_save_Report_internet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        datastore([tracker.get_slot("name"), tracker.get_slot("phone_number"), tracker.get_slot("router_status"), tracker.get_slot("phone_status"), tracker.get_slot("Instrument_status")])
        dispatcher.utter_message(text="your complain recorded successfully!")

        return []


class ActionUtterGoodbye(Action):
    def name(self) -> Text:
        return "action_utter_goodbye"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        flag = dict_to_pickle()
        if flag:
            with open('rasaproject4\old_conv.pkl', 'rb') as f:
                # Load the data from the file
                old_conv = pickle.load(f)

            print(old_conv)

        # Send the custom JSON response
        dispatcher.utter_message(text="thank you for calling us. have a nice day!")

        firebase_datastore('chuula', old_conv) # 'chuula' is a dummy username
        return []
# class ActionUtterGoodbye(Action):
#     def name(self) -> Text:
#         return "utter_goodbye"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         value_to_return = True
#
#         # Send the value back as part of the response
#         dispatcher.utter_message(text="thank you for calling us. have a nice day!",metadata={"value": value_to_return})
#
#         # Include the value in the metadata of the response
#         return []

    # class ActionUtterGoodbye(Action):
    #     def name(self) -> Text:
    #         return "utter_goodbye"
    #
    #     def run(self, dispatcher: CollectingDispatcher,
    #             tracker: Tracker,
    #             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    #         # Generate the custom JSON response
    #
    #         json_response = {
    #             "message": "thank you for calling us. have a nice day!",
    #             "meta": True
    #         }
    #         # Send the custom JSON response
    #         dispatcher.utter_message(json_message=json_response)
    #         dispatcher.utter_message(text="your complain recorded successfully!")
    #
    #         return []
