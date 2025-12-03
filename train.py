from ultralytics import YOLO
import torch


model = YOLO("yolo11n.pt")

print("###### Model Loaded ######")

results = model.train(
    data="yolo_data/data.yaml",
    epochs=10,
    imgsz=640, # image size
    batch=16,
    lr0=0.001,
    workers=4,
    device=0 if torch.backends.mps.is_available() else "cpu", # use CUDA in kaggle
    name="dice_model_v1",
    verbose=True,
)

print("\n###### Training Finished ######")
print(results)

print("\n###### Running Validation ######")
val_results = model.val()

print("\n=== Validation Summary ===")
print(f"Precision:      {val_results.results_dict['metrics/precision']:.4f}")
print(f"Recall:         {val_results.results_dict['metrics/recall']:.4f}")
print(f"mAP50:          {val_results.results_dict['metrics/mAP50']:.4f}")
print(f"mAP50-95:       {val_results.results_dict['metrics/mAP50-95']:.4f}")

print("\n###### Class-wise accuracy ######")
for cls_id, cls_name in enumerate(model.names):
    precision = val_results.box.pr[cls_id]
    recall = val_results.box.re[cls_id]
    print(f"Class {cls_id} ({cls_name}): Precision={precision:.3f}, Recall={recall:.3f}")

print("\nBest weights saved at:")
print("  runs/detect/dice_model_v1/weights/best.pt")