from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json, time, os

# Configuration Chrome headless
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Supprime cette ligne si tu veux voir Chrome s'ouvrir

# Service ChromeDriver (adapté à Selenium 4+)
service = Service("C:\\chromedriver\\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Lien de la page des BDC
url = "https://www.marchespublics.gov.ma/bdc/entreprise/consultation/"
driver.get(url)
time.sleep(3)  # Attendre le chargement

bdcs = []
rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

# Extraction des lignes du tableau
for row in rows:
    try:
        ref = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()
        objet = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text.strip()
        acheteur = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text.strip()
        lieu = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text.strip()
        date = row.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.strip()
        zip_url = row.find_element(By.CSS_SELECTOR, "td:nth-child(6) a").get_attribute("href")

        bdcs.append({
            "reference": ref,
            "objet": objet,
            "acheteur": acheteur,
            "lieu": lieu,
            "date": date,
            "fichier_zip": zip_url
        })
    except:
        continue

driver.quit()

# Chemin de sortie
output_path = "data/bdc.json"

# Comparer avec les anciens BDC
if os.path.exists(output_path):
    with open(output_path, "r", encoding="utf-8") as f:
        old_bdcs = json.load(f)
    old_refs = {bdc['reference'] for bdc in old_bdcs}
    new_bdcs = [bdc for bdc in bdcs if bdc['reference'] not in old_refs]
    all_bdcs = old_bdcs + new_bdcs
else:
    all_bdcs = bdcs

# Enregistrement du fichier final
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_bdcs, f, indent=2, ensure_ascii=False)

print(f"✅ {len(bdcs)} BDC extraits.")
