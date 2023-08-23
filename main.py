from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

load_dotenv()

PROMISED_DOWN = 10
PROMISED_UP = 100


class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.down = PROMISED_DOWN
        self.up = PROMISED_UP
        self.wait = WebDriverWait(self.driver, 60)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        self.driver.find_element(By.CLASS_NAME, "start-text").click()
        time.sleep(60)
        
        speed_results = self.driver.find_elements(
            By.CSS_SELECTOR, ".result-container-speed span.result-data-large.number.result-data-value"
        )

        for result in speed_results:
            self.down, self.up = (float(result.text) for result in speed_results)
        print(f"Down Speed: {self.down}, Up Speed: {self.up}")

    def tweet_at_provider(self):
        self.driver.get("https://twitter.com/")
        self.driver.find_element(By.XPATH,
                                 "/html/body/div/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a").click()
        email = self.wait.until(EC.visibility_of_element_located((By.NAME, "text")))
        email.send_keys(os.environ.get("TWITTER_EMAIL"), Keys.ENTER)
        # password = self.wait.until(EC.visibility_of_element_located((By.NAME, "password")))
        # password.send_keys(os.environ.get("TWITTER_PASSWORD"), Keys.ENTER)

        try:
            pass_input = self.driver.find_element(By.XPATH,
                                                  "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]"
                                                  "/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div"
                                                  "/div[2]/div[1]/input")
            pass_input.send_keys(os.environ.get("TWITTER_PASSWORD"))
            pass_input.send_keys(Keys.ENTER)
        except NoSuchElementException:
            username = self.driver.find_element(By.XPATH,
                                                "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/"
                                                "div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input")
            username.send_keys("example")  # Your Username here in case Twitter asks for username before asking password
            username.send_keys(Keys.ENTER)
            time.sleep(5)
            pass_input = self.driver.find_element(By.XPATH,
                                                  "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/"
                                                  "div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input")
            pass_input.send_keys(os.environ.get("TWITTER_PASSWORD"))
            pass_input.send_keys(Keys.ENTER)

        post = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/"
                                                                     "div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/"
                                                                     "div/div[2]/div[1]/div/div/div/div/div/div/div/div/"
                                                                     "div/div/label/div[1]/div/div/div/div/div/div[2]/"
                                                                     "div/div/div/div")))
        post.send_keys(f"Hey, internet provider, why is my internet speed {self.down}down/{self.up}up")

        time.sleep(5)


bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
bot.tweet_at_provider()
