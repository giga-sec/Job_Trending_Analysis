from selenium import webdriver
from selenium.webdriver.common.by import By
import time

browser = webdriver.Chrome()
browser.get('https://ph.indeed.com/jobs?q=part+time&l=Mandaue%2C+Cebu&vjk=ffb76a95e69ff49d')

time.sleep(5)

# Find the <ul> element with selector "#mosaic-provider-jobcards > ul"
ul_element = browser.find_element(By.CSS_SELECTOR, "#mosaic-provider-jobcards > ul")

# Find the first <li> tag inside the <ul> element with selector "li:nth-child(1)"
li_element = ul_element.find_element(By.CSS_SELECTOR, "li:nth-child(1)")

print(li_element.text)

browser.quit = False
