BASE_URL = "https://edt-api.univ-avignon.fr/app.php"

CLASSROOM_AVAILAIBILITY_URL = BASE_URL + "/api/salles/disponibilite"
CERI_OPTIONS_LIST_URL = BASE_URL + "/api/elements"
JOKE_URL = "http://localhost/api/joke/index.php"

def OPTIONS_BY_FORMATION_URL(codeFormation):
    return "{0}/api/tdoptions/{1}".format(BASE_URL, codeFormation)

def EDT_BY_FORMATION_URL(codeFormation):
    return "{0}/api/events_promotion/{1}".format(BASE_URL, codeFormation)

def EDT_BY_OPTIONS_URL(codeOptions):
    return "{0}/api/events_tdoption/{1}".format(BASE_URL, "-".join(codeOptions))