

from ocr import OCRDetector
from baike_crawler import parse_baike
import re

import numpy as np

import streamlit as st


from ocr import OCRDetector
from baike_crawler import parse_baike
import re
import numpy as np
import streamlit as st

import cv2
import time


ocr = OCRDetector()





class MyRandom:
    def __init__(self,num):
        self.random_num=num

def my_hash_func(my_random):
    num = my_random.random_num
    return num



st.title('配料表识别v3.0')
uploaded_file = st.file_uploader("上传配料表", ['png', 'jpg', 'jpeg'])


if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
     # get image
    image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    image = cv2.resize(image, (500, 500))
    st.title("原始图片")
    st.image(image, channels="BGR")

    col1, col2 = st.columns(2)
    with col1:

        if st.button("图片裁剪"):
            cv2.destroyAllWindows()
            rect = cv2.selectROI("选择截图区域", image, False)
            cropped_img = image[int(rect[1]):int(rect[1] + rect[3]), int(rect[0]):int(rect[0] + rect[2])]
            st.image(cropped_img, channels="BGR")
            st.info('正在进行OCR识别')
            try:
                # ocr识别配料表中
                ocr_pred = ocr.predict(cropped_img)
            except Exception as e:
                st.error(f"发生错误: {e}")
            else:
                # 返回结果为空，则未识别
                if not ocr_pred:
                    st.warning('未识别出配料表，请重新上传')
                else:
                    # 抓取配料信息
                    items = re.split('，|、|,|、', ocr_pred)

                    for k in items:
                        if k.startswith("添加量") or k.startswith("非"):
                            items.remove(k)

                    print("===>>>>", items)
                st.success(f'识别出 {len(items)} 种配料，准备爬取详细信息')

                for i, item in enumerate(items):
                    sub_title, desc = parse_baike(item)
                    st.subheader(item)
                    st.text(sub_title)
                    if desc == '':
                        st.caption('无详细信息')
                    else:
                        # 正则优化
                        desc = desc.replace('防腐剂', '<font color="#FF0000">防腐剂</font>')
                        desc = desc.replace('防腐', '<font color="#FF0000">防腐</font>')
                        desc = desc.replace('甜味剂', '<font color="#FF0000">甜味剂</font>')
                        desc = desc.replace('着色剂', '<font color="#FF0000">着色剂</font>')
                        desc = desc.replace('食品添加剂', '<font color="#FF0000">食品添加剂</font>')
                        desc = desc.replace('增稠剂', '<font color="#FF0000">增稠剂</font>')
                        desc = desc.replace('剂', '<font color="#FF0000">剂</font>')
                        st.caption(desc, unsafe_allow_html=True)
                    with st.spinner(f'配料爬取中，已完成 {i+1}/{len(items)}'):
                        time.sleep(5)

    with col2:
     if st.button("图片识别"):
            ocr_pred = ocr.predict(image)
            # 返回结果为空，则未识别
            if not ocr_pred:
                st.warning('未识别出配料表，请重新上传')
            else:
                # 抓取配料信息
                items = re.split('，|、|,|、', ocr_pred)

                for k in items:
                    if k.startswith("添加量") or k.startswith("非"):
                        items.remove(k)

                print("===>>>>", items)
            st.success(f'识别出 {len(items)} 种配料，准备爬取详细信息')

            for i, item in enumerate(items):
                sub_title, desc = parse_baike(item)
                st.subheader(item)
                st.text(sub_title)
                if desc == '':
                    st.caption('无详细信息')
                else:
                    # 正则优化
                    desc = desc.replace('防腐剂', '<font color="#FF0000">防腐剂</font>')
                    desc = desc.replace('防腐', '<font color="#FF0000">防腐</font>')
                    desc = desc.replace('甜味剂', '<font color="#FF0000">甜味剂</font>')
                    desc = desc.replace('着色剂', '<font color="#FF0000">着色剂</font>')
                    desc = desc.replace('食品添加剂', '<font color="#FF0000">食品添加剂</font>')
                    desc = desc.replace('增稠剂', '<font color="#FF0000">增稠剂</font>')
                    desc = desc.replace('剂', '<font color="#FF0000">剂</font>')
                    st.caption(desc, unsafe_allow_html=True)
                with st.spinner(f'配料爬取中，已完成 {i + 1}/{len(items)}'):
                    time.sleep(5)




