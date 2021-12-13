
import urllib.request
import json

def send_request(url, data):

    try:
        if(data is not None) and (len(data)>0):
            dataArray = []
            for name, value in data.items():
                dataArray.append("{0}={1}".format(name, value))
            
            glue= "&"
            dataStr = glue.join(dataArray)

            url = "{0}?{1}".format(url, dataStr)

        res = urllib.request.urlopen(url)
        encoding = res.info().get_content_charset('utf-8')
        with res as response:
            data = response.read()
            data = json.loads(data.decode(encoding))
            return data

    except Exception as error:
        print("Error => ", error)
        return None