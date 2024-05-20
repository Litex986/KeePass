# README - KeePass en Python avec Interface Tkinter

## Description

Ce projet est un gestionnaire de mots de passe (KeePass) développé en Python avec une interface graphique utilisant Tkinter. Il utilise des techniques de chiffrement avancées pour assurer la sécurité des données.

## Installation

Avant de commencer, assurez-vous d'avoir installé les bibliothèques nécessaires ([pycryptodome](https://pypi.org/project/pycryptodome/), [pycryptodomex](https://pypi.org/project/pycryptodomex/), [tkinter](https://docs.python.org/fr/3/library/tkinter.html) et [pyperclip](https://pypi.org/project/pyperclip/)). Vous pouvez les installer en utilisant `pip` :

```bash
pip install pycryptodome
pip install pycryptodomex
pip install pyperclip
```

## Utilisation

Pour déverrouiller le KeePass, vous devez fournir deux mots de passe. Lors de la première utilisation, entrez les deux mots de passe comme si vous vous y connectiez normalement.

### Chiffrement des Données

Les données du KeePass sont chiffrées en utilisant la fonction HKDF pour dériver les deux clés de KeePass en trois clés (KEY0, KEY1, KEY2) avec SHA512 :

- **KEY1** : Utilisée pour chiffrer tous les sites.
- **KEY2** : Dérivée en deux clés pour chaque site, une pour chiffrer le nom d'utilisateur et l'autre pour le mot de passe.
- **KEY0** : Utilisée pour chiffrer l'ensemble des données lors de l'enregistrement dans un fichier.

L'utilisation des clés est la suivante :

```
site_Web + username      + password
KEY1     + dérivée KEY2  + dérivée KEY2
```

### Génération de Mots de Passe

Le générateur de mots de passe crée des mots de passe de 29 caractères comprenant :

- 6 chiffres (`"0123456789"`)
- 6 caractères minuscules (`"azertyuiopqsdfghjklmwxcvbn"`)
- 6 caractères majuscules (`"AZERTYUIOPQSDFGHJKLMWXCVBN"`)
- 6 caractères spéciaux (`"!»#$%&'()*+,-./:;<=>?@[\]^_`{|}~"`)
- 5 caractères dérivés du hash (SHA512) du deuxième mot de passe du KeePass (calculé uniquement au dernier moment sans jamais être enregistré).

## Exécution du Projet

Pour exécuter le projet, lancez simplement le script principal :

```bash
python KeePass.py
```

Cela ouvrira l'interface graphique où vous pourrez gérer vos mots de passe en toute sécurité.


## Auteurs

- [Litex986](https://github.com/Litex986) - Développeur principal
