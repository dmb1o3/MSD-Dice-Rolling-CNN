import os
from ultralytics import YOLO
import numpy as np
import pandas as pd
import cv2
import glob

# Set up what images model should look at
train_image_folder = r'C:\Users\mrjoy\PycharmProjects\MSD-Dice-Rolling-CNN\Annotated-Data\YOLO\FPYS\images\Train'
val_image_folder = r'C:\Users\mrjoy\PycharmProjects\MSD-Dice-Rolling-CNN\Annotated-Data\YOLO\FPYS\images\Val'
image_paths = glob.glob(os.path.join(train_image_folder, '*.jpg')) + \
              glob.glob(os.path.join(train_image_folder, '*.png')) + \
              glob.glob(os.path.join(train_image_folder, '*.jpeg')) + \
              glob.glob(os.path.join(val_image_folder, '*.jpg')) + \
              glob.glob(os.path.join(val_image_folder, '*.png')) + \
              glob.glob(os.path.join(val_image_folder, '*.jpeg'))


def get_segment_crop(img,tol=0, mask=None):
    # Ensure the mask is a boolean array
    mask = mask.astype(bool)

    # Find the bounding box of the non-zero pixels
    x_indices = np.any(mask, axis=0)  # Columns where mask is True
    y_indices = np.any(mask, axis=1)  # Rows where mask is True

    if not np.any(x_indices) or not np.any(y_indices):
        return None  # Return None if no object is found

    # Get the bounding box coordinates
    x_min, x_max = np.where(x_indices)[0][[0, -1]]
    y_min, y_max = np.where(y_indices)[0][[0, -1]]

    # Crop the image using the bounding box
    return img[y_min:y_max + 1, x_min:x_max + 1]


def run_model():
    # Load model
    model_folder = "YOLOv11_dice_segmentation_experiment_batch_5_epoch_400_patience_20"
    model = YOLO("./runs/segment/" + model_folder + "/weights/best.pt")

    for image_path in image_paths:
        print(f'\nRunning inference on {image_path}')
        img = cv2.imread(image_path)
        results = model(img)
        results = results[0]
        result_dict = results.to_df().to_dict()
        for i in result_dict['name']:
            # Get bounding box
            box = result_dict['box']
            x_min = int(box[i]['x1'])
            y_min = int(box[i]['y1'])
            x_max = int(box[i]['x2'])
            y_max = int(box[i]['y2'])
            # Crop image
            cropped_img = img[y_min:y_max, x_min:x_max]
            # Set up file name and path to save crop
            filename = f"{os.path.basename(image_path)[:-4]}_crop_{i}.jpg"  # Change .png to your desired format
            dice_type = result_dict["name"][i]
            save_path = f'./runs/predictions/box/{dice_type}/'
            os.makedirs(save_path, exist_ok=True)
            save_path = save_path + filename
            # Save the cropped image
            cv2.imwrite(save_path, cropped_img)  # Use mask.numpy() to get the image data
            print(f"Saved cropped image to {save_path}")
            # @TODO Crop by segment

if __name__ == '__main__':
    run_model()