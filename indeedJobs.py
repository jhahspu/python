from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import datetime
import json

#start driver
driver = webdriver.Chrome()

#go to address
driver.get("https://ie.indeed.com/")

# init obj
jobs = []

try:
  # wait for load and check if element is on page
  locationInput = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "text-input-where"))
    )

  # send some keys to element if on page
  if locationInput:
    locationInput.send_keys("Cavan Town, County Cavan")
    locationInput.submit()

  # suppose previous step worked and now we have a bunhc of jobs
  # let's get the data.. I'm interested in job title, company, and link
  for job in driver.find_elements_by_class_name('clickcard'):
    jobTitle = job.find_element_by_class_name('jobtitle').text
    jobLink = job.find_element_by_class_name('jobtitle').get_attribute('href')
    company = job.find_element_by_class_name('company ').text
    
    # since I'm gonna look at this data later let's just gather it
    jobs.append({'title': jobTitle, 'company': company, 'link': jobLink})

finally:
    driver.quit()

# propper naming convention in my org
now = datetime.datetime.now()
fname = "jobs_" + now.strftime("%Y%m%d_%H%M%S") + ".json"

# asuming everything went well, I'll have some data in a json, and I'll have reading material for later :)
with open(fname, 'w') as f:
    json.dump(jobs, f, indent=2)