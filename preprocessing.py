# detect dice
import os, shutil, random
from pathlib import Path


def create_yaml(out_dir):
    yaml_text = f"""
path: {out_dir}
train: images/train
val: images/val

names:
    1: '1
    2: '2'
    3: '3'
    4: '4'
    5: '5'
    6: '6'
nc: 6
        """
        
    with open(out_dir / "data.yaml", "w") as file:
        file.write(yaml_text)
        
    print("data.yaml file created")
        
    
def process_dataset(dataset_dir="data", out_dir="yolo_data", val_ratio=0.2):
    dataset_dir, out_dir = Path(dataset_dir), Path(out_dir)
    
    images_dir = dataset_dir / "images"
    labels_dir = dataset_dir / "labels"
    
    
    (out_dir / "images" / "train").mkdir(parents=True, exist_ok=True)
    (out_dir / "images" / "val").mkdir(parents=True, exist_ok=True)
    (out_dir / "labels" / "train").mkdir(parents=True, exist_ok=True)
    (out_dir / "labels" / "val").mkdir(parents=True, exist_ok=True)

    dataset_images = list(images_dir.glob("*jpg"))
    random.shuffle(dataset_images)
    
    train_test_split = int(len(dataset_images) * (1 - val_ratio))
    train_images = dataset_images[:train_test_split]
    val_images = dataset_images[train_test_split:]
    
    def move_split(img_list, split_name):
        for img_path in img_list:
            lbl_path = labels_dir / (img_path.stem + ".txt")
            if lbl_path.exists():
                shutil.copy(img_path, out_dir / "images" / split_name / img_path.name)
                shutil.copy(lbl_path, out_dir / "labels" / split_name / lbl_path.name)
        print(f"{split_name} images and labels moved")
        
    move_split(train_images, "train")
    move_split(val_images, "val")
    
    
    # create yaml file
    create_yaml(out_dir)
    
    print("Dataset prepared")
    
    
def main():
    process_dataset()
    
if __name__ == '__main__':
    create_yaml(Path("yolo_data"))
    # main()

    