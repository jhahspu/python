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

# init a slice.. oh this is python not go.
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

  # ok.. so for each job just get the job title, company and link and...
  for job in driver.find_elements_by_class_name('clickcard'):
    jobTitle = job.find_element_by_class_name('jobtitle').text
    jobLink = job.find_element_by_class_name('jobtitle').get_attribute('href')
    company = job.find_element_by_class_name('company ').text
    
    # ... dump into this slice
    jobs.append({'title': jobTitle, 'company': company, 'link': jobLink})

finally:
    driver.quit()

# propper naming convention in my organization
now = datetime.datetime.now()
fname = "jobs_" + now.strftime("%Y%m%d_%H%M%S") + ".json"

# reading material for later.. 
with open(fname, 'w') as f:
    json.dump(jobs, f, indent=2)
