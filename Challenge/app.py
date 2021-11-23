# 1) Dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# 2) Set the Flask app.
app = Flask(__name__)

# 3) Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# 4) Home Route
@app.route("/")
def index():
    mars = mongo.db.mars_app.find_one()
    return render_template("index.html", mars=mars)

# 5) Scrape Route:
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars_app
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

# 6) Code that tells Flask to run the code.
if __name__ == "__main__":
   app.run()
