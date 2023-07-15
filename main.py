import selenium.common.exceptions
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from time import sleep
from random import randint


def remove_html_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()


def save_to_file(texts):
    with open("jobs.txt", "a", encoding="utf-8") as f:
        for text in texts:
            f.write(text + "\n")
    print("Job saved!")


browser = uc.Chrome()
browser.quit = False
browser.maximize_window()
link = "https://ph.indeed.com/jobs?q=part+time&l=Mandaue%2C+Cebu&vjk"
browser.get(link)
browser.execute_script("document.body.style.zoom='80%'")
sleep(2)


# This is used to navigate through website pages
page_num = 0

# Selects the Job by prescedence in the list
list_position = 1
scanned_last_page = False
while scanned_last_page is False:
    try:
        xpath_li_element = f'//*[@id="mosaic-provider-jobcards"]/ul/li[{list_position}]'
        li_element = browser.find_element(By.XPATH, xpath_li_element)
        list_position += 1  # Useful for next iteration, moves selector to next job in list
        try:
            li_element.click()
            sleep(randint(4, 10))
        except selenium.common.exceptions.ElementNotInteractableException \
                or selenium.common.exceptions.ElementClickInterceptedException:
            # We could try to fetch the link of the failed link
            print("Failed Links: {browser.current_url}")
            continue

        # Scrape the following data
        xpath_job_title = '//*[@id="jobsearch-ViewjobPaneWrapper"]/div/div/div/div[1]/div/div/div[1]/div[1]'
        job_title = browser.find_element(
            By.XPATH, xpath_job_title).get_attribute("outerHTML")
        job_title = remove_html_tags(job_title)

        xpath_job_company = '//*[@id="jobsearch-ViewjobPaneWrapper"]/div/div/div/div[1]/div/div/div[1]/div[2]/div/div/div/div[1]/div'
        job_company = browser.find_element(
            By.XPATH, xpath_job_company).get_attribute("outerHTML")
        job_company = remove_html_tags(job_company)

        xpath_job_location = '//*[@id="jobsearch-ViewjobPaneWrapper"]/div/div/div/div[1]/div/div/div[1]/div[2]/div/div/div/div[2]'
        job_location = browser.find_element(
            By.XPATH, xpath_job_location).get_attribute("outerHTML")
        job_location = remove_html_tags(job_location)

        try:
            xpath_job_salary = '//*[@id="salaryInfoAndJobType"]'
            job_salary = browser.find_element(
                By.XPATH, xpath_job_salary).get_attribute("outerHTML")
            job_salary = remove_html_tags(job_salary)
        except selenium.common.exceptions.NoSuchElementException:
            job_salary = ""

        xpath_job_description = '//*[@id="jobDescriptionText"]'
        job_description = browser.find_element(
            By.XPATH, xpath_job_description).get_attribute("outerHTML")
        job_description = remove_html_tags(job_description)

        """
        print(f"Job Company: {job_company}")
        print(f"Job Location: {job_location}")
        print(f"Job Salary: {job_salary}")
        print(f"Job Description: \n{job_description}")
        print(f"Link: {browser.current_url}")
        print("==^ End of Job ^== ")
        """
        texts = [
            f"Job Title: {job_title}"
            f"Job Company: {job_company}",
            f"Job Location: {job_location}",
            f"Job Salary: {job_salary}",
            f"Job Description: \n{job_description}",
            f"Link: {browser.current_url}",
            "===========^ End of Job ^===============",
        ]
        save_to_file(texts)

    except selenium.common.exceptions.NoSuchElementException:
        # Basically we're moving to the next page in the list
        print(f"!! Last Position of Job List: {list_position}")
        list_position = 1  # Reset the counter of job lists

        # Clicks the next page
        try:
            # If no button beside the current button, then throw an ERROR "NoSuchElementException"
            # This means we're now on the last page and no further read is needed
            next_page_button = "#jobsearch-JapanPage > div > div > div.jobsearch-SerpMainContent > div.jobsearch-LeftPane > nav > div:nth-child(6) > a"
            browser.find_element(By.CSS_SELECTOR, next_page_button)

            # Success, now move to the next page
            page_num += 10  
            browser.get(link + f"&start={page_num}")
            print("!! Next Page\n")
            sleep(randint(4, 7))

            # Remove Modal
            try:
                # Check if the modal exists
                modal_div = browser.find_element(
                    By.CSS_SELECTOR, "#mosaic-desktopserpjapopup")
                if modal_div:
                    # Click the close button to remove modal
                    css_selector_button = "div.css-otmc9o.eu4oa1w0 > button"
                    close_button = modal_div.find_element(
                        By.CSS_SELECTOR, css_selector_button)
                    close_button.click()  # Check if a button exists to the right side of the current button
            except selenium.common.exceptions.NoSuchElementException:
                pass
        except selenium.common.exceptions.NoSuchElementException:
            # We've now reached the end of page, there's no longer next button
            scanned_last_page = True
            print("No More Pages")
            sleep(1000)
