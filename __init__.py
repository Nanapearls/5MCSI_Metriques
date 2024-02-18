from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')#commentaires
@app.route("/contact/")
def MaPremiereAPI():
   return render_template('ananas.html') 

@app.route('/histogramme/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    jour = []
    temp=[]
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        jour.append(dt_value)
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        temp.append(temp_day_value)
    data = {'Jour': jour, "Température": temp}
    df = pd.DataFrame(data)    
    sns.histplot(x=jour, bins=len(jour), kde=False, color='skyblue')
    plt.xlabel('Jour')
    plt.ylabel("Température")
    plt.title("Les Températures journalières")
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
    plt.close()
   # return render_template('histogramme.html', image_base64=image_base64)
    return render_template('histogramme.html')

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})
  
if __name__ == "__main__":
  app.run(debug=True)
