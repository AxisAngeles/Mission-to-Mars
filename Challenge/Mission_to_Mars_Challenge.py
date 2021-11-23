#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[105]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[5]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[6]:


slide_elem.find('div', class_='content_title')


# In[7]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[9]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[10]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[12]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[13]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[14]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[15]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[16]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[106]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[171]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
titles = []
image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
mars_soup = soup(html, 'html.parser')

### Find hemisphere's images and titles
hemisphere_desc = mars_soup.select('div.description')

### Create a list for each title
[titles.append(hem.find('h3').get_text()) for hem in hemisphere_desc if hem not in titles]

### Click in each img and get the corresponding URL
images_elems = browser.find_by_tag('div.description a')

for img in range(len(images_elems)):
    full_image_elem = browser.find_by_tag('div.description a')[img]
    full_image_elem.click()
    full_img_soup = soup(browser.html, 'html.parser')
    img_url_rel = full_img_soup.find('img', class_='wide-image').get('src')
    img_url = f'https://marshemispheres.com/{img_url_rel}'
    if img_url not in image_urls:
        image_urls.append(img_url)
    browser.visit(url)

### Zip the images and titles to make the final list of dictionaries 
hems_info = zip(image_urls,titles)

for hem in hems_info:
    hem_dicts = {}
    hem_dicts["img_url"]=hem[0]
    hem_dicts["title"]=hem[1]
    hemisphere_image_urls.append(hem_dicts)


# In[172]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[173]:


# 5. Quit the browser
browser.quit()

