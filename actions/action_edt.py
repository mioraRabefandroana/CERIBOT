from typing import Any, Dict, List, Text
from dictionary.dict_formation import get_formation_acronym
from utils.api_urls import CERI_FORMATION_LIST_URL, DATE_PARSER_URL, EDT_BY_FORMATION_URL, EDT_BY_OPTIONS_URL, OPTIONS_BY_FORMATION_URL
from utils.custom_html import custom_response_message, to_html
from utils.custom_messages import INTRO_EDT, INTRO_SALLE_DISPONIBLE, NO_CLASSROOM_AVAILABLE, NOT_FOUND_EDT, NOT_FOUND_FORMATION, NOT_FOUND_NIVEAU
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
import re

from datetime import datetime
import subprocess

from utils.custom_url_request import send_post_request, send_request

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
    def get_result_message(self):
        # no available classroom
        if(self.message):
            msg = self.message
            html = to_html( "<h2>{0}</h2>".format(msg) )

        elif(not self.edt or len(self.edt) == 0 or not self.formationName):
            msg = NOT_FOUND_EDT
            html = to_html( "<h2>{0}</h2>".format(msg) )

        else:        
            msg = ""
            html = "<h3 class='formation-name'>{0}</h2>".format(self.formationName)
            html += "<div class='edt-date'>{0}</div>".format( datetime.strptime(self.date, '%Y-%m-%d').strftime('%d/%m/%Y') )
            for subject in self.edt:
                hourStart = self.extract_hour( subject.get("start") )
                hourEnd = self.extract_hour( subject.get("end") )

                html += "{0} - {1}\n".format(hourStart, hourEnd)
                html += self.subject_html(subject)

                msg += self.speakable_subject(subject.get("title")) +",\n"                

            html = to_html( "<div class='edt'>{0}</div>".format(html) )
            
            msg = INTRO_EDT + "\n" + self.formationName + ", \n" + self.date + ", \n" + msg

        return custom_response_message(msg, html)
    

    def subject_html(self, subject):
        return "<div class='edt-subject'>{0}</div>".format(subject.get("title")) 
        
    """
    format salle libelle into a better speakable text for NAO/Pepper
    """
    def speakable_subject(self, subjectTitle):        
        subjectTitle = re.sub(r'\n',",\n", subjectTitle)
        subjectTitle = re.sub(r' : '," ,: ", subjectTitle)
        subjectTitle = re.sub(r' = '," . ",subjectTitle)
        return subjectTitle


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
    def get_code_formation(self):
        for o in self.fromations:
            name = o.get("name")
            if( 
                self.is_fromation_names_equal(self.formation, name) 
                and
                self.is_fromation_names_equal(self.niveau, name) 
            ):
                return o.get("code"), name

        return None, None

    def is_fromation_names_equal(self, name1, name2):
        # remove all white space for better comparison
        name1 = name1.replace(" ","")
        name2 = name2.replace(" ","")

        return (name1.lower() in name2.lower()) or (name1.lower() in name2.lower())
    
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
        if(niveau is None):
            return None
        
        prefix = self.get_niveau_prefix(niveau)
        if(prefix is None):
            return None
        
        suffix = self.get_niveau_suffix(niveau)
        if(suffix is None):
            return prefix
        
        niveau = prefix + suffix
        
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
    
    """
    get date
    return today's date if no date has been found
    """
    def get_date(self):
        try:
            text = self.tracker.latest_message.get("text")
            res = send_post_request(DATE_PARSER_URL, {"text": text})
            # print("PARSED DATE :", res.get("results").get("date"))
            return res.get("results").get("date")

        except Exception:
            return f'{datetime.now():%Y-%m-%d}'


    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        self.tracker = tracker
        print("----action_edt-----")
        self.message = ""

        self.set_fromations()  

        # get date
        self.date = self.get_date()   

        # get niveau
        self.niveau = self.get_niveau()
        
        if(not self.niveau):
            dispatcher.utter_message( NOT_FOUND_NIVEAU )
            return []

        # get formation
        self.formation = self.get_formation()
        if(not self.formation):
            dispatcher.utter_message( NOT_FOUND_FORMATION )
            return []

        # get code formation : needed for the api requests
        codeFormation, self.formationName = self.get_code_formation()
        
        url = EDT_BY_FORMATION_URL(codeFormation)
        edt = send_request(url, [])

        if( (not edt) or ("results" not in edt) ):
            self.message = NOT_FOUND_EDT
        else:            
            self.edt = edt.get("results")
            self.edt = self.filter_edt({"date": self.date})
            # self.message = self.get_result_message()        
        
        # DEBUG
        print("------------------")
        print([
            self.get_formation(),
            self.niveau,
            self.date
        ])
        print("selected formation =>", self.formationName)
        print("edt URL :", url)

        dispatcher.utter_message(self.get_result_message())
        return []