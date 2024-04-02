from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

def getWebsiteDriver():
    path = 'C:/Users/ACER/Downloads/chromedriver_win32/chromedriver.exe'
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=service, options=options)
    return driver


if __name__=="__main__":
    website = 'https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1'
    try: 
        #driver = getWebsiteDriver(website)
        list_of_laptops = []
        laptops_data = []
        driver = getWebsiteDriver()
        for page in range(1, 10):
            website = f'https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={page}'
            driver.get(website)
            Laptops = driver.find_elements(By.XPATH, '//div[@class="_2kHMtA"]//a')
            for laptop in Laptops:
                list_of_laptops.append(laptop.get_attribute('href'))
            time.sleep(5)

        for link in list_of_laptops:
            driver.get(link)
            time.sleep(3)
            try:
                read_more = driver.find_element(By.XPATH, '//div//button[@class="_2KpZ6l _1FH0tX"]')
                read_more.click()
            except:
                pass
            laptop_name = driver.find_element(By.XPATH, '//h1//span').text
            current_price = driver.find_element(By.XPATH, '//div[@class="_25b18c"]//div[@class="_30jeq3 _16Jk6d"]').text
            try:
                MRP_price = driver.find_element(By.XPATH, '//div[@class="_25b18c"]//div[@class="_3I9_wc _2p6lqe"]').text
            except:
                MRP_price = "N/A"

            try:
                rating = driver.find_element(By.XPATH, '//div[@class="gUuXy- _16VRIQ"]//span//div[@class="_3LWZlK"]').text
            except:
                rating = "NA"

            data = {
                'Laptop Name': laptop_name,
                'Current Price': current_price,
                'MRP Price': MRP_price,
                'Rating': rating
            }

            specifications = driver.find_elements(By.XPATH, '//div[@class="_3k-BhJ"][2]//tr')
            for spec in specifications:
                key = spec.find_element(By.XPATH, './/td[1]').text
                value = spec.find_element(By.XPATH, './/td[2]').text
                data[key] = value

            laptops_data.append(data)

        df = pd.DataFrame(laptops_data)  # Convert list of dictionaries to DataFrame
        
        # Save DataFrame to CSV file
        df.to_csv('laptops_data.csv', index=False)
        
        print("Data saved to laptops_data.csv")

        driver.quit()
    except Exception as e:
        print("Driver Connection Failed " + str(e))
    
    