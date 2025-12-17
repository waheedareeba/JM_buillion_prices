# app.py — fixed version for selenium/standalone-chrome
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
import selenium_stealth
import random
from io import BytesIO
import time

def fetch_gold_prices():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    # THIS IS THE KEY PART
    selenium_stealth.stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win64",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        run_on_insecure_origins=True,
    )

    # Random delay to look human
    time.sleep(random.uniform(3, 7))
    # Stealth: hide webdriver flag
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false
            });
            window.navigator.chrome = {
                runtime: {},
                loadTimes: () => {},
                csi: () => {}
            };
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 5]
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        """
    })

    urls = [
        "https://www.jmbullion.com/1-gram-varied-gold-bar/",
        "https://www.jmbullion.com/1-oz-argor-heraeus-gold-bar/",
        "https://www.jmbullion.com/1-10-oz-american-gold-eagle/",
        "https://www.jmbullion.com/1-4-oz-american-gold-eagle/",
        "https://www.jmbullion.com/1-2-oz-american-gold-eagle/",
        "https://www.jmbullion.com/1-oz-american-gold-eagle/",
        "https://www.jmbullion.com/1-oz-gold-maple-leaf-vy-abr/",
        "https://www.jmbullion.com/1-oz-american-gold-buffalo-vy/",
        "https://www.jmbullion.com/1-oz-silver-bar/",
        "https://www.jmbullion.com/5-oz-silver-bar/",
        "https://www.jmbullion.com/10-oz-silver-bar/",
        "https://www.jmbullion.com/100-oz-silver-bar/",
        "https://www.jmbullion.com/1-oz-silver-round/",
        "https://www.jmbullion.com/american-silver-eagle-cull/",
        "https://www.jmbullion.com/1-oz-american-silver-eagle-tube-mintsealed-random-year/"
    ]

    results = []
    wait = WebDriverWait(driver, 10)

    for url in urls:
        try:
            driver.get(url)
            time.sleep(2)

            # Primary price selector (current as of Dec 2025)
            try:
                price = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.p-1.border-r span"))).text.strip()
            except:
                try:
                    price = driver.find_element(By.CSS_SELECTOR, "span.price", "div.price-block span.price").text.strip()
                except:
                    price = "Price not found"

            results.append({
                "Price": price,
                "URL": url,
                "Fetched At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        except Exception as e:
            results.append({
                "Price": f"Failed: {str(e)[:50]}",
                "URL": url,
                "Fetched At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    driver.quit()
    return pd.DataFrame(results)

# --- Streamlit UI (unchanged) ---
st.set_page_config(page_title="JM Bullion Prices", layout="wide")
st.title("Precious Metals Price Fetcher (JM Bullion)")
st.markdown("Click below to fetch live prices")

if st.button("Fetch Latest Prices", type="primary"):
    with st.spinner("Launching browser..."):
        df = fetch_gold_prices()
        st.success("Done!")
        st.dataframe(df, use_container_width=True)
        
        # Excel download
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        st.download_button(
            "Download Excel",
            buffer,
            f"jmbullion_prices_{datetime.now():%Y%m%d_%H%M}.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )