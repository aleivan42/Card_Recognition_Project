from config import N_TREES, CACHE_DIR, CARD_SET, HASH_DIM
from annoy import AnnoyIndex
from tqdm import tqdm

def build_annoy_index(hashes, n_trees=N_TREES):

    index_path = CACHE_DIR / f'annoy_index_{CARD_SET or "all"}_{len(hashes)}.ann'
    
    ann = AnnoyIndex(HASH_DIM, 'angular')  # Angular works best for binary hashes
    
    if index_path.exists():
        print('Annoy index found in cache')
        ann.load(str(index_path))
        return ann
    
    print(f'Building Annoy index with {n_trees} trees')
    for i, h_vec in enumerate(tqdm(hashes, desc='Building index')):
        ann.add_item(i, h_vec)
    
    ann.build(n_trees)
    ann.save(str(index_path))
    print(f'Index built and saved: {index_path}')
    
    return ann