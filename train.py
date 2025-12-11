import torch
from ultralytics import YOLO # type: ignore
import os

# NOTE: 2 methods:
    # 1. Increase epochs on 11n
    # 2. try more intensive yolo11s or yolo11m
# existing model
model = YOLO("runs/yolo/dice_model_v1/weights/last.pt")
    # 100 epochs

# model = YOLO("yolo11n.pt")
# model = YOLO("yolo11m.pt") 
print("###### Model Loaded ######")

output_dir = os.path.join(os.getcwd(), "runs/yolo")
os.makedirs(output_dir, exist_ok=True)

device = (
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else
    "cpu"
)

results = model.train(
    epochs=50, # 

    data="yolo_data/data.yaml",
    project=output_dir,
    name="dice_model_v2", #  100 epochs
    exist_ok=True,

    imgsz=640, # image size
    batch=16,
    lr0=0.001,
    
    workers=4,
    device=device,
    verbose=True,
)

print("\n###### Training Finished ######")
print(results)



print("\n###### Running Validation ######")
val_results = model.val(
    project=output_dir, 
    name="dice_model_v2_val"  
)

print("\n###### Validation Metrics ######")
precision     = val_results.results_dict.get("metrics/precision(B)", None)
recall        = val_results.results_dict.get("metrics/recall(B)", None)
map50         = val_results.results_dict.get("metrics/mAP50(B)", None)
map5095       = val_results.results_dict.get("metrics/mAP50-95(B)", None)

print(f"Precision: {precision:.4f}" if precision else "Precision not found")
print(f"Recall:    {recall:.4f}" if recall else "Recall not found")
print(f"mAP50:     {map50:.4f}" if map50 else "mAP50 not found")
print(f"mAP50-95:  {map5095:.4f}" if map5095 else "mAP50-95 not found")



print("\n###### Accuracy per Class (Dice #) ######")
metrics = val_results.box
for cls_id, cls_name in enumerate(model.names):
    precision = metrics.p[cls_id]
    recall = metrics.r[cls_id]
    ap50 = metrics.ap50[cls_id]
    ap5095 = metrics.ap[cls_id]
    
    print(f"Class {cls_id} ({cls_name}): "
          f"P={precision:.3f}, R={recall:.3f}, "
          f"AP50={ap50:.3f}, AP50-95={ap5095:.3f}")

print("\nBest weights saved at:")
print("  runs/detect/dice_model_v1/weights/best.pt")