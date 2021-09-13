from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from flask import Flask
from flask_pymongo import PyMongo
import time

# Browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

scraped_data = {}

# Mars News
nasa_url = "https://redplanetscience.com" 
browser.visit(nasa_url)
time.sleep(5)

html = browser.html
soup = bs(html, 'html.parser')

news_title = soup.find('div', class_='content_title').text
news_p = soup.find('div', class_='article_teaser_body').text
print(news_title)
print(news_p)

scrape_nasa_news={"Title":news_title, "Paragraph":news_p}
scrape_nasa_news
scraped_data ["Title"] = news_title
scraped_data["Paragraph"] = news_p

# Feature Photo
mars_url = "https://spaceimages-mars.com" 
browser.visit( mars_url)
image_html = browser.html
soup = bs( image_html, "html.parser")

featured_image = soup.find_all("img", class_ = "headerimage fade-in")[0]["src"]
featured_image_url = mars_url + "/" + featured_image
print(featured_image_url)

jpl = {"featured_image_url":featured_image_url}
scraped_data["img_url"] = featured_image_url

browser.quit()

# Mars Facts
facts_url = "https://galaxyfacts-mars.com/"
facts_data = pd.read_html(facts_url)
facts_data
facts_df = facts_data[0]
facts_table = facts_df.to_html(index=False)
facts_table.replace("\n", "")
mars_facts = {"htmlTable":facts_data}
scraped_data["htmlTable"] = facts_df.to_html


# Mars Hemispheres
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
hem_url = 'https://marshemispheres.com/'
browser.visit(hem_url)
html = browser.html
soup = bs(html, 'html.parser')

items = soup.find_all('div', class_='item')

hemi_urls = []
hemi_title = []
for item in items:
    hemi_urls.append( hem_url + item.find('a')['href'])
    hemi_title.append( item.find('h3').text.strip())

hemi_img_urls = []
for url in hemi_urls:
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    source_url = hem_url + soup.find('img',class_='wide-image')['src']
    hemi_img_urls.append( source_url)

usgs = []
for i in range( len( hemi_title)):
    usgs.append({ 'title':hemi_title[i], 'img_url':hemi_img_urls[i]})

# Dictionary of all Mars Info Scraped
mars_dict ={"Title": news_title, "Paragraph": news_p, "featured_image_url": featured_image_url, 
            "facts_table": facts_table, "hem_url":hem_url}

browser.quit()