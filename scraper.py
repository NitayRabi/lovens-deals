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
        "name": "Bikes Bikes Bikes",
        "location": "Amstelstroomlaan 8, Amsterdam",
        "neighborhood": "Amsterdam (Amstelkwartier)",
        "url": "https://www.bikesbikesbikes.nl/pages/lovens-aanbieding",
        "pickup": "Amsterdam (Amstelkwartier)",
        "maintenance": "Full local workshop (25% off maintenance labor promo)",
        "test_ride": "Yes (spacious outdoor test area)",
        "notes": "€500 direct discount off MSRP on all Lovens Explorer 2 models + 15% off Qover theft insurance & 25% off maintenance labor!",
        "models": [
            {"category": "S100", "model": "Explorer 2 S100", "motor": "Bosch Cargo Line (100Nm)", "gears": "Enviolo Extreme", "base_price": 6599, "deal_price": 6099, "status": "€500 Aanbieding"},
            {"category": "S75", "model": "Explorer 2 S75", "motor": "Bosch Performance (75Nm)", "gears": "Enviolo HD", "base_price": 6299, "deal_price": 5799, "status": "€500 Aanbieding"}
        ]
    },
    {
        "name": "Fietsenwinkel.nl Amsterdam",
        "location": "Overtoom 8, 1054 HH Amsterdam",
        "neighborhood": "Amsterdam West / Centrum (Overtoom / Vondelpark)",
        "url": "https://fietsenwinkel.nl/lovens-explorer-2-s100",
        "pickup": "Amsterdam (Overtoom 8)",
        "maintenance": "In-store workshop (Voorzien van een werkplaats) + E-Bakfiets Servicepakket (€199/2yr)",
        "test_ride": "Yes (test rides right into Vondelpark)",
        "notes": "Black Friday instore deals live! Includes free ready-to-ride assembly (t.w.v. €99) and optional 2-year bakfiets maintenance package.",
        "models": [
            {"category": "S100", "model": "Explorer 2 S100", "motor": "Bosch Cargo Line (100Nm)", "gears": "Enviolo Heavy Duty", "base_price": 6599, "deal_price": 6199, "status": "Black Friday Deal", "url": "https://fietsenwinkel.nl/lovens-explorer-2-s100"},
            {"category": "S75", "model": "Explorer 2 S75", "motor": "Bosch Performance (75Nm)", "gears": "Enviolo Heavy Duty", "base_price": 6599, "deal_price": 5699, "status": "Black Friday Deal", "url": "https://fietsenwinkel.nl/lovens-explorer-2-s75"}
        ]
    },
    {
        "name": "QicQ Amsterdam",
        "location": "KNSM-Laan 11, Amsterdam",
        "neighborhood": "Amsterdam Oost (KNSM-Eiland)",
        "url": "https://shop.qicq.nl/elektrische-bakfietsen/lovens/",
        "pickup": "Amsterdam (KNSM-Eiland)",
        "maintenance": "Dedicated Bosch & Lovens service center on KNSM-Eiland",
        "test_ride": "Yes (dedicated quiet quay route)",
        "notes": "Premium e-bike specialist. Known for Black Friday €500-€700 discount or free accessory bundle (Raincover + LED ~€490 value).",
        "models": [
            {"category": "S100", "model": "Explorer 2 S100", "motor": "Bosch Cargo Line (100Nm)", "gears": "Enviolo Extreme", "base_price": 7199, "deal_price": 6499, "status": "In Stock / Test Ride"},
            {"category": "S75", "model": "Explorer 2 S75", "motor": "Bosch Performance (75Nm)", "gears": "Enviolo Heavy Duty", "base_price": 6299, "deal_price": 5699, "status": "In Stock / Test Ride"}
        ]
    },
    {
        "name": "Fietsvoordeelshop Amsterdam",
        "location": "Parnassusweg 398, Amsterdam",
        "neighborhood": "Amsterdam Zuid",
        "url": "https://www.fietsvoordeelshop.nl/bakfietsen/elektrische-bakfietsen/lovens",
        "pickup": "Amsterdam Zuid & Home Service",
        "maintenance": "In-store Amsterdam Zuid workshop + mobile service van",
        "test_ride": "Yes",
        "notes": "Large volume dealer in Zuid. Strong cash clearance discounts on in-stock Explorer 2 S75 & S100 Auto models.",
        "models": [
            {"category": "S100", "model": "Explorer 2 S100 Auto", "motor": "Bosch Cargo Line (100Nm)", "gears": "Enviolo Automatiq", "base_price": 7399, "deal_price": 6699, "status": "Stock available"},
            {"category": "S75", "model": "Explorer 2 S75", "motor": "Bosch Performance (75Nm)", "gears": "Enviolo Heavy Duty", "base_price": 6199, "deal_price": 5499, "status": "Special Autumn Price"}
        ]
    },
    {
        "name": "DrBeyk Amsterdam",
        "location": "Eerste Schinkelstraat 16, Amsterdam",
        "neighborhood": "Amsterdam Zuid / West (Schinkelbuurt)",
        "url": "https://www.drbeykonline.nl/collections/lovens-bakfietsen",
        "pickup": "Amsterdam (Schinkelbuurt)",
        "maintenance": "Specialist Amsterdam bakfiets repair & maintenance shop",
        "test_ride": "Yes",
        "notes": "Dedicated local Amsterdam bakfiets specialist. Highly rated for ongoing family bike maintenance and fast local repairs.",
        "models": [
            {"category": "S100", "model": "Explorer S100 / S85", "motor": "Bosch Cargo Line", "gears": "Enviolo Heavy Duty", "base_price": 6999, "deal_price": 6299, "status": "In Showroom"},
            {"category": "S75", "model": "Explorer S75", "motor": "Bosch Performance (75Nm)", "gears": "Enviolo Heavy Duty", "base_price": 6099, "deal_price": 5499, "status": "In Showroom"}
        ]
    },
    {
        "name": "Urban E-Bikes",
        "location": "Danie Theronstraat 22 & Overtoom 459, Amsterdam",
        "neighborhood": "Amsterdam Oost & West",
        "url": "https://www.urbanebikes.nl/48-lovens",
        "pickup": "Amsterdam Oost / West",
        "maintenance": "Two Amsterdam service workshops (Oost & Overtoom)",
        "test_ride": "Yes",
        "notes": "Two full-service locations in Amsterdam. Offers trade-in options and seasonal accessory promotions.",
        "models": [
            {"category": "S100", "model": "Explorer 2 S100", "motor": "Bosch Cargo Line (100Nm)", "gears": "Enviolo Extreme", "base_price": 7199, "deal_price": 6599, "status": "Order / Pickup"},
            {"category": "S75", "model": "Explorer 2 S75", "motor": "Bosch Performance (75Nm)", "gears": "Enviolo HD", "base_price": 6299, "deal_price": 5699, "status": "Order / Pickup"}
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

    # Live check Fietsenwinkel.nl S100 & S75
    fw_s100 = fetch_html("https://fietsenwinkel.nl/lovens-explorer-2-s100")
    if fw_s100:
        m = re.search(r'Adviesprijs:\s*€\s*([0-9.]+),[0-9]{2}\s*€\s*([0-9.]+),[0-9]{2}', fw_s100)
        if m:
            for d in dealers:
                if "Fietsenwinkel.nl" in d["name"]:
                    d["models"][0]["base_price"] = int(m.group(1).replace(".", ""))
                    d["models"][0]["deal_price"] = int(m.group(2).replace(".", ""))

    fw_s75 = fetch_html("https://fietsenwinkel.nl/lovens-explorer-2-s75")
    if fw_s75:
        m = re.search(r'Adviesprijs:\s*€\s*([0-9.]+),[0-9]{2}\s*€\s*([0-9.]+),[0-9]{2}', fw_s75)
        if m:
            for d in dealers:
                if "Fietsenwinkel.nl" in d["name"]:
                    d["models"][1]["base_price"] = int(m.group(1).replace(".", ""))
                    d["models"][1]["deal_price"] = int(m.group(2).replace(".", ""))

live_check()

# Build model-grouped structure for side-by-side comparison by model
models_by_category = {
    "S100": {
        "title": "Lovens Explorer 2 S100 (100Nm Cargo Line)",
        "subtitle": "Bosch Cargo Line (100Nm) • Enviolo Extreme / Automatiq • Best for bridges, hills & 2+ kids",
        "offers": []
    },
    "S75": {
        "title": "Lovens Explorer 2 S75 (75Nm Performance Line)",
        "subtitle": "Bosch Performance Line (75Nm) • Enviolo Heavy Duty • Smooth city cruising",
        "offers": []
    }
}

for d in dealers:
    for m in d["models"]:
        cat = m.get("category", "S100" if "100" in m["model"] else "S75")
        offer = {
            "shop_name": d["name"],
            "location": d["location"],
            "neighborhood": d.get("neighborhood", d["pickup"]),
            "maintenance": d.get("maintenance", "Local Amsterdam workshop"),
            "test_ride": d["test_ride"],
            "url": m.get("url", d["url"]),
            "notes": d["notes"],
            "model": m["model"],
            "motor": m["motor"],
            "gears": m["gears"],
            "base_price": m["base_price"],
            "deal_price": m["deal_price"],
            "savings": m["base_price"] - m["deal_price"],
            "status": m["status"]
        }
        models_by_category[cat]["offers"].append(offer)

# Sort each model category by lowest deal_price first
for cat in models_by_category:
    models_by_category[cat]["offers"].sort(key=lambda x: x["deal_price"])

output = {
    "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "target_focus": "Lovens Explorer 2 S100 & S75 (Amsterdam Maintenance Shops Only)",
    "black_friday_window": "Mid-November to Early December (official BF: late Nov)",
    "official_promo": "Free Rain Cover (Regenhuif ~€360) + LED strip (~€130) package often bundled",
    "models_comparison": models_by_category,
    "dealers": dealers
}

with open("/home/nitayrabi/projects/lovens-deals/deals.json", "w") as f:
    json.dump(output, f, indent=2)

print("deals.json created successfully.")
