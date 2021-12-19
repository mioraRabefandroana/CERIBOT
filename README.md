# CERIBOT

## Dépendance
[requirement.txt](requirement.txt)


```bash
pip install -r requirement.txt
```

## Entrainement
```bash
rasa train --domain domain
```

## Démarage serveurs
### duckling
```bash
sudo docker run -p 8000:8000 rasa/duckling
```
