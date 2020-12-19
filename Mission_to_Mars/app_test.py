from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars_test

### RUN APP ###
app = Flask(__name__)


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_test_11

mars_facts = db.facts
mars_img = db.images
mars_news = db.news

@app.route('/')
def index():
    facts = list(db.facts.find())
    img = list(db.images.find())
    news = list(db.news.find())
    return render_template('index.html', facts=facts, img=img, news=news)

@app.route('/scrape')
def scraper():
    scrape_mars_test.scrape()
    return redirect("/", code=302)

@app.route('/data')
def data():
    facts = list(db.facts.find())
    img = list(db.images.find())
    news = list(db.news.find_one())
    return render_template('index.html', facts=facts, img=img, news=news)

if __name__ == "__main__":
    app.run(debug=True)