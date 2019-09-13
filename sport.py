from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session.__init__ import Session
from tempfile import mkdtemp
import requests


app = Flask(__name__)
# app.config.from_object('app_config')
app.config["TEMPLATES_AUTO_RELOAD"] = True
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# SCOPES = ['https://www.googleapis.com/auth/calendar']
# API_SERVICE_NAME = 'calendar'
# API_VERSION = 'v3'
# CLIENT_SECRET_FILE = "/home/mprojekt/mysite/client_secret.json"
# API_KEY_FILE_NAME = 'credentials.json'   # Name of json file you downloaded earlier
# CALENDAR_ID = 'primary'
# CREDS_FILENAME = 'credentials.json'
URL = "https://live-stream365.com/api/get.php?key=84bd360faa5112bad32d69407a25e53d&lang=ru"
headers = {

 'content-type': 'application/json',

}

def api():
    response = requests.request("GET", URL, headers=headers)
    response = response.json()
    return response
@app.route("/")
def home():
    response = requests.request("GET", URL, headers=headers)
    response = response.json()

    print(response)
    # for i in response["Value"]:
    #     print(i['Start'])
    return render_template('home.html', response=response)
@app.route("/event/<id>")
def event(id):
    response = requests.request("GET", URL, headers=headers)
    response = response.json()
    # print(response['Value'][])
    for events in response['Value']:
        if events['Url'] == f"https://live-stream365.com/online/84bd360faa5112bad32d69407a25e53d/{id}":
            return render_template("event.html", event=events)
    return render_template("event.html")
@app.route('/search', methods=["GET", "POST"])
def search():
    event_list = []
    print(event_list)
    if request.method == 'POST':
        event_list = []
        response = api()
        for events in response['Value']:
            if request.form.get('search').lower() in events['Opp1'].lower() or request.form.get('search').lower() in events['Opp2'].lower() or events['Opp2'].lower() in request.form.get('search').lower() or  events['Opp1'].lower() in request.form.get('search').lower() or request.form.get('search').lower() in events['Sport'].lower():
                event_list.append(events)
                print(events)
                print(event_list)
        return render_template("search.html", event=event_list)
    return render_template("search.html")
if __name__ == '__main__':
    app.run(debug=True)