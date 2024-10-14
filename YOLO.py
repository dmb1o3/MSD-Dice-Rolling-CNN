from ultralytics import YOLO
import torch
import os

YOLOv8_SEG = "yolov8n-seg.pt"
YOLOv11_SEG = "yolo11n-seg.pt"

def train_model():
    data_path = "./Annotated-Data/YOLO/FPYS/data.yaml"
    model = YOLO(YOLOv11_SEG)

    model.train(
        data=data_path,
        epochs=400,
        batch=5,
        name="YOLOv11_dice_segmentation_experiment_batch_5_epoch_400_patience_20",
        flipud=0.5,
        patience=20,
    )

    # Run validation to check metrics
    val_results = model.val(data=data_path)
    print(val_results)

    # Predict on a test image
    test_image = os.path.join(os.getcwd(), 'Annotated-Data/YOLO/FPYS/images/val/image_23.jpg')
    results = model(test_image)

    for result in results:
        result.show()
        result.save("annotated_image.jpg")


def run_model():
    data_path = "./runs/segment/YOLOv8_dice_segmentation_experiment/weights/best.pt"
    model = YOLO(data_path)

    test_image = os.path.join(os.getcwd(), 'Annotated-Data/FPYS/images/val/image_23.jpg')
    results = model(test_image)
    masks = results[0].masks
    boxes = results[0].boxes
    classes = results[0].names

    print(classes)




if __name__ == '__main__':
    train_model()