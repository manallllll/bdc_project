from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from bs4 import BeautifulSoup
import time


class AoScraperTanmia:
    def __init__(self, max_pages=5):
        self.max_pages = max_pages
        self.base_url = "https://tanmia.ma/appels-doffres"
        self.driver = self._init_driver()
        self.collection = self._init_mongo()

    def _init_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=options)

    def _init_mongo(self):
        client = MongoClient("mongodb://localhost:27017/")
        db = client["ao_db"]
        return db["ao_results"]

    def charger_page(self, page_num):
        url = f"{self.base_url}/{page_num}/"
        print(f"➡️ Chargement : {url}")
        self.driver.get(url)
        time.sleep(2)
        return self.driver.page_source

    def extraire_liens_details(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        boutons = soup.select("a.elementor-post__read-more")
        urls = [btn.get("href") for btn in boutons if btn.get("href")]
        print(f"🔗 {len(urls)} liens extraits")
        return urls

    def extraire_details_ao(self, url):
        print(f"🔍 Détail : {url}")
        self.driver.get(url)
        time.sleep(1.5)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        titre = soup.find("h1")
        date = soup.select_one(".elementor-post-info__item--type-date time")
        description = soup.select_one(".elementor-widget-theme-post-content")
        fichier_link = soup.select_one("ul.post-attachments a")

        return {
            "url": url,
            "titre": titre.get_text(strip=True) if titre else None,
            "date_publication": date.get_text(strip=True) if date else None,
            "description": description.get_text(strip=True) if description else None,
            "fichier": fichier_link.get("href") if fichier_link else None,
        }

    def inserer_si_nouveau(self, ao):
        if ao["titre"] and not self.collection.find_one({"titre": ao["titre"]}):
            self.collection.insert_one(ao)
            print(f"✅ Ajouté : {ao['titre']}")
        else:
            print(f"⏭️ Déjà existant ou titre manquant.")

    def run(self):
        for page in range(1, self.max_pages + 1):
            try:
                html = self.charger_page(page)
                urls = self.extraire_liens_details(html)
                for url in urls:
                    try:
                        ao = self.extraire_details_ao(url)
                        self.inserer_si_nouveau(ao)
                    except Exception as e:
                        print(f"⚠️ Erreur détail : {e}")
            except Exception as e:
                print(f"⚠️ Erreur page : {e}")
        self.driver.quit()


if __name__ == "__main__":
    scraper = AoScraperTanmia(max_pages=5)
    scraper.run()
