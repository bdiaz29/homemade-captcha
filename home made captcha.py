from tkinter import *
import PIL
from PIL import Image, ImageGrab, ImageTk
import numpy as np
from tkinter import filedialog
import os.path
from os import path
import xlwt
from tkinter import messagebox
from tensorflow.keras.preprocessing.image import ImageDataGenerator

wb = xlwt.Workbook()
ws = wb.add_sheet('data')

file_list = [None]
destination = "destination"
source = "source"
filepath = "1.jpg"
name = ""
counter = 0
counter2 = 0
counter3=0
image_from_file = np.zeros((240, 320, 3))
image_zoomed = np.zeros((240, 320, 3))
datagen = ImageDataGenerator()
datagen2=ImageDataGenerator()

picture_panel = [Label] * 25
blank = np.uint8(np.zeros((240, 320, 3)))
activated = [int] * 25
tkimg2 = [None] * 25
count = 0
for x in range(5):
    for y in range(5):
        activated[count] = 0
        count = count + 1


def split_images(array):
    temp = np.zeros((5, 5, 48, 64, 3))

    for x in range(5):
        for y in range(5):
            offsetx = x * 64
            offsety = y * 48
            temp[x, y] = array[offsety:offsety + 48, offsetx:offsetx + 64]

    temp = np.uint8(temp)
    return temp


def assign_source():
    global source
    global file_list
    global counter
    source = filedialog.askdirectory() + "/"
    file_list = os.listdir(source)
    #file_list = list_files1(source)
    counter = int(start_txt.get())
    load_image_file(source + file_list[counter])
    update_images()
    zoom_image()
    name_txt.configure(state="disabled")
    start_txt.configure(state="disabled")
    update_all()



def done(event):
    wb.save(destination + "/dataSet" + name + "_" + ".xls")
    messagebox.showinfo("goodbye", "datset is done")
    root.destroy()


def save_load_next():
    save()
    load_next()


def save_load_next2(event):
    save_load_next()


def load_next2(event):
    load_next()


def load_next():
    global counter
    global file_list
    counter = counter + 1

    P = source + "/" + file_list[counter]


    load_image_file(P)
    update_images()
    zoom_image()
    update_all()
    deselect_all()


def save():
    global source
    global file_list, image_from_file
    global counter, counter2, activated
    global ws
    save_shift()
    update_all()
    return
    counter2 = counter2 + 1
    im = np.uint8(image_from_file)
    im = Image.fromarray(im)
    im.save(destination + "/pictures/" + name + "_" + str(counter2) + ".jpeg")
    ws.write(counter2, 0, name + "_" + str(counter2) + ".jpeg")
    for i in range(1, 26):
        T=activated[i - 1]
        ws.write(counter2, i, str(T))
    save_shift()
    update_all()


def assign_destination():
    global destination, ws, wb
    global name
    name = name_txt.get()
    dest_String = filedialog.askdirectory()
    destination = dest_String + "/DataSet_" + name + "/"
    if not os.path.isdir(destination):
        os.mkdir(destination)
    if not os.path.isdir(destination + "pictures/"):
        os.mkdir(destination + "pictures/")

    if not os.path.isdir(destination + "pictures/0"):
        os.mkdir(destination + "pictures/0")

    if not os.path.isdir(destination + "pictures/1"):
        os.mkdir(destination + "pictures/1")


    ws.write(counter2, 0, "ID")
    for i in range(1, 26):
        ws.write(0, i, "x" + str(i))
    update_all()


def update_all():
    global destination, source, file_list, counter, counter2
    destination_lbl.configure(text=str(destination))
    so = str(source) + str(file_list[counter])
    source_lbl.configure(text=so)
    counter_lbl.configure(text=str(counter2))


def update_images():
    global tkimg2
    global image_from_file
    global picture_panel
    # im=split_images(image_from_file)
    im = split_images(image_from_file)
    count = 0

    for x in range(5):
        for y in range(5):
            tkimg2[count] = ImageTk.PhotoImage(Image.fromarray(np.uint8(im[x, y])))
            count = count + 1

    count = 0
    for x1 in range(5):
        for y1 in range(5):
            picture_panel[count].configure(image=tkimg2[count])
            picture_panel[count].image = tkimg2[count]
            count = count + 1

    zoom_image()


