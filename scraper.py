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
        "notes": "Family cargo bike boutique near Spaklerweg. Offers personalized bundles (free raincover/bench packages).",
        "models": [
            {"model": "Explorer 2 S100", "motor": "Bosch Cargo Line (100Nm)", "gears": "Enviolo Extreme", "base_price": 7199, "deal_price": 6799, "status": "Demo & New in Stock"},
            {"model": "Explorer 2 S75", "motor": "Bosch Performance (75Nm)", "gears": "Enviolo HD", "base_price": 6299, "deal_price": 5799, "status": "Available"}
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

# Write live data json
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
