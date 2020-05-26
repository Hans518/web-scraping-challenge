from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape_revised


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route('/')
def index():

    mars_data = mongo.db.collection.find_one()

    return render_template('index.html', mars=mars_data)


@app.route('/scrape')
def scrape():

    # Run the scrape function
    mars_scrape_data = mars_scrape_revised.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_scrape_data, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
