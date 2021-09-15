from flask import (Flask, render_template, request, redirect)
from flask_pymongo import PyMongo
import scrape_mars

# instantiate Flask
app = Flask(__name__)

# MongoDB connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Identify collection
mars_data = mongo.db.mars_data

# Render index.html page
@app.route("/")
def index():

    mars_info = mars_data.find_one()
    return render_template("index.html", mars_data=mars_info)

# Route to trigger webscrapping, then return to index for rendering
@app.route("/scrape")
def scraper():

    # mars_data.drop()

    scraped_data = scrape()
    mars_data.insert_many([scraped_data])
    
    # mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mongo.db.mars_data.update({}, mars_data, upsert=True)
    return redirect('/', code=302)


if __name__ == "__main__":
    app.run(debug=True)
