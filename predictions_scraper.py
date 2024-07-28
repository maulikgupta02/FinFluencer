from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
import time
import pandas


chrome_options = Options()
chrome_options.add_argument('--incognito')

driver=webdriver.Chrome(options=chrome_options)
driver.get("https://economictimes.indiatimes.com/markets/stocks/recos")


for i in range(100):

    try:
        
        time.sleep(5)

        # Wait for the element to be clickable
        autoload_continue = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "autoload_continue"))
        )

        # Move to the element before clicking
        ActionChains(driver).move_to_element(autoload_continue).click().perform()
        time.sleep(3)

        # Handle alerts if present
        try:
            alert = driver.switch_to.alert
            alert.accept()  # You can also use alert.dismiss() to dismiss the alert
        except:
            pass  # No alert present

    except Exception as e:
        print(e)
        break


preds={'prediction':[],'source':[],'stock_info':[],'datetime':[]}

# Find all elements with class name "eachStory"
recoms = driver.find_elements(By.CLASS_NAME, "eachStory")

# Iterate through each "eachStory" element
for recom in recoms:
    # Find elements within each "eachStory" element
    prediction = (recom.find_element(By.TAG_NAME, "a")).text
    stock_info = (recom.find_element(By.TAG_NAME, "p")).text
    time_element = recom.find_element(By.TAG_NAME, "time")
    
    # Get the datetime attribute value
    datetime = time_element.get_attribute("data-time")
    
    # Print the information for each "eachStory"
    if len(prediction.split(":"))!=2:
        continue
    # print(prediction)
    prediction,source=prediction.split(":")

    preds["datetime"].append(datetime)
    preds["prediction"].append(prediction)
    preds["source"].append(source)
    preds["stock_info"].append(stock_info)


df=pandas.DataFrame(preds)
print(df.head())
df.to_csv("predictions.csv")
# Close the WebDriver
driver.quit()