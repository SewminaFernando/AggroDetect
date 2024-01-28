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


class ActionSaveReport(Action):

    def name(self) -> Text:
        return "action_save_Report"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Datastore
        dispatcher.utter_message(text="Hello World!")

        return []


class FormDataCollect(FormAction):
    # def validate_name(self,slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict,)-> Dict[Text, Any]:
    # def validate_phone_number(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker,
    #                       domain: DomainDict, ) -> Dict[Text, Any]:

    def name(self) -> Text:

        return "validate_simple_pizza_form"

    def validate_name(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        return {"name": slot_value}

    def validate_phone_number(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        return {"phone_number": slot_value}

    def validate_complain(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:

    def validate_router_status(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:

    def validate_phone_status(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:

    def validate_Instrument_status(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:


    # @staticmethod
    # def required_slots(tracker: "Tracker") -> List[Text]:
    #     return ["name", "number", "complain", "router_status", "phone_status", "Instrument_status"]
    #
    # def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
    #     return {
    #         "name": [self.from_entity(entity="name")], "number": [self.from_entity(entity="p_number")],
    #         "complain": [self.from_text()], "router_status": [self.from_text()], "Instrument_status": [self.from_text()]
    #     }
    #
    # def submit(
    #         self,
    #         dispatcher: "CollectingDispatcher",
    #         tracker: "Tracker",
    #         domain: Dict[Text, Any],
    # ) -> List[EventType]:
    #     dispatcher.utter_message("your complain is recorded successfully. Our agent will call with progress. ")
    #     return []
