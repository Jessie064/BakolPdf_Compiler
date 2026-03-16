import subprocess, sys, os

os.chdir(r"C:\Users\Jessie\OneDrive\Desktop\pdf compiler")
result = subprocess.run(
    [sys.executable, "manage.py", "migrate"],
    capture_output=True,
    text=True
)
print("=== STDOUT ===")
print(result.stdout)
print("=== STDERR ===")
print(result.stderr)
print("=== Exit code:", result.returncode)
