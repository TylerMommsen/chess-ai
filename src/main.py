from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get('https://chess.com')

title = driver.title

driver.implicitly_wait(0.5)

input("Press Enter to close the browser...")

coordinates = driver.find_element(By.XPATH, "//*[@id='board-play-computer']//*[name()='svg']")
square_names = coordinates.find_elements(By.XPATH, ".//*")

print(square_names)

driver.quit()
