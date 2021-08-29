import tkinter as tk
from tkinter import ttk  
from PIL import Image, ImageTk, ImageGrab, ImageEnhance
import pytesseract
from ctypes import windll
user32 = windll.user32
user32.SetProcessDPIAware()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
root = tk.Tk()
root.title("ImgtoText")
root.resizable(0, 0)



def copy_to_clipboard(win, text):
    win.clipboard_clear()
    win.clipboard_append(text)


def get_text_from_img(img):
    return pytesseract.image_to_string(img)


def show_image(image):


    #show the img
    img_win = tk.Toplevel()
    img_win.image = ImageTk.PhotoImage(image)
    tk.Label(img_win, image=img_win.image).pack()

    # #activity indicator
    # progress = ttk.Progressbar(img_win,orient='horizontal',mode="indeterminate")
    # progress.pack()            
    
    user_text_toprint = get_text_from_img(img=image)
    
    #text obtained, remove the progress bar(?) and display the text

    text_label_win = tk.Text(img_win) 
    text_label_win.insert(1.0, user_text_toprint)#insert the text
    text_label_win.pack()

    img_win.grab_set()


def area_sel():
    x1 = y1 = x2 = y2 = 0
    roi_image = None

    def on_mouse_down(event):
        nonlocal x1, y1
        x1, y1 = event.x, event.y
        canvas.create_rectangle(x1, y1, x1, y1, outline='red', tag='roi')

    def on_mouse_move(event):
        nonlocal roi_image, x2, y2
        x2, y2 = event.x, event.y
        canvas.delete('roi-image') # remove old overlay image
        roi_image = image.crop((x1, y1, x2, y2)) # get the image of selected region
        canvas.image = ImageTk.PhotoImage(roi_image)
        canvas.create_image(x1, y1, image=canvas.image, tag=('roi-image'), anchor='nw')
        canvas.coords('roi', x1, y1, x2, y2)
        # make sure the select rectangle is on top of the overlay image
        canvas.lift('roi') 

    root.withdraw()  # hide the root window
    image = ImageGrab.grab()  # grab the fullscreen as select region background
    bgimage = ImageEnhance.Brightness(image).enhance(0.3)  # darken the capture image
    # create a fullscreen window to perform the select region action
    win = tk.Toplevel()
    win.attributes('-fullscreen', 1)
    win.attributes('-topmost', 1)
    canvas = tk.Canvas(win, highlightthickness=0)
    canvas.pack(fill='both', expand=1)
    tkimage = ImageTk.PhotoImage(bgimage)
    canvas.create_image(0, 0, image=tkimage, anchor='nw', tag='images')
    # bind the mouse events for selecting region
    win.bind('<ButtonPress-1>', on_mouse_down)
    win.bind('<B1-Motion>', on_mouse_move)
    win.bind('<ButtonRelease-1>', lambda e: win.destroy())
    # use Esc key to abort the capture
    win.bind('<Escape>', lambda e: win.destroy())
    # make the capture window modal
    win.focus_force()
    win.grab_set()
    win.wait_window(win)
    root.deiconify()  # restore root window
    # show the capture image
    if roi_image:
        show_image(roi_image)

tk.Button(root, text='点击此处选择区域', width=30, command=area_sel).pack()

root.mainloop()