from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

#get the data
driver = webdriver.Chrome()
driver.get("https://ie.indeed.com/")

jobs = []

try:
  locationInput = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "text-input-where"))
    )

  if locationInput:
    locationInput.send_keys("Cavan Town, County Cavan")
    locationInput.submit()

  for job in driver.find_elements_by_class_name('clickcard'):
    jobTitle = job.find_element_by_class_name('jobtitle').text
    company = job.find_element_by_class_name('company ').text

    jobs.append({'title': jobTitle, 'company': company})

finally:
    driver.quit()

print(jobs)