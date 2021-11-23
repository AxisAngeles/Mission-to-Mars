#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# Import PANDAS to scrape tables
import pandas as pd

# Import Datetime
import datetime as dt

def scrape_all():

    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Set the two returning variables from mars_news.
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
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
    return df.to_html(classes="table table-striped")


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


