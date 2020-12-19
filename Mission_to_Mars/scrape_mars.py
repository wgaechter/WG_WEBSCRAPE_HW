from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import pymongo

def init_browser():
    executable_path = {"executable_path": "C:\Program Files\Google\Chrome\Application\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

# def IMGscrape():
#     browser = init_browser()

#     url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
#     browser.visit(url)

#     html = browser.html
#     soup = BeautifulSoup(html, "html.parser")

#     img = soup.find('article', class_='carousel_item')
#     img_url_long = str(img['style'])

#     print(img_url_long)

#     img_url_short = img_url_long.split("'")[1].strip()
#     base_url = 'https://www.jpl.nasa.gov'

#     featured_image_url = (str(base_url) + str(img_url_short))

#     return featured_image_url

# hemisphere_image_urls_test = []
# news_list = []

def scrape():
    ### CALL IN SPLINTER ###

    browser = init_browser()

    ### CONNECT TO MONGODB ###
    # Create DB and collections

    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    db = client.mars

    db.create_collection('facts')
    db.create_collection('images')
    db.create_collection('news')

    mongo_facts = db.facts
    mongo_images = db.images
    mongo_news = db.news

    ### INITIAL IMAGE PULL ###

    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    img = soup.find('article', class_='carousel_item')
    img_url_long = str(img['style'])

    img_url_short = img_url_long.split("'")[1].strip()
    base_url = 'https://www.jpl.nasa.gov'

    featured_image_url = (str(base_url) + str(img_url_short))

    large_img_dict = {"title": 'large_img', "URL": featured_image_url}

    mongo_images.insert_one(large_img_dict)

    ### NEWS SCRAPE ###

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    results = soup.find_all('div', class_='list_text')

    for r in results:
        news_title = r.find('a').text
        IP = r.find('div', class_="article_teaser_body").text

        news_dict = {"title": news_title, "body": IP}
        
        mongo_news.insert_one(news_dict)

    ### PANDAS FACTS TABLE ###

    mars_facts_url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(mars_facts_url)
    mars_facts = mars_table[0]
    mars_facts.columns = ['Item', 'Figure']
    facts_dict = mars_facts.to_dict('records')

    for fact in facts_dict:
        mongo_facts.insert_one(fact)

    ### HEMISPHERE IMAGE PULL ###
    url_list = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced', 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced', 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced', 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']

    for u in url_list:
        browser.visit(u)

        html = browser.html
        soup = BeautifulSoup(html, "html.parser")

        mars_img = soup.find('img', class_='wide-image')
        mars_img_url_half = str(mars_img['src'])

        mars_base_url = 'https://astrogeology.usgs.gov'

        mars_img_url = (mars_base_url + mars_img_url_half)

        title = soup.find('h2', class_='title').text
        image_dict = {"title": title, "URL": mars_img_url}

        mongo_images.insert_one(image_dict)
        
    #return featured_image_url
    #return mars_facts.head(1)
    #return print(hemisphere_image_urls_test)
    #return print(news_list)
    return print("Completed Scrape and Mongo Connection")







