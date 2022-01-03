from datetime import datetime
from typing import Any, Dict, List, Text
from utils.custom_html import custom_response_message, to_html
from utils.custom_url_request import send_post_request, send_request
from utils.api_urls import CLASSROOM_AVAILAIBILITY_URL, DATE_PARSER_URL
from utils.custom_messages import INTRO_SALLE_DISPONIBLE, NO_CLASSROOM_AVAILABLE
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
import re

class ActionSalleDisponible(Action):
    def name(self) -> Text:

        return "action_salle_disponible"

    """
    save resutls
    """
    def set_result(self, value):
        self.results = value.get("results")

    """
    convert results (json format) into a readable message
    """
    def get_result_message(self):
        # no available classroom
        if(not self.results or len(self.results) == 0):
            return NO_CLASSROOM_AVAILABLE
        
        msg = INTRO_SALLE_DISPONIBLE
        htmlIntro = "<h2 id='salle-disponible-title'>{0}</h2>".format(INTRO_SALLE_DISPONIBLE.replace(",",""))
        html = ""
        for salle in self.results:
            libelle = salle["libelle"]
            msg += self.speakable_salle_libelle(libelle) + ",\n"
            html += "<div class='salle-disponible'>{0}</div>".format(libelle)
        html = to_html( "{0}<div id='salle-diponible-wrapper'>{1}</div>".format(htmlIntro, html) )
        return custom_response_message(msg, html)

    """
    format salle libelle into a better speakable text for NAO/Pepper
    """
    def speakable_salle_libelle(self, libelle):
        if("stat" not in libelle):
            libelle = re.sub(r'^s',"salle ", libelle)
        libelle = re.sub(r'=',".",libelle)
        libelle = re.sub(r' 0'," ",libelle)
        return libelle

    def get_site(self):
        return "CERI"
    
    """
    get date
    return today's date if no date has been found
    """
    def get_date_and_hour(self):
        try:
            text = self.tracker.latest_message.get("text")
            res = send_post_request(DATE_PARSER_URL, {"text": text})
            # print("PARSED DATE0 :", res)
            date =  res.get("results").get("date")

            hours =  res.get("results").get("hours")
            minTime = datetime.now().replace(hour=8, minute=30)
            maxTime = datetime.now().replace(hour=19, minute=0)
            hour = None
            for h in hours:
                givenTime = datetime.now().replace(hour=int(h[0:2]), minute=int(h[3:5]))
                if (givenTime > maxTime) or (givenTime < minTime) :
                    continue
                hour = h
                break
            
            if(not date):
                date = f'{datetime.now():%Y-%m-%d}'
            if(not hour):
                hour = f'{datetime.now():%H:00}'

            return {
                "date": date,
                "hour": hour
            }

        except Exception as e:
            print("e=> ", e)
            return {
                "date": f'{datetime.now():%Y-%m-%d}',
                "hour": f'{datetime.now():%H:00}'
            }
            # return f'{datetime.now():%Y-%m-%d}'
    
    # fixed at 1h30
    def get_duree(self):
        return "1.30"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("----action_classroom_availability-----")
        self.tracker = tracker
        dateHour = self.get_date_and_hour()

        url = CLASSROOM_AVAILAIBILITY_URL

        requestData = {
            "site": self.get_site(),
            "date": dateHour.get("date"),
            "debut": dateHour.get("hour").replace(":","."),
            "duree": self.get_duree()
        }
        print(requestData)

        data = send_request(url, requestData)
        self.set_result( data )


        dispatcher.utter_message(self.get_result_message())
        return []