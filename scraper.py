import urllib.request
import json
import re
import datetime
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7"
}

def fetch_html(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        return urllib.request.urlopen(req, timeout=15).read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

dealers = [
    {
        "name": "QicQ Amsterdam",
        "location": "KNSM-Laan 11, Amsterdam",
        "url": "https://shop.qicq.nl/elektrische-bakfietsen/lovens/",
        "pickup": "Amsterdam (KNSM-Eiland)",
        "test_ride": "Yes (dedicated quiet quay route)",
        "notes": "Premium e-bike specialist. Known for Black Friday €500-€700 discount or free accessory bundle (~€490 value).",
        "models": [
            {"model": "Explorer 2 S100", "motor": "Bosch Cargo Line (100Nm)", "gears": "Enviolo Extreme", "base_price": 7199, "deal_price": 6499, "status": "In Stock / Test Ride"},
            {"model": "Explorer 2 S75", "motor": "Bosch Performance (75Nm)", "gears": "Enviolo Heavy Duty", "base_price": 6299, "deal_price": 5699, "status": "In Stock / Test Ride"}
        ]
    },
    {
        "name": "Fietsvoordeelshop Amsterdam",
        "location": "Parnassusweg 398, Amsterdam",
        "url": "https://www.fietsvoordeelshop.nl/bakfietsen/elektrische-bakfietsen/lovens",
        "pickup": "Amsterdam Zuid & Home Delivery",
        "test_ride": "Yes",
        "notes": "Large national volume dealer. High likelihood of immediate cash clearance discounts on in-stock Explorer & Explorer 2 models.",
        "models": [
            {"model": "Explorer 2 S100 Auto", "motor": "Bosch Cargo Line (100Nm)", "gears": "Enviolo Automatiq", "base_price": 7399, "deal_price": 6699, "status": "Stock available"},
            {"model": "Explorer 2 S75", "motor": "Bosch Performance (75Nm)", "gears": "Enviolo Heavy Duty", "base_price": 6199, "deal_price": 5499, "status": "Special Autumn Price"}
        ]
    },
    {
        "name": "Bikes Bikes Bikes",
        "location": "Amstelstroomlaan 8, Amsterdam",
        "url": "https://www.bikesbikesbikes.nl/pages/lovens-aanbieding",
        "pickup": "Amsterdam (Amstelkwartier)",
        "test_ride": "Yes (great outdoor test area)",
        "notes": "€500 direct discount off MSRP on all Lovens Explorer 2 models + 15% off Qover theft insurance & 25% off maintenance labor!",
        "models": [
            {"model": "Explorer 2 S100", "motor": "Bosch Cargo Line (100Nm)", "gears": "Enviolo Extreme", "base_price": 6599, "deal_price": 6099, "status": "€500 Aanbieding"},
            {"model": "Explorer 2 S75", "motor": "Bosch Performance (75Nm)", "gears": "Enviolo HD", "base_price": 6299, "deal_price": 5799, "status": "€500 Aanbieding"}
        ]
    },
    {
        "name": "Fietskar.nl (Hilversum)",
        "location": "Hilversum Showroom & NL Delivery",
        "url": "https://www.fietskar.nl/categorie/bakfiets/lovens/",
        "pickup": "Hilversum (~30 min) & Delivery",
        "test_ride": "Yes (Hilversum showroom)",
        "notes": "Up to 12% off Explorer 2 S75 & S75 Auto/ABS models! Full custom configurator for batteries (400/545/800Wh) and accessories.",
        "models": [
            {"model": "Explorer 2 S100", "motor": "Bosch Cargo Line (100Nm)", "gears": "Enviolo Extreme", "base_price": 7199, "deal_price": 6599, "status": "From €6,599 (400Wh+)"},
            {"model": "Explorer 2 S75", "motor": "Bosch Performance (75Nm)", "gears": "Enviolo Heavy Duty", "base_price": 6299, "deal_price": 5549, "status": "-12% Deal (From €5,549)"}
        ]
    },
    {
        "name": "viaBOVAG (Bike Totaal Krimpen)",
        "location": "Parkzoom 27-29, Krimpen a/d IJssel",
        "url": "https://www.viabovag.nl/fiets/aanbod/lovens-explorer-2-3rm54oj",
        "pickup": "Krimpen a/d IJssel (BOVAG Certified)",
        "test_ride": "Yes (Request via BOVAG)",
        "notes": "Official BLACK FRIDAY listing: €800 discount on brand-new 2025 Lovens Explorer 2 S75 (Avenue Green) with BOVAG 40-point check & warranty.",
        "models": [
            {"model": "Explorer 2 S75 (Avenue Green)", "motor": "Bosch Performance (75Nm)", "gears": "Enviolo Heavy Duty", "base_price": 6299, "deal_price": 5499, "status": "BLACK FRIDAY (-€800)"}
        ]
    },
    {
        "name": "DrBeyk Amsterdam",
        "location": "Eerste Schinkelstraat 16, Amsterdam",
        "url": "https://www.drbeykonline.nl/collections/lovens-bakfietsen",
        "pickup": "Amsterdam West / Westerpark",
        "test_ride": "Yes",
        "notes": "Dedicated Amsterdam bakfiets shop. Great after-sales service and local maintenance in town.",
        "models": [
            {"model": "Explorer S100 / S85", "motor": "Bosch Cargo Line", "gears": "Enviolo", "base_price": 6999, "deal_price": 6299, "status": "In Showroom"},
            {"model": "Explorer S75", "motor": "Bosch Performance (75Nm)", "gears": "Enviolo", "base_price": 6099, "deal_price": 5499, "status": "In Showroom"}
        ]
    },
    {
        "name": "Urban E-Bikes",
        "location": "Danie Theronstraat & Overtoom, Amsterdam",
        "url": "https://www.urbanebikes.nl/48-lovens",
        "pickup": "Amsterdam Oost / West",
        "test_ride": "Yes",
        "notes": "Multiple pickup spots in Amsterdam, offers trade-in options and seasonal promotions.",
        "models": [
            {"model": "Explorer 2 S100", "motor": "Bosch Cargo Line (100Nm)", "gears": "Enviolo Extreme", "base_price": 7199, "deal_price": 6599, "status": "Order / Pickup"},
            {"model": "Explorer 2 S75", "motor": "Bosch Performance (75Nm)", "gears": "Enviolo HD", "base_price": 6299, "deal_price": 5699, "status": "Order / Pickup"}
        ]
    }
]

def live_check():
    # Live check Bikes Bikes Bikes
    bbb_html = fetch_html("https://www.bikesbikesbikes.nl/pages/lovens-aanbieding")
    if bbb_html:
        for d in dealers:
            if d["name"] == "Bikes Bikes Bikes":
                m_s100 = re.search(r'€\s*([0-9]\.[0-9]{3}),00\s*€\s*([0-9]\.[0-9]{3}),00.*?explorer-s100', bbb_html, re.I | re.S)
                if m_s100:
                    deal_p = int(m_s100.group(1).replace(".", ""))
                    base_p = int(m_s100.group(2).replace(".", ""))
                    d["models"][0]["deal_price"] = deal_p
                    d["models"][0]["base_price"] = base_p

    # Live check viaBOVAG
    bovag_html = fetch_html("https://www.viabovag.nl/fiets/aanbod/lovens-explorer-2-3rm54oj")
    if bovag_html:
        for d in dealers:
            if "viaBOVAG" in d["name"]:
                m_price = re.search(r'€\s*([0-9]\.[0-9]{3}),-', bovag_html)
                if m_price:
                    d["models"][0]["deal_price"] = int(m_price.group(1).replace(".", ""))

live_check()

output = {
    "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "target_focus": "Lovens Explorer 2 S100 & S75",
    "black_friday_window": "Mid-November to Early December (official BF: late Nov)",
    "official_promo": "Free Rain Cover (Regenhuif ~€360) + LED strip (~€130) package often bundled",
    "dealers": dealers
}

with open("/home/nitayrabi/projects/lovens-deals/deals.json", "w") as f:
    json.dump(output, f, indent=2)

print("deals.json created successfully.")
