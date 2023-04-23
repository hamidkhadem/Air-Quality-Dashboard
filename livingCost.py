# Import the required library
import requests
from bs4 import BeautifulSoup

# defined function to get name of country and return html of Numbo
def get_country_html(country_name):
    # link of webpage of desired country on numbeo.com
    url = "https://www.numbeo.com/cost-of-living/country_result.jsp?country=Iran"
    # "https://www.numbeo.com/cost-of-living/country_result.jsp?country=" + country_name
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    html = response.content
    # scraped html file
    scraped = BeautifulSoup(html, "html.parser")
    # return html of website
    return scraped.body

# This function get body of webpage and return family and single living cost
def get_estimated_cost(html):
    # soup.find("span", {"class": "real number", "data-value": True})['data-value']
    div = html.find("div", class_ = "innerWidth")
    
    # div = div.find("div")
    
    return div

# test the functions
if __name__=="__main__":
    html = get_country_html("Iran")
    x = get_estimated_cost(html)
    
    print(type(html))
    print(x)


