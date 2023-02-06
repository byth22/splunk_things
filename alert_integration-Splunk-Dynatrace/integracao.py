# -*- coding: utf-8 -*-
# Written by Byth22 in 21/10/22
# ===============================
# Integration script to send Splunk WAF Alert named R1 to Dynatrace
# Custom Device.
# The WAF data is sent to Splunk and mapped as an alert.
# The alert from WAF is based on a single IP and its hits.
#
#   Alert example: IP: 10.10.10.10 - 10000 hits

import requests
import json
import time
import datetime

# Class to read created csv file by Splunk Alert.
class Reader: 
    def __init__(self, path):
        self.path = path

    # Reading last line from .csv file.
    def read_last_line(self): 
        # Looping to attempt two times to read the file.
        for i in range(1,3):
            try:
                with open(self.path, "r") as file:
                    # get last line, replace comma to colon and store it.
                    self.last_line = file.readlines()[1].replace(","," : ")
                    break

            except IOError:
                time.sleep(5)
                pass

        #return 1

    def get_last_line(self):
        # Return content without new lines
        return self.last_line.strip('\n')

class Sender:
    def __init__(self, texto):
        self.texto = texto
        self.description = 'Contagem de eventos baseado em regra de bot\
manager (WAF Akakmai) para endpoint /<YOUR_ENDPOINT> no host\
<YOUR_HOST_THAT_GENERATE_LOGS>. IP e quantidade:'

        self.annotationDescription = 'Error a ser tratado pelo time de\
seguranca: (contato_aqui)'

    # Payload creator function.
    def payloadCreator(self):
        # Join parsed text from dyna.csv to payload R1 alert template.
        # Set and custom your payload based on custom device.
        self.data = '''{
    "eventType": "RESOURCE_CONTENTION",
        "attachRules": {
            "entityIds": ["<YOUR_CUSTOM_DEVICE>"],
            "tagRule": [{
                "meTypes": ["HOST"],
                "tags": [{
                    "context": "CONTEXTLESS",
                    "key": "<YOUR_KEY>"
                } ]
            }]
        },
        "source": "SPLUNK",
        "title": "Alerta R1 - Akamai %s",
        "description": "%s",
        "annotationDescription": "%s"
}
''' % (str(datetime.datetime.now()), str(self.description)+' '+str(self.texto), str(self.annotationDescription))

        return 0

    def requester(self):
        # Required header.
        headers = {
            'Content-Type': 'application/json',
        }

        # Required Param.
        # Set your Api Token in the Api-token iten.
        params = {
            'Api-Token': \
            'YOUR_APY_TOKEN',
        }

        # Stored response.
        # Set your Dynatrace Api Endpoints in the first argument.
        response = requests.post('https://<YOUR_DYNA_ENDPOINT>.dynatrace.com/api/v1/events',
                                 params=params,
                                 headers=headers,
                                 data=self.data)

        return 0

            
if __name__ == '__main__':
    # instancing Reader Class
    arquivo = Reader('/opt/splunk/etc/apps/search/lookups/dyna-teste.csv')

    # Reading last line from .csv
    arquivo.read_last_line()

    # Sending request to API
    envio = Sender(arquivo.get_last_line())
    envio.payloadCreator()
    envio.requester()
