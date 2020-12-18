from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

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

def scrape():
    browser = init_browser()

    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    img = soup.find('article', class_='carousel_item')
    img_url_long = str(img['style'])

    img_url_short = img_url_long.split("'")[1].strip()
    base_url = 'https://www.jpl.nasa.gov'

    featured_image_url = (str(base_url) + str(img_url_short))

    return featured_image_url

    ### PANDAS FACTS TABLE

    mars_facts_url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(mars_facts_url)
    mars_facts = mars_table[0]
    mars_facts.columns = ['Item', 'Figure']

    ### HEMISPHERE IMAGE PULL
    url_list = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced', 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced', 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced', 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']

    for url in url_list:
        browser.visit(url)

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

    return print(hemisphere_image_urls_test)



