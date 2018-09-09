from twilio.twiml.messaging_response import MessagingResponse
import os
from flask import Flask, request
import urllib2
import json

app = Flask(__name__)

def getWeather (zip) :

	url = 'http://api.openweathermap.org/data/2.5/forecast?zip='+str(zip)+'&APPID=7be810aae98a845e8ed9e9e40db54b9d'
	response = urllib2.urlopen(url)

	html = response.read()
	data = json.loads(html)
	for i in range(0,3):
	    weather = data['list'][i]['weather'][0]['description']
	    if "rain" in weather:
	        final_weather = weather
	    else:
	        final_weather = weather

	min = 400
	max = 0
	for i in range(0,3):
	    temperature_min = data['list'][i]['main']['temp_min']
	    temperature_max = data['list'][i]['main']['temp_max']
	    if temperature_max > max:
	        max = temperature_max
	    if temperature_min < min:
	        min = temperature_min

	low_temp = 'Low: '+str(1.8(min-273.15)+32)+'F'
	high_temp = 'Low: '+str(1.8(max-273.15)+32)+'F'
	response.close()
	return "Your zipcode is {}, \n {} \n {} \n {}".format(zip,final_weather,low_temp,high_temp)

@app.route("/sms", methods=['POST'])
def incoming_sms():

    body = request.values.get('Body', None)
    print(request.values)
    print(body)

    resp = MessagingResponse()
    resp.message(getWeather(body))

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

