"""
Train a custom YOLOv8 PPE-detection model.

Recommended dataset: the Roboflow "Construction Site Safety Image Dataset"
(PPE: hardhat, mask, safety vest, + NO- variants) — free to download in
YOLOv8 format. Any dataset with the same class layout works.

Usage:
    1. Download a dataset in YOLOv8 format (data.yaml + images/ + labels/).
    2. pip install ultralytics
    3. python train_model.py --data /path/to/data.yaml --epochs 100

The resulting best.pt should be copied to backend and referenced via the
MODEL_PATH env var (see backend/.env.example).
"""
import argparse

from ultralytics import YOLO


def main():
    parser = argparse.ArgumentParser(description="Train a YOLOv8 PPE detector")
    parser.add_argument("--data", required=True, help="Path to dataset data.yaml")
    parser.add_argument("--model", default="yolov8n.pt", help="Base model to fine-tune from")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--device", default="0", help="'0' for GPU, 'cpu' for CPU")
    parser.add_argument("--project", default="runs/ppe_detect")
    args = parser.parse_args()

    model = YOLO(args.model)
    model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        project=args.project,
        name="train",
        patience=20,
        augment=True,
    )

    metrics = model.val()
    print("Validation metrics:", metrics.results_dict)

    # Export for edge/production deployment
    model.export(format="onnx")
    print(f"\nBest weights: {args.project}/train/weights/best.pt")
    print("Copy this file to backend/ and set MODEL_PATH accordingly.")


if __name__ == "__main__":
    main()
