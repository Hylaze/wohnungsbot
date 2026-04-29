import requests
from bs4 import BeautifulSoup
import time
import json
import os
from lxml import html
import urllib
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retries = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
)

# =============================
# CONFIG
# =============================

# GEWOBAG
GEWOBAG_URL_TWOROOM_BESTLOCATIONS = "https://www.gewobag.de/fuer-mietinteressentinnen/mietangebote/wohnung/?objekttyp%5B%5D=wohnung&bezirke_filter%5B%5D=pankow-prenzlauer-berg&zimmer_von=2&zimmer_bis=4&keinwbs=1"
GEWOBAG_URL_ONEROOM_ALL = "https://www.gewobag.de/fuer-mietinteressentinnen/mietangebote/wohnung/?objekttyp%5B%5D=wohnung&bezirke_all=1&bezirke_filter%5B%5D=charlottenburg-wilmersdorf&bezirke_filter%5B%5D=charlottenburg-wilmersdorf-charlottenburg&bezirke_filter%5B%5D=charlottenburg-wilmersdorf-grunewald&bezirke_filter%5B%5D=charlottenburg-wilmersdorf-wilmersdorf&bezirke_filter%5B%5D=friedrichshain-kreuzberg&bezirke_filter%5B%5D=friedrichshain-kreuzberg-friedrichshain&bezirke_filter%5B%5D=friedrichshain-kreuzberg-kreuzberg&bezirke_filter%5B%5D=lichtenberg&bezirke_filter%5B%5D=lichtenberg-alt-hohenschoenhausen&bezirke_filter%5B%5D=lichtenberg-falkenberg&bezirke_filter%5B%5D=lichtenberg-fennpfuhl&bezirke_filter%5B%5D=lichtenberg-friedrichsfelde&bezirke_filter%5B%5D=lichtenberg-lichtenberg&bezirke_filter%5B%5D=marzahn-hellersdorf&bezirke_filter%5B%5D=marzahn-hellersdorf-marzahn&bezirke_filter%5B%5D=mitte&bezirke_filter%5B%5D=mitte-moabit&bezirke_filter%5B%5D=mitte-tiergarten&bezirke_filter%5B%5D=mitte-wedding&bezirke_filter%5B%5D=neukoelln&bezirke_filter%5B%5D=neukoelln-britz&bezirke_filter%5B%5D=neukoelln-buckow&bezirke_filter%5B%5D=neukoelln-rudow&bezirke_filter%5B%5D=pankow&bezirke_filter%5B%5D=pankow-prenzlauer-berg&bezirke_filter%5B%5D=pankow-weissensee&bezirke_filter%5B%5D=reinickendorf&bezirke_filter%5B%5D=reinickendorf-hermsdorf&bezirke_filter%5B%5D=reinickendorf-reinickendorf&bezirke_filter%5B%5D=reinickendorf-tegel&bezirke_filter%5B%5D=reinickendorf-waidmannslust&bezirke_filter%5B%5D=spandau&bezirke_filter%5B%5D=spandau-hakenfelde&bezirke_filter%5B%5D=spandau-haselhorst&bezirke_filter%5B%5D=spandau-siemensstadt&bezirke_filter%5B%5D=spandau-spandau&bezirke_filter%5B%5D=steglitz-zehlendorf&bezirke_filter%5B%5D=steglitz-zehlendorf-lichterfelde&bezirke_filter%5B%5D=tempelhof-schoeneberg&bezirke_filter%5B%5D=tempelhof-schoeneberg-lichtenrade&bezirke_filter%5B%5D=tempelhof-schoeneberg-mariendorf&bezirke_filter%5B%5D=tempelhof-schoeneberg-marienfelde&bezirke_filter%5B%5D=tempelhof-schoeneberg-schoeneberg&bezirke_filter%5B%5D=tempelhof-schoeneberg-tempelhof&bezirke_filter%5B%5D=treptow-koepenick&bezirke_filter%5B%5D=treptow-koepenick-gruenau&bezirke_filter%5B%5D=treptow-koepenick-niederschoeneweide&gesamtmiete_von=&gesamtmiete_bis=&gesamtflaeche_von=&gesamtflaeche_bis=&zimmer_von=&zimmer_bis=1&sort-by="
IBW_SEARCH_URL = "https://www.inberlinwohnen.de/wohnungsfinder"

