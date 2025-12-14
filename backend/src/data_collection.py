"""
Data collection utilities for the Fake Product Detection System.

This module provides utilities for collecting, organizing, and labeling
product images for training the classification model.
"""
import os
import json
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import hashlib
from src.models import TrainingSample


class DatasetOrganizer:
    """
    Organizes product images into train/val/test splits.
    
    Directory structure:
    data/
    ├── raw/                    # Raw collected images
    ├── processed/              # Processed and organized
    │   ├── train/
    │   │   ├── original/
    │   │   └── fake/
    │   ├── val/
    │   │   ├── original/
    │   │   └── fake/
    │   └── test/
    │       ├── original/
    │       └── fake/
    └── metadata/               # JSON metadata files
    """
    
    def __init__(self, base_path: str = "./data"):
        """
        Initialize dataset organizer.
        
        Args:
            base_path: Base directory for dataset
        """
        self.base_path = Path(base_path)
        self.raw_path = self.base_path / "raw"
        self.processed_path = self.base_path / "processed"
        self.metadata_path = self.base_path / "metadata"
        
        # Split ratios
        self.train_ratio = 0.7
        self.val_ratio = 0.15
        self.test_ratio = 0.15
        
    def create_directory_structure(self):
        """Create the dataset directory structure."""
        # Create main directories
        self.raw_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        
        # Create split directories
        for split in ['train', 'val', 'test']:
            for label in ['original', 'fake']:
                split_dir = self.processed_path / split / label
                split_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Created directory structure at {self.base_path}")
    
    def compute_file_hash(self, file_path: str) -> str:
        """
        Compute SHA256 hash of a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Hex digest of file hash
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def organize_dataset(
        self,
        source_dir: str,
        label: str,
        category: str = "general",
        train_ratio: float = None,
        val_ratio: float = None,
        test_ratio: float = None
    ) -> Dict[str, int]:
        """
        Organize images from source directory into train/val/test splits.
        
        Args:
            source_dir: Directory containing images to organize
            label: Label for images ("original" or "fake")
            category: Product category
            train_ratio: Training set ratio (default: 0.7)
            val_ratio: Validation set ratio (default: 0.15)
            test_ratio: Test set ratio (default: 0.15)
            
        Returns:
            Dictionary with counts for each split
        """
        if train_ratio:
            self.train_ratio = train_ratio
        if val_ratio:
            self.val_ratio = val_ratio
        if test_ratio:
            self.test_ratio = test_ratio
        
        # Validate ratios
        total_ratio = self.train_ratio + self.val_ratio + self.test_ratio
        if abs(total_ratio - 1.0) > 0.01:
            raise ValueError(f"Split ratios must sum to 1.0, got {total_ratio}")
        
        # Validate label
        if label not in ['original', 'fake']:
            raise ValueError(f"Label must be 'original' or 'fake', got '{label}'")
        
        # Get all image files
        source_path = Path(source_dir)
        if not source_path.exists():
            raise FileNotFoundError(f"Source directory not found: {source_dir}")
        
        image_extensions = {'.jpg', '.jpeg', '.png', '.heic'}
        image_files = [
            f for f in source_path.iterdir()
            if f.is_file() and f.suffix.lower() in image_extensions
        ]
        
        if not image_files:
            print(f"⚠️  No images found in {source_dir}")
            return {'train': 0, 'val': 0, 'test': 0}
        
        # Shuffle files (using hash for deterministic shuffle)
        image_files.sort(key=lambda x: self.compute_file_hash(str(x)))
        
        # Calculate split indices
        n_total = len(image_files)
        n_train = int(n_total * self.train_ratio)
        n_val = int(n_total * self.val_ratio)
        
        # Split files
        train_files = image_files[:n_train]
        val_files = image_files[n_train:n_train + n_val]
        test_files = image_files[n_train + n_val:]
        
        # Copy files to appropriate directories
        counts = {'train': 0, 'val': 0, 'test': 0}
        metadata_records = []
        
        for split, files in [('train', train_files), ('val', val_files), ('test', test_files)]:
            dest_dir = self.processed_path / split / label
            
            for file_path in files:
                # Generate unique filename
                file_hash = self.compute_file_hash(str(file_path))[:8]
                new_filename = f"{category}_{label}_{file_hash}{file_path.suffix}"
                dest_path = dest_dir / new_filename
                
                # Copy file
                shutil.copy2(file_path, dest_path)
                counts[split] += 1
                
                # Create metadata record
                metadata_records.append({
                    'original_path': str(file_path),
                    'new_path': str(dest_path),
                    'split': split,
                    'label': label,
                    'category': category,
                    'file_hash': file_hash,
                    'timestamp': datetime.utcnow().isoformat()
                })
        
        # Save metadata
        metadata_file = self.metadata_path / f"{category}_{label}_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata_records, f, indent=2)
        
        print(f"✅ Organized {n_total} images:")
        print(f"   Train: {counts['train']} ({counts['train']/n_total*100:.1f}%)")
        print(f"   Val: {counts['val']} ({counts['val']/n_total*100:.1f}%)")
        print(f"   Test: {counts['test']} ({counts['test']/n_total*100:.1f}%)")
        
        return counts
    
    def get_dataset_statistics(self) -> Dict:
        """
        Get statistics about the organized dataset.
        
        Returns:
            Dictionary with dataset statistics
        """
        stats = {
            'train': {'original': 0, 'fake': 0},
            'val': {'original': 0, 'fake': 0},
            'test': {'original': 0, 'fake': 0}
        }
        
        for split in ['train', 'val', 'test']:
            for label in ['original', 'fake']:
                split_dir = self.processed_path / split / label
                if split_dir.exists():
                    stats[split][label] = len(list(split_dir.glob('*')))
        
        # Calculate totals
        stats['total'] = {
            'original': sum(stats[s]['original'] for s in ['train', 'val', 'test']),
            'fake': sum(stats[s]['fake'] for s in ['train', 'val', 'test']),
            'all': sum(sum(stats[s].values()) for s in ['train', 'val', 'test'])
        }
        
        # Calculate balance
        if stats['total']['all'] > 0:
            stats['balance'] = {
                'original_pct': stats['total']['original'] / stats['total']['all'] * 100,
                'fake_pct': stats['total']['fake'] / stats['total']['all'] * 100
            }
        
        return stats
    
    def print_dataset_summary(self):
        """Print a summary of the dataset."""
        stats = self.get_dataset_statistics()
        
        print("\n" + "="*50)
        print("DATASET SUMMARY")
        print("="*50)
        
        for split in ['train', 'val', 'test']:
            total = stats[split]['original'] + stats[split]['fake']
            print(f"\n{split.upper()}:")
            print(f"  Original: {stats[split]['original']:4d}")
            print(f"  Fake:     {stats[split]['fake']:4d}")
            print(f"  Total:    {total:4d}")
        
        print(f"\nTOTAL:")
        print(f"  Original: {stats['total']['original']:4d} ({stats['balance']['original_pct']:.1f}%)")
        print(f"  Fake:     {stats['total']['fake']:4d} ({stats['balance']['fake_pct']:.1f}%)")
        print(f"  All:      {stats['total']['all']:4d}")
        print("="*50 + "\n")
    
    def create_training_samples_list(self, split: str = 'train') -> List[TrainingSample]:
        """
        Create a list of TrainingSample objects for a given split.
        
        Args:
            split: Dataset split ('train', 'val', or 'test')
            
        Returns:
            List of TrainingSample objects
        """
        samples = []
        
        for label_idx, label in enumerate(['original', 'fake']):
            split_dir = self.processed_path / split / label
            
            if not split_dir.exists():
                continue
            
            for image_path in split_dir.glob('*'):
                if image_path.is_file():
                    # Extract category from filename
                    parts = image_path.stem.split('_')
                    category = parts[0] if len(parts) > 0 else "unknown"
                    
                    sample = TrainingSample(
                        image_path=str(image_path),
                        label=label_idx,  # 0 = Original, 1 = Fake
                        product_category=category,
                        source="organized_dataset",
                        verified=True,
                        metadata={
                            'split': split,
                            'filename': image_path.name
                        }
                    )
                    samples.append(sample)
        
        return samples


class DataLabeler:
    """
    Utilities for labeling and verifying product images.
    """
    
    def __init__(self, metadata_path: str = "./data/metadata"):
        """
        Initialize data labeler.
        
        Args:
            metadata_path: Path to metadata directory
        """
        self.metadata_path = Path(metadata_path)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
    
    def create_labeling_task(
        self,
        image_dir: str,
        task_name: str,
        category: str = "general"
    ) -> str:
        """
        Create a labeling task for a directory of images.
        
        Args:
            image_dir: Directory containing images to label
            task_name: Name for this labeling task
            category: Product category
            
        Returns:
            Path to labeling task file
        """
        image_path = Path(image_dir)
        if not image_path.exists():
            raise FileNotFoundError(f"Image directory not found: {image_dir}")
        
        # Get all images
        image_extensions = {'.jpg', '.jpeg', '.png', '.heic'}
        images = [
            str(f) for f in image_path.iterdir()
            if f.is_file() and f.suffix.lower() in image_extensions
        ]
        
        # Create labeling task
        task = {
            'task_name': task_name,
            'category': category,
            'created_at': datetime.utcnow().isoformat(),
            'total_images': len(images),
            'labeled_count': 0,
            'images': [
                {
                    'path': img,
                    'label': None,
                    'verified': False,
                    'notes': ''
                }
                for img in images
            ]
        }
        
        # Save task file
        task_file = self.metadata_path / f"labeling_task_{task_name}.json"
        with open(task_file, 'w') as f:
            json.dump(task, f, indent=2)
        
        print(f"✅ Created labeling task: {task_file}")
        print(f"   Total images: {len(images)}")
        
        return str(task_file)
    
    def load_labeling_task(self, task_file: str) -> Dict:
        """
        Load a labeling task.
        
        Args:
            task_file: Path to task file
            
        Returns:
            Task dictionary
        """
        with open(task_file, 'r') as f:
            return json.load(f)
    
    def save_labeling_task(self, task_file: str, task: Dict):
        """
        Save a labeling task.
        
        Args:
            task_file: Path to task file
            task: Task dictionary
        """
        with open(task_file, 'w') as f:
            json.dump(task, f, indent=2)
    
    def get_labeling_progress(self, task_file: str) -> Dict:
        """
        Get progress statistics for a labeling task.
        
        Args:
            task_file: Path to task file
            
        Returns:
            Progress statistics
        """
        task = self.load_labeling_task(task_file)
        
        labeled = sum(1 for img in task['images'] if img['label'] is not None)
        verified = sum(1 for img in task['images'] if img['verified'])
        
        return {
            'total': task['total_images'],
            'labeled': labeled,
            'verified': verified,
            'unlabeled': task['total_images'] - labeled,
            'progress_pct': (labeled / task['total_images'] * 100) if task['total_images'] > 0 else 0
        }


def create_sample_dataset_structure():
    """
    Create a sample dataset structure for demonstration.
    
    This creates empty directories and a README explaining how to add data.
    """
    organizer = DatasetOrganizer()
    organizer.create_directory_structure()
    
    # Create README
    readme_content = """# Product Image Dataset

