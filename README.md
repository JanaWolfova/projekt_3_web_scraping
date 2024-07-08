# Scraper výsledků voleb z roku 2017

Tento projekt scrapuje volební výsledky zadaného územního celku a ukládá je do souboru CSV.

## Instalace

1. Klonujte tento repozitář.
2. Vytvořte a aktivujte virtuální prostředí.
3. Nainstalujte knihovny uvedené v requirements.txt:

git clone <repo-url>
cd <repo-directory>

### Vytvoření virtuálního prostředí

python -m venv myvenv

### Aktivace virtuálního prostředí

Na Windows:

venv\Scripts\activate.bat

Na MacOS/Linux:

source venv/bin/activate

### Instalace knihoven

pip install -r requirements.txt

## Spuštění

python web_scraping.py "district" output_file

- **district**: Vybraný okres, pro který chcete získat výsledky voleb roku 2017.
- **output_file**: Název souboru, do kterého se uloží výsledky.

### Příklad

python web_scraping.py "Brno-město" vysledky




# Seznam dostupných okresů

    Praha
    Benešov
    Beroun
    Kladno
    Kolín
    Kutná Hora
    Mělník
    Mladá Boleslav
    Nymburk
    Praha-východ
    Praha-západ
    Příbram
    Rakovník
    České Budějovice
    Český Krumlov
    Jindřichův Hradec
    Písek
    Prachatice
    Strakonice
    Tábor
    Domažlice
    Klatovy
    Plzeň-město
    Plzeň-jih
    Plzeň-sever
    Rokycany
    Tachov
    Cheb
    Karlovy Vary
    Sokolov
    Děčín
    Chomutov
    Litoměřice
    Louny
    Most
    Teplice
    Ústí nad Labem
    Česká Lípa
    Jablonec nad Nisou
    Liberec
    Semily
    Hradec Králové
    Jičín
    Náchod
    Rychnov nad Kněžnou
    Trutnov
    Chrudim
    Pardubice
    Svitavy
    Ústí nad Orlicí
    Havlíčkův Brod
    Jihlava
    Pelhřimov
    Třebíč
    Žďár nad Sázavou
    Blansko
    Brno-město
    Brno-venkov
    Břeclav
    Hodonín
    Vyškov
    Znojmo
    Jeseník
    Olomouc
    Prostějov
    Přerov
    Šumperk
    Kroměříž
    Uherské Hradiště
    Vsetín
    Zlín
    Bruntál
    Frýdek-Místek
    Karviná
    Nový Jičín
    Opava
    Ostrava-město


    autor
    Jana Wolfová
