"""
Quick local demo: runs PPE detection on your webcam (or a video file) and
shows the annotated feed in an OpenCV window — no backend/frontend needed.
Useful for sanity-checking a newly trained model before wiring it into the app.

Usage:
    python scripts/demo.py --source 0
    python scripts/demo.py --source /path/to/video.mp4 --model backend/best.pt
"""
import argparse
import sys
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))
from app.detection import PPEDetector  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="0")
    parser.add_argument("--model", default="yolov8n.pt")
    args = parser.parse_args()

    detector = PPEDetector(model_path=args.model)
    source = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"Could not open source: {args.source}")
        return

    print("Press 'q' to quit.")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        detections = detector.infer(frame)
        annotated = detector.annotate(frame, detections)
        cv2.imshow("PPE Compliance Demo", annotated)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
