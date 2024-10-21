import os
import shutil
from ultralytics import YOLO
import numpy as np
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


def run_dice_roll_model(model, cropped_img, parent_image_name, crop_number):
    results = model(cropped_img)
    dice_rolls = {"name":{}}
    # Set up file name and path to save crop
    filename = f"{parent_image_name}_{crop_number}.jpg"  # Change .png to your desired format
    save_path = f'./demo/classify/'
    os.makedirs(save_path, exist_ok=True)
    save_path = save_path + filename
    # Save the cropped image
    results[0].save(save_path)  # Use mask.numpy() to get the image data
    # save results
    dice_roll = results[0].names[results[0].probs.top1]

    # print(f"Saved cropped image to {save_path}")

    return dice_roll


def run_dice_type_dice_roll_models():
    # Load dice type model
    dice_type_folder = "YOLOv8_Newest_run"
    dice_type_model = YOLO("./runs/segment/" + dice_type_folder + "/weights/best.pt")
    # Load dice roll model
    dice_roll_folder = "YOLOv11_Rolls_All_Not_Including_Recent_Data"
    dice_roll_model = YOLO("./runs/classify/" + dice_roll_folder + "/weights/best.pt")

    image_folder = r'./demo/'
    image_paths = glob.glob(os.path.join(image_folder, '*.jpg'))

    result_dict = {'name': {}, "rolls": {}}

    for image_path in image_paths:
        print(f'\nRunning inference on {image_path}')
        # Read image
        img = cv2.imread(image_path)
        # Run result
        results = dice_type_model(img)
        # Get first frame since just a photo
        results = results[0]
        # Transform into dictionary
        result_dict = results.to_df().to_dict()
        result_dict["rolls"] = {}
        # If we detected dice for each dice crop and segment
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

                result_dict["rolls"][i] = run_dice_roll_model(dice_roll_model, cropped_img, os.path.basename(image_path)[:-4], i)

                # Set up file name and path to save crop
                filename = f"{os.path.basename(image_path)[:-4]}_crop_{i}.jpg"  # Change .png to your desired format

                # save_path = f'./runs/predictions/seg_and_box_newest_run/{dice_type}/'
                save_path = f'./demo/segment/'
                os.makedirs(save_path, exist_ok=True)
                save_path = save_path + filename
                # Save the cropped image
                cv2.imwrite(save_path, cropped_img)  # Use mask.numpy() to get the image data
                print(f"Saved cropped image to {save_path}")

    return result_dict["name"], result_dict["rolls"]



def run_models():
    # If the exist clear out folders
    classify_folder = "./demo/classify"
    segment_folder = "./demo/segment"
    if os.path.exists(classify_folder):
        shutil.rmtree(classify_folder)
    if os.path.exists(segment_folder):
        shutil.rmtree(segment_folder)

    # Run models
    dice_type, dice_rolls = run_dice_type_dice_roll_models()

    # Print out what was detected including unreadable
    print("Detected")
    print(dice_type)
    print(dice_rolls)

    # Print out output filtering out unreadable results
    print("Output")
    total = 0
    for key, value in dice_rolls.items():
        if value != "Unreadable":
            print("Detected dice " + str(key) + " type " + dice_type[key] + " with roll " + value)
            total += int(value)

    print("Total: " + str(total))


# @TODO when done testing stop image from saving predictions of rolls
if __name__ == '__main__':
    run_models()
