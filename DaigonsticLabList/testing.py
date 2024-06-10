import pandas as pd

df = pd.read_csv('D:\Webscrapping_Selenium\webScraperVenv\DaigonsticLabList\List_of_Provinces_in_turkey.csv')

for index, row in df.iterrows():
    # Access the data in each row
    data = row[0]  # Assuming each row contains only one string
    
    # Process the data as needed
    print(f"'{row.iloc[0]}'")  # 

