from pathlib import Path

HASH_SIZE      = 16        # Perceptual hash size (16x16 = 256-bit vector). It's enough for a single set, I didn't try with more cards
HASH_DIM       = HASH_SIZE * HASH_SIZE
N_TREES        = 20        
N_NEIGHBORS    = 5         
MAX_CARDS      = 2000      
CARD_SET       = 'sos'     # I'm using sos (Secrets of Strixhaven, 2026) as they are the only cards I have laying around at the moment
                           # Set to None to load ENTIRE database. It works, but it's not fast
CACHE_DIR      = Path('mtg_cache')
CACHE_DIR.mkdir(exist_ok=True)
 
# Card dimensions for perspective correction
CARD_W = 488   # Standard MTG card width in pixels
CARD_H = 680   # Standard MTG card height in pixels
 
print('Configuration loaded')
print(f'  Hash size: {HASH_SIZE}×{HASH_SIZE} = {HASH_DIM} dimensions')
print(f'  Max cards loaded: {MAX_CARDS}')