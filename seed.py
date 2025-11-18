import os
import subprocess
import sys
import time
import django

# --------------------------
# Step 1: Install Required Packages
# --------------------------
try:
    print("\n Installing required packages...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True
    )
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True
    )
    print(" Packages installed successfully.\n")
except Exception as e:
    print(f" Package installation failed: {e}")

# --------------------------
# Step 2: Django Environment Setup
# --------------------------
try:
    print(" Setting up Django environment...")
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "project.settings"
    )  # <-- change project name if needed
    django.setup()
    print(" Django environment ready.\n")
except Exception as e:
    print(f" Django setup failed: {e}")
    sys.exit(1)

# --------------------------
# Step 3: Run Migrations
# --------------------------
try:
    print("Making migrations...")
    subprocess.run([sys.executable, "manage.py", "makemigrations"], check=True)

    print("Applying migrations...")
    subprocess.run([sys.executable, "manage.py", "migrate"], check=True)

    print("Migrations completed.\n")
except subprocess.CalledProcessError as e:
    print(f" Migration error: {e}")
    sys.exit(1)

# --------------------------
# Step 4: Start Django Server
# --------------------------
print("Setup complete!")
print("Starting Django server at: http://127.0.0.1:8000")
time.sleep(1)

try:
    subprocess.run([sys.executable, "manage.py", "runserver"])
except KeyboardInterrupt:
    print("\n Server stopped by user.")
