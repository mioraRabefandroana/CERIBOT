# API Quizz
Cet api retourne un quizz aléatoirement et vérife les résultat envoyé
## Récupération d'un quizz
Il suffit de lui envoyer une requête http. un quizz sera retourné au hasard
### Résultat
Un quizz a le format de données suivant
```
{
    "results":{
        // l'ID du quizz
        "id":3,

        // la question
        "question":"Qu'est-ce qu'un CPU ?",

        // les choix
        "choix":["Un processeur","Une carte ,video","Un disque dur"],

        // la réponse : correspondant à l'index de la liste dees choix à partir de 1
        "reponse":1}
    }
```

## Vérification d'un quizz
Envoyé en paramètre de requête GET le quizz ID et la réponse 
### Exemple
```
http://localhost:8000/api/quizz/index.php?quizz=1&reponse=un
```
### Résultat
```
{
    "results":
        {
            // statut de la réponse : vrai ou faux
            "juste":true,

            // reponse proposer par l'utilisateur (envoyé)
            "proposer":1,

            // réponse exact en text
            "reponse":"1 , HTTP",

            // détails du quizz
            "quizz": {
                "id":1,
                "question":
                "Quel est le langage informatique le plus couramment utilis\u00e9 pour \u00e9crire les pages web ?",
                "choix":["HTML","HTTP","Java"],
                "reponse":1}}
            }
```
