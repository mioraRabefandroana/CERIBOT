from typing import Any, Dict, List, Text
from utils.api_urls import CERI_OPTIONS_LIST_URL, EDT_BY_FORMATION_URL, EDT_BY_OPTIONS_URL, OPTIONS_BY_FORMATION_URL
from utils.custom_messages import INTRO_EDT, INTRO_SALLE_DISPONIBLE, NO_CLASSROOM_AVAILABLE, NOT_FOUND_EDT
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
import re

from datetime import datetime

from utils.custom_url_request import send_request

"""
Niveau : ex: Master 1, Licence 2, ...
Formation (filière) : ex: ILSEN, ...
-------
Options : CLA, ALT, Appli 1, Appli 2
"""

class ActionEdt(Action):
    def name(self) -> Text:

        return "action_edt"

    
    """
    save resutls
    """
    def set_result(self, value):
        self.results = value.get("results")

    """
    convert results (json format) into a readable message
    """
    # TODO : formater toutes les données pour la lecture
    def get_result_message(self):
        # no available classroom
        if(not self.edt or len(self.edt) == 0 or not self.formationName):
            return NOT_FOUND_EDT
        
        msg = INTRO_EDT +"\n"
        msg += self.formationName + ", \n"
        msg += self.date + ", \n"
        for subject in self.edt:
            hourStart = self.extract_hour( subject.get("start") )
            hourEnd = self.extract_hour( subject.get("end") )
            msg += "de, {0} à {1},\n".format(hourStart, hourEnd)

            msg += self.speakable_subject(subject.get("title")) +",\n"

            msg += "\n\n"
            
        return msg
    
    # TODO : appliquer le formatage
    def speakable_subject(self, subjectTitle):        
        subjectTitle = re.sub(r'\n',",\n", subjectTitle)
        subjectTitle = re.sub(r' : '," ,: ", subjectTitle)
        subjectTitle = re.sub(r' = '," . ",subjectTitle)
        return subjectTitle
    
    """
    format salle libelle into a better speakable text for NAO/Pepper
    """
    def speakable_salle_libelle(self, libelle):
        libelle = re.sub(r'^s',"salle ", libelle)
        libelle = re.sub(r'=',".",libelle)
        libelle = re.sub(r' 0'," ",libelle)
        return libelle

    """
    get all options for CERI site
    """
    def get_ceri_options_list(self):
        url = CERI_OPTIONS_LIST_URL
        options = send_request(url,{}).get("results")
        for o in options:            
            if((o.get("letter") is not None) and (o.get("letter").lower() == "informatique")):
                return o.get("names")

        return []

    """
    get code formation by a given formation name and niveau
    """
    def get_code_formation_by_formation_and_niveau(self, formation, niveau):
        for o in self.options:
            name = o.get("name")
            if( 
                self.is_option_names_equal(formation, name) 
                and
                self.is_option_names_equal(niveau, name) 
            ):
                return o.get("code"), name

        return None, None
    
    # TODO : modifier par la condition d'égalité (distance de leve.. machin)
    def is_option_names_equal(self, name1, name2):
        return name1.lower() in name2.lower()
    
    """
    save options
    """
    def set_options(self):    
        self.options = self.get_ceri_options_list()
    
    """
    filter edt 
        filer : {date, ..}
    """
    def filter_edt(self, filter):
        date = filter.get("date")
        filteredEdt = []
        for subject in self.edt:
            subjectDate = self.extract_date(subject.get("start"))

            if(subjectDate == date):
                filteredEdt.append(subject)
        
        return filteredEdt

    """
    extract date string from a given datetime string
        first 10 char
    """
    def extract_date(self, value):
        return value[0:10]

    """
    extract hour
        from position 11 to 16
    """
    def extract_hour(self, value):
        return value[11:16]

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("----action_edt-----")

        # TODO : RAJOUTER LE TRAITEMENT (nettoyage) des données envoyé (<=> les phrases brutes)

        self.set_options()

        # url = BASE_URL + "api/salles/disponibilite"
        # requestData = {
        #     "niveau": "",
        #     "formation": "ILSEN",
        #     "option": "3"
        # }

        # data = send_request(url, requestData)
        # self.set_result( data )

        # TODO : remplacer par la valeur des slots
        niveau = "m2"
        formation = "ilsen"

        codeFormation, self.formationName = self.get_code_formation_by_formation_and_niveau(formation, niveau)
        # url = OPTIONS_BY_FORMATION_URL(codeFormation)
        # print(url)
        url = EDT_BY_FORMATION_URL(codeFormation)
        edt = send_request(url, [])
        self.date = f'{datetime.now():%Y-%m-%d}'

        if( (not edt) or ("results" not in edt) ):
            self.message = NOT_FOUND_EDT
        else:            
            # print(formationName)
            self.edt = edt.get("results")
            self.edt = self.filter_edt({"date": self.date})

            self.message = self.get_result_message()
        
        
        print("selected formation =>", self.formationName)
        print("edt URL :", url)
       
        #     print(options)
        #     options = options.get("results")
        #     options = [ o.get("code") for o in options ]
        #     print("url ==>", EDT_BY_OPTIONS_URL(options))
        #     # edt = send_request(EDT_BY_OPTIONS_URL(options), []).get("results")
        #     self.message = "succès"    
        # print(options)

        #TODO :
        # lister les option - OK
        # filtrer par filière : - OK
        #   rehercher la filière envoyé par le slot - WAITING
        # filter par option :
        #  1. interpreter l'option
        #  2. filter par l'option trouver

        # dispatcher.utter_message(self.get_result_message())
        dispatcher.utter_message(self.message)

        # return [SlotSet("name", personName)]
        return []