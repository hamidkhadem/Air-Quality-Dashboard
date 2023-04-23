# useful link for learing scraping by selenium:
# https://www.scrapingbee.com/blog/selenium-python/

# Import the required library
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# This function get the name of country and return body of numbeo
def get_numbeo_body(country_name):
    # link of webpage of desired country on numbeo.com
    url = "https://www.numbeo.com/cost-of-living/country_result.jsp?country=" + country_name
    # create options for using non GUI web driver
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    # download a desired url webpage
    driver.get(url)
    # find the body tage
    body = driver.find_element(By.TAG_NAME, "body")
    # return type is <class 'selenium.webdriver.remote.webelement.WebElement'>
    return body
    
#  This function get the body of numboe webpage and return living cost for family
def get_family_cost(body):
    # find element by xpath/ it's find the span for family cost
    family_cost = body.find_element(By.XPATH, "//span[@class='emp_number']")
    # get text of span
    text_price = family_cost.text
    return text_price

# Defined a function that get the price string and return value in Integer
# The format of string is string_price ="1,635.2$"
def get_int_price(string_price):
    pass

# Defined a function that get string list of countries name and return pandas data frame
def livingCost_df(list_countries_name):
    pass

# test the functions
if __name__=="__main__":
    # pass
    body = get_numbeo_body("Iraq")
    price = get_family_cost(body)
    print(price)
    print("------------------------------")
    print(type(body))
