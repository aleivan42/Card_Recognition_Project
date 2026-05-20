import imagehash
import pickle
import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm
from config import HASH_SIZE, CARD_SET, CACHE_DIR
import numpy as np

def compute_phash(img_pil, hash_size=HASH_SIZE):
    h = imagehash.phash(img_pil, hash_size=hash_size)
    # Convert hash to floating-point binary vector for Annoy
    return h.hash.flatten().astype(np.float32)
 
 
def download_and_hash_cards(cards):

    index_cache = CACHE_DIR / f'hashes_{CARD_SET or "all"}_{len(cards)}.pkl'
    if index_cache.exists():
        print('Hash index found in cache')
        with open(index_cache, 'rb') as f:
            return pickle.load(f)
 
    hashes   = []
    metadata = []
    errors   = 0
 
    for card in tqdm(cards, desc='Downloading & hashing'):
        img_url = card['image_uris']['normal']
        try:
            resp = requests.get(img_url, timeout=5)
            resp.raise_for_status()
            img_pil = Image.open(BytesIO(resp.content))
            
            h_vec = compute_phash(img_pil)
            hashes.append(h_vec)
            metadata.append({
                'name':      card['name'],
                'set_name':  card.get('set_name', 'Unknown'),
                'set':       card.get('set', ''),
                'rarity':    card.get('rarity', 'common'),
                'image_url': img_url,
                'prices':    card.get('prices', {}),
                'scryfall_uri': card.get('scryfall_uri', ''),
            })
        except Exception as e:
            errors += 1
            if errors < 5:  # Show only first few errors
                print(f'Error downloading {card.get("name", "?")} : {e}')
 
    print(f'{len(hashes)} cards hashed successfully ({errors} errors)')
 
  
    with open(index_cache, 'wb') as f:
        pickle.dump((hashes, metadata), f)
 
    return hashes, metadata