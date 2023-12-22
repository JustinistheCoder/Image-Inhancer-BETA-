import cv2
import numpy as np

def enhance_roi(roi, scale_factor):
    # Resize (enlarge) the ROI
    enlarged_roi = cv2.resize(roi, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

    lab = cv2.cvtColor(enlarged_roi, cv2.COLOR_BGR2Lab)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    enhanced_lab = cv2.merge((l, a, b))
    enhanced_roi = cv2.cvtColor(enhanced_lab, cv2.COLOR_Lab2BGR)

    alpha = 1.5
    beta = -0.5
    gamma = 0
    blurred = cv2.GaussianBlur(enhanced_roi, (0, 0), 3)
    sharpened_roi = cv2.addWeighted(enhanced_roi, alpha, blurred, beta, gamma)
    return sharpened_roi

def draw_rectangle(event, x, y, flags, param):
    global roi_coords, clone

    if event == cv2.EVENT_LBUTTONDOWN:
        roi_coords = [(x, y)]

    elif event == cv2.EVENT_LBUTTONUP:
        roi_coords.append((x, y))
        cv2.rectangle(clone, roi_coords[0], roi_coords[1], (0, 255, 0), 2)
        cv2.imshow("Image", clone)

image_path = 'testmk2.jpg'  # Use the path 
image = cv2.imread(image_path)
clone = image.copy()
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", draw_rectangle)

while True:
    cv2.imshow("Image", clone)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("r"):  # Reset 
        clone = image.copy()
    elif key == ord("c"):  # Confirm 
        break

if len(roi_coords) == 2:
    x1, y1 = roi_coords[0]
    x2, y2 = roi_coords[1]
    roi = image[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]
    
    scale_factor = 2  # size

    enhanced_roi = enhance_roi(roi, scale_factor)

    cv2.imshow('Your picture but better', enhanced_roi)
    cv2.waitKey(0)
    cv2.imwrite('/mnt/data/enhanced_enlarged_roi_image.jpg', enhanced_roi)

cv2.destroyAllWindows()
