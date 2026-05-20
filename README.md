# Card_Recognition_Project
Code du projet pour le séminaire d'Introduction au Traitement d'Image (SP26)


Système de reconnaissance de cartes Magic: The Gathering en temps réel par webcam, SANS machine learning, uniquement par traitement d'image classique et recherche de voisin approximatif.

---

## Fonctionnement

1. **Détection** — la carte est isolée dans le flux vidéo par analyse des contours (Canny) et filtrage géométrique
2. **Correction de perspective** — transformation homographique pour redresser la carte à 488×680 px
3. **Hachage perceptuel** — compression de l'image en vecteur binaire de 256 bits via DCT (pHash)
4. **Recherche ANN** — comparaison au voisin le plus proche dans un index Annoy construit sur la base Scryfall
5. **Résultat** — nom de la carte et prix en temps réel (EUR / USD)

---

## Installation

```bash
git clone https://github.com/aleivan42/Card_Recognition_Project
cd Card_Recognition_Project
pip install -r requirements.txt
python main.py
```

À la première exécution, le programme télécharge les métadonnées et les images depuis l'API Scryfall et les met en cache localement. Les lancements suivants sont quasi-instantanés.

---

## Configuration

Tous les paramètres se trouvent dans `config.py` :

| Paramètre | Valeur par défaut | Description |
|-----------|-------------------|-------------|
| `CARD_SET` | `'sos'` | Code du set à charger (`None` pour la base complète) |
| `MAX_CARDS` | `2000` | Nombre maximum de cartes chargées |
| `HASH_SIZE` | `16` | Taille du hash perceptuel (16×16 = 256 bits) |
| `N_TREES` | `20` | Nombre d'arbres dans l'index Annoy |

---

## Utilisation

| Touche | Action |
|--------|--------|
| `ESPACE` | Reconnaître la carte en focus |
| `Q` | Quitter |

---

## Limites connues

La détection repose sur des hypothèses géométriques simples (4 sommets, ratio fixe). Elle fonctionne bien sur les cartes standard, mais peut échouer sur des bordures décoratives complexes comme les **Mystical Archive**, où Canny détecte de nombreux contours internes avant le bord extérieur de la carte.