def on_click(event):
    global activated
    W = event.widget._name
    x = int(W[0])
    y = int(W[2])
    st = W[4:6]
    count = int(W[4:7]) - 100
    picture_panel[count].configure(background="red")
    activated[count] = 1
    detect_size()
    zoom_image()


def right_click(event):
    global activated

    W = event.widget._name
    x = int(W[0])
    y = int(W[2])
    st = W[4:6]
    count = int(W[4:7]) - 100
    activated[count] = 0
    detect_size()
    picture_panel[count].configure(background="white")
    zoom_image()


def reset():
    global activated
    count = 0
    for x in range(5):
        for y in range(5):
            activated[count] = 1


def load_image_file(fpath):
    global image_from_file, tk_img, tkimg2
    global counter
    img_data = PIL.Image.open(fpath)
    img_d=img_data.resize((320, 240))
    img_arr = np.array(img_d)


    if np.shape(img_arr) != ((240, 320, 3)):
        messagebox.showinfo("error", "bad dimension ")
        counter = counter + 1
        return
    image_from_file = np.uint8(img_arr)
    im = split_images(image_from_file)
    count = 0
    for x in range(5):
        for y in range(5):
            tkimg2[count] = ImageTk.PhotoImage(Image.fromarray(im[x, y]))
            count = count + 1


def detect_size():
    global activated
    temp2 = np.zeros((2, 5, 5))
    size = np.array((0, 0, 0, 0))
    size.astype(int)
    A = 0
    B = 0
    C = 0
    D = 0

    first = np.full((5), 5)
    second = np.full((5), 5)
    third = np.full((5), 5)
    fourth = np.full((5), 5)
    arr = np.zeros((5, 5))

    arr = np.reshape(activated, (5, 5))
    arr3 = np.fliplr(arr)
    arr2 = np.flipud(arr)
    count = 0
    for y in range(5):
        for x in range(5):
            p = 1
            if arr[x, y] == 1:
                first[y] = x
                break
            if x == 4 and arr[x, y] == 0:
                first[y] = 5
    A = np.min(first)

    count = 0
    for x in range(5):
        for y in range(5):
            if arr[x, y] == 1:
                second[x] = y
                break
            if y == 4 and arr[x, y] == 0:
                second[x] = 5
    B = np.min(second)

    for y in range(5):
        for x in range(5):
            p = 1
            if arr2[x, y] == 1:
                third[y] = x
                break
            if x == 4 and arr2[x, y] == 0:
                third[y] = 5
    C = 5 - np.min(third)

    for x in range(5):
        for y in range(5):
            if arr3[x, y] == 1:
                fourth[x] = y
                break
            if y == 4 and arr2[x, y] == 0:
                fourth[x] = 5
    D = 5 - np.min(fourth)

    size[0] = abs(A * 64)
    size[1] = abs(C * 64)
    size[2] = abs(B * 48)
    size[3] = abs(D * 48)

    # print(str(size))

    return size


def zoom_image():
    global image_from_file
    global image_zoomed
    para = detect_size()
    x1 = min(para[1], para[0])
    x2 = max(para[1], para[0])
    y1 = min(para[2], para[3])
    y2 = max(para[2], para[3])
    height = y2 - y1
    width = x2 - x1
    # print(y1,y2,x1,x2)
    extracted = image_from_file[y1:y2, x1:x2]
    extracted = np.uint8(extracted)
    extracted2 = Image.fromarray(extracted)
    new_image = extracted2.resize((320, 240))
    image_zoomed = np.array(new_image)
    # scaled_im=scaled_resize(x1,x2,y1,y2,image_from_file)
    # image_zoomed=np.array(scaled_im)
    # scaled_im.resize((320,240))
    # new_image =ImageTk.PhotoImage(new_image)

    conv_img = Image.fromarray(image_zoomed)
    new_image = ImageTk.PhotoImage(conv_img)
    zoom_panel.configure(image=new_image)
    zoom_panel.image = new_image


