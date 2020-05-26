# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pprint
import pandas as pd
import time


def mars_facts():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    hemispheres = []

    for i in range(4):

        browser.find_by_css('a.product-item h3')[i].click()

        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find('h2', class_="title").get_text()
        link = soup.find("a", text="Sample").get("href")
        hemisphere = {"title" : title,
                    "link" : link}
        hemispheres.append(hemisphere)
        browser.back()

        
    pprint.pprint(hemisphere)

mars_facts()