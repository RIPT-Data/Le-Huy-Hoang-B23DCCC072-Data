from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = "https://www.amazon.com/s?k=shoes&crid=MU245XPWQ6MS&sprefix=sh%2Caps%2C413&ref=nb_sb_noss_2"

data = []

try:
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    print("Page title:", driver.title)
    products = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 's-card-container')]")))

    # Lặp qua từng sản phẩm để lấy thông tin
    for product in products:
        try:
            title = product.find_element(By.XPATH, ".//span[contains(@class, 'a-size-base-plus a-color-base a-text-normal')]").text
            print(f"Product Title: {title}")  # Kiểm tra xem tên sản phẩm có được lấy hay không
            try:
                price = product.find_element(By.CLASS_NAME, "a-price-whole").text
            except Exception as e:
                print(f"Price not found for {title}: {e}")
                price = "N/A"  # Nếu không có giá

            data.append({"Title": title, "Price": price})
        except Exception as e:
            print(f"Error extracting product info: {e}")

finally:
    driver.quit()

if not data:
    print("Không có dữ liệu nào được thu thập.")
else:
    output_path = r"D:\Nhóm Data\Crawler Data\data\amazon_products.xlsx"
    df = pd.DataFrame(data)
    df.to_excel(output_path, index=False)
    print(f"Dữ liệu đã được lưu vào file {output_path}")