def scaled_resize(x1, x2, y1, y2, arr):
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    if width == 320:
        im = np.uint8(arr)
        im = Image.fromarray(im)
        return im
    elif height == 240:
        im = np.uint8(arr)
        im = Image.fromarray(im)
        return im

    if width >= height:
        height = int(width * .75)
    else:
        width = int(height * 1.3333333)

    if x1 <= 160:
        if y1 <= 120:
            X1 = x1
            X2 = x1 + width
            Y1 = y1
            Y2 = y1 + height
            p = 0
        else:
            X1 = x1
            X2 = x1 + width
            Y1 = y1 - height
            Y2 = y1
            p = 1

    else:
        if y1 <= 120:
            X1 = x1 - width
            X2 = x1
            Y1 = y1
            Y2 = y1 + height
            p = 0
            p = 2
        else:
            X1 = x1 - width
            X2 = x1
            Y1 = y1 - height
            Y2 = y1
            p = 0
            p = 2
            p = 3
    im = arr[Y1:Y2, X1:X2]
    im = np.uint8(im)
    # print(im.shape)
    im = Image.fromarray(im)
    # print(X1,X2,Y1,Y2)
    newim = im.resize((320, 240))
    return newim


def pass_image():
    global image_from_file
    global image_zoomed
    image_from_file = image_zoomed
    update_images()
    deselect_all()


def deselect_all():
    global activated
    for i in range(25):
        activated[i] = 0
        picture_panel[i].configure(background="white")
    detect_size()
    zoom_image()


def select_all():
    global activated
    for i in range(25):
        activated[i] = 1
        picture_panel[i].configure(background="red")
    detect_size()
    zoom_image()


def detect_bounds():
    global activated
    # global ImageDataGenerator
    temp2 = np.zeros((2, 5, 5))
    size = np.array((0, 0, 0, 0))
    size.astype(int)
    A = 0
    B = 0
    C = 0
    D = 0

    first = np.full((5), 5)
    second = np.full((5), 5)
    third = np.full((5), 5)
    fourth = np.full((5), 5)
    arr = np.zeros((5, 5))

    arr = np.reshape(activated, (5, 5))
    arr3 = np.fliplr(arr)
    arr2 = np.flipud(arr)
    count = 0
    for y in range(5):
        for x in range(5):
            p = 1
            if arr[x, y] == 1:
                first[y] = x
                break
            if x == 4 and arr[x, y] == 0:
                first[y] = 5
    A = np.min(first)

    count = 0
    for x in range(5):
        for y in range(5):
            if arr[x, y] == 1:
                second[x] = y
                break
            if y == 4 and arr[x, y] == 0:
                second[x] = 5
    B = np.min(second)

    for y in range(5):
        for x in range(5):
            p = 1
            if arr2[x, y] == 1:
                third[y] = x
                break
            if x == 4 and arr2[x, y] == 0:
                third[y] = 5
    C = 5 - np.min(third)

    for x in range(5):
        for y in range(5):
            if arr3[x, y] == 1:
                fourth[x] = y
                break
            if y == 4 and arr2[x, y] == 0:
                fourth[x] = 5
    D = 5 - np.min(fourth)

    size[0] = abs(A)
    size[1] = abs(C)
    size[2] = abs(B)
    size[3] = abs(D)

    # print(str(size))

    return size


def save_shift():
    global image_from_file
    global activated,destination
    global counter2,name,counter3

    act_arr = np.reshape(activated, (5, 5))
    act_arr2=act_arr
    bounds = detect_bounds()

    if bounds[0]==5 and bounds[2]==5:
        return


    yiter = int(bounds[2] + (6-bounds[3]))
    xiter = int(bounds[0] + (6-bounds[1]))

    ydiff = int(abs(bounds[2] - bounds[3] - 1))
    xdiff = int(abs(bounds[0] - bounds[1] - 1))

    for y in range(yiter):
        for x in range(xiter):
            X = int((x-bounds[0])*-64)
            Y = int((y-bounds[2]) *-48)
            new_img = datagen.apply_transform(x=image_from_file,
                                              transform_parameters={'tx': Y, 'ty': X})
            act_arr2 = np.roll(act_arr, (x-bounds[0]), axis=1)
            act_arr2 = np.roll(act_arr2, (y-bounds[2]), axis=0)
            new_img=np.uint8(new_img)
            im=Image.fromarray(new_img)
            im.save(destination + "pictures/1/" + name + "_" + str(counter2) + ".jpeg")
            counter2 = counter2 + 1
            ws.write(counter2, 0, name + "_" + str(counter2) + ".jpeg")
            act_arr3=np.reshape(act_arr2,(25))
            for xl in range(1, 26):
                T = act_arr3[xl - 1]
                ws.write(counter2, xl, str(T))

    for y in range(yiter):
        for x in range(xiter):
            X = int((x-bounds[0])*-64)
            Y = int((y-bounds[2]) *-48)
            blocked = blocked_out(image_from_file)
            new_blocked = datagen2.apply_transform(x=blocked, transform_parameters={'tx': Y, 'ty': X})
            new_blocked = np.uint8(new_blocked)
            imblock = Image.fromarray(new_blocked)
            imblock.save(destination + "/pictures/0/" + name + "_" + str(counter3) + ".jpeg")
            counter3=counter3+1




