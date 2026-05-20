from config import CACHE_DIR
import requests
import json

def fetch_scryfall_bulk():
    """Download complete card list from Scryfall API"""
    cache_path = CACHE_DIR / 'cards_meta.json'
    if cache_path.exists():
        print('Metadata already in cache')
        with open(cache_path) as f:
            return json.load(f)
        
    print('Downloading Scryfall bulk list')
    bulk_info = requests.get('https://api.scryfall.com/bulk-data/default-cards').json()
    bulk_url  = bulk_info['download_uri']

    print(f'   URL: {bulk_url}')
    resp = requests.get(bulk_url, stream=True)
    cards = resp.json()
 
    with open(cache_path, 'w') as f:
        json.dump(cards, f)
 
    print(f'{len(cards):,} cards downloaded')
    return cards

def filter_cards(cards, set_code=None, max_n=None):
    
    filtered = [
        c for c in cards
        if c.get('image_uris', {}).get('normal')   # image available
        and c.get('lang') == 'en'                  # english version
        and (set_code is None or c.get('set') == set_code)
    ]
    if max_n:
        filtered = filtered[:max_n]
    print(f'{len(filtered):,} cards selected after filtering')
    return filtered