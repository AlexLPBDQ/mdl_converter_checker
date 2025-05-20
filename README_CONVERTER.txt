📦 Convertisseur de modèles .MDL pour Source Engine (Garry's Mod, Hammer, etc.)

🎯 Ce script vous permet de convertir automatiquement des modèles .mdl vers une version spécifique (ex : 48), compatible avec les outils comme Hammer, VBSP, ou le moteur Source utilisé par Garry's Mod.

🔧 Pourquoi l'utiliser ?
Certains modèles sont compilés dans une version plus récente (ex : 49), ce qui provoque des erreurs dans Hammer ou lors de la compilation de maps :
❌ Warning! Invalid model version 49 (48 expected)

✅ Ce que le script fait :
• Décompile proprement le modèle avec Crowbar
• Corrige la version via le fichier .qc et/ou patch direct du .mdl
• Recompile avec studiomdl.exe dans le dossier d'origine
• Nettoie automatiquement les fichiers inutiles après usage
• Restaure les fichiers d'origine en cas d'erreur de compilation
• Permet l'utilisation du multithread et des sauvegardes optionnelles

⚠️ **IMPORTANT — DISCLAMER**
Il est fortement recommandé de faire une **sauvegarde complète de votre dossier `models/`** avant d'utiliser ce script.
Bien qu'une option de sauvegarde automatique soit intégrée, cela n'exclut pas les risques liés à des écrasements de fichiers ou erreurs de manipulation.

👤 Fonctionne avec Python 3, Crowbar CLI et studiomdl.exe.
Utilisation simple : vous entrez les chemins requis et les options souhaitées à l’exécution.

📁 Idéal pour rendre des packs de modèles compatibles avec les outils Source plus anciens ou éviter les erreurs de version dans Hammer.