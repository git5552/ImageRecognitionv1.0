import  os,cv2

from ocr import OCRDetector

ocr = OCRDetector()
cv2_img = cv2.imread('./1.png')
# ocr识别配料表中
ocr_pred = ocr.predict(cv2_img)
print(ocr_pred)