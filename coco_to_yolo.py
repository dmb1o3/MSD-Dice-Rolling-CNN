from ultralytics.data.converter import convert_coco
import os


def coco_to_yolo():
    folder_name = input("Name of the folder located in Annotated-Data that contains COCO json ")
    folder_path = os.getcwd() + "/Annotated-Data/" + folder_name + "/"
    convert_coco(folder_path, save_dir=folder_path + "YOLO-Data", use_segments=True)

if __name__ == '__main__':
    coco_to_yolo()