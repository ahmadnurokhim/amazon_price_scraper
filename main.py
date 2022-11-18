from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


collected_data = []
grand_total = 0.0

wd = webdriver.Firefox()

# read the keywords
products = []
with open('keywords.txt', 'r') as f:
    for x in f.readlines():
        products.append(x.strip())

# scrap the product prices and names
for product in products:
    wd.get(f"https://www.amazon.com/s?k={product}")
    whole = wd.find_element(By.XPATH, "//div[@data-component-type='s-search-result' and not(contains(@class,'AdHolder')) and descendant::span[@class='a-price-whole']]//span[@class='a-price-whole']").text
    fraction = wd.find_element(By.XPATH, "//div[@data-component-type='s-search-result' and not(contains(@class,'AdHolder')) and descendant::span[@class='a-price-whole']]//span[@class='a-price-fraction']").text
    name = wd.find_element(By.XPATH, "//div[@data-component-type='s-search-result' and not(contains(@class,'AdHolder')) and descendant::span[@class='a-price-whole']]//span[@class='a-size-medium a-color-base a-text-normal']").text
    
    print(f"${whole}.{fraction}\t {name}")
    collected_data.append([float(f"{whole}.{fraction}".strip("$").replace(",", "")), name])
    grand_total += float(f"{whole}.{fraction}".strip("$").replace(",", ""))
wd.close()

# print out the grand total
print(f'Grand Total: ${grand_total}')

# export to csv
pd.DataFrame(collected_data, columns=['price', 'name']).to_csv('result.csv', sep='\t', index=False)
