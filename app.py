from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
from scrape_mars import scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Identify collection
mars_data = mongo.db.mars_data

# Render index.html palge
@app.route("/")
def index():

    mars_info = mars_data.find_one()
    return render_template("index.html", data_db=mars_info)

# Route to trigger webscrapping, then return to index for rendering
@app.route("/scrape")
def scraper():

    mars_data.drop()

    scraped_data = scrape()
    mars_data.insert_many([scraped_data])
    
    # mars = mongo.db.mars
    # mars_data = scrape_mars.scrape_all()
    # mars.update({}, mars_data, upsert=True)
    return redirect('/', code=302)


if __name__ == "__main__":
    app.run(debug=True)
