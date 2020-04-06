from flask import Flask, render_template, request,Markup
import requests
import numpy as np
import os
import base64
from io import BytesIO
import matplotlib.pylab as plt

app = Flask(__name__)

def fetch():
    no_of_results = request.form["number"]
    link = "https://api.thingspeak.com/channels/1019362/feeds.json?api_key=VURU7P85PQ06OZAX&results="
    data_info = requests.get(link)
    data = data_info.json()
    print(data)
    no_of_results = int(no_of_results)
    return data,no_of_results

@app.route('/')
def home():
    imgFile = "./static/img.png"
    if os.path.isfile(imgFile):
        os.remove(imgFile)
    return render_template('pollution.html')

@app.route('/page',methods = ['POST'])
def fetch_data():
    info,no_of_results = fetch()
    total_values = len(info["feeds"])
    if total_values <= no_of_results:
        total_fetch = 0
    else:
        total_fetch = total_values-no_of_results
    date = [x["created_at"] for x in info["feeds"][total_fetch:]]
    value = [int(x["field1"]) if int(x["field1"])>=100 else int(x["field1"])*100 if int(x["field1"])<10 else int(x["field1"])*10 for x in info["feeds"][total_fetch:]]
    temp = zip(date,value)
    date = [x[:10] for x in date]
    d = {date[i]:value[i] for i in range(len(date))}
    d = sorted(d.items())
    x,y = zip(*d)
    plt.plot(x,y, color='green', linestyle='solid', linewidth = 2)
    plt.xlabel('Date', fontsize=15)
    plt.ylabel('Pollution', fontsize=15)
    plt.yticks(np.arange(100, 2000, 150))
    plt.savefig('./static/img.png')
    html = "<img src='./static/img.png'>"
    return render_template('result.html',temp = temp,image = Markup(html))

if __name__ == '__main__':
   app.run(port = 1234,debug = True)