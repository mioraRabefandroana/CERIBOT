# DATE PARSER
Cet api a été conçu pour récupérer la date et heure contenu dans un texte.
## Fonctionement
Il suffit d'envoyer une requête post avec le format de données suivant:
```
{"text": "le texte contenant la date à extraire"}
```
## Format de sortie
```
{
    "results" {
        "date" : "AAAA-mm-dd",
        "hour" => "hh:mm"
    }
}
```

## Dépendance
Cet api fait appel à un serveur `Duckling` en local. Il faut donc que celui-ci soit en marche pour que l'api puisse fonctionner.
```
sudo docker run -p 8000:8000 rasa/duckling
```
