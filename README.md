# Fightclub

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
python3 main.py
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

### Pour quitter
- Appuyez sur `Échap`

## Système de combat

### Combos
- Enchaînez les coups en moins de 0.5 seconde
- Chaque coup augmente les dégâts de 20%
- Maximum : 2x dégâts
- Le combo se réinitialise après 1 seconde

### Attaques spéciales
- Disponibles après 2 coups réussis
- Dégâts plus importants
- Plus long temps de récupération


