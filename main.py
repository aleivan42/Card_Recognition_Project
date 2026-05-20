from data_acquisition import fetch_scryfall_bulk, filter_cards
from ann_index import build_annoy_index
from config import CARD_SET, MAX_CARDS
from demo import run_webcam_demo
from phash import download_and_hash_cards

def main():
    print("\n" + "="*60)
    print("MTG CARD RECOGNITION - REAL-TIME DETECTION")
    print("="*60 + "\n")
    
    print("Step 1: Loading card database")
    all_cards = fetch_scryfall_bulk()
    selected_cards = filter_cards(all_cards, set_code=CARD_SET, max_n=MAX_CARDS)
    
    print("\nStep 2: Computing perceptual hashes")
    hashes, metadata = download_and_hash_cards(selected_cards)
    
    print("\nStep 3: Building ANN search index")
    ann_index = build_annoy_index(hashes)
    
    print(f"\nSystem ready! Database contains {len(metadata)} cards")
    
    print("\nStep 4: Starting webcam demo")
    run_webcam_demo(ann_index, metadata)
 
 
main()