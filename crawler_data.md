# Báo cáo: Thu thập Dữ liệu Sản phẩm từ Amazon Bằng Selenium

## 1. Giới thiệu

Trong báo cáo này sẽ trình bày về quá trình thu thập dữ liệu sản phẩm từ trang Amazon bằng cách sử dụng Selenium, một công cụ phổ biến để tự động hóa trình duyệt web.

## 2. Công cụ và Môi trường

- **Ngôn ngữ Lập trình**: Python
- **Thư viện Sử dụng**:
  - `selenium`: Điều khiển trình duyệt và thu thập dữ liệu.
  - `webdriver_manager`: Tự động cài đặt và cập nhật ChromeDriver.
  - `pandas`: Xử lý và xuất dữ liệu ra file Excel.
- **Trình duyệt**: Google Chrome
- **Hệ Điều Hành**: Windows

## 3. Code

Dưới đây là phần code đầy đủ được sử dụng để thu thập dữ liệu từ trang Amazon.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Cài đặt tùy chọn cho Chrome
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  # Tắt GPU để tránh lỗi trong trình duyệt
chrome_options.add_argument("--no-sandbox")  # Chạy trình duyệt không cần sandbox
chrome_options.add_argument("--disable-dev-shm-usage")  # Sử dụng bộ nhớ ảo
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
)  # Giả lập user-agent của trình duyệt

# Khởi tạo WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL Amazon
url = "https://www.amazon.com/s?k=shoes&crid=MU245XPWQ6MS&sprefix=sh%2Caps%2C413&ref=nb_sb_noss_2"

# Tạo danh sách để lưu dữ liệu sản phẩm
data = []

try:
    driver.get(url)  # Mở trang web Amazon
    wait = WebDriverWait(driver, 10)  # Đợi tối đa 10 giây để tải trang
    print("Page title:", driver.title)  # In tiêu đề trang để kiểm tra trang có tải đúng không

    # Tìm tất cả các sản phẩm trên trang
    products = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 's-card-container')]")))  # Chờ đến khi các sản phẩm xuất hiện

    # Lặp qua từng sản phẩm để lấy thông tin
    for product in products:
        try:
            title = product.find_element(By.XPATH, ".//span[contains(@class, 'a-size-base-plus a-color-base a-text-normal')]").text  # Lấy tên sản phẩm
            print(f"Product Title: {title}")  # Kiểm tra xem tên sản phẩm có được lấy hay không

            try:
                price = product.find_element(By.CLASS_NAME, "a-price-whole").text  # Lấy giá sản phẩm
            except Exception as e:
                print(f"Price not found for {title}: {e}")  # Thông báo nếu không tìm thấy giá
                price = "N/A"  # Nếu không có giá, gán là N/A

            # Thêm tên và giá sản phẩm vào danh sách
            data.append({"Title": title, "Price": price})
        except Exception as e:
            print(f"Error extracting product info: {e}")  # In ra lỗi nếu gặp phải vấn đề trong quá trình lấy thông tin

finally:
    driver.quit()  # Đóng trình duyệt

# Kiểm tra xem có dữ liệu không
if not data:
    print("Không có dữ liệu nào được thu thập.")  # Thông báo nếu không có dữ liệu
else:
    # Đường dẫn lưu file Excel
    output_path = r"D:\Nhóm Data\Crawler Data\data\amazon_products.xlsx"
    df = pd.DataFrame(data)  # Tạo DataFrame từ dữ liệu thu thập được
    df.to_excel(output_path, index=False)  # Xuất dữ liệu ra file Excel
    print(f"Dữ liệu đã được lưu vào file {output_path}")  # Thông báo khi lưu thành công
```
