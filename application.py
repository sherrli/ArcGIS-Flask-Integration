from flask import Flask, redirect, render_template, request, url_for, jsonify
import os
from flask_simple_geoip import SimpleGeoIP
from twilio.rest import Client
from helpers import lookup


app = Flask(__name__)

simple_geoip = SimpleGeoIP(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/smalltrails")
def smalltrails():
    return render_template("smalltrails.html")

@app.route("/diseases")
def diseases():
    return render_template("diseases.html")
    
@app.route("/userlocation")
def userlocation():
    geoip_data = simple_geoip.get_geoip_data()
    latitute = geoip_data["location"]["lat"]
    longitude = geoip_data["location"]["lng"]

    if not os.environ.get("TWILIO_AUTH_TOKEN"):
        raise RuntimeError("AUTH_TOKEN not set")
    auth_token=os.environ.get("TWILIO_AUTH_TOKEN")
    
    if not os.environ.get("TWILIO_ACCOUNT_SID"):
        raise RuntimeError("ACCOUNT_SID not set")
    account_sid=os.environ.get("TWILIO_ACCOUNT_SID")
    
    if not os.environ.get("twilio_from"):
        raise RuntimeError("from number not set")
    twilio_from=os.environ.get("twilio_from")
    
    if not os.environ.get("TWILIO_ACCOUNT_SID"):
        raise RuntimeError("to number not set")
    to_num=os.environ.get("to_num")

    client = Client(account_sid, auth_token)
    
    message = client.messages \
        .create(
             body='This is the ship that made the Kessel Run in fourteen parsecs?',
             from_=twilio_from,
             to=to_num
         )
    
    print(message.sid)
    
    
    return render_template("userlocation.html", lat=latitute, lon=longitude)
    
    
@app.route("/news")
def news():
    """Look up articles for geo."""

    # ensure parameters are present
    # geo = request.args.get("geo")
    geo = '95060'
    if not geo:
        raise RuntimeError("missing geo")

    # lookup articles and store them as JSON array
    article_list = lookup(geo)

    # TODO
    print(article_list)
    news = jsonify(article_list)    
    print(news)
    # return render_template("index.html")
    return article_list

    
@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


if __name__ == "__main__":

    app.secret_key = 'LOL MONEY'
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8081
    )
    
