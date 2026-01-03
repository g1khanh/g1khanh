from bs4 import BeautifulSoup

def parse_company(html, stt):
    soup = BeautifulSoup(html, "html.parser")

    # Lấy tên công ty
    company_tag = soup.select_one("h1.fs-3.text-capitalize")
    company_name = company_tag.get_text(strip=True) if company_tag else "Không rõ"

    # Địa chỉ: tìm thẻ có icon fa-location-arrow rồi lấy text cha
    address_tag = soup.select_one("i.fa-location-arrow")
    address = address_tag.parent.get_text(strip=True) if address_tag else "Không rõ"

    # Số điện thoại: tìm thẻ có icon fa-phone rồi lấy text cha
    phone_tag = soup.select_one("a[href^='tel:']")
    phone = phone_tag["href"].replace("tel:", "").strip() if phone_tag else "Không rõ"
    # hotline
    hotline_tag = soup.select_one("p:has(i.fa-mobile-screen-button) a[href^='tel:']")
    hotline_number = hotline_tag.get_text(strip=True) if hotline_tag else "Không có"

    # Email: lấy từ href mailto
    email_tag = soup.select_one("a[href^='mailto:']")
    email = email_tag["href"].replace("mailto:", "").strip() if email_tag else "Không rõ"

    # Website: tìm thẻ có icon fa-globe rồi lấy href
    website_tag = soup.select_one("p:has(i.fa-globe) a")
    company_link = website_tag["href"].strip() if website_tag and website_tag.has_attr("href") else "Không rõ"

    return {
        "STT": stt,
        "Tên công ty": company_name,
        "Địa chỉ": address,
        "SDT": phone,
        "Hotline": hotline_number,
        "Email": email,
        "Link công ty": company_link,
    }