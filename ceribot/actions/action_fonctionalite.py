from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker

from utils.custom_html import custom_response_message, to_html
from utils.custom_messages import INTRO_FUNCTIONALITY

class ActionFunctionality(Action):
    def name(self) -> Text:
        return "action_fonctionalite"

    """
    convert results (json format) into a readable message
    """
    def get_result_message(self):
        text = self.get_functionalities_text()
        html = to_html( self.get_functionalities_html() )
        print(html)
        return custom_response_message(text, html)

    """
    functionalities list
    """
    def get_functionalities(self):
        functionalities = [
            "Vous pouvez me demander votre emploi du temps en précisant votre filière, niveau de formation et la date.",
            "Je peux vous donner la liste des salles disponibles pour une date donnée, l'heure de début.",
            "Si vous voulez rigoler, j'ai quelques blagues pour vous donner le sourire",
            "Besoin de challenge? Je peux évaluer votre culture générale via un quizz",
            "Vous pouvez me demander la météo",
            "Je peux consulter un wiki aussi pour vous depuis wikipedia"
        ]
        return functionalities

    """
    text formated functionalities
    """
    def get_functionalities_text(self):
        return INTRO_FUNCTIONALITY + ",\n".join(self.get_functionalities())

    """
    html formated functionalities
    """
    def get_functionalities_html(self):
        functionalities = self.get_functionalities()
        htmlIntro = "<h2 class='functionality-intro'>{0}</h2>".format(INTRO_FUNCTIONALITY)

        htmlWrapper= "<div class='functionality'>{0}</div>"
        functionalitiesHtml = "".join( [htmlWrapper.format(f) for f in functionalities] )

        return  htmlIntro + functionalitiesHtml

    """
    format functionality into a better speakable text for NAO/Pepper
    """
    def speakable_functionality(self, functionality):
        return functionality

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("----action_functionality-----")     

        dispatcher.utter_message( self.get_result_message() )
        return []