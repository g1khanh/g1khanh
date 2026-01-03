from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

def get_categories(driver):
    categories = []
    current_page = 1

    while True:
        try:
            # Thu thập danh mục từ trang hiện tại
            elements = driver.find_elements(
                By.CSS_SELECTOR,
                "p.fw-semibold.text-capitalize a"  # Selector cho thẻ <a> bên trong <p>
            )
            print(f"🔍 Tìm thấy {len(elements)} danh mục trên trang {current_page}.")
            for el in elements:
                print(f"- HTML: {el.get_attribute('outerHTML')}")  # In ra HTML của thẻ <a>
                name = el.text.strip()
                url = el.get_attribute("href")

                if name and url:
                    categories.append({
                        "name": name,
                        "url": url
                    })

            # Tìm tất cả các liên kết phân trang
            pagination_links = driver.find_elements(
                By.CSS_SELECTOR,
                "div#paging a"  # Selector cho các liên kết phân trang
            )

            # Xác định tổng số trang từ liên kết cuối cùng
            total_pages = 1
            for link in pagination_links:
                try:
                    page_number = int(link.text.strip())
                    total_pages = max(total_pages, page_number)
                except ValueError:
                    pass

            print(f"🔍 Tổng số trang: {total_pages}")

            # Lấy liên kết của trang tiếp theo
            next_page = None
            for link in pagination_links:
                if link.text.strip().lower() == "next":
                    next_page = link
                    break

            if next_page and current_page < total_pages:
                try:
                    # Cuộn đến phần tử trước khi nhấn
                    driver.execute_script("arguments[0].scrollIntoView();", next_page)
                    next_page.click()
                except ElementClickInterceptedException:
                    print("⚠️ Phần tử bị che khuất, sử dụng JavaScript để nhấn.")
                    driver.execute_script("arguments[0].click();", next_page)

                current_page += 1
                print(f"➡️ Chuyển sang trang {current_page}...")
                time.sleep(2)  # Đợi trang tải
            else:
                print("❌ Đã đến trang cuối cùng. Dừng phân trang.")
                break

        except NoSuchElementException:
            print("❌ Lỗi khi tìm liên kết phân trang. Dừng phân trang.")
            break

    return categories


def get_company_links(driver):
    links = set()
    current_page = 1

    while True:
        try:
            # Thu thập liên kết công ty từ trang hiện tại
            items = driver.find_elements(
                By.CSS_SELECTOR,
                "h2.fs-5.pb-0.text-capitalize a"  # Selector cho thẻ <a> liên kết công ty
            )
            print(f"🔍 Tìm thấy {len(items)} liên kết công ty trên trang {current_page}.")
            for it in items:
                print(f"- HTML: {it.get_attribute('outerHTML')}")  # In ra HTML của thẻ <a>
                href = it.get_attribute("href")
                if href:
                    links.add(href)

            # Tìm tất cả các liên kết phân trang
            pagination_links = driver.find_elements(
                By.CSS_SELECTOR,
                "div#paging a"  # Selector cho các liên kết phân trang
            )

            # Xác định tổng số trang từ liên kết cuối cùng
            total_pages = 1
            for link in pagination_links:
                try:
                    page_number = int(link.text.strip())
                    total_pages = max(total_pages, page_number)
                except ValueError:
                    pass

            # Xác định số trang hiện tại
            try:
                current_page_element = driver.find_element(
                    By.CSS_SELECTOR,
                    "div#paging a.page_active"  # Selector cho trang hiện tại
                )
                current_page = int(current_page_element.text.strip())
            except NoSuchElementException:
                print("❌ Không thể xác định trang hiện tại.")
                break

            print(f"🔍 Trang hiện tại: {current_page}, Tổng số trang: {total_pages}")

            # Dừng nếu đã đến trang cuối cùng
            if current_page >= total_pages:
                print("❌ Đã đến trang cuối cùng. Dừng phân trang.")
                break

            # Lấy liên kết của trang tiếp theo
            next_page = None
            for link in pagination_links:
                if link.text.strip().lower() == "tiếp":
                    next_page = link
                    break

            if next_page:
                try:
                    # Cuộn đến phần tử trước khi nhấn
                    driver.execute_script("arguments[0].scrollIntoView();", next_page)
                    next_page.click()
                except ElementClickInterceptedException:
                    print("⚠️ Phần tử bị che khuất, sử dụng JavaScript để nhấn.")
                    driver.execute_script("arguments[0].click();", next_page)

                time.sleep(2)  # Đợi trang tải
            else:
                print("❌ Không tìm thấy trang tiếp theo. Dừng phân trang.")
                break

        except NoSuchElementException:
            print("❌ Lỗi khi tìm liên kết phân trang. Dừng phân trang.")
            break

    return list(links)
