import os
import struct
import subprocess
import shutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# === ENTRÉES INTERACTIVES ===
print("🎮 Bienvenue dans le convertisseur de modèles .MDL vers Source Engine !\n")

try:
    target_version = int(input("🎯 Entrez la version cible des modèles [.mdl] (par défaut : 48) : ") or 48)
except ValueError:
    target_version = 48

def normalize_path(path):
    return os.path.normpath(path.strip('"').replace("\\", "/"))

models_path = normalize_path(input("📁 Entrez le chemin vers le dossier contenant les modèles : "))
while not os.path.exists(models_path):
    models_path = normalize_path(input("❌ Dossier invalide. Réessayez : "))

while True:
    studiomdl_dir = normalize_path(input("📦 Entrez le dossier contenant studiomdl.exe : "))
    possible_path = os.path.join(studiomdl_dir, "studiomdl.exe")
    if os.path.isfile(possible_path):
        studiomdl_path = possible_path
        break
    else:
        print("❌ studiomdl.exe introuvable dans ce dossier. Réessayez.")

enable_backup = input("💾 Souhaitez-vous créer une sauvegarde automatique des fichiers ? (o/n) : ").lower() == "o"
if enable_backup:
    auto_backup_folder = os.path.join("auto_backup")
    os.makedirs(auto_backup_folder, exist_ok=True)
else:
    auto_backup_folder = normalize_path(input("📂 Entrez le chemin vers le dossier de backup existant : "))
    while not os.path.exists(auto_backup_folder):
        auto_backup_folder = normalize_path(input("❌ Dossier introuvable. Réessayez : "))

enable_multithread = input("⚙️ Souhaitez-vous activer le mode multithread ? (o/n) : ").lower() == "o"
max_threads = 1
if enable_multithread:
    try:
        max_threads = int(input("🔧 Combien de cœurs souhaitez-vous utiliser (1 à 8) : "))
        max_threads = max(1, min(max_threads, 8))
    except ValueError:
        max_threads = 4

# === CONFIGURATION ===
CROWBAR_PATH = "crowbar/Crowbar.exe"
MIN_VERSION_ALLOWED = 45
TEMP_EXTENSIONS = [".qc", ".smd", ".qci", ".vta", ".vproj"]
LOG_PATH = "log.txt"

log_lock = threading.Lock()

# === LOGGING ===
def log(message):
    print(message)
    with log_lock:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"{message}\n")

# === OUTILS DE FICHIERS ===
def get_mdl_version(filepath):
    try:
        with open(filepath, "rb") as f:
            f.seek(4)
            version = struct.unpack("i", f.read(4))[0]
            return version
    except Exception as e:
        log(f"[Erreur] Lecture impossible {filepath} : {e}")
        return None

def force_set_mdl_version(filepath, version):
    try:
        with open(filepath, "r+b") as f:
            f.seek(4)
            f.write(struct.pack("i", version))
        log(f"🛠️ Correction forcée du fichier {os.path.basename(filepath)} → version {version}")
    except Exception as e:
        log(f"[⚠️] Impossible de modifier la version du fichier : {e}")

def snapshot_files(folder):
    return set(os.listdir(folder))

def cleanup_new_files(folder, before_set):
    after_set = set(os.listdir(folder))
    new_files = after_set - before_set
    for file in new_files:
        full_path = os.path.join(folder, file)
        if os.path.isdir(full_path) and file.endswith("_anims"):
            log(f"🗑️ Suppression du dossier généré : {file}")
            shutil.rmtree(full_path, ignore_errors=True)
        elif any(file.endswith(ext) for ext in TEMP_EXTENSIONS):
            try:
                os.remove(full_path)
                log(f"🗑️ Suppression du fichier généré : {file}")
            except Exception as e:
                log(f"⚠️ Erreur suppression fichier : {file} → {e}")

def backup_model_files(model_path):
    if not enable_backup:
        return
    base = os.path.splitext(model_path)[0]
    rel = os.path.relpath(base, models_path)
    extensions = [".mdl", ".vvd", ".dx90.vtx", ".phy"]
    for ext in extensions:
        src = base + ext
        if os.path.exists(src):
            dst = os.path.join(auto_backup_folder, rel + ext)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            log(f"💾 Sauvegardé : {rel + ext}")

def restore_model_files(model_path):
    base = os.path.splitext(os.path.relpath(model_path, models_path))[0]
    extensions = [".mdl", ".vvd", ".dx90.vtx", ".phy"]
    for ext in extensions:
        backup_file = os.path.join(auto_backup_folder, base + ext)
        target_file = os.path.join(models_path, base + ext)
        if os.path.exists(backup_file):
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            shutil.copy2(backup_file, target_file)
            log(f"♻️ Restauration : {base + ext}")

# === COMPILE / DÉCOMPILE ===
def decompile_and_recompile(model_path, working_dir):
    qc_filename = os.path.basename(model_path).replace(".mdl", ".qc")
    qc_path = os.path.join(working_dir, qc_filename)
    already_decompiled = os.path.exists(qc_path)

    backup_model_files(model_path)
    before = snapshot_files(working_dir)

    if not already_decompiled:
        log(f"🔧 Décompilation : {model_path}")
        subprocess.run([
            CROWBAR_PATH,
            "-p", model_path,
            "-o", working_dir
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        log(f"⚠️ {qc_filename} déjà présent → skip décompilation")

    if os.path.exists(qc_path):
        with open(qc_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        found = False
        for i, line in enumerate(lines):
            if "$modelversion" in line:
                lines[i] = f"$modelversion {target_version}\n"
                found = True
                break
        if not found:
            lines.insert(0, f"$modelversion {target_version}\n")

        with open(qc_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        result = subprocess.run(
            [studiomdl_path, qc_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=working_dir
        )

        if "Error opening" in result.stdout or "Error opening" in result.stderr:
            log(f"[💥] Erreur compilation : {qc_path} → restauration")
            restore_model_files(model_path)
        else:
            cleanup_new_files(working_dir, before)
            force_set_mdl_version(model_path, target_version)
            log(f"✅ Compilation réussie : {qc_path}")
            version_after = get_mdl_version(model_path)
            log(f"🧪 Version finale : {version_after}")
    else:
        log(f"[✘] Fichier .qc introuvable : {qc_path}")
        restore_model_files(model_path)

# === TRAITEMENT PAR MODÈLE ===
def process_model(full_path, root):
    file = os.path.basename(full_path)
    try:
        version = get_mdl_version(full_path)
        if version is None:
            return
        if version == target_version:
            log(f"[✓] {file} → version {version} : OK")
        elif version >= MIN_VERSION_ALLOWED:
            log(f"[!] {file} → version {version} : recompilation → {target_version}")
            decompile_and_recompile(full_path, root)
        else:
            log(f"[🕳️] {file} → version trop ancienne → ignoré")
    except Exception as e:
        log(f"[❌] Erreur : {file} → {e}")

# === LANCEMENT MULTITHREAD ===
def process_all_models():
    tasks = []
    for root, _, files in os.walk(models_path):
        for file in files:
            if file.endswith(".mdl"):
                full_path = os.path.join(root, file)
                tasks.append((full_path, root))

    if enable_multithread:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [executor.submit(process_model, path, root) for path, root in tasks]
            for future in as_completed(futures):
                pass
    else:
        for full_path, root in tasks:
            process_model(full_path, root)

# === MAIN ===
if __name__ == "__main__":
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("")
    log(f"===== Début — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====")
    process_all_models()
    log("===== Fin du traitement =====")
    input("\n✅ Terminé. Appuyez sur Entrée pour fermer...")