def blocked_out(input_image):
    global activated
    A=np.reshape(activated, (5, 5))
    B=input_image
    for y in range(5):
        for x in range(5):
            if A[x,y]==1:
                B[y*48:(y*48)+48,x*64:(x*64)+64]=[0,0,0]
    return B



    canvas = np.zeros((720, 960, 3))


root = Tk()
tk_img = [[ImageTk] * 5] * 5
window = Frame(root)
root.geometry('850x850')
window.grid(column=0, row=0)

# file frame
file_frame = Frame(master=window)
file_frame.grid(column=0, row=0)

destination_btn = Button(file_frame, text="destination", command=assign_destination)
destination_btn.grid(column=0, row=1)
destination_lbl = Label(file_frame, text="destination")
destination_lbl.grid(column=1, row=1)
name_lbl = Label(file_frame, text="Project Name")
name_lbl.grid(column=2, row=2)
name_txt = Entry(file_frame, width=25)
name_txt.grid(column=3, row=2)

source_btn = Button(file_frame, text="source", command=assign_source)
source_btn.grid(column=0, row=0)
source_lbl = Label(file_frame, text=source)
source_lbl.grid(column=1, row=0)
start_lb = Label(file_frame, text="start position")
start_lb.grid(column=2, row=0)
start_txt = Entry(file_frame, width=10)
start_txt.insert(0, "0")
start_txt.grid(column=3, row=0)
counter_lbl = Label(file_frame, text="0")
counter_lbl.grid(column=3, row=1)

# picture frame
picture_frame = Frame(master=window, height=500, width=500)
picture_frame.grid(column=0, row=1)

load_btn = Button(master=window, text="load next image", command=load_next)
load_btn.grid(column=1, row=1)
save_btn = Button(master=window, text="save image", command=save)
save_btn.grid(column=2, row=1)

saveL_btn = Button(master=window, text="save and load next image", command=save_load_next)
saveL_btn.grid(column=3, row=1)

blank2 = Image.fromarray(blank)
blank2 = ImageTk.PhotoImage(blank2)
# pass button
pass_btn = Button(master=window, text="Pass image up ", padx=10, pady=10, command=pass_image)
pass_btn.grid(column=0, row=2)

deselect_btn = Button(master=window, text="deselect all", padx=10, pady=10, command=deselect_all)
deselect_btn.grid(column=1, row=2)
select_all_btn = Button(master=window, text="select all", padx=10, pady=10, command=select_all)
select_all_btn.grid(column=2, row=2)

# zoomed picture
zoom_panel = Label(master=window, image=blank2)
zoom_panel.grid(column=0, row=3)
zoom_panel.image = blank2

blank_array = split_images(blank)
for x in range(5):
    for y in range(5):
        tk_img[x][y] = ImageTk.PhotoImage(Image.fromarray(blank_array[x, y]))
count = 0
for x in range(5):
    for y in range(5):
        temp = str(x) + "_" + str(y) + "_" + str(count + 100) + "_end"
        picture_panel[count] = Label(master=picture_frame, image=tk_img[x][y], name=temp, text=temp)
        picture_panel[count].grid(column=x, row=y, padx=1, pady=1)
        picture_panel[count].bind("<Button-1>", on_click, )
        picture_panel[count].bind("<Button-3>", right_click, )
        count = count + 1

control_frame1 = Frame(master=window)
control_frame1.grid(column=0, row=2)
root.bind("<q>", done)
root.bind("<space>", save_load_next2)
root.bind("<p>", load_next2)

window.mainloop()
