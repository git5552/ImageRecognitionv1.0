import numpy as np
import streamlit as st
import cv2
from ocr import OCRDetector
from baike_crawler import parse_baike
import re

import numpy as np
import pandas as pd
import streamlit as st

import cv2
import time
import matplotlib.pyplot as plt

ocr = OCRDetector()
st.title('配料表识别v1.0')
uploaded_file = st.file_uploader("上传配料表", ['png', 'jpg', 'jpeg'])
if uploaded_file is not None:


    bytes_data = uploaded_file.getvalue()
    # get image
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    # deal image
    st.image(uploaded_file)
    # ocr识别配料表中
    ocr_pred = ocr.predict(cv2_img)
    # 返回结果为空，则未识别
    if not ocr_pred:
        st.warning('未识别出配料表，请重新上传')
    else:
        # 抓取配料信息
        items = re.split('，|、|,|、', ocr_pred)

        for k  in items:
           if k.startswith("添加量") or k.startswith("非") :
              items.remove(k)


        print("===",items)
        st.success(f'识别出 {len(items)} 种配料，准备爬取详细信息')
        for i, item in enumerate(items):



            sub_title, desc = parse_baike(item)

            st.subheader(item)
            st.text(sub_title)
            if desc == '':
                st.caption('无详细信息')
            else:
                # 偷个懒， 后面可以用正则优化
                desc = desc.replace('防腐剂', '<font color="#FF0000">防腐剂</font>')
                desc = desc.replace('防腐', '<font color="#FF0000">防腐</font>')
                desc = desc.replace('甜味剂', '<font color="#FF0000">甜味剂</font>')
                desc = desc.replace('着色剂', '<font color="#FF0000">着色剂</font>')
                desc = desc.replace('食品添加剂', '<font color="#FF0000">食品添加剂</font>')
                desc = desc.replace('增稠剂', '<font color="#FF0000">增稠剂</font>')
                desc = desc.replace('剂', '<font color="#FF0000">剂</font>')
                st.caption(desc, unsafe_allow_html=True)
            with st.spinner(f'配料爬取中，已完成 {i+1}/{len(items)}'):
                time.sleep(3)



class MyRandom:
    def __init__(self,num):
        self.random_num=num

def my_hash_func(my_random):
    num = my_random.random_num
    return num


