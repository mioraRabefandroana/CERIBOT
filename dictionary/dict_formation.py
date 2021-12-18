
from utils.levenshtein import levenshtein


# seuil de comparaison
threshold = 90

# WARNING : the order is very important HERE : informatique must come before sicom ;)
formations = {
    "informatique": "informatique",
    "intelligence artificielle": "ia",
    "inge du logiciel de la societe num": "ilsen",
    "systemes informatiques communicants": "sicom",
}


"""
get formation acronym by formation using fromation dictionary
"""
def get_formation_acronym(formation):
    for name, acronym in formations.items():
        if (formation in name) or (name in formation):
            print("selected :", formation , "->", name,",",acronym)
            return acronym

    return formation


# print("--",formation," vs ", name)
# coeff = levenshtein( formation.replace(" ",""), name.replace(" ","") )
# print("coeffff ====>", coeff)
# if( coeff >= threshold ):