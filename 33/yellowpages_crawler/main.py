from browser import create_driver
from crawler import get_categories, get_company_links
from parser import parse_company
from config import BASE_URL, HEADLESS, DETAIL_DELAY
import pandas as pd
import time
import os

def main():
    if not os.path.exists("data"):
        os.makedirs("data")

    driver = create_driver(headless=HEADLESS)
    driver.get(BASE_URL)
    time.sleep(3)

    categories = get_categories(driver)
    if not categories:
        print("❌ Không tìm thấy danh mục nào.")
        driver.quit()
        return

    print(f"🔹 Tổng danh mục: {len(categories)}")

    # Duyệt qua tất cả danh mục, không cần chọn
    for cat in categories:
        print(f"\n📂 Danh mục: {cat['name']}")
        if not cat.get("url"):
            print(f"❌ Danh mục '{cat['name']}' không có URL hợp lệ.")
            continue

        driver.get(cat["url"])
        time.sleep(2)

        links = get_company_links(driver)
        if not links:
            print(f"❌ Không tìm thấy công ty nào trong danh mục {cat['name']}.")
            continue

        print(f"   → {len(links)} công ty")

        results = []
        for idx, link in enumerate(links, start=1):
            driver.get(link)
            time.sleep(DETAIL_DELAY)
            html = driver.page_source
            data = parse_company(html, stt=idx)
            if not data:
                print(f"❌ Không thể phân tích dữ liệu từ URL: {link}")
                continue
            data["STT"] = idx
            results.append(data)

        # Xuất file Excel riêng cho từng danh mục
        if results:
            df = pd.DataFrame(results)
            safe_name = cat['name'].replace(" ", "_").replace("/", "_").replace("\\", "_")
            output_file = f"data/{safe_name}.xlsx"
            df.to_excel(output_file, index=False)
            print(f"✅ Đã xuất file: {output_file}")
        else:
            print(f"❌ Không có dữ liệu nào trong danh mục {cat['name']}")

    driver.quit()
    # if results:
    #     df = pd.DataFrame(results)
    #     df.to_excel("data/yellowpages_companies.xlsx", index=False)
    #     print("\n✅ Hoàn tất! File: data/yellowpages_companies.xlsx")
    # else:
    #     print("❌ Không có dữ liệu nào được thu thập.")

    # Xuất dữ liệu ra file Excel
    all_data = []
    for index, html in enumerate(company_links, start=1):
        data = parse_company(html, stt=index)  # Truyền số thứ tự vào hàm parse_company
        all_data.append(data)

    # Xuất dữ liệu ra file Excel
    df = pd.DataFrame(all_data)
    output_file = "company_data.xlsx"
    df.to_excel(output_file, index=False)
    print(f"✅ Dữ liệu đã được xuất ra file: {output_file}")

if __name__ == "__main__":
    main()
