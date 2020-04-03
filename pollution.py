from flask import Flask, render_template, request
import requests
app = Flask(__name__)

def fetch():
    no_of_results = request.form["number"]
    print(no_of_results)
    link = "https://api.thingspeak.com/channels/1019362/feeds.json?results="+no_of_results
    data_info = requests.get(link)
    data = data_info.json()
    return data

@app.route('/')
def home():
   return render_template('pollution.html')

@app.route('/page',methods = ['POST'])
def fetch_data():
    info = fetch()
    print(info["feeds"])
    return render_template('pollution.html',temp = info["feeds"])

if __name__ == '__main__':
   app.run(port = 1234,debug = True)