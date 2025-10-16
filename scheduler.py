import schedule
import time
import subprocess
from datetime import datetime
import os

def run_blog_generator():
    """Lance le script de génération de blog et commit les changements"""
    print(f"\n{'='*60}")
    print(f"[{datetime.now()}] Démarrage du générateur de blog...")
    print(f"{'='*60}\n")
    
    try:
        # Lancer le script blog_generator_script.py
        result = subprocess.run(
            ["python", "blog_generator_script.py"],
            capture_output=True,
            text=True,
            timeout=3600  # Timeout de 1 heure
        )
        
        if result.returncode == 0:
            print(f"✅ Script terminé avec succès")
            print(result.stdout)
            
            # Commit automatique des fichiers modifiés (comme dans ton workflow)
            print("\n📝 Sauvegarde des modifications sur GitHub...")
            
            # Configuration git
            subprocess.run(["git", "config", "--global", "user.email", "railway-bot@users.noreply.github.com"])
            subprocess.run(["git", "config", "--global", "user.name", "Railway Bot"])
            
            # Ajouter les fichiers modifiés
            subprocess.run(["git", "add", "sujets.csv"])
            if os.path.exists("sujets_traites.csv"):
                subprocess.run(["git", "add", "sujets_traites.csv"])
            
            # Commit
            commit_result = subprocess.run(
                ["git", "commit", "-m", f"🤖 Article publié automatiquement - {datetime.now().strftime('%Y-%m-%d %H:%M')}"],
                capture_output=True
            )
            
            if commit_result.returncode == 0:
                # Push
                push_result = subprocess.run(["git", "push"], capture_output=True)
                if push_result.returncode == 0:
                    print("✅ Modifications sauvegardées sur GitHub")
                else:
                    print(f"⚠️ Erreur lors du push: {push_result.stderr.decode()}")
            else:
                print("ℹ️ Aucun changement à commiter")
                
        else:
            print(f"❌ Erreur lors de l'exécution")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("❌ Le script a dépassé le timeout d'1 heure")
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
    
    print(f"\n{'='*60}")
    print(f"[{datetime.now()}] Fin de l'exécution")
    print(f"{'='*60}\n")

# Planifier l'exécution 2 fois par semaine
# Mardi à 10h UTC (11h Paris hiver, 12h Paris été)
schedule.every().tuesday.at("10:00").do(run_blog_generator)

# Vendredi à 10h UTC
schedule.every().friday.at("10:00").do(run_blog_generator)

print("🚀 Scheduler démarré !")
print("📅 Exécution programmée :")
print("   - Mardi à 10h00 UTC")
print("   - Vendredi à 10h00 UTC")
print("⏳ En attente de la prochaine exécution...")

# Boucle infinie
while True:
    schedule.run_pending()
    time.sleep(60)  # Vérifie toutes les minutes
