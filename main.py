from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time


def create_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0")

    service = Service("chromedriver-win64/chromedriver.exe")
    return webdriver.Chrome(service=service, options=options)


def scrape_ml_repos():
    browser = create_webdriver()

    try:
        print("Opening GitHub search page...")
        browser.get("https://github.com/collections/machine-learning")

        # hard wait because GitHub hates Selenium
        time.sleep(8)

        print("Collecting all links...")
        links = browser.find_elements(By.TAG_NAME, "a")

        repo_data = []
        seen = set()

        for link in links:
            href = link.get_attribute("href")

            if not href:
                continue

            # match https://github.com/owner/repo
            if href.startswith("https://github.com/") and href.count("/") == 4:
                if href not in seen:
                    seen.add(href)
                    repo_name = href.replace("https://github.com/", "")

                    repo_data.append({
                        "name": repo_name,
                        "link": href
                    })

                    print(f"✔ {repo_name}")

        df = pd.DataFrame(repo_data)
        print(f"\nScraped {len(df)} repositories")
        return df

    finally:
        browser.quit()


if __name__ == "__main__":
    print("=" * 60)
    print("GitHub Machine Learning Repo Scraper")
    print("=" * 60)

    df = scrape_ml_repos()

    if df is not None and not df.empty:
        df.to_csv("ml_repos.csv", index=False)
        print("\n🔥 Saved to ml_repos.csv")
    else:
        print("\n❌ No repos found")

