# CERIBOT

## Entrainement
```bash
rasa train --domain domain
```

## Démarage serveurs
### serveur rasa
```bash
rasa run --enable-api --cors "*"
```
### serveur rasa actions
```bash
rasa run actions
```

## Dépendance externe
### duckling
[Duckling](https://duckling.wit.ai/) est un serveur permettant l'extraction des dates contenu dans du texte
```bash
sudo docker run -p 8000:8000 rasa/duckling
```
