import cv2
from config import N_NEIGHBORS
from PIL import Image
import numpy as np
from phash import compute_phash

def recognize_card(card_img, ann_index, metadata, n_neighbors=N_NEIGHBORS):
    if isinstance(card_img, np.ndarray):
        card_pil = Image.fromarray(cv2.cvtColor(card_img, cv2.COLOR_BGR2RGB))
    else:
        card_pil = card_img
    
    query_hash = compute_phash(card_pil)
    
    indices, distances = ann_index.get_nns_by_vector(
        query_hash, 
        n_neighbors, 
        include_distances=True
    )
    
    results = []
    for idx, dist in zip(indices, distances):
        results.append({
            'metadata': metadata[idx],
            'distance': dist,
            'similarity': 1 - (dist / 2)
        })
    
    return results

def display_result(results, card_img):
    if not results:
        print("No results found")
        return
    
    best = results[0]
    meta = best['metadata']
    
    display = card_img.copy()
    h, w = display.shape[:2]
    
    price_eur = meta['prices'].get('eur') or "N/A"
    price_usd = meta['prices'].get('usd') or "N/A"
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    cv2.rectangle(display, (0, 0), (w, 60), (0, 0, 0), -1)
    cv2.rectangle(display, (0, h-80), (w, h), (0, 0, 0), -1)
    cv2.putText(display, meta['name'], (10, 25), font, 0.7, (0, 255, 0), 2)
    cv2.putText(display, f"Match: {best['similarity']*100:.1f}%", (10, 50), font, 0.5, (200, 200, 200), 1)
    cv2.putText(display, f"Price: {price_eur} EUR / {price_usd} USD", (10, h-50), font, 0.6, (255, 255, 255), 2)
    cv2.putText(display, "Source: Scryfall.com", (10, h-20), font, 0.5, (150, 150, 150), 1)
    cv2.imshow('Result - Press any key', display)
    