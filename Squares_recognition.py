import math
import cv2
import pytesseract
from os import remove
from tkinter import messagebox


def take_picture():
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Binary photo", frame)

        k = cv2.waitKey(1)
        if k % 256 == 32:
            img_name = "Binary.png"
            cv2.imwrite(img_name, frame)
            cv2.destroyAllWindows()
            return img_name


def draw_squares(img_path):
    img = cv2.imread(img_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray_img, 127, 255, 1)

    contours, h = cv2.findContours(thresh, 1, 2)
    coords = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 8000 > area > 1500:
            x, y, w, h = cv2.boundingRect(cnt)
            small_square = img[y + 3:y + h - 3, x + 3:x + h - 3]
            coords.append((x, y))
            cv2.drawContours(img, [cnt], 0, (0, 0, 255), 1)
            gray = cv2.cvtColor(small_square, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3, 3), 0)
            thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
            invert = 255 - opening
            cv2.imwrite('ROI_{}.png'.format((x, y)), invert)

    cv2.imshow('the board', img)
    answer = messagebox.askquestion(title="Binary solver", message="Do you want to take a new picture?")
    if answer == "no":
        cv2.destroyAllWindows()
        return coords
    elif answer == "yes":
        cv2.destroyAllWindows()
        remove_photos(coords)
        return None


def remove_photos(coords):
    for co in coords:
        remove('ROI_{}.png'.format(co))


def recog(co):
    end = []
    row = []
    nb_rows = int(math.sqrt(len(co)))
    # coordinate sorting sco = sorted coordinates
    sco = sorted(co, key=lambda x: x[1])
    for i in range(nb_rows):
        i = i * nb_rows
        j = i + nb_rows
        sco[i:j] = sorted(sco[i:j], key=lambda x: x[0])
    co = sco

    for i in range(len(co)):
        c = co[i]
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        text = pytesseract.image_to_string('ROI_{}.png'.format(c), config='--psm 10 -c tessedit_char_whitelist=01')
        if text == '1':
            row.append(1)
        elif text == "0":
            row.append(0)
        else:
            row.append('')
        if (i + 1) % nb_rows == 0:
            end.append(row)
            row = []
    remove_photos(co)
    return end


def binary_photo():
    co = None
    while co is None:
        img_name = take_picture()
        co = draw_squares(img_name)
    grid = recog(co)
    return grid
