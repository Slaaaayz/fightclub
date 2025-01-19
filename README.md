# Fight Club

Un jeu de combat 2D inspiré de Brawlhalla, développé avec Pygame.

## Installation et Lancement

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances
```bash
pip install -r requirements.txt
```

### Lancement du jeu
```bash
python3 main.py # Linux
python main.py # Windows
```

## Comment jouer

### Contrôles

#### Joueur 1 (Gauche)
- **Déplacement** 
  - `Q` : Gauche
  - `D` : Droite
  - `Z` : Saut (double saut possible)
- **Attaques**
  - `S` : Attaque légère (5 dégâts)
  - `A` : Attaque lourde (10 dégâts)
  - `E` : Attaque spéciale (15 dégâts)

#### Joueur 2 (Droite)
- **Déplacement**
  - `←` : Gauche
  - `→` : Droite
  - `↑` : Saut (double saut possible)
- **Attaques**
  - `Entrée` : Attaque légère
  - `↓` : Attaque lourde
  - `Shift Droit` : Attaque spéciale

### Règles du jeu

- Chaque joueur a 3 vies
- La barre de vie se recharge à 100% après chaque mort
- Plus les dégâts sont élevés, plus le knockback est important
- Les combos augmentent les dégâts (jusqu'à 2x)
- Perdre toutes ses vies = défaite
- Tomber de la plateforme = perte d'une vie

### Système de combat

#### Types d'attaques
- **Attaque légère** : 
  - Dégâts : 5
  - Portée : Courte
  
- **Attaque lourde** :
  - Dégâts : 10
  - Portée : Moyenne

- **Attaque spéciale** :
  - Dégâts : 15
  - Portée : Longue

#### Système de Combo
- Enchaînez les coups en moins de 0.5 seconde
- Chaque coup réussi augmente les dégâts de 20%
- Maximum : 2x dégâts
- Le combo se réinitialise après 1 seconde sans coup

### Options
- Réglage du volume (Master, Musique, SFX)
- Affichage des FPS
- Affichage des contrôles


### Credit
- CHORT Maxime
- DIARD Tristan
- ANDREANI Noah