from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

website = 'https://www.google.com/maps/'
path = 'C:/Users/ACER/Downloads/chromedriver_win32/chromedriver.exe'
df = pd.read_csv('D:\Webscrapping_Selenium\webScraperVenv\DaigonsticLabList\List_of_Provinces_in_turkey.csv')
service = Service()
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()  # Maximize the browser window
driver.get(website)

# search_list = [
#     '"diagnostic centres, gaziantep, turkiye"', '"diagnostic centres, amasya, turkiye"'
# ]

search_list = pd.read_csv('D:\Webscrapping_Selenium\webScraperVenv\DaigonsticLabList\List_of_cities_in_turkey.csv')

data = {'Name': [], 'Contact Number': [], 'Website': []}

for index, search_query in search_list.iterrows():
    formatted_query = f'"{search_query.iloc[0]}"'
    print(f"Searching for {formatted_query}")
    time.sleep(2)
    input_box_search = driver.find_element(By.XPATH, '//input[@id="searchboxinput"]')
    input_box_search.clear()
    time.sleep(1)
    input_box_search.send_keys(formatted_query)
    input_box_search.send_keys(Keys.ENTER)
    time.sleep(10)  # Waiting for the page to load initially
    
    # Find the specified div containing the scrollable results
    try:
        div_side_bar = driver.find_element(By.XPATH, '//div[@class="m6QErb DxyBCb kA9KIf dS8AEf ecceSd"]')
        
        # Scroll down the div containing the results until reaching the end of the list
        keep_scrolling = True
        while keep_scrolling:
            div_side_bar.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
            div_side_bar.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
            html = driver.find_element(By.TAG_NAME, "html").get_attribute('outerHTML')
            if html.find("You've reached the end of the list.") != -1:
                keep_scrolling = False

        # Extract data from each result container
        result_containers = driver.find_elements(By.XPATH, '//div[@class="Nv2PK tH5CWc THOPZb "]')
        for container in result_containers:
            time.sleep(2)
            try:
                name = container.find_element(By.XPATH, './/div[@class="lI9IFe "]//div[@class="NrDZNb"]').text
            except NoSuchElementException:
                name = 'NaN'
            try:
                contact = container.find_element(By.XPATH, './/div[@class="lI9IFe "]//div[@class="W4Efsd"]/span/span[@class="UsdlK"]').text
            except NoSuchElementException:
                contact = 'NaN'
            try:
                website = container.find_element(By.XPATH, './/div[@class="lI9IFe "]//div[@class="Rwjeuc"]/div[@class="etWJQ jym1ob kdfrQc bWQG4d "]/a').get_attribute('href')
            except NoSuchElementException:
                website = 'NaN'
            data['Name'].append(name)
            data['Contact Number'].append(contact)
            data['Website'].append(website)

            #print("Google Map Link:", google_map_link)
            print("Name:", name)
            print("Contact Number:", contact)
            print("Website:", website)
    except NoSuchElementException:
        print(f"No search results found for {formatted_query}")
        # Append NaN values for all fields if no search results found
        data['Name'].append('NaN')
        data['Contact Number'].append('NaN')
        data['Website'].append('NaN')

# Create a DataFrame from the scraped data
scraped_df = pd.DataFrame(data)

# Write the scraped data to an Excel file
scraped_df.to_excel('C:/Users/ACER/Documents/DaignosticDataCity1.xlsx', index=False)

time.sleep(4)
driver.quit()