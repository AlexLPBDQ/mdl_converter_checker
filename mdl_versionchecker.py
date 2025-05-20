import os
import struct

def get_mdl_version(filepath):
    try:
        with open(filepath, "rb") as f:
            f.seek(4)
            version = struct.unpack("i", f.read(4))[0]
            return version
    except Exception as e:
        return f"[Erreur] {filepath} : {e}"

def check_all_mdls_in(folder, target_version, show_matching):
    print(f"\n📁 Analyse des fichiers .mdl dans : {folder}\n")
    found_any = False
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".mdl"):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, folder)
                version = get_mdl_version(path)

                if isinstance(version, int):
                    if (show_matching and version == target_version) or (not show_matching and version != target_version):
                        print(f"{rel_path:60} → version {version}")
                        found_any = True
                else:
                    print(f"{rel_path:60} → {version}")
                    found_any = True

    if not found_any:
        print("✅ Aucun fichier correspondant à ce critère trouvé.")

if __name__ == "__main__":
    print("🔎 Vérification des versions .MDL\n")
    path = input("📁 Entrez le dossier à analyser (ex : D:\\gmod\\models) : ").strip('"').replace("\\", "/")
    while not os.path.exists(path):
        path = input("❌ Dossier introuvable. Réessayez : ").strip('"').replace("\\", "/")

    try:
        target_version = int(input("🎯 Entrez la version cible à rechercher (ex : 48) : "))
    except ValueError:
        print("❌ Version invalide. Par défaut : 48")
        target_version = 48

    mode = input("🔍 Voulez-vous afficher les modèles dans cette version ? (o/n) : ").lower()
    show_matching = mode == "o"

    check_all_mdls_in(path, target_version, show_matching)
    input("\n✅ Terminé. Appuyez sur Entrée pour fermer...")
