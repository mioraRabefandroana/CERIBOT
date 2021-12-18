from typing import Any, Dict, List, Text
from dictionary.dict_formation import get_formation_acronym
from utils.api_urls import CERI_FORMATION_LIST_URL, EDT_BY_FORMATION_URL, EDT_BY_OPTIONS_URL, OPTIONS_BY_FORMATION_URL
from utils.custom_messages import INTRO_EDT, INTRO_SALLE_DISPONIBLE, NO_CLASSROOM_AVAILABLE, NOT_FOUND_EDT, NOT_FOUND_FORMATION, NOT_FOUND_NIVEAU
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
    get all fromations for CERI site
    """
    def get_ceri_formation_list(self):
        url = CERI_FORMATION_LIST_URL
        fromations = send_request(url,{}).get("results")
        for o in fromations:            
            if((o.get("letter") is not None) and (o.get("letter").lower() == "informatique")):
                return o.get("names")

        return []

    """
    get code formation by a given formation name and niveau
    """
    def get_code_formation_by_formation_and_niveau(self, formation, niveau):
        for o in self.fromations:
            name = o.get("name")
            if( 
                self.is_fromation_names_equal(formation, name) 
                and
                self.is_fromation_names_equal(niveau, name) 
            ):
                return o.get("code"), name

        return None, None
    
    # TODO : ~modifier par la condition d'égalité (distance de Levenshtein)
    def is_fromation_names_equal(self, name1, name2):
        # remove all white space for better comparison
        name1 = name1.replace(" ","")
        name2 = name2.replace(" ","")

        return name1.lower() in name2.lower()
    
    """
    save fromations
    """
    def set_fromations(self):    
        self.fromations = self.get_ceri_formation_list()
    
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
    
    """
    get niveau
        format: m1, m2, l1, ....
    """
    def get_niveau(self):
        niveau = self.tracker.get_slot("niveau")
        print("niveau0: ", niveau)
        if(niveau is None):
            return None
        
        prefix = self.get_niveau_prefix(niveau)
        if(prefix is None):
            return None
        
        suffix = self.get_niveau_suffix(niveau)
        if(suffix is None):
            return prefix
        
        niveau = prefix + suffix
        print(">>>> niveau slot: [{}]".format(niveau))
        
        return niveau

    """
    try to format a given level (niveau)
    output: 
        - m for master, 
        - l for licence , 
        -else return the full level name
    """
    def get_niveau_prefix(self, niveau):  
        niveauStr = "".join( re.findall("[A-Za-z]", niveau.lower()) )
        if(not niveauStr):
            return None

        # master and licence
        niveauPrefixes = ["m", "l"] #m : master; l: licence
        for prefix in niveauPrefixes:
            res = "".join( re.findall("^{0}".format(prefix), niveauStr) )
            if(res):
                return res        
        
        return niveau

    """
    try to get the level (niveau)
        1, 2, 3
    """
    def get_niveau_suffix(self, niveau):        
        niveau = niveau.lower()
        suffix = "".join( re.findall("[0-9]", niveau) )
        if(not suffix):
            return None
        return suffix

    """
    get formation acronym for easy search
        using dictionary and comparison by "distance of levenstein"
    """
    def get_formation(self):
        formation = self.tracker.get_slot("formation")
        print("formation0 :", formation)
        if( not formation ):
            return None
        
        return get_formation_acronym(formation)
    

    def get_date(self):
        date = self.tracker.get_slot("date")
        # if(date is None):
        
        return f'{datetime.now():%Y-%m-%d}'

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        self.tracker = tracker
        print("----action_edt-----")

        # TODO : RAJOUTER LE TRAITEMENT (nettoyage) des données envoyé (<=> les phrases brutes)

        self.set_fromations()

        # url = BASE_URL + "api/salles/disponibilite"
        # requestData = {
        #     "niveau": "",
        #     "formation": "ILSEN",
        #     "option": "3"
        # }

        # data = send_request(url, requestData)
        # self.set_result( data )

        # TODO : remplacer par la valeur des slots
        # niveau = "m2"
        niveau = self.get_niveau()
        
        if(not niveau):
            dispatcher.utter_message( NOT_FOUND_NIVEAU )
            return []

        # formation = "ilsen"
        formation = self.get_formation()
        if(not formation):
            dispatcher.utter_message( NOT_FOUND_FORMATION )
            return []

        # DEBUG
        print("--------------- slots ---- ")
        print([
            self.get_formation(),
            self.get_niveau()
        ])

        # get code formation : needed for the api requests
        codeFormation, self.formationName = self.get_code_formation_by_formation_and_niveau(formation, niveau)
        
        # url = OPTIONS_BY_FORMATION_URL(codeFormation)
        # print(url)

        url = EDT_BY_FORMATION_URL(codeFormation)
        edt = send_request(url, [])

        self.date = self.get_date()        

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
        #   rehercher la filière envoyé par le slot
        #~ filter par option :  - WAITING
        #  1. interpreter l'option
        #  2. filter par l'option trouver

        # dispatcher.utter_message(self.get_result_message())
        dispatcher.utter_message(self.message)

        # return [SlotSet("name", personName)]
        return []