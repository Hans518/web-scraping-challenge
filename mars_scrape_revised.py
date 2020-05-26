from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # create mars_data dict that we can insert into mongo

    # Visit news site to grab first news story. 
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html

    # Create Soup object for news site 
    soup = BeautifulSoup(html, 'lxml')
    news_title = soup.find('div', class_="bottom_gradient").h3.text
    news_p = soup.find('div', class_="article_teaser_body").text

    ###                                                                         ###    
     # ------------------------------------------------------------------------- #
    ###                                                                         ### 

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # HTML object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Click the full image button 
    image_class = soup.find('a', class_="button fancybox")
    full_image_click = image_class.get("id")
    browser.click_link_by_id(full_image_click)
    browser.is_element_present_by_id("fancybox-lock")
    time.sleep(10)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # after_full_image_click = soup.body.prettify()

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
    base_url = "https://www.jpl.nasa.gov"
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

    df = pd.read_html(url)
    mars_facts = df[0]
    mars_facts = mars_facts.set_index(0)
    mars_facts = mars_facts.rename(columns={0:'', 1:'value'})
    mars_facts_table = mars_facts.to_html(index_names=False)
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
        "news_title" : news_title,
        "news_desc" : news_p,
        "feat_im" : im_url,
        "weather" : mars_weather,
        "facts" : mars_facts_table,
        "hemispheres" : hemispheres
    }

    return mars_dict
    



