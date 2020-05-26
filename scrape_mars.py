
# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pprint
import pandas as pd
import time


def scrape_mars():

    # Defines the path to the chrome driver and create a browser object
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    # Defines url of site to be scraped and navigates to it
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # HTML object 
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'lxml')
    #print(soup.prettify())
    time.sleep(5)
    # Scrapes the first news headline and description and save to variable 
    news_title = soup.find('div', class_="bottom_gradient").h3.text
    news_p = soup.find('div', class_="article_teaser_body").text

    ###                                                                         ###    
     # ------------------------------------------------------------------------- #
    ###                                                                         ### 

    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # HTML object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Click the full image button 
    image_class = soup.find('a', class_="button fancybox")
    full_image_click = image_class.get("id")
    browser.click_link_by_id(full_image_click)
    browser.is_element_present_by_id("fancybox-lock", wait_time=10)
    time.sleep(10)


    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    after_full_image_click = soup.body.prettify()

    # Clicks the more info button
    b = soup.body.find('div', class_="buttons")
    lin = b.find_all('a')
    more_in = lin[1].get('href')
    browser.links.find_by_partial_href(more_in).click()
    

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Scraping partial url for featured image and saving to variable. Then appending the partial url to a base url for a full url to the featured image.
    base_url = "jpl.nasa.gov"
    im_page = soup.select_one("figure.lede a img")
    im = im_page.get("src")
    im_url = base_url + im

    ###                                                                         ###    
     # ------------------------------------------------------------------------- #
    ###                                                                         ### 

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(5)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").text

    ###                                                                         ###    
     # ------------------------------------------------------------------------- #
    ###                                                                         ### 

    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find_all('td')

    df = pd.read_html(url)
    mars_facts = df[0]

    mars_facts_table = mars_facts.to_html()
    #mars_facts_table = mars_facts_table.replace('\n', '')
    #pprint.pprint(mars_facts_table)

    ###                                                                         ###    
     # ------------------------------------------------------------------------- #
    ###                                                                         ### 

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

    ###                                                                         ###    
     # ------------------------------------------------------------------------- #
    ###                                                                         ###
    browser.quit()

    mars_dict = {
        "feat_im" : im_url,
        "news_title" : news_title,
        "news_desc" : news_p,
        "weather" : mars_weather,
        "facts" : mars_facts_table,
        "hemishperes" : hemispheres
    } 

    print(mars_dict)

    #printing function results
    # print("------------------------------------------------------")
    # print(" ")
    # print(f' Image url: {im_url}')
    # print(" ")
    # print("------------------------------------------------------")
    # print(" ")
    # print(f' News title: {news_title}')
    # print(f' News desc: {news_p}')
    # print(" ")
    # print("------------------------------------------------------")
    # print(" ")
    # print(f' Mars weather: {mars_weather}')
    # print(" ")
    # print("------------------------------------------------------")
    # print(" ")
    # print(f' Mars facts: {mars_facts_table}')
    # print(" ")
    # print("------------------------------------------------------")
    # print(" ")
    # print(f' Mars Hemispheres: {hemispheres}')
    # print(" ")
    # print("------------------------------------------------------")

scrape_mars()

