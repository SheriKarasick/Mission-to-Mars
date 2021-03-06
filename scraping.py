#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import traceback 

def scrape_all():
    # Initiate headless driver for deployment   
    executable_path = {'executable_path': '/users/sharonkaasick/downloads/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemi(browser),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data

# Visit the mars nasa news site
def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        
    except AttributeError as e:
        return e
    return news_title, news_p

### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    
    try:
        # find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    
    except AttributeError:
        img_url_rel = ""

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
        #Assign columns and set index of dataframe
        df.columns=['description', 'value']
        df.set_index('description', inplace=True)
        #Convert dataframe into html format, add bootstrap
        return df.to_html()
    except BaseException:
        traceback.print_exc()
        return None

# WORKING CODE FOR CHALLENGE

def mars_hemi(browser):
    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    description = img_soup.find_all('div', class_=('description'))

    list_mars = []
    img_title = []
    
    for item in description:
        extract = item.find('a', class_=('itemLink product-item'))
        img_base = extract.get("href")
        img_url_sm = f'https://astrogeology.usgs.gov{img_base}.tif'
        list_mars.append(img_url_sm)
        #print(img_url_sm)

    full_image_elem_hemi = img_soup.find_all('a', class_=('itemLink product-item'))
    hemi_title_list = []

    for item in full_image_elem_hemi: 
        extract = item.find('alt', class_='itemLink product-item')
        hemi_title = item.text
        hemi_title_list.append(hemi_title)
        #print(hemi_title_list) 
    
    hemi_title_list_clean = [string for string in hemi_title_list if string != '']


    img_url = []
    
    for i, item in enumerate(list_mars):
        browser.visit(item)
        browser.is_element_present_by_text('Sample', wait_time=1)
        original_elem = browser.find_link_by_partial_text('Sample')
        original_elem.click()
        high_res = original_elem["href"]
        img_url.append(high_res)
        
       
        traceback.print_exc()

    
    hemispheres = []

    for item in range(4):
        title = hemi_title_list_clean[item]
        url = img_url[item]
        hemi_item = {'title': title, 'img_url': url}
        hemispheres.append(hemi_item)
        # print("img_url", img_url)

    # print(hemispheres)

    return hemispheres

## END WORKING CODE FOR CHALLENGE 

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

