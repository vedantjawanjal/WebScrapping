from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

website = 'https://airomedical.com/hospitals'
path = 'C:/Users/ACER/Downloads/chromedriver_win32/chromedriver.exe'

service = Service()
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

try:
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(website)

    # Wait for the container to be present before scrolling
    wait = WebDriverWait(driver, 20)
    container = wait.until(EC.presence_of_element_located((By.ID, 'hospitals')))

    time.sleep(3)
    # Scroll down to load all data dynamically
    SCROLL_PAUSE_TIME = 5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


    data = []
    hospital_links = []
    hospitals = container.find_elements(By.XPATH, './/div[@class="HospitalPaginationCard_container__HxuNc"]')
    for hospital in hospitals:  
        link = hospital.find_element(By.XPATH, './/div[@class="HospitalCard_title__Tw4ZU"]/a').get_attribute("href")
        hospital_links.append(link)

    for link in hospital_links:
        driver.get(link)
        hospital_name = driver.find_element(By.XPATH, '//h1[@class="MainInfo_titleName__rhrVM"]').text
        about_hospital = driver.find_element(By.CLASS_NAME, "AboutBlock_message__oiMr8").text
        #Departments = driver.find_element(By.XPATH, '//div[@class="DepartmentsSection_departments__slnN8"]')
        
        print("Hospital Name:", hospital_name)
        print("about_hospital", about_hospital)
        data.append({"Hospital Name": hospital_name, "About Hospital": about_hospital})

    df = pd.DataFrame(data)
    df.to_csv("hospital_data.csv", index=False)

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally: 
    # Close the WebDriver
    driver.quit()