import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from datetime import datetime
from io import BytesIO

# ---------------- SCRAPER FUNCTION ---------------- #

def fetch_gold_prices():
    
    driver = webdriver.Chrome()


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

    for url in urls:
        driver.get(url)
        time.sleep(2)

        try:
            price_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.p-1.border-r span"))
            )
            price = price_div.text
        except:
            price = "Price not found"

        results.append({
            "URL": url,
            "Price": price,
            "Fetched At": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

    driver.quit()

    return pd.DataFrame(results)



# ---------------- FRONTEND (STREAMLIT) ---------------- #

st.set_page_config(page_title="Gold Price Fetcher", layout="centered")

st.title("💰 Gold Price Fetcher")
st.write("Click the button below to fetch latest gold prices from JM Bullion.")

if st.button("Fetch Latest Prices"):
    with st.spinner("Fetching prices... please wait 10–20 seconds"):
        df = fetch_gold_prices()

    st.success("Prices fetched successfully!")
    st.dataframe(df)

    # Convert to Excel
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)

    st.download_button(
        label="⬇️ Download Excel File",
        data=buffer,
        file_name=f"gold_prices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
