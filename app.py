# Import dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

#Set up flask
app = Flask(__name__)

# Connect Python to Mongo using PyMongo
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Deine route for the html page
@app.route("/")
def index(): #Runs a function to create the index page
   mars = mongo.db.mars.find_one() #finds the Mars collectionin our database
   return render_template("index.html", mars=mars) #tells flask to return an html template

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

if __name__ == "__main__":
    app.run()