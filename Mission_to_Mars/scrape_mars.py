from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import pymongo

def init_browser():
    executable_path = {"executable_path": "C:\Program Files\Google\Chrome\Application\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def IMGscrape():
    browser = init_browser()

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    img = soup.find('article', class_='carousel_item')
    img_url_long = str(img['style'])

    print(img_url_long)

    img_url_short = img_url_long.split("'")[1].strip()
    base_url = 'https://www.jpl.nasa.gov'

    featured_image_url = (str(base_url) + str(img_url_short))

    return featured_image_url

hemisphere_image_urls_test = []
news_list = []

def scrape():
    ### CALL IN SPLINTER ###

    browser = init_browser()

    ### INITIAL IMAGE PULL

    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    img = soup.find('article', class_='carousel_item')
    img_url_long = str(img['style'])

    img_url_short = img_url_long.split("'")[1].strip()
    base_url = 'https://www.jpl.nasa.gov'

    featured_image_url = (str(base_url) + str(img_url_short))

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
        news_copy = news_dict.copy()
        news_list.append(news_copy)

    ### PANDAS FACTS TABLE

    mars_facts_url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(mars_facts_url)
    mars_facts = mars_table[0]
    mars_facts.columns = ['Item', 'Figure']

    ### HEMISPHERE IMAGE PULL
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
        hemi_dict = {"title": title, "URL": mars_img_url}
        hemi_copy = hemi_dict.copy()
        hemisphere_image_urls_test.append(hemi_copy)

    return featured_image_url
    return mars_facts.head(1)
    return print(hemisphere_image_urls_test)
    return print(news_list)

    ### UPLOAD TO LOCAL MONGO DB ###

    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    db = client.hemisphere_db
    collection = db.items

    collection.insert_

### FLASK SERVER ###




