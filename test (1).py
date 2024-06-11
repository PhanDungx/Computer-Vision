import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def open_file():
    global img, original_img
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
        img = resize_image(img, max_height=500)
        original_img = img.copy()  # Sao lưu ảnh gốc
        show_image(img)

def show_image(image):
    global img_id, img_tk # Sử dụng img_tk là biến toàn cục để tránh bị thu gom
    img_pil = Image.fromarray(image)
    img_tk = ImageTk.PhotoImage(img_pil)
    canvas.delete(img_id)
    img_id = canvas.create_image(0, 0, anchor=tk.NW, image=img_tk) #Northwest: góc bắc phía tây
    canvas.config(scrollregion=canvas.bbox(tk.ALL)) #cập nhật kích thước cuộn   
    
def resize_image(image, max_height=400):
    h, w = image.shape[:2]
    ratio = max_height / h
    return cv2.resize(image, (int(w * ratio), int(h * ratio)))

def rotate_image():
    global img
    if img is not None:
        try:
            angle = float(angle_entry.get())
        except ValueError:
            return
        h, w = img.shape[:2]    
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        img = cv2.warpAffine(img, matrix, (w, h), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_REPLICATE)
        show_image(img)

def reset_image():
    global img, original_img
    img = original_img.copy()  # Sử dụng ảnh gốc
    show_image(img)

def distortion_image():
    global img
    if img is not None:
        try:
            x = float(horizontal_entry.get())
            y = float(vertical_entry.get())
        except ValueError:
            return
        img = cv2.resize(img, None, fx=x, fy=y, interpolation=cv2.INTER_LINEAR)
        show_image(img)

def zoom_in():
    global img
    if img is not None:
        try:
            factor = float(zoom_entry.get())
        except ValueError:
            return
        img = cv2.resize(img, None, fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC)
        show_image(img)

root = tk.Tk()
root.title("Ứng dụng Biến đổi Ảnh")
root.geometry("700x600")

canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#thanh cuộn ngang
scrollbar_x = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

canvas.configure(xscrollcommand=scrollbar_x.set)

#thanh cuộn dọc
canvas.configure(yscrollcommand=scrollbar.set)

# Kích thước canvas có thể điều chỉnh tự do
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

open_button = tk.Button(root, text="Mở Ảnh", command=open_file, bg="skyblue", fg="white", font=("Calibri", 15, "bold"))
open_button.pack(pady=20)

# Nhập góc xoay
angle_label = tk.Label(root, text="Nhập góc xoay:", bg="lightgray", font=("Calibri", 15, "bold"))
angle_label.pack(pady=5)
angle_entry = tk.Entry(root, font=("Calibri", 15))
angle_entry.pack(pady=5)

rotate_button = tk.Button(root, text="Xoay Ảnh", command=rotate_image, bg="purple", fg="white", font=("Calibri", 15, "bold"))
rotate_button.pack(pady=5)

distortion_label = tk.Label(root, text="Nhập tỉ lệ bóp méo:", bg="lightgray", font=("Calibri", 15, "bold"))
distortion_label.pack(pady=5)
horizontal_entry = tk.Entry(root, font=("Calibri", 15))
horizontal_entry.pack(pady=5)
vertical_entry = tk.Entry(root, font=("Calibri", 15))
vertical_entry.pack(pady=5)

transform_button = tk.Button(root, text="Bóp méo ảnh", command=distortion_image, bg="orange", fg="white", font=("Calibri", 15, "bold"))
transform_button.pack(pady=5)

zoom_label = tk.Label(root, text="Nhập độ phóng:", bg="lightgray", font=("Calibri", 15, "bold"))
zoom_label.pack(pady=5)
zoom_entry = tk.Entry(root, font=("Calibri", 15))
zoom_entry.pack(pady=5)

zoom_in_button = tk.Button(root, text="Phóng to ảnh", command=zoom_in, bg="blue", fg="white", font=("Calibri", 15, "bold"))
zoom_in_button.pack(pady=5)

reset_button = tk.Button(root, text="Reset Ảnh", command=reset_image, bg="green", fg="white", font=("Calibri", 15, "bold"))
reset_button.pack(pady=20)

img_id = None      # ID của ảnh hiện tại trên canvas
img = None         # Ảnh hiện tại
original_img = None  # Ảnh gốc

root.mainloop()