## Directory Structure

```
data/
├── raw/                    # Place raw collected images here
│   ├── original/          # Authentic product images
│   └── fake/              # Counterfeit product images
├── processed/             # Organized dataset (auto-generated)
│   ├── train/
│   │   ├── original/
│   │   └── fake/
│   ├── val/
│   │   ├── original/
│   │   └── fake/
│   └── test/
│       ├── original/
│       └── fake/
└── metadata/              # JSON metadata files
```

## How to Add Data

1. **Collect Images**: Place raw product images in `data/raw/`
   - Authentic products → `data/raw/original/`
   - Counterfeit products → `data/raw/fake/`

2. **Organize Dataset**: Run the organization script
   ```python
   from data_collection import DatasetOrganizer
   
   organizer = DatasetOrganizer()
   organizer.organize_dataset(
       source_dir="data/raw/original",
       label="original",
       category="electronics"
   )
   organizer.organize_dataset(
       source_dir="data/raw/fake",
       label="fake",
       category="electronics"
   )
   ```

3. **Check Statistics**:
   ```python
   organizer.print_dataset_summary()
   ```

## Data Requirements

- **Minimum**: 1000 images per category (500 original + 500 fake)
- **Recommended**: 5000+ images per category
- **Balance**: Aim for 50/50 split between original and fake
- **Formats**: JPEG, PNG, HEIC
- **Size**: Up to 10MB per image

## Data Sources

- Kaggle datasets
- Academic research datasets
- Web scraping (with permission)
- Manual collection
- Synthetic data generation

## Labeling

Use the DataLabeler class to create labeling tasks for unlabeled images.
"""
    
    readme_path = organizer.base_path / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Created README at {readme_path}")


if __name__ == "__main__":
    # Create sample dataset structure
    create_sample_dataset_structure()
