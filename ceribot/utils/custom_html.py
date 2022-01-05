import os
messageGlue = "$$$$$"

# without css : for Pepper
def to_html(text):
    html = '<div>{0}</div>'
    html = html.format( text.replace("\n", "<br/>").replace("\\n", "<br/>") )
    return html

# with css : for browser
# def to_html(text):
#     css = get_css()
#     html = '<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link href="css/style.css" rel="stylesheet">{0}<title>CERIBOT</title></head><body>{1}</body></html>'
#     html = html.format( css, text.replace("\n", "<br/>").replace("\\n", "<br/>") )
#     return html


def get_css():
    try:
        cssFilePath = os.getcwd()+"/utils/style.css"
        f = open(cssFilePath, "r")
        css =  f.read()
        return "<style>{0}</style>".format( css )
    except Exception:
        print("Error ---> : CSS")
        return ""

def custom_response_message(text, html):

    f = open("page.html", "w")
    f.write(html)
    f.close()

    return "{0}$$$$${1}".format(text,html)