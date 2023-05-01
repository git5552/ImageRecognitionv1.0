from ocr import OCRDetector
from baike_crawler import parse_baike
import re
import numpy as np
import streamlit as st
from io import BytesIO
from ocr import OCRDetector
from baike_crawler import parse_baike
import re
import numpy as np
import streamlit as st
from PIL import Image
import cv2
import time
from streamlit_cropper import st_cropper

ocr = OCRDetector()

class MyRandom:
    def __init__(self,num):
        self.random_num=num

def my_hash_func(my_random):
    num = my_random.random_num
    return num


def crop_image(image):
    rect = cv2.selectROI("选择截图区域", image, False)
    cropped_img = image[int(rect[1]):int(rect[1] + rect[3]), int(rect[0]):int(rect[0] + rect[2])]
    return cropped_img

# def crop_image(image):
#     rect = cv2.selectROI("选择截图区域", image, False)
#     cropped_img = image[int(rect[1]):int(rect[1] + rect[3]), int(rect[0]):int(rect[0] + rect[2])]
#     return cropped_img





st.set_option('deprecation.showfileUploaderEncoding', False)

# Upload an image and set some options for demo purposes
st.title('配料表识别v3.0')
uploaded_file = st.sidebar.file_uploader(label='上传配料表', type=['png', 'jpg', 'jpeg'])
realtime_update = st.sidebar.checkbox(label="是否实时更新", value=True)
box_color = st.sidebar.color_picker(label="选框颜色", value='#000000')

aspect_choice = st.sidebar.radio(label="纵横比", options=["1:1", "16:9", "自定义"])
aspect_dict = {
    "1:1": (1, 1),
    "16:9": (16, 9),
    "自定义": None
}
aspect_ratio = aspect_dict[aspect_choice]

return_type_choice = st.sidebar.radio(label="Return type", options=["图片裁剪", "自定义坐标"])
return_type_dict = {
    "图片裁剪": "image",
    "自定义坐标": "box"
}
return_type = return_type_dict[return_type_choice]

if uploaded_file:
    img = Image.open(uploaded_file)
    if not realtime_update:
        st.write("双击保存图片")
    if return_type == 'box':
        rect = st_cropper(
            img,
            realtime_update=realtime_update,
            box_color=box_color,
            aspect_ratio=aspect_ratio,
            return_type=return_type
        )
        raw_image = np.asarray(img).astype('uint8')
        left, top, width, height = tuple(map(int, rect.values()))
        st.write(rect)
        masked_image = np.zeros(raw_image.shape, dtype='uint8')
        masked_image[top:top + height, left:left + width] = raw_image[top:top + height, left:left + width]

        # Convert the masked image back to Image object and resize
        masked_image = Image.fromarray(masked_image)
        masked_image = masked_image.resize(img.size)

        st.image(masked_image, caption='裁剪后的图片')
    else:
        # Convert cropped image to numpy array and resize
        cropped_img = st_cropper(
            img,
            realtime_update=realtime_update,
            box_color=box_color,
            aspect_ratio=aspect_ratio,
            return_type=return_type
        )

        # Convert PIL Image to numpy array
        masked_image = np.array(cropped_img)

        # Convert numpy array to PIL Image
        masked_image = Image.fromarray(masked_image)

        # Resize masked_image
        _ = masked_image.thumbnail((500, 500))

        st.image(masked_image)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("裁剪后识别"):
            st.info('正在进行配料识别')
            # Convert PIL Image to byte buffer
            buffered = BytesIO()
            masked_image.save(buffered, format="PNG")
            bytes_data = buffered.getvalue()

            image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            image = cv2.resize(image, (500,500))
            ocr_pred = ocr.predict(image)
            items = []
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
                        time.sleep(2)

    with col2:
        # file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        # image = cv2.imdecode(file_bytes, 1)
        if st.button("原图识别"):
            bytes_data = uploaded_file.getvalue()
            # get image
            image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            image = cv2.resize(image, (500, 500))
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
                        time.sleep(2)




