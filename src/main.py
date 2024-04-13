from selenium import webdriver
from selenium.webdriver.common.by import By

import gui

def open_browser():
  driver = webdriver.Chrome()

  driver.get('https://chess.com')

  driver.implicitly_wait(0.5)

  input("Press Enter to close the browser...")

  driver.quit()


def start_autoplay():
  pass