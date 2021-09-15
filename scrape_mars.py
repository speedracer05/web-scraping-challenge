from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import time

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
scrape_nasa_news={"Title":news_title, "Paragraph":news_p}
scraped_data ["Title"] = news_title
scraped_data["Paragraph"] = news_p

# Featured Image
mars_url = "https://spaceimages-mars.com" 
browser.visit( mars_url)
image_html = browser.html
soup = bs( image_html, "html.parser")
featured_image = soup.find_all("img", class_ = "headerimage fade-in")[0]["src"]
featured_image_url = mars_url + "/" + featured_image
jpl = {"ImageURL":featured_image_url}
jpl
scraped_data["ImageURL"] = featured_image_url
browser.quit()

# Mars Facts
facts_url = "https://galaxyfacts-mars.com/"
facts_data = pd.read_html(facts_url)
facts_data[1]
mars_facts = facts_data[1]
mars_facts.rename(columns={0: "Description",1: "Mars"}, inplace=True)
mars_facts = mars_facts.set_index("Description")

facts_table = mars_facts.to_html(index=False)
facts_table
scraped_data["TableHTML"] = mars_facts.to_html()

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
    
hemisphere_urls = []
for i in range(len(hemi_title)):
    hemisphere_urls.append({"title":hemi_title[i], "url":hemi_img_urls[i]})

browser.quit()

# Dictionary of all Mars Info
mars_dict ={"Title": news_title, "Paragraph": news_p, "ImageURL": featured_image_url, 
            "Table": facts_table, "ListImages": hemisphere_urls}
mars_dict


# MongoDB and Flask Application
from pymongo import MongoClient
conn =  "mongodb://localhost:27017/mars_mission_scraping"
client =  pymongo.MongoClient(conn)

db = client.mars_mission_scraping
db.mars_data.drop()
db.mars_data.insert_many([mars_dict])

query_result = (db.mars_d.find())
query_result

browser.quit()

if __name__ == "__main__":

    print(scrape_all())