# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import os
import subprocess
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

import requests
from rasa.shared.core.trackers import DialogueStateTracker
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from interface.save_report import datastore


class ActionSaveReportFull(Action):

    def name(self) -> Text:
        return "action_save_Report_full"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        datastore(tracker.get_slot("name"), tracker.get_slot("phoneNumber"), tracker.get_slot("issue"))
        dispatcher.utter_message(text="your complain recorded successfully!")

        return []


class ValidateReportFullInfoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_Report_full_Info_form"

    def validate_name(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker,
                      domain: Dict[Text, Any]) -> Dict[Text, Any]:
        if not slot_value:
            dispatcher.utter_message(text="Please provide your name.")
            print(slot_value)
            return {"name": None}
        print(slot_value)
        return {"name": slot_value}

    def validate_phoneNumber(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker,
                             domain: Dict[Text, Any]) -> Dict[Text, Any]:
        if not slot_value:
            dispatcher.utter_message(text="Please provide your phone_number.")
            return {"phoneNumber": None}
        if (len(slot_value) == 10 or len(slot_value) == 12):
            print(slot_value, "=", len(slot_value))
            return {"phoneNumber": slot_value}
        dispatcher.utter_message(text="Please provide your valid phone number.")
        return {"phoneNumber": None}

class AskForIssueAction(Action):
    def name(self) -> Text:
        return "action_ask_issue"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> dict[str, Any] | dict[str, None]:
        dispatcher.utter_message(text="Could you please tell me your problem briefly?, then I can make a complaint "
                                      "for you. our technical teams will handle your issue as soon as possible, "
                                      "and let you know.")
        issue = tracker.latest_message.get("text")
        if issue:
            return {"issue": issue}
        return {"issue": None}


class ActionUtterGoodbye(Action):
    def name(self) -> Text:
        return "action_utter_goodbye"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: DialogueStateTracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_user_details",
                                 triggered=True)
        return []


class TerminateServerAction(Action):
    def name(self) -> Text:
        return "action_terminate_server"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Terminate the Rasa chatbot
        os._exit(0)
        return []
