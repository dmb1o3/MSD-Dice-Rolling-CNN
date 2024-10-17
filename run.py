import os
from ultralytics import YOLO
import numpy as np
import pandas as pd
import cv2
import glob



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


def run_dice_roll_model():
    # Load model
    model_folder = "YOLOv11_Rolls17"
    model = YOLO("./runs/classify/" + model_folder + "/weights/best.pt")
    results = model("./runs/predictions/seg_and_box_test/")

    # Set up what images model should look at
    image_folder = r'./runs/predictions/seg_and_box_test'
    image_paths = glob.glob(os.path.join(image_folder, '*.jpg'))

    for i in range(0, len(results)):
        # Set up file name and path to save crop
        filename = f"{os.path.basename(image_paths[i])[:-4]}.jpg"  # Change .png to your desired format
        save_path = f'./runs/predictions/rolls/'
        os.makedirs(save_path, exist_ok=True)
        save_path = save_path + filename
        # Save the cropped image
        results[i].save(save_path)  # Use mask.numpy() to get the image data
        print(f"Saved cropped image to {save_path}")


def run_dice_type_model():
    # Load model
    model_folder = "YOLOv8_Newest_run"
    model = YOLO("./runs/segment/" + model_folder + "/weights/best.pt")

    # Set up what images model should look at
    train_image_folder = r'C:\Users\mrjoy\PycharmProjects\MSD-Dice-Rolling-CNN\Annotated-Data\YOLO\FPYS\images\Train'
    val_image_folder = r'C:\Users\mrjoy\PycharmProjects\MSD-Dice-Rolling-CNN\Annotated-Data\YOLO\FPYS\images\Val'
    image_paths = glob.glob(os.path.join(train_image_folder, '*.jpg')) + \
                  glob.glob(os.path.join(train_image_folder, '*.png')) + \
                  glob.glob(os.path.join(train_image_folder, '*.jpeg')) + \
                  glob.glob(os.path.join(val_image_folder, '*.jpg')) + \
                  glob.glob(os.path.join(val_image_folder, '*.png')) + \
                  glob.glob(os.path.join(val_image_folder, '*.jpeg'))

    for image_path in image_paths:
        print(f'\nRunning inference on {image_path}')
        img = cv2.imread(image_path)
        results = model(img)
        results = results[0]
        result_dict = results.to_df().to_dict()
        print(result_dict)
        if result_dict:
            for i in result_dict['name']:
                mask_points = np.array(list(zip(result_dict['segments'][i]['x'], result_dict['segments'][i]['y'])),
                                       dtype=np.int32)
                mask = np.zeros(img.shape[:2], dtype=np.uint8)  # Create a black mask
                cv2.fillPoly(mask, [mask_points], 255)  # Fill the polygon with white

                # Apply the mask to the cropped image
                masked_img = cv2.bitwise_and(img, img, mask=mask)

                # Crop by bounding box
                # Get bounding box
                box = result_dict['box']
                x_min = int(box[i]['x1'])
                y_min = int(box[i]['y1'])
                x_max = int(box[i]['x2'])
                y_max = int(box[i]['y2'])
                # Crop image
                cropped_img = masked_img[y_min:y_max, x_min:x_max]
                # Set up file name and path to save crop
                filename = f"{os.path.basename(image_path)[:-4]}_crop_{i}.jpg"  # Change .png to your desired format
                dice_type = result_dict["name"][i]
                # save_path = f'./runs/predictions/seg_and_box_newest_run/{dice_type}/'
                save_path = f'./runs/predictions/seg_and_box_test/'
                os.makedirs(save_path, exist_ok=True)
                save_path = save_path + filename
                # Save the cropped image
                cv2.imwrite(save_path, cropped_img)  # Use mask.numpy() to get the image data
                print(f"Saved cropped image to {save_path}")


if __name__ == '__main__':
    #run_dice_type_model()
    run_dice_roll_model()