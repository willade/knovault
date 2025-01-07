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

        # Debug log
        print(f"Intent detected: {intent}")
        print(f"Page slot detected: {page_name}")

        # Map intent to default pages if page_name isn't explicitly mentioned
        if not page_name:
            intent = tracker.get_intent_of_latest_message()
            intent_to_page = {
                "submit_lesson": "submit",  # Map intent to 'submit' page
                "search_lesson": "lessons",
                "open_page": "home"  # Default to home
            }
            page_name = intent_to_page.get(intent)

        # Map slot values to web app routes
        page_routes = {
            "home": "/",
            "Profile": "Profile",
            "submit_lesson": "submit",
            "lessons": "lessons",
            "analytics": "analytics"
        }

        if page_name and page_name.lower() in page_routes:
            route = page_routes[page_name.lower()]
            json_payload={"action": "navigate", "page": route, "text": "Opening the {page_name} page..."}
            dispatcher.utter_message(json_message=json_payload)
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
            dispatcher.utter_message(json_message={"action": "search", "query": keyword, "text": "Searching for {keyword}."})
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
