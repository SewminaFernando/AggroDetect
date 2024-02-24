# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
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


    # def extract_phone_status(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
    #         List[Dict[Text, Any]]:
    #     phone_status = tracker.latest_message.get("text")
    #     if phone_status:
    #         return {"phone_status": phone_status}
    #     print(phone_status)
    #     return {}
    #
    # def extract_Instrument_status(self, dispatcher: CollectingDispatcher, tracker: Tracker,
    #                                     domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    #     Instrument_status = tracker.latest_message.get("text")
    #     if Instrument_status:
    #         return {"Instrument_status": Instrument_status}
    #     return {}

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
        if len(slot_value)!=10 | len(slot_value) != 12:
            dispatcher.utter_message(text="Please provide your valid phone number.")
            return {"phoneNumber": None}
        print(slot_value,"=",len(slot_value))
        return {"phoneNumber": slot_value}




    # def validate_router_status(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker,
    #                            domain: Dict[Text, Any]) -> Dict[Text, Any]:
    #     if not slot_value:
    #         dispatcher.utter_message(text="Please provide your router_status.")
    #         return {"router_status": None}
    #     return {"router_status": slot_value}
    #
    # def validate_phone_status(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker,
    #                           domain: Dict[Text, Any]) -> Dict[Text, Any]:
    #     if not slot_value:
    #         dispatcher.utter_message(text="Please provide your phone_status.")
    #         return {"phone_status": None}
    #     return {"phone_status": slot_value}
    #
    # def validate_Instrument_status(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker,
    #                                domain: Dict[Text, Any]) -> Dict[Text, Any]:
    #     if not slot_value:
    #         dispatcher.utter_message(text="Please provide your Instrument_status.")
    #         return {"Instrument_status": None}
    #     return {"Instrument_status": slot_value}


class AskForissueAction(Action):
    def name(self) -> Text:
        return "action_ask_issue"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> dict[str, Any] | dict[str, None]:
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
