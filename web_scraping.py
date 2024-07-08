import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_districts():
    """
    Funkce na získání všech okresů ze stránky.
    :return: seznam okresů
    """
    url = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Chyba při přístupu na stránku")
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    districts = []
    
    rows = soup.find_all("tr")
    
    for row in rows:
        cells = row.find_all("td")
        
        if len(cells) >= 4:
            district_name = cells[1].get_text(strip=True)
            district_code = cells[3].find("a")["href"]
            districts.append({"name": district_name, "code": district_code})
    
    
    return districts

def print_districts(districts):
    """
    Vypíše aktuální seznam okresů.
    :param districts: seznam okresů
    """
    for district in districts:
        print(f"{district["name"]}")

def set_url_for_district(districts, district_name):
    """
    Funkce pro nastavení URL pro zadaný okres na základě názvu.
    :param districts: seznam všech okresů
    :param district_name: název okresu pro vyhledání
    :return: URL adresa daného okresu
    """
    for district in districts:
        if district["name"] == district_name:
            district_code = district["code"]
            district_url = f"https://volby.cz/pls/ps2017nss/{district_code}"
            return district_url
    raise ValueError("Okres nenalezen")

def get_village_urls(district_url):
    """
    Funkce získá seznam URL adres obcí (villages) z daného URL adresy okresu (district_url).
    :param district_url: URL adresa okresu
    :return: seznam slovníků s názvy obcí, kódy obcí a jejich URL adresami
    """
    response = requests.get(district_url)
    
    if response.status_code != 200:
        raise Exception(f"Chyba při přístupu na stránku {district_url}")
    
    soup = BeautifulSoup(response.text, "html.parser")

    village_urls = []

    # tabulky jsou tři, musíme dát soup.find_all 
    rows = soup.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 0:
            link = cells[0].find("a")
            if link:
                village_code = cells[0].get_text(strip=True)
                village_name = cells[1].get_text(strip=True)
                village_url_suffix = link["href"]
                village_url = f"https://volby.cz/pls/ps2017nss/{village_url_suffix}"
                village_urls.append({"code": village_code, "name": village_name, "url": village_url})

    return village_urls

def scrape_village_results(village):
    """
    Funkce pro scrapování volebních výsledků z jednotlivých obcí.
    :param village: slovník obsahující URL, kód a název obce
    :return: slovník s výsledky hlasování pro obec
    """
    
    response = requests.get(village["url"])
    if response.status_code != 200:
        raise Exception(f"Chyba při přístupu na stránku {village["url"]}")

    soup = BeautifulSoup(response.text, "html.parser")

    # \xa0 je mezera &nbsp; v datech
    voters_registered = int(soup.find("td", class_="cislo", headers="sa2").get_text(strip=True).strip().replace("\xa0", ""))
    envelopes_issued = int(soup.find("td", class_="cislo", headers="sa3").get_text(strip=True).strip().replace("\xa0", ""))
    valid_votes = int(soup.find("td", class_="cislo", headers="sa5").get_text(strip=True).strip().replace("\xa0", ""))

    party_votes = {}
    party_rows = soup.find_all("tr")[5:]
    for row in party_rows:
        cells = row.find_all("td")
        
        if len(cells) >= 3:
            # zkusíme zjistit počet hlasu, kdyz ne, je to řádek který vynecháme
            try:
                votes = int(cells[2].get_text(strip=True).strip().replace("\xa0", ""))
                party_name = cells[1].get_text(strip=True).strip()
            except:
                votes = -1
            
            if votes >= 0:
                party_votes[party_name] = votes
    
    return {
        "code": village["code"],
        "name": village["name"],
        "voters_registered": voters_registered,
        "envelopes_issued": envelopes_issued,
        "valid_votes": valid_votes,
        "party_votes": party_votes
    }

def flatten_data(data):
    """
    Funkce převede strukturovaná data do dvourozměrného formátu, vhodného pro uložení do CSV souboru.
    :param data: seznam slovníků s volebními výsledky pro jednotlivé obce
    :return: seznam plochých slovníků, kde klíče jsou názvy sloupců a hodnoty jsou hodnoty pro jednotlivé buňky
    """
    flattened = []
    for row in data:
        flat_row = {
            "code": row["code"],
            "name": row["name"],
            "voters_registered": row["voters_registered"],
            "envelopes_issued": row["envelopes_issued"],
            "valid_votes": row["valid_votes"]
        }
        #.update vloží každý prvek dictu jako další prvek
        flat_row.update(row["party_votes"])
        flattened.append(flat_row)
    return flattened

def save_data_to_csv(data, filename):
    """
    Funkce pro uložení dat do CSV souboru.
    :param data: seznam plochých slovníků s volebními výsledky
    :param filename: název souboru pro uložení CSV
    """
    if not filename.endswith(".csv"):
        filename += ".csv"

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def main():
    """
    Hlavní funkce programu, která koordinuje jednotlivé kroky pro získání a uložení volebních dat.
    """
    # Krok 1: Zavolá funkci pro request nabízených krajů
    districts = get_districts()
    
    try:
        district_name = sys.argv[1]
        output_filename = sys.argv[2]
        district_url = set_url_for_district(districts, district_name)
    #index mimo pole - nejsou zadané parametry
    except IndexError:
        print("Usage: python web_scraping.py \"<district_name>\" <output_filename>")
        print("Available districts:")
        print_districts(districts)
        sys.exit(1)
    #ValueError vraci set_url_for_district kdyz nenajde okres
    except ValueError:
        print("Wrong district!")
        print("Usage: python web_scraping.py \"<district_name>\" <output_filename>")
        print("Available districts:")
        print_districts(districts)
        sys.exit(1)
        
    # Krok 3: Získá seznam URL adres obcí z daného okresu
    village_urls = get_village_urls(district_url)
    
    # Krok 4: Pro každou obec scrapuje výsledky a přidá je do seznamu
    village_results = []
    for village in village_urls:
        village_data = scrape_village_results(village)
        village_results.append(village_data)
    
    # Krok 5: Převede data do plochého formátu vhodného pro CSV
    flattened_data = flatten_data(village_results)
    
    # Krok 6: Uloží data do CSV souboru
    
    save_data_to_csv(flattened_data, output_filename)
    
    print(f"Data byla úspěšně uložena do souboru {output_filename}")

if __name__ == "__main__":
    main()

