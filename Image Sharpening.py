import cv2
image = cv2.imread("test image.jpg") # input your image in text brackets
if image is None:
    print("Image did not load properly")
    exit()
gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY )  
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)  
Sharp_image = cv2.addWeighted(gray_image, 1.5, blurred_image, -0,5, 0)
cv2.imwrite('sharp_image.jpg', Sharp_image)
cv2.imshow('Sharp_image.jpg', Sharp_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
