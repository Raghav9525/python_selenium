from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def scrape_data():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = "https://www.7nishchay-yuvaupmission.bihar.gov.in/listofcollegedetail"
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        link = wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody/tr[1]/td[1]/a[1]")))

        link.click()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        html_dom = driver.page_source
        return {"html": html_dom}

    finally:
        driver.quit()

@app.route("/scrape", methods=["GET"])
def scrape():
    data = scrape_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
