from tkinter import *
from tkinter import filedialog

from PIL import ImageTk, Image

from tools import *

root = Tk()
root.title("KitiK")
root.geometry("800x600")
# root.resizable(width=False, height=False)

current_image, new_image = "", ""


def donothing():
    filewin = Toplevel(root)
    button = Button(filewin, text="Do nothing button")
    button.pack()


def open_image():
    global label
    global current_image
    global opened_image

    new_image = filedialog.askopenfilename(initialdir="~/Pictures", title="Open image",
                                           filetypes=(("JPG files", "*.jpg"), ("PNG files", "*.png")))
    root.title("{} - AIVO".format(new_image.split("/")[-1]))
    current_image = new_image
    opened_image = current_image
    image = ImageTk.PhotoImage(Image.open(new_image))

    label.pack_forget()
    label = Label(image=image, anchor=CENTER)
    label.image = image
    label.pack()


def rotate_an_image(direction):
    global label
    global current_image
    global opened_image

    angle = 90

    if direction == "RIGHT":
        angle *= -1

    new_image = rotate(cv2.imread(opened_image), angle)
    current_image = new_image
    image = ImageTk.PhotoImage(Image.fromarray(new_image))

    label.pack_forget()
    label = Label(image=image, anchor=CENTER)
    label.image = image
    label.pack()


def convert_image_to_gray():
    global label
    global current_image
    global opened_image

    new_image = rgb_to_gray(cv2.imread(opened_image))
    current_image = new_image
    image = ImageTk.PhotoImage(Image.fromarray(new_image))

    label.pack_forget()
    label = Label(image=image, anchor=CENTER)
    label.image = image
    label.pack()


def convert_image_to_binary_image():
    global label
    global current_image
    global opened_image

    new_image = binarize(cv2.imread(opened_image), 128)
    current_image = new_image
    image = ImageTk.PhotoImage(Image.fromarray(new_image))

    label.pack_forget()
    label = Label(image=image, anchor=CENTER)
    label.image = image
    label.pack()


def convert_image_to_inversed_image():
    global label
    global current_image
    global opened_image

    new_image = inverse(cv2.imread(opened_image))
    current_image = new_image
    image = ImageTk.PhotoImage(Image.fromarray(new_image))

    label.pack_forget()
    label = Label(image=image, anchor=CENTER)
    label.image = image
    label.pack()


def adjust_image_contraste():
    global label
    global current_image
    global opened_image

    new_image = equalize_histogram(cv2.imread(opened_image))
    current_image = new_image
    image = ImageTk.PhotoImage(Image.fromarray(new_image))

    label.pack_forget()
    label = Label(image=image, anchor=CENTER)
    label.image = image
    label.pack()


def adjust_image_luminosity():
    global label
    global current_image
    global opened_image

    new_image = stretch_histogram(cv2.imread(opened_image), 64, 192)
    current_image = new_image
    image = ImageTk.PhotoImage(Image.fromarray(new_image))

    label.pack_forget()
    label = Label(image=image, anchor=CENTER)
    label.image = image
    label.pack()


def blur_an_image():
    global label
    global current_image
    global opened_image

    new_image = blur(cv2.imread(opened_image))
    current_image = new_image
    image = ImageTk.PhotoImage(Image.fromarray(new_image))

    label.pack_forget()
    label = Label(image=image, anchor=CENTER)
    label.image = image
    label.pack()


def extract_edge_on_image():
    global label
    global current_image
    global opened_image

    new_image = detect_edge(cv2.imread(opened_image))
    currentImage = new_image
    image = ImageTk.PhotoImage(Image.fromarray(new_image))

    label.pack_forget()
    label = Label(image=image, anchor=CENTER)
    label.image = image
    label.pack()


def opening_morph_trans_on_image():
    global label
    global current_image
    global opened_image

    new_image = opening(cv2.imread(opened_image))
    current_image = new_image
    image = ImageTk.PhotoImage(Image.fromarray(new_image))

    label.pack_forget()
    label = Label(image=image, anchor=CENTER)
    label.image = image
    label.pack()


