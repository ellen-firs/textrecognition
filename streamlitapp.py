from PIL import Image
import streamlit as st
import os
import easyocr
import cv2

def save_uploaded_file(uploaded_file):
    try:
        with open(os.path.join(uploaded_file.name), 'wb') as f:
            f.write(uploaded_file.getbuffer())
        return 1
    except:
        return 0


def text_recognition():
    uploaded_file = st.sidebar.file_uploader('')
    if uploaded_file is not None:
        if save_uploaded_file(uploaded_file):
            if (st.sidebar.button('Распознавание')):
                display_image = Image.open(uploaded_file)
                reader = easyocr.Reader(["ru", "en"])
                result = reader.readtext(uploaded_file.name, detail=0, paragraph=True)
                col1, col2 = st.columns((1, 1))
                with col1:
                    st.info('Загруженное изображение:')
                    st.image(display_image)
                with col2:
                    st.success('Распознанный текст:')
                    st.write(result)

def carplate_recognition():
    carplate_haar_cascade = cv2.CascadeClassifier('haar_cascades/haarcascade_russian_plate_number.xml')
    uploaded_file = st.sidebar.file_uploader('')
    if uploaded_file is not None:
        if save_uploaded_file(uploaded_file):
            if (st.sidebar.button('Распознавание')):
                display_image = Image.open(uploaded_file)
                reader = easyocr.Reader(["en"])
                carplate_img = cv2.cvtColor(cv2.imread(uploaded_file.name), cv2.COLOR_BGR2RGB)
                carplate_rects = carplate_haar_cascade.detectMultiScale(carplate_img, scaleFactor=1.1, minNeighbors=5)
                for x, y, w, h in carplate_rects:
                    carplate_img = carplate_img[y + 15:y + h - 10, x + 15:x + w - 20]
                width = int(carplate_img.shape[1] * 150 / 100)
                height = int(carplate_img.shape[0] * 150 / 100)
                dim = (width, height)
                resized_image = cv2.resize(carplate_img, dim, interpolation=cv2.INTER_AREA)
                carplate_extract_img_gray = cv2.cvtColor(resized_image, cv2.COLOR_RGB2GRAY)
                reader.readtext(carplate_extract_img_gray, detail=0, paragraph=True, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                col1, col2, col3 = st.columns((1, 1, 1))
                with col1:
                    st.info('Загруженное изображение:')
                    st.image(display_image)
                with col2:
                    st.info('Автомобильный номер:')
                    st.image(resized_image)
                with col3:
                    st.success('Распознанный текст:')
                    st.write(result)




def main():
    st.set_page_config(page_title='Текст с изображения', layout='wide')
    st.title("Работа №1")
    st.sidebar.title('Режимы работы')
    choose = st.sidebar.selectbox("Выберите необходимую операцию", ("Выбрать...",
                                     "1. Распознавание текста с изображения",
                                     "2. Распознавание автомобильных номеров"))

    st.sidebar.title('Загрузка изображения')
    if choose == "1. Распознавание текста с изображения":
        text_recognition()
    elif choose == "2. Распознавание автомобильных номеров":
        carplate_recognition()

if __name__ == '__main__':
    main()
