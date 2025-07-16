from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from bs4 import BeautifulSoup
import time
import re


class BdcScraperMongo:
    def __init__(self, start_page=1, max_pages=5):
        self.start_page = start_page
        self.max_pages = max_pages
        self.base_url = "https://www.marchespublics.gov.ma/bdc/entreprise/consultation/"
        self.details_base = "https://www.marchespublics.gov.ma"
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
        db = client["bdc_db"]
        return db["bdc_results"]

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

        # ✅ Extraire référence à partir du <h4>#...</h4>
        ref_text = soup.find("h4")
        reference = None
        if ref_text:
            match = re.search(r"#?([\w/-]+)", ref_text.get_text(strip=True))
            if match:
                reference = match.group(1)

        # ✅ Objet
        objet = None
        objet_container = soup.find("span", string="Objet")
        if objet_container:
            span_obj = objet_container.find_next("span", class_="text-black")
            if span_obj:
                objet = span_obj.get_text(strip=True)

        # ✅ Acheteur
        acheteur = None
        acheteur_title = soup.find("span", string="Acheteur public")
        if acheteur_title:
            acheteur_span = acheteur_title.find_next_sibling("span")
            if acheteur_span:
                acheteur = acheteur_span.get_text(strip=True)

        bdc = {
            "url": url,
            "reference": reference,
            "objet": objet,
            "acheteur": acheteur,
            "lieu": safe_select_text("#location + div span.truncate-one-line"),
            "date_mise_en_ligne": safe_select_text("#dateMiseEnLigne + div span.truncate-one-line"),
            "date_limite": safe_select_text("#calendar + div span:last-child"),
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

    def inserer_si_nouveau(self, bdc):
        if bdc["reference"] and not self.collection.find_one({"reference": bdc["reference"]}):
            self.collection.insert_one(bdc)
            print(f"✅ Inséré : {bdc['reference']}")
        else:
            print(f"⏩ Déjà existant ou référence manquante : {bdc['reference']}")

    def run(self):
        for page in range(self.start_page, self.start_page + self.max_pages):
            html = self.charger_page(page)
            urls = self.extraire_liste_bdc(html)
            for url in urls:
                try:
                    bdc_data = self.extraire_detail_bdc(url)
                    self.inserer_si_nouveau(bdc_data)
                except Exception as e:
                    print(f"⚠️ Erreur lors de l'extraction : {e}")
        self.driver.quit()


if __name__ == "__main__":
    scraper = BdcScraperMongo(start_page=1, max_pages=2)
    scraper.run()