# get query on https://www.inberlinwohnen.de/wohnungsfinder: search for flats, copy q from URL
IBW_QUERY_TWOROOM_BESTLOCATIONS = "eyJpdiI6InpHNEZkYkJIRFY4QjZDV0hUYVBIeUE9PSIsInZhbHVlIjoiZUY0ODNqZzR2bGVybkpkWDFlUEQ4SmppdG1oeGxFeWdPa3JkWVZ5VEEzZm05QzNOc2l4cVIwdDR2UnBGR05ldXFSQTJkVlVDOGFYR3YxN0FUVTZySTVqUEdyN3VTU0t1Ly82VmdDUFJWdm1ic1RlY2RnRkQ2TmkvZnlUWDNrODZuSk9NT0NwRWg0RVdwVEpxdXA2clIwbko0M3JiMWJyUVJlclJzT3IybmM1UzhUekE2NUlFYkY5aHBnbElrTWdBUUIycHhRR2w3NDUxSFdZbkZLZ3JqMjd0SUNPcEUvZ0RpQkg5ODczbHc5M2srdG52OUlmMXFDbW02c0VJem0xSzVhNHdBcnBCcmFuRGZvc2FMeVg5cExmdFppRWNpV2hhM0ltWXNxY2N1U2s3OWFKN1lYdS9rVzMxQlVmeGx0Y1RIWmRhd2RFZmliekt6TWpxTWZZNHU5cVh1bURpTTVvWlJNSEFIa0Q1VytmTCtzL2JuaktSMU9pbVhxM0UrdStnZU83aGlCQ3drZ1RXUWtzVlpmSWxNRGJhUHNCa21xc0RtRUVUL1VDMnlHU1ZhYVVCUTY3L0w0dlFpY3ZhSS9mZXNYSHlTM0hodUlQWThEbWxOUDFIYndFQ0N3VW5XWDBJOVMzcVhQY1NReUU9IiwibWFjIjoiNWFmMDZjZmJmN2ZkMjZmZGVjY2NlZTRhMDBhMmI1Mjc3ODUyYmJmZGJhZWU3NjVhZGNmNTZlZjFkYWE2NTdiYSIsInRhZyI6IiJ9"
IBW_QUERY_ONEROOM_ALL = "eyJpdiI6IldINGhxV0hOdzZhL29WdUZkZVo5R2c9PSIsInZhbHVlIjoiM3dyRjFSdmJPOElKODBvM0hRM0xNRzJvMG43eEI5Y3ZMTHE2bUM0YlZsL2dKRmowK2tYU0RQQmRkQkZMMXl5cmJVa1p4cDNuVDY4VHMzSFE2MmFzVVlMUTlDYVJtcFh3RUNJSjRYclkxOWVMOFlNc0J2V25yb3BVZnN5TmEveVZPZEgzZ1cvMEZGdGYxdiswMG05MUppMDRyWFg5UzEwVHZnN04rOVY5b2dDMEFHbjNaZ1Y3RXRSei9kTGxxbXZuVmF0MGxNUUFGMXJUeExoMmFxRnZIblVIZm5RVW5pVlFnZEVIMHVDVTZ6TnJmcGZBeFVtUG9YSUVNS0VkNXZTZWVuTE9WZUFVUXNYRUVkNk43RVR0KzF1UHF2cy93YXZBck9QdGFGVXAxL2lHTjBRbHV4ZllpYkVBMzBZTGVoNFJDc0twNHkzZ1pTN0dJOXVNRVhLK3FFN2Y3Sms4dGQyUnd4TU9LYXZ1QnpLaHZueXJuV2t2cXZYdzJoSDB0alFiQjRlcHdEUFBJZWtDalZVQWNHM0xqV1c4czhuZXN3QlBlb2JkNDYzWjcrbz0iLCJtYWMiOiJhNDIwNDMyYzA3NDM3ZjU0NWY3MWUzNTdlZTlmZmU4MGQ5MDNlMzU1YjUyY2Q5OTYxMDRhNDkzZmE5MjM4OGI5IiwidGFnIjoiIn0%3D"


