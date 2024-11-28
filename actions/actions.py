from typing import Text, List, Dict, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionOpenPage(Action):
    def name(self) -> Text:
        return "action_open_page"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve the page_name slot
        page_name = tracker.get_slot('page_name')

        if page_name:
            dispatcher.utter_message(text=f"Opening the page: {page_name}")
            dispatcher.utter_message(json_message={"action": "navigate", "page": page_name})
            # Optionally send a JSON event for the front-end
            # e.g., {"event": "open_page", "page_name": page_name}
        else:
            dispatcher.utter_message(text="I couldn't find the page name. Can you specify which page you want to open?")
        
        return []

class ActionSaveLesson(Action):
    def name(self) -> Text:
        return "action_save_lesson"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve slots
        phase = tracker.get_slot('phase')
        issue = tracker.get_slot('issue')
        solution = tracker.get_slot('solution')
        recommendation = tracker.get_slot('recommendation')

        if phase and issue and solution and recommendation:
            # Simulate saving the lesson to a database
            # Replace this with actual database logic
            dispatcher.utter_message(text=(
                f"Lesson saved successfully!\n"
                f"Phase: {phase}\n"
                f"Issue: {issue}\n"
                f"Solution: {solution}\n"
                f"Recommendation: {recommendation}"
            ))
        else:
            dispatcher.utter_message(text="Some details are missing. Please provide all required information.")

        # Reset slots after saving
        return [SlotSet("phase", None), SlotSet("issue", None),
                SlotSet("solution", None), SlotSet("recommendation", None)]

class ActionSearchLesson(Action):
    def name(self) -> Text:
        return "action_search_lesson"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve the query or keyword slot
        keyword = tracker.get_slot('page_name')  # Assuming "page_name" holds the keyword for simplicity
        if keyword:
            # Simulate a database search
            # Replace this with actual search logic
            mock_lessons = [
                {"title": "Budget Management", "phase": "Planning"},
                {"title": "Scope Creep Handling", "phase": "Execution"},
                {"title": "Communication Tips", "phase": "Closing"}
            ]
            results = [lesson for lesson in mock_lessons if keyword.lower() in lesson["title"].lower()]

            if results:
                response = "\n".join([f"{lesson['title']} ({lesson['phase']})" for lesson in results])
                dispatcher.utter_message(text=f"Found the following lessons:\n{response}")
            else:
                dispatcher.utter_message(text=f"No lessons found for '{keyword}'. Try another keyword.")
        else:
            dispatcher.utter_message(text="Please provide a topic or keyword to search for lessons.")
        
        return []

class ActionGetRecommendations(Action):
    def name(self) -> Text:
        return "action_get_recommendations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve the phase slot
        phase = tracker.get_slot('phase')
        if phase:
            # Simulate fetching recommendations
            # Replace this with actual recommendation logic
            mock_recommendations = {
                "planning": ["Define clear budgets early", "Engage stakeholders at the beginning"],
                "execution": ["Monitor resources daily", "Address risks proactively"],
                "closing": ["Document lessons learned", "Celebrate team achievements"]
            }
            recommendations = mock_recommendations.get(phase.lower(), [])
            if recommendations:
                response = "\n".join(recommendations)
                dispatcher.utter_message(text=f"Recommendations for the {phase} phase:\n{response}")
            else:
                dispatcher.utter_message(text=f"No specific recommendations found for the {phase} phase.")
        else:
            dispatcher.utter_message(text="Please specify a project phase to get recommendations.")

        return []

class ActionFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="I'm sorry, I couldn't understand your request. Could you try rephrasing?")
        return []