def closing_morph_trans_on_image():
    global label
    global current_image
    global opened_image

    new_image = closing(cv2.imread(opened_image))
    current_image = new_image
    image = ImageTk.PhotoImage(Image.fromarray(new_image))

    label.pack_forget()
    label = Label(image=image, anchor=CENTER)
    label.image = image
    label.pack()


def oth_morph_trans_on_image():
    global label
    global current_image
    global opened_image

    new_image = opening_top_hat(cv2.imread(opened_image))
    current_image = new_image
    image = ImageTk.PhotoImage(Image.fromarray(new_image))

    label.pack_forget()
    label = Label(image=image, anchor=CENTER)
    label.image = image
    label.pack()


def cth_morph_trans_on_image():
    global label
    global current_image
    global opened_image

    new_image = closing_top_hat(cv2.imread(opened_image))
    current_image = new_image
    image = ImageTk.PhotoImage(Image.fromarray(new_image))

    label.pack_forget()
    label = Label(image=image, anchor=CENTER)
    label.image = image
    label.pack()


def show_histogram():
    global opened_image

    histogram = compute_histogram(cv2.imread(opened_image))
    plt.plot(histogram)
    plt.xlabel('Gray level')
    plt.ylabel('Count')
    plt.title("Histogram of the image in gray level")
    plt.show()


def save_image():
    global current_image

    if current_image:
        # imageName = currentImage.split("/")[-1]
        image_name = current_image
        cv2.imwrite(image_name, current_image)
    else:
        save_as_image()


def save_as_image():
    global current_image

    image_name = filedialog.asksaveasfilename(defaultextension=".png", initialdir="~/Pictures/", title="Save an image", filetypes=(("PNG files", "*.png"), ("JPG files", "*.jpg")))

    if image_name:
        # imageName = imageName.split("/")[-1]
        cv2.imwrite(image_name, current_image)
        root.title("{} - AIVO".format(image_name.split("/")[-1]))


def close_image():
    global label
    label.pack_forget()
    label = Label(text="Select an image...", anchor=CENTER)
    label.pack()


menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=open_image)
filemenu.add_command(label="Save", command=save_image)
filemenu.add_command(label="Save as", command=save_as_image)
filemenu.add_command(label="Close", command=close_image)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)
editmenu.add_command(label="Redo", command=donothing)

menubar.add_cascade(label="Edit", menu=editmenu)

imagemenu = Menu(menubar, tearoff=0)
imagemenu.add_command(label="Flip Horizontally", command=donothing)
imagemenu.add_command(label="Flip Vertically", command=donothing)
imagemenu.add_command(label="Rotate Right", command=lambda: rotate_an_image("RIGHT"))
imagemenu.add_command(label="Rotate Left", command=lambda: rotate_an_image("LEFT"))
imagemenu.add_command(label="Adjust contraste", command=adjust_image_contraste)
imagemenu.add_command(label="Adjust luminosity", command=adjust_image_luminosity)
imagemenu.add_command(label="Gray color", command=convert_image_to_gray)
imagemenu.add_command(label="BW color", command=convert_image_to_binary_image)
imagemenu.add_command(label="Negative color", command=convert_image_to_inversed_image)
imagemenu.add_command(label="Blur image", command=blur_an_image)
imagemenu.add_command(label="Edge detect", command=extract_edge_on_image)
imagemenu.add_command(label="Morph Trans Opening", command=opening_morph_trans_on_image)
imagemenu.add_command(label="Morph Trans Closing", command=closing_morph_trans_on_image)
imagemenu.add_command(label="Morph Trans OTH", command=oth_morph_trans_on_image)
imagemenu.add_command(label="Morph Trans CTH", command=cth_morph_trans_on_image)
imagemenu.add_command(label="Voir l'histogramme", command=show_histogram)

menubar.add_cascade(label="Image", menu=imagemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=donothing)
helpmenu.add_command(label="About", command=donothing)

menubar.add_cascade(label="Help", menu=helpmenu)

label = Label(root, text="Select an image...", anchor=CENTER)
label.pack()

root.config(menu=menubar)
root.mainloop()