CHECK_INTERVAL = 300  # seconds
GEWOBAG_FILE = "gewobag_listings.json"
IBW_FILE = "ibw_listings.json"

BOT_TOKEN = ""

CHAT_IDS = [
    "" # your chat token 
      # weitere
]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


session = requests.Session()
session.headers.update(HEADERS)

session.mount("https://", HTTPAdapter(max_retries=retries))
# =============================
# TELEGRAM FUNCTION
# =============================

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    for chat_id in CHAT_IDS:
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        requests.post(url, data=payload)

# =============================
# GEWOBAG SCRAPER
# =============================
def safe_get(url, **kwargs):
    try:
        return session.get(url, timeout=15, **kwargs)
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None
        
def get_gewobag_listings():
    response = safe_get(GEWOBAG_URL_TWOROOM_BESTLOCATIONS, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    listings = []
    offers = soup.find_all("article", class_="angebot-big-box")
    for offer in offers:
        link = offer.find("a", class_="read-more-link")
        if link and link.get("href"):
            listings.append(link["href"])
    return listings

def get_gewobag_details(url):
    try:
        r = safe_get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
    except:
        return None

    def get_text(selector):
        el = soup.select_one(selector)
        return el.text.strip() if el else "N/A"

    return {
        "bezirk": get_text("tr.angebot-region td"),
        "adresse": get_text("tr.angebot-address address"),
        "flaeche": get_text("tr.angebot-area td"),
        "kosten": get_text("tr.angebot-kosten td"),
        "link": url
    }

def save_gewobag(listings):
    with open(GEWOBAG_FILE, "w") as f:
        json.dump(listings, f)

def load_gewobag():
    if os.path.exists(GEWOBAG_FILE):
        with open(GEWOBAG_FILE, "r") as f:
            return json.load(f)
    return []

# =============================
# INBERLINWOHNEN SCRAPER
# =============================

def get_ibw_listings():
    params = {"q": IBW_QUERY_TWOROOM_BESTLOCATIONS}
    resp = requests.get(IBW_SEARCH_URL, headers=HEADERS, params=params, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    snapshots = soup.find_all(attrs={"wire:snapshot": True})
    listings = []

    for snap in snapshots:
        snap_json = snap.get("wire:snapshot")
        if not snap_json:
            continue    
        try:
            data = json.loads(snap_json)
            apartments = data.get("data", {}).get("data", [])
            for apt in apartments:
                # Extract address info
                addr_list = apt.get("address", [])
                if not addr_list:
                    continue
                addr = addr_list[0]
                street = addr.get("street_name", "")
                number = addr.get("street_number", "")
                zip_code = addr.get("zip_code", "")
                district = ""
                if isinstance(addr.get("district"), list) and addr["district"]:
                    first_district = next((d for d in addr["district"] if isinstance(d, dict) and "name" in d), {})
                    district = first_district.get("name", "")
                elif isinstance(addr.get("district"), dict):
                    district = addr["district"].get("name", "")

                # Extract flat attributes
                flat_attrs = []
                for attr_group in apt.get("flat_attributes", []):
                    for attr_item in attr_group:
                        if isinstance(attr_item, dict) and "flat_attribute_id" in attr_item:
                            flat_attrs.append(attr_item["flat_attribute_id"])

                # Extract heating types
                heating_types = []
                for ht_group in apt.get("flat_heating_types", []):
                    for ht_item in ht_group:
                        if isinstance(ht_item, dict) and "flat_heating_type_id" in ht_item:
                            heating_types.append(ht_item["flat_heating_type_id"])

                rent_net = float(apt.get("rent_net", 0))
                extra_costs = float(apt.get("extra_costs", 0))
                rent_gross = rent_net + extra_costs
                rent_gross_str = f"€{rent_gross:,.2f}"  # z.B. €822.45

                listings.append({
                    "title": apt.get("title"),
                    "link": apt.get("deeplink"),
                    "rooms": apt.get("rooms"),
                    "area": apt.get("area"),
                    "rent_net": rent_net,
                    "extra_costs": extra_costs,
                    "rent_gross": rent_gross_str,
                    "bezirk": district,
                    "adresse": f"{street} {number}, {zip_code}",
                    "flaeche": apt.get("area"),
                    "attributes": flat_attrs,
                    "heating_types": heating_types
                })
        except Exception:
            continue    
    return listings


def save_ibw(listings):
    with open(IBW_FILE, "w") as f:
        json.dump(listings, f)

def load_ibw():
    if os.path.exists(IBW_FILE):
        with open(IBW_FILE, "r") as f:
            return json.load(f)
    return []

# =============================
# MAIN LOOP
# =============================

print("🔎 Monitoring GEWOBAG + InBerlinWohnen for new listings...")
send_telegram("🚀 Housing bot started successfully.")

gewobag_known = load_gewobag()
ibw_known = load_ibw()

# First run: don't alert old listings
if not gewobag_known:
    gewobag_known = get_gewobag_listings()
    save_gewobag(gewobag_known)
print("gewo:",gewobag_known)
if not ibw_known:
    ibw_known = [f['link'] for f in get_ibw_listings()]
    save_ibw(ibw_known)
print("ibw:",ibw_known)
print("ibwlen",len(ibw_known))
try:
    while True:
        # Fetch current listings
        gewobag_current = get_gewobag_listings()
        ibw_current = [f['link'] for f in get_ibw_listings()]

        # Detect new listings
        new_gewobag = [l for l in gewobag_current if l not in gewobag_known]
        new_ibw = [l for l in ibw_current if l not in ibw_known]
        if not new_gewobag and not new_ibw:
           print("No new listings.")
        # Send alerts for GEWOBAG
        for listing in new_gewobag:
            details = get_gewobag_details(listing)
            if details:
                message = f"""
🚨 <b>New GEWOBAG Apartment</b>
📍 <b>Bezirk:</b> {details['bezirk']}
🏠 <b>Adresse:</b> {details['adresse']}
📐 <b>Fläche:</b> {details['flaeche']}m²
💰 <b>Gesamtmiete:</b> {details['kosten']}
🔗 {details['link']}
"""
                send_telegram(message)
                print("New GEWOBAG listing sent:", details['link'])

        # Send alerts for InBerlinWohnen
        ibw_all = get_ibw_listings()
        for listing in new_ibw:
            details = next((f for f in ibw_all if f["link"] == listing), None)
            if details:
                message = f"""
🚨 <b>New InBerlinWohnen Apartment</b>
📍 <b>Bezirk:</b> {details['bezirk']}
🏠 <b>Adresse:</b> {details['adresse']}
📐 <b>Fläche:</b> {details['flaeche']}m²
💰 <b>Gesamtmiete:</b> {details['rent_gross']}€
🔗 {details['link']}
"""
                send_telegram(message)
                print("New InBerlinWohnen listing sent:", details['link'])

        # Save updated known listings
        gewobag_known = gewobag_current
        ibw_known = ibw_current
        save_gewobag(gewobag_known)
        save_ibw(ibw_known)

        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("\n🛑 Bot stopped manually.")
    send_telegram("🛑 Housing bot stopped manually.")
