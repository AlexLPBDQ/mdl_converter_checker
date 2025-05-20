# 🔧 Source Engine MDL Tools

Ce dépôt contient deux outils Python conçus pour faciliter la gestion et la conversion des modèles `.mdl` dans des projets utilisant le **Source Engine** (notamment **Garry's Mod** et **Hammer++**).

---

## 🔁 `mdl_converter.py` — Convertisseur de modèles `.mdl`

Ce script permet de **décompiler, corriger et recompiler** automatiquement des modèles `.mdl` pour les rendre compatibles avec les outils Source plus anciens (comme Hammer ou vbsp).

### ✅ Fonctionnalités :
- Conversion automatique vers une version `.mdl` ciblée (par défaut : `48`)
- Décompilation via **Crowbar CLI**
- Recompilation via **studiomdl.exe**
- Ajout ou correction du `$modelversion` dans les fichiers `.qc`
- Patch manuel du fichier `.mdl` en cas de besoin
- Suppression des fichiers `.qc`, `.smd`, `_anims`, etc. si générés
- Multithreading configurable (jusqu'à 8 threads)
- Sauvegarde automatique des fichiers d'origine (optionnelle)
- Restauration automatique en cas d’échec de compilation

### ⚠️ Important (Disclaimer)
Il est fortement recommandé de faire une **sauvegarde complète de votre dossier `models/` avant d'exécuter ce script**, même si une option de sauvegarde automatique est incluse. Le script peut écraser des fichiers existants.

---

## 🔍 `mdl_checker.py` — Vérificateur de versions `.mdl`

Ce script scanne récursivement un dossier pour afficher :
- soit tous les modèles `.mdl` compilés **dans une version spécifique**
- soit ceux **qui ne correspondent pas à cette version**

### ✅ Utilité :
- Repérer rapidement les modèles incompatibles avec votre version cible (ex : 49 vs 48)
- Préparer une conversion de masse avec `mdl_converter.py`

---

## 🧱 Prérequis
- [Python 3](https://www.python.org/)
- [Crowbar (CLI)](https://steamcommunity.com/groups/CrowbarTool)
- `studiomdl.exe` (disponible dans Garry’s Mod ou les SDK Source)

---

## 🗂️ Structure
```
.
├── mdl_converter.py     # Script interactif de conversion automatique
├── mdl_checker.py       # Script de vérification de version .mdl
├── crowbar/             # Placez Crowbar CLI ici
└── auto_backup/         # Créé automatiquement si les backups sont activés
```

---

## 📖 Licence
Ces scripts sont fournis à titre d’outil libre pour moddeurs Source. Aucune garantie. Utilisation à vos risques.
