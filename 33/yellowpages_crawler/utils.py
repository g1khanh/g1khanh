import time

def infinite_scroll(driver, delay=2):
    last_height = driver.execute_script(
        "return document.documentElement.scrollHeight"
    )

    while True:
        driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);"
        )
        time.sleep(delay)

        new_height = driver.execute_script(
            "return document.documentElement.scrollHeight"
        )

        if new_height == last_height:
            break
        last_height = new_height
