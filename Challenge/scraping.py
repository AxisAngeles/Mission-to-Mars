#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoupsc
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# Import PANDAS to scrape tables
import pandas as pd

# Import Datetime
import datetime as dt

### ----------------------------------------------------
### D2. UPDATE THE WEB APP WITH MARS'S HEMISPHERE DATA
### ----------------------------------------------------

def scrape_all():

    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Set the two returning variables from mars_news.
    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = hemisphere_data(browser)

    # Run all scraping functions and store results in dictionary
    data = {
      
      ### D2-STEP 2) Create a new dict to hold the list of dictionaries
      # with the URL string and title of each hemisphere image
      "hemisphere_data": hemisphere_image_urls,
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now()}

    # Stop webdriver and return data
    browser.quit()
    return data



# -----------------------------------------------------------------------------------------------
# Scraping function
# -----------------------------------------------------------------------------------------------

def mars_news(browser):
    
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1) # Optional delay for loading the page

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')    # Contains all the HTML parsed with B.Soup

    # Add >>> TRY / EXCEPT <<< for error handling.
    try:
        slide_elem = news_soup.select_one('div.list_text')   # Creates a variable with ONE <div> </div>.
        #slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()      # Shows only the text.

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title , news_p


### D2-STEP 3) Create a function that will scrape the hemisphere data 
# Return the scraped data as a list of dictionaries with the URL string and title of each hemisphere image.

def hemisphere_data(browser):

    # Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []
    titles = []
    image_urls = []

    # Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    mars_soup = soup(html, 'html.parser')
    hemisphere_desc = mars_soup.select('div.description')

    # Create a list with each Hemisphere title.
    [titles.append(hem.find('h3').get_text()) for hem in hemisphere_desc if hem not in titles]

    # Click in each img and get the corresponding URL
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

    # Return the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls


# # HTML PARSER - IMAGES

def featured_image(browser):
    
    # Visit different URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]    # Find 'button' tags (there are 3 of them) --> we need the 2nd one.
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the >>> relative <<< image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')   # >>> .get() <<< retrieves the element.

    except AttributeError:
        return None

    # Use the base URL to create an >>> absolute <<< URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# # Scrape Tables with Pandas

def mars_facts():

    try:
        # Use .read_html() function to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0] # read_html only searches and return a list of tables.
    
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-hover")
    #return df.to_html(classes="table table-striped")


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


