# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa.shared.core.trackers import DialogueStateTracker
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from interface.save_report import datastore


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
            tracker: DialogueStateTracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_user_details",
                                 triggered=True)
        return []
