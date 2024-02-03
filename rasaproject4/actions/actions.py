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

from save_report import Datastore


class ActionSaveReport(Action):

    def name(self) -> Text:
        return "action_save_Report"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Datastore(tracker.get_slot("name"),tracker.get_slot("phone_number"),tracker.get_slot("router_status"),tracker.get_slot("phone_status"), tracker.get_slot("Instrument_status"))
        dispatcher.utter_message(text="your complain posted successfully!")

        return []

