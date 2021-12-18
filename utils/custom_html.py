
messageGlue = "$$$$$"
def to_html(text):
    html = '<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link href="css/style.css" rel="stylesheet"><title>CERIBOT</title></head><body>{0}</body></html>'
    html = html.format(text).replace("\n", "<br/>").replace("\\n", "<br/>")
    return html

def custom_response_message(text, html):
    return "{0}$$$$${1}".format(text,html)