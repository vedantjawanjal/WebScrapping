from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

website = 'https://en.wikipedia.org/wiki/List_of_cities_in_the_United_Arab_Emirates'
path = 'C:/Users/ACER/Downloads/chromedriver_win32/chromedriver.exe'

service = Service()
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)
driver.get(website)
time.sleep(1)
country = "UAE"
Province = driver.find_elements(By.XPATH, '//table[@class="wikitable sortable jquery-tablesorter"][1]/tbody/tr/td[2]') 
cities = driver.find_elements(By.XPATH, '//table[@class="wikitable sortable jquery-tablesorter"][2]/tbody/tr/td[1]')
list_of_cities = []
for city in Province+cities:
    city_name = city.text
    string_to_search = f"diagnostic centres, {city_name}, {country}"
    #print(string_to_search)
    list_of_cities.append(string_to_search)
unique_province =list(set(list_of_cities))
list_of_cities_in_turkey = {
    'Cities': unique_province, 
}
df = pd.DataFrame(list_of_cities_in_turkey)
print(df)
df['Cities'] = df['Cities'].str.lower()
df.to_csv("List_of_Cities_in_UAE.csv", index=False)

driver.quit()