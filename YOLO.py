from ultralytics import YOLO
import torch
import os

YOLOv8_SEG = "yolov8n-seg.pt"
YOLOv11_SEG = "yolo11n-seg.pt"
YOLOv11_CLS = "yolo11n-cls.pt"


def train_dice_type_model():
    """
    Train a YOLO segmentation model to detect dice type i.e d3, d6 ...
    :return:
    """
    data_path = "./Annotated-Data/YOLO/FPYS/data.yaml"
    model = YOLO(YOLOv8_SEG)

    model.train(
        data=data_path,
        epochs=400,
        batch=32,
        name="YOLOv8_Newest_run",
        flipud=0.5,
        patience=20,
        degrees=180,
        mixup=0.3,
        copy_paste=0.3,
        hsv_h=0.04,
        shear=0.0,
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


def train_dice_roll_model():
    """
    Train a YOLO classification model to detect what number is rolled on a die
    :return:
    """
    data_path = "./Annotated-Data/YOLO/Rolls/All"
    model = YOLO(YOLOv11_CLS)

    model.train(
        data=data_path,
        epochs=400,
        batch=10,
        name="YOLOv11_Rolls_All_Not_Including_Recent_Data",
        flipud=0.5,
        patience=20,
        degrees=180,
        mixup=0.3,
        copy_paste=0.3,
        hsv_h=0.04,
        shear=0.0,
    )

    # Run validation to check metrics
    val_results = model.val(data=data_path)
    print(val_results)



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
    train_dice_roll_model()