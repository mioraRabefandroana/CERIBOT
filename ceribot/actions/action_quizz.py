from typing import Any, Dict, List, Text
# from actions.utils.custom_url_request import send_request
from utils.api_urls import JOKE_URL, QUIZZ_URL
from rasa_sdk import Action, Tracker
import urllib.request
import json
import subprocess
from rasa_sdk.events import SlotSet

from utils.custom_html import custom_response_message, to_html
from utils.custom_messages import QUIZZ_FALSE, QUIZZ_NOTICE, QUIZZ_TRUE
from utils.custom_url_request import send_request

class ActionGetQuizz(Action):
    def name(self) -> Text:
        return "get_quizz"

    """
    convert results (json format) into a readable message
    """
    def get_result_message(self):

        question = self.quizz.get("question")
        print(question)
        msg = question + ",\n"
        html = "<h2 class='quizz-question'>{0}</h2>".format( question )

        choices = self.quizz.get("choix")
        msg += QUIZZ_NOTICE

        for i,choice in enumerate(choices):
            html += "<div class='quizz-choice'>{0} - {1}</div>".format( (i+1), choice )
            msg += "{0} : {1},\n".format( i, choice )

        html += "<div class='quizz-notice'>{0}</div>".format( QUIZZ_NOTICE.replace(",", "") )

        html = to_html( html )

        return custom_response_message(msg, html)


    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("----get_quizz-----")        
        url = QUIZZ_URL
        self.quizz = json.loads( urllib.request.urlopen(url).read() ).get("results")

        dispatcher.utter_message(self.get_result_message())
        return [SlotSet("quizz", self.quizz.get("id"))]



class ActionSubmitQuizz(Action):
    def name(self) -> Text:
        return "submit_quizz"

    """
    convert results (json format) into a readable message
    """
    def get_result_message(self):
        quizz = self.quizzResult.get("quizz")
        isCorrect = self.quizzResult.get("juste") == True
        correctAnswer = self.quizzResult.get("reponse")
        html = ""
        msg = ""
        if( isCorrect ):
            msg = QUIZZ_TRUE
            html = "<h1 class='quizz-message quizz-message-success'>{0}</h1>".format( QUIZZ_TRUE )
        else:
            msg = QUIZZ_FALSE
            html = "<h1 class='quizz-message quizz-message-error'>{0}</h1>".format( QUIZZ_FALSE )
            msg += "La bonne réponse est, :\n {0}".format(correctAnswer)
        


        question = quizz.get("question")
        html += "<h2 class='quizz-question'>{0}</h2>".format( question )

        choices = quizz.get("choix")
        msg += QUIZZ_NOTICE

        formatedUserAnswer = self.quizzResult.get("proposer")
        for i,choice in enumerate(choices):
            className = ""
            if(int(i+1) == int(quizz.get("reponse"))):
                className = "correct-answer"

            if not isCorrect and (int(i+1) == formatedUserAnswer):
                className = "wrong-answer"
            html += "<div class='quizz-choice {0}'>{1} - {2}</div>".format( className, (i+1), choice )

        html = to_html( html )

        return custom_response_message(msg, html)

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("----submit_quizz-----")
        try:
            quizzId = tracker.get_slot("quizz")
            self.userAnswer = tracker.get_slot("reponse_quizz")
            
            url = QUIZZ_URL
            self.quizzResult = send_request(url, {
                "quizz": quizzId,
                "reponse": self.userAnswer
            }).get("results")
            
            print([quizzId, self.userAnswer])

            dispatcher.utter_message(self.get_result_message())
            
            # reset quizz after finishing
            return [SlotSet("quizz", None)]

        except Exception as error:
            print("error =>", error)
            dispatcher.utter_message("Pas de quizz en cours")
            return []