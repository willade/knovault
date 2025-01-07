from typing import Text, List, Dict, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from flask import url_for


# 1. Open Page Action
class ActionOpenPage(Action):
    def name(self) -> Text:
        return "action_open_page"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        page_name = tracker.get_slot('page_name')
        intent = tracker.get_intent_of_latest_message()

        # Map intent to default pages if page_name isn't explicitly mentioned
        if not page_name:
            intent_to_page = {
                "submit_lesson": "submit",
                "search_lesson": "lessons",
                "open_page": "home"
            }
            page_name = intent_to_page.get(intent)

        # Normalize page_name for matching
        page_routes = {
            "home": "/",
            "profile": "/profile",
            "submit": "/submit",
            "lessons": "/lessons",
            "analytics": "/analytics"
        }

        route = page_routes.get(page_name.lower())
        print(f"Intent: {intent}, Page Name: {page_name}, Route: {route}")

        if route:
            dispatcher.utter_message(json_message={"action": "navigate", "page": route, "text": f"Opening the {page_name} page..."})
            return []

        dispatcher.utter_message(text="I couldn't find the page you mentioned. Please try again.")
        return []


# 2. Search Lesson Action
class ActionSearchLesson(Action):
    def name(self) -> Text:
        return "action_search_lesson"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        keyword = tracker.get_slot('query')  # Assuming "page_name" is used as the search keyword slot

        if keyword:
            dispatcher.utter_message(json_message={"action": "search", "query": keyword, "text": "Searching........."})
        else:
            dispatcher.utter_message(json_message={"text": "Please provide a keyword to search for lessons."})

        return []


#3. Default Fallback Action
class ActionFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="I'm sorry, I couldn't understand your request. Could you try rephrasing?")
        return []
