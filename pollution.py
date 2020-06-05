from flask import Flask, render_template, request, Markup
import requests
import plotly as py
import plotly.graph_objs as go

app = Flask(__name__)

def fetch():
    try:
        no_of_results = request.form["number"]
    except:
        no_of_results = 6
    link = "https://api.thingspeak.com/channels/1019362/feeds.json?api_key=VURU7P85PQ06OZAX&results="
    data_info = requests.get(link)
    data = data_info.json()
    print("Json data from URL")
    print(data)
    print("no_of_results",no_of_results)
    no_of_results = int(no_of_results)
    return data,no_of_results

def results(with_graph = 1):
    info,no_of_results = fetch()
    total_values = len(info["feeds"])
    if total_values <= no_of_results:
        total_fetch = 0
    else:
        total_fetch = total_values-no_of_results
    date = [x["created_at"] for x in info["feeds"][total_fetch:] if int(x["field1"]) > 1000]
    value = [int(x["field1"]) for x in info["feeds"][total_fetch:] if int(x["field1"]) > 1000]
    temp = zip(date,value)
    print("date,time : ",date)
    print("Pollution value : ",value)
    if with_graph == 1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=date,y=value))
        fig.layout["font"] = dict(color="#000000",size=16)
        fig.layout["legend"] = dict(font=dict(color="black", size=12), orientation="h", bgcolor="#b0c4de")
        fig.layout["paper_bgcolor"] = "#f9f9f9"
        fig.layout['plot_bgcolor'] = "#f9f9f9"
        # fig.layout['width']=500  
        fig.layout.margin={'t':20,'l':20,'b':20,'r':20}  
        fig.layout.title=fig.layout.title={
            'text': "Visualization",
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'}
        fig.show()
    return temp

@app.route('/')
def home():
    data = results(with_graph = 0)
    return render_template('pollution.html',data = data)

@app.route('/page',methods = ['POST'])
def fetch_data():
    data = results()
    return render_template('pollution.html',data = data)

if __name__ == '__main__':
   app.run(port = 1234,debug = True)