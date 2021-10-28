from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    #setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

mars_info ={} 
    
def scrape_mars_news():
    browser = init_browser()
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    
 
    
    #parse HTML into beautiful soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text.strip()
    news_p = soup.find('div', class_='article_teaser_body').text.strip()
    mars_info["news_title"]=news_title
    mars_info["news_p"]=news_p
    
    # Close the browser after scraping
    browser.quit()
    
    return mars_info

def scrape_mars_image():
    browser = init_browser()
    #visit the url for the Featured Space Image Site 
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)
        
    #parse HTML into beautiful soup
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')
    image = soup2.find('img',class_='thumbimg')['src']
    featured_image_url = url2+image
    mars_info["featured_image_url"]=featured_image_url
    
    # Close the browser after scraping
    browser.quit()
    return mars_info


def scrape_mars_facts():
    browser = init_browser()
    
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    

    df = tables[0]
    header_row=0
    df.columns=df.iloc[header_row]
    df=df.drop(header_row)
    df2=df.reset_index(drop=True)
    html_table=df2.to_html()
    mars_info["mars_facts"]=html_table
    # Close the browser after scraping
    browser.quit()
    
    return mars_info


def scrape_mars_hemisphere():
    browser = init_browser()
    #visit the astrogeology site to obtain high res images for each of Mar's hemisphere
    hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(hemisphere_url)
    

    #parse HTML into beautiful soup
    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')
    item_list = soup3.find_all('div', class_='item')
    
    
    img_url= []
    title_name=[]

    for i in item_list:
        new_url = i.a['href']
        full_url = hemisphere_url+new_url
        browser.visit(full_url)
        html_new=browser.html
        imagesoup = BeautifulSoup(html_new, 'html.parser')
        full_size = imagesoup.find('li').a['href']
        full_size_url =hemisphere_url+full_size
        print(full_size_url)
        img_url.append(full_size_url)
        title = imagesoup.find('h2', class_='title').text
        print(title)
        title_name.append(title)
        
        new_list = list(zip(title_name, img_url))
        
        hemisphere_image_urls=[]
        for a in new_list:
            hemisphere_image_urls.append({'title':a[0], 'img_url':a[1]})
    mars_info["img_url"]=  img_url
    mars_info["title_name"]=  title_name
    mars_info["IMG"]= hemisphere_image_urls
    
    # Close the browser after scraping
    browser.quit()
    
    return mars_info     

       


