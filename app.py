from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use Flask Pymongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_dict = mongo.db.mars_dict.find_one()
    # Return template and data
    return render_template("index.html", mars=mars_dict)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run scrape function
    mars_dict = mongo.db.scrape_info()

    # Update Mongo database using update and upsert=True
    mars_dict.db.collection.