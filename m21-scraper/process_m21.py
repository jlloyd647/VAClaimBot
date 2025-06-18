import subprocess

print("📘 Running: build_flat_index.py")
result1 = subprocess.run(["python", "build_flat_index.py"])
if result1.returncode != 0:
    print("❌ Indexing failed")
    exit(1)

print("🧩 Running: chunk_m21_content.py")
result2 = subprocess.run(["python", "chunk_m21_content.py"])
if result2.returncode != 0:
    print("❌ Chunking failed")
    exit(1)

print("✅ All done!")