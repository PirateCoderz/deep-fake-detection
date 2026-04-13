import os
import sys

dirs_to_check = {
    'train/original': r'G:\Github\Pirate-Coderz\deep-fake-detection\data\train\original',
    'train/fake': r'G:\Github\Pirate-Coderz\deep-fake-detection\data\train\fake',
}

for label, d in dirs_to_check.items():
    if os.path.exists(d):
        files = os.listdir(d)
        print(f"{label}: {len(files)} files", flush=True)
    else:
        print(f"{label}: DOES NOT EXIST", flush=True)
