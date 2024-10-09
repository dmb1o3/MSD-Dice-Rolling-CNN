from ultralytics import YOLO
from ultralytics.data.converter import convert_coco
import os

YOLOv8_SEG = "yolov8n-seg.pt"
YOLOv11_SEG = "yolo11n-seg.pt"


def coco_to_yolo():
    folder_name = input("Name of the folder located in Annotated-Data that contains COCO json ")
    folder_path = os.getcwd() + "/Annotated-Data/" + folder_name + "/"
    convert_coco(folder_path, save_dir=folder_path + "YOLO-Data", use_segments=True)

def run_model():
    data_path = "./Annotated-Data/FPYS/data.yaml"
    model = YOLO(YOLOv8_SEG)
    model.train(
        data=data_path,
        epochs=100,
        batch=10,
        name="YOLOv8_dice_segmentation_experiment_batch_10",
    )

    # Run validation to check metrics
    val_results = model.val(data=data_path)
    print(val_results)

    # Predict on a test image
    test_image = os.path.join(os.getcwd(), 'Annotated-Data/FPYS/images/val/image_23.jpg')
    results = model(test_image)  # This returns predictions

    for result in results:
        result.show()
        result.save("annotated_image.jpg")


if __name__ == '__main__':
    run_model()