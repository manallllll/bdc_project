from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json


class BdcScraper:
    def __init__(self, start_page=1, max_pages=5, output_file='bdc_data.json'):
        self.start_page = start_page
        self.max_pages = max_pages
        self.base_url = "https://www.marchespublics.gov.ma/bdc/entreprise/consultation/"
        self.details_base = "https://www.marchespublics.gov.ma"
        self.data = []
        self.output_file = output_file
        self.driver = self._init_driver()

    def _init_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=options)

    def charger_page(self, page_num):
        print(f"➡️ Chargement de la page {page_num}...")
        self.driver.get(f"{self.base_url}?page={page_num}")
        time.sleep(2)
        return self.driver.page_source

    def extraire_liste_bdc(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select("div.entreprise__card")
        urls = []
        for card in cards:
            relative_link = card.select_one("a.font-bold.table__links")
            if relative_link:
                full_url = self.details_base + relative_link.get('href')
                urls.append(full_url)
        return urls

    def extraire_detail_bdc(self, url):
        print(f"🔍 Extraction des détails pour : {url}")
        self.driver.get(url)
        time.sleep(1.5)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        def safe_select_text(selector):
            try:
                el = soup.select_one(selector)
                return el.get_text(strip=True) if el else None
            except:
                return None

        bdc = {
            "url": url,
            "reference": safe_select_text("div.main-content a.font-bold.table__links"),
            "objet": safe_select_text("div.main-content a.truncate_fullWidth.table__links"),
            "acheteur": safe_select_text("div.main-content a.table__links span.font-bold.text-small + span"),
            "lieu": safe_select_text("#location + .d-flex span.truncate-one-line"),
            "date_mise_en_ligne": safe_select_text("#dateMiseEnLigne + .d-flex span.truncate-one-line"),
            "date_limite": safe_select_text("#calendar + .d-flex span:last-child"),
            "fichiers_attaches": [
                self.details_base + a.get("href")
                for a in soup.select("a.nounderlinelink")
            ],
            "articles": []
        }

        for article_div in soup.select(".accordion-item"):
            title = article_div.select_one("h2 button")
            characteristics = article_div.select_one(".accordion-body span.text-black")
            unite = article_div.find("span", string=lambda t: t and "Unité de mesure" in t)
            quantite = article_div.find("span", string=lambda t: t and "Quantité" in t)
            tva = article_div.find("span", string=lambda t: t and "TVA" in t)
            garanties = article_div.find("span", string=lambda t: t and "Garanties exigées" in t)

            article_data = {
                "title": title.get_text(strip=True) if title else None,
                "characteristics": characteristics.get_text(strip=True) if characteristics else None,
                "unite": unite.find_next("div").text if unite else None,
                "quantite": quantite.find_next("div").text if quantite else None,
                "tva": tva.find_next("div").text if tva else None,
                "garanties": garanties.find_next("div").text if garanties else None,
            }
            bdc["articles"].append(article_data)

        return bdc

    def enregistrer_bdc(self, bdc):
        self.data.append(bdc)

    def sauvegarder_json(self):
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"✅ Données sauvegardées dans {self.output_file}")

    def run(self):
        for page in range(self.start_page, self.start_page + self.max_pages):
            html = self.charger_page(page)
            urls = self.extraire_liste_bdc(html)
            for url in urls:
                try:
                    bdc_data = self.extraire_detail_bdc(url)
                    self.enregistrer_bdc(bdc_data)
                except Exception as e:
                    print(f"⚠️ Erreur lors de l'extraction : {e}")
        self.sauvegarder_json()
        self.driver.quit()


if __name__ == "__main__":
    scraper = BdcScraper(start_page=1, max_pages=10)
    scraper.run()
