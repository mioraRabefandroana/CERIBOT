
from utils.levenshtein import levenshtein


# seuil de comparaison
threshold = 90

formations = {
    "intelligence artificielle": "ia",
    "inge du logiciel de la societe num": "ilsen",
    "systemes informatiques communicants": "sicom",
    "informatique": "informatique"
}


"""
get formation acronym by formation using fromation dictionary
"""
def get_formation_acronym(formation):
    for name, acronym in formations.items():
        if (formation in name) or (name in formation):
            return acronym

    return formation


# print("--",formation," vs ", name)
# coeff = levenshtein( formation.replace(" ",""), name.replace(" ","") )
# print("coeffff ====>", coeff)
# if( coeff >= threshold ):