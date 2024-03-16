from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

website = 'https://www.adamchoi.co.uk/overs/detailed'
path = 'C:/Users/ACER/Downloads/chromedriver_win32/chromedriver.exe'

service = Service()
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)
driver.get(website)

all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches_button.click()
Country_list  = driver.find_element(By.XPATH, '//select[@id="country"]')
list = Country_list.find_elements(By.TAG_NAME, 'option')
contry_dropdown_list = []
for i in list:
    contry_dropdown_list.append(i.text)

dropdown = Select(driver.find_element(By.ID, 'country'))
for country in contry_dropdown_list:
    print(country)
    dropdown.select_by_visible_text(country)
    time.sleep(3)

    matches = driver.find_elements(By.TAG_NAME, 'tr')
    date = []
    home_team = []
    score = []
    away_team = []

    for match in matches:
        date.append(match.find_element(By.XPATH, './td[1]').text)
        print(match.find_element(By.XPATH, './td[1]').text)
        home_team.append(match.find_element(By.XPATH, './td[2]').text)
        score.append(match.find_element(By.XPATH, './td[3]').text)   
        away_team.append(match.find_element(By.XPATH, './td[4]').text)


    data = pd.DataFrame({
            'date': date,
            'home_team': home_team,
            'score': score,
            'away_team': away_team,
        })
    data.to_csv(f'{country}_football_data.csv', index=False)

    print(data)
#driver.quit()