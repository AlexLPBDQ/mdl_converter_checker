🔎 Outil de vérification de version des fichiers .MDL

🎯 Ce petit script vous permet de repérer rapidement les modèles .mdl qui :
• Sont compilés dans une version spécifique (ex : 48)
• OU ne sont pas dans cette version (ex : 49, 44, etc.)

📦 Pourquoi c’est utile ?
Si vous utilisez des modèles dans un projet Hammer ou GMod, la version du modèle doit souvent être exactement 48. Autrement, vous verrez des erreurs dans le log ou le modèle ne s’affichera pas.

✅ Ce que le script fait :
• Parcourt récursivement tous les fichiers .mdl dans un dossier
• Affiche uniquement ceux qui correspondent (ou non) à la version que vous indiquez
• Utile pour repérer rapidement les modèles à corriger avec le convertisseur

👤 Simple à utiliser, fonctionne avec Python 3.
Parfait pour faire un tri avant de convertir des modèles.