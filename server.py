from flask import json
from flask import request
from flask import Flask
import subprocess
import sys
import os

app = Flask(__name__)

@app.route("/")
def main():
    return "Welcome to Flask http server"


@app.route('/prometheus', methods=['POST'])

def webhook_api_prometheus():
    if request.headers['Content-Type'] == 'application/json':
        print ("json file received ")
        my_date = json.dumps(request.json)
        dict_info = json.loads(my_date)
        for i in dict_info['alerts']:
            alert =i['labels']['alertname']
            alert_loc = i['labels']['instance']
            print(alert,alert_loc)
            if(alert == 'HighCpuLoad'):
                print("Request for Scaling...")

                out = subprocess.Popen("ps -Alf | grep 'python autoscale.py' | wc | tr -s  \ | cut -f2 -d' '",stdout = subprocess.PIPE,shell =True)
                (numpro,err) = out.communicate()

                #print(int(numpro))
                if int(numpro) <= 2 :
                    print('Scaling in Progress...')
                    os.system('python autoscaleup.py 1')
                else:
                   print("XOpera already running..Try again Later")
            elif(alert == 'LowCpuLoad'):

                print('Time to Scale Down')
                out = subprocess.Popen("ps -Alf | grep 'python autoscale.py' | wc | tr -s  \ | cut -f2 -d' '",stdout = subprocess.PIPE,shell =True)
                (numpro,err) = out.communicate()

                #print(int(numpro))
                if int(numpro) <= 2 :
                    print('Scaling in Progress...')
                    os.system('python autoscaleup.py -1')
                else:
                   print("XOpera already running..Try again Later")

            elif(alert == 'InstanceDown'):
                print('Restart Instance/Node exporter')
            else:
                print('some other thing')
        return (my_date)
    else:
        return("Connected Anyway")





if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5004)
