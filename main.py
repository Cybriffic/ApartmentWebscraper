# Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time

# Get the html of the apartment website URL (Willow) and convert it to text
willow_url = "https://appbrewery.github.io/Zillow-Clone/"
response = requests.get(willow_url)
website_html = response.text

# Get the price, address and link of all the apartments
soup = BeautifulSoup(website_html, "html.parser")
prices = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
addresses = soup.find_all(name="address")
links = soup.find_all(name="a", class_="property-card-link")


#Append all the prices into a list.
#We first get the text of the item, then remove all the unnecessary info like /mo, + 1bd, etc...
price_list = [(((((item.getText()).replace('+/mo', '')).replace('/mo',''))).replace('+ 1 bd', '')).replace('+ 1bd', '') for item in prices]

#Append all the addressess into a list.
#We first get the text of the item, then replace '|' with ','
address_list = [((item.getText()).replace('|', ',')).strip() for item in addresses]


#Append all the links into a list.
link_list = [item.get("href") for item in links]


# Prevent chrome from closing
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Opens Google Forum
forum_url = "https://docs.google.com/forms/d/e/1FAIpQLSdnk3xdyRsp9FnbChDLX2zgUkBldywEJ5-zZRVL6FYI_1FPVQ/viewform?usp=sf_link"
driver = webdriver.Chrome(options=chrome_options)
driver.get(forum_url)


# For every item in the range of 0 and no.of apartments...
for item in range(0, len(prices)):

    #We get the current price, address and link
    current_price = price_list[item]
    current_address = address_list[item]
    current_link = link_list[item]

    # We get the textboxes (for typing in the address, price and link) as well as the button to submit our inputs.
    forum_address = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    forum_price = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    forum_link = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_forum = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    #We send in the current address, current price and current link.
    forum_address.send_keys(current_address)
    forum_price.send_keys(current_price)
    forum_link.send_keys(current_link)

    #We submit the forum.
    submit_forum.click()

    #Waits 3 seconds, and clicks on 'submit another response' to submit another response.
    time.sleep(3)
    submit_again = driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_again.click()

    #Wait 1 second, just to ensure the program wouldn't crash.
    time.sleep(1)
