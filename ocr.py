from paddleocr import PaddleOCR


<<<<<<< HEAD



=======
>>>>>>> 8b0d0e4 (4/30)
#创建OCRDetector类，将OCR检测和识别的功能封装
class OCRDetector:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=False,
                             lang="ch",
                             use_gpu=False,
                            rec_model_dir = './models/ch_rec_infer/',
                            cls_model_dir = './models/ch_cls_infer/',
                            det_model_dir = './models/ch_det_infer/')


    def predict(self, img):

        result = self.ocr.ocr(img, cls=True)

        max_line = 5
        ingredients = []
        line_is_valid = False
        # print(result)
        for line in result:
            # print(line)
            for i in line:
                # print(i)
                text = i[1][0] # 获取识别出来的文本
                # print(text)  配料：生牛乳，燕麦粒浓浆，聚葡萄糖，木糖醇，乳

                # 麦芽糖浆，乳粉（添加量≥4.5%），麦芽糊精，果葡糖浆，浓缩枣汁（添加量≥0.6%）单双甘油脂肪酸酯，羧甲基纤维素钠
                # 麦芽糖浆，乳粉，麦芽糊精，果葡糖浆，浓缩枣汁,单双甘油脂肪酸酯，羧甲基纤维素钠


                if text.startswith("配料：") or text.startswith("配料表：") or  text.startswith("产品配料："):
                    line_is_valid = True
                    text = text.replace('配料：', '')
                    text = text.replace('配料表：', '')


                #读取连续的 max_line 行
                if line_is_valid :
                    ingredients.append(text)
                    if len(ingredients) >= max_line or text.endswith('。'):
                        break

        # 多行配料合成1行
        res = ''.join(ingredients)
        res = res.replace('。', '').replace('（',' ').replace(' ','，').replace('）','').replace('%',"%，")

        print(res)
        return res
<<<<<<< HEAD
=======

>>>>>>> 8b0d0e4 (4/30)
