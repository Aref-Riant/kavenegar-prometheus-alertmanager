from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from io import BytesIO
from kavenegar import *
import datetime

listen_on = 6725
labels_to_use = ["alertname", "cluster", "instance", "severity"]
group_by_label = "alertname"
sms_hold_time_minutes = 10
kavenegar_token = "****"
receptors = "****"
sender = "***"

messages = dict()
last_sms_timestamp = datetime.datetime.min

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        alerts = json.loads(body)
        global messages
        global last_sms_timestamp
        print(b'This is POST request. ')
        print(b'Received: ')
        #print(alerts['alerts'])
        #print(response.getvalue())

        for alert in alerts['alerts']:
            message = ""
            if (alert['status'] == "firing"):
                for label in labels_to_use:
                    message += label + ": " + alert['labels'][label] + "\n"
                    if (label == group_by_label):
                        pass
                    else:
                        if not alert['labels'][group_by_label] in messages: messages[alert['labels'][group_by_label]] = dict()
                        if not label in messages[alert['labels'][group_by_label]]: messages[alert['labels'][group_by_label]][label] = set()
                        messages[alert['labels'][group_by_label]][label].add(alert['labels'][label])
            #print(message)
        print(messages)
        if ((datetime.datetime.now() - last_sms_timestamp) > datetime.timedelta(minutes = sms_hold_time_minutes)):
            try:
                api = KavenegarAPI(kavenegar_token)
                params = {
                        'sender': sender,
                        'receptor': receptors,
                        'message': str(messages),
                        }
                response = api.sms_send(params)
                print(str(response).encode('utf-8'))
                messages = dict()
                last_sms_timestamp = datetime.datetime.now()
            except APIException as e:
                print(e)
            except HTTPException as e:
                print(e)



httpd = HTTPServer(('localhost', listen_on), SimpleHTTPRequestHandler)
httpd.serve_forever()
                                                                                                                                                          74,21         Bot

