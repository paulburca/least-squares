import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import matplotlib.pyplot as plt


def make_function(m, b):
    def func(x): return m * x + b
    return func


def calculate(data):
    sumx = 0
    sumy = 0
    sumx2 = 0
    sumxy = 0

    points = data
    for entry in points.values():
        x = float(entry.get("x"))
        y = float(entry.get("y"))
        sumx += x
        sumy += y
        sumx2 += x * x
        sumxy += x * y
    n = len(points)
    try:
        m = (n * sumxy - sumx * sumy) / (n * sumx2 - sumx * sumx)
        b = (sumy - m * sumx) / n
    except ZeroDivisionError:
        return False
    return m, b


def parse_points(func, data):
    xs = [float(i.get("x")) for i in data.values()]
    ys = [float(i.get("y")) for i in data.values()]
    yfs = [func(x) for x in xs]
    return xs, ys, yfs


def create_plot(xs, ys, yfs):
    plt.xlabel("x")
    plt.ylabel("y")
    plt.plot(xs, yfs, color='red', label='Function')
    plt.scatter(xs, ys)
    labels = [f"({x},{y})" for x, y in zip(xs, ys)]
    for label, x, y in zip(labels, xs, ys):
        plt.annotate(label, xy=(x, y), xytext=(5, -5), textcoords='offset points')
    for x, y, yf in zip(xs, ys, yfs):
        label = str(abs(y - yf))
        plt.plot([x, x], [y, yf], color='black', linestyle='dashed', label=label)
    plt.plot(xs, ys, color="blue")
    mx = max(max(xs), max(ys), max(yfs))
    mn = min(min(xs), min(ys), min(yfs))
    plt.xlim([mn - 0.5, mx + 0.5])
    plt.ylim([mn - 0.5, mx + 0.5])


def create_line(data):
    x = calculate(data)
    if not x:
        interface.print_error("Invalid data")
        return
    else:
        m, b = x
    func = make_function(m, b)
    xs, ys, yfs = parse_points(func, data)
    plt.clf()
    plt.title("Function: (" + str(m) + ") * x + (" + str(b) + ")")
    create_plot(xs, ys, yfs)
    plt.show()


def parse_data(data):
    pairs = dict()
    temp = data.replace('(', '').split('),')
    i = 0
    if len(temp) == 1:
        return False
    for t in temp:
        vals = t.replace(')', '').replace(' ', '').split(',')
        if len(vals) < 2:
            return False
        pairs.update({i: {"x": vals[0], "y": vals[1]}})
        i += 1
        try:
            float(pairs.get(i - 1).get('x'))
            float(pairs.get(i - 1).get('y'))
        except ValueError:
            return False
    return pairs


def execute_file():
    f = interface.get_file_name()
    if f:
        with open(f, 'r') as t:
            txt = t.read()
        values = parse_data(txt)
        if not values:
            interface.print_error("Invalid values")
        else:
            create_line(values)
    else:
        interface.print_error("File not\nselected")


def execute_textbox():
    txt = interface.get_text().get("1.0", "end")
    if len(txt) == 1:
        interface.print_error("No data in\nthe textbox")
        return
    values = parse_data(txt)
    if not values:
        interface.print_error("Invalid values")
    else:
        create_line(values)


def execute_entries():
    entries = interface.get_entries()
    data = dict()
    i = 0
    if not entries.check_values():
        interface.print_error("Invalid values")
        return
    for entry in entries.entries.values():
        data.update({i: {"x": float(entry.get("x").get()), "y": float(entry.get("y").get())}})
        i += 1
    create_line(data)


def execute():
    interface.hide_error()
    val = interface.get_var().get()
    if val == 0:
        interface.print_error("Method not\nselected")
    elif val == 1:
        execute_file()
    elif val == 2:
        execute_textbox()
    elif val == 3:
        execute_entries()


class Entries:
    entries = dict()
    start = 4
    length = 0

    def __init__(self, i):
        self.interface = i

    def add(self):
        self.interface.hide_error()
        if self.length != 35:
            entry1 = ttk.Entry(self.interface.get_frame())
            entry2 = ttk.Entry(self.interface.get_frame())
            self.entries.update({self.length: {"x": entry1, "y": entry2}})
            self.length += 1
            entry1.grid(column=0, row=self.length + self.start)
            entry2.grid(column=1, row=self.length + self.start)
        else:
            self.interface.print_error("Maximum set\nof values: 35")

    def remove(self):
        self.interface.hide_error()
        if self.length != 2:
            self.length -= 1
            entryx = self.entries.get(self.length).get("x")
            entryy = self.entries.get(self.length).get("y")
            self.entries.pop(self.length)
            entryx.destroy()
            entryy.destroy()
        else:
            self.interface.print_error("Minimum set\nof values: 2")

    def check_values(self):
        try:
            [float(i.get("x").get()) for i in self.entries.values()]
            [float(i.get("y").get()) for i in self.entries.values()]
            return True
        except ValueError:
            return False


def openfile():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    file_label = interface.get_file_label()
    interface.get_file_label().grid_forget()
    interface.set_file_name(fd.askopenfilename(filetypes=filetypes))
    if not interface.get_file_name():
        file_label.config(text="File not selected")
    file_label.grid(column=1, row=3)


class Interface:
    def __init__(self):
        def build_frame():
            root = Tk()
            frm = ttk.Frame(root, padding=10)
            frm.grid()
            return root, frm

        def build_button(frm):
            ttk.Button(frm, text="Calculate", command=execute).grid(column=1, row=0)

        def build_error(frm):
            error = ttk.Label(frm)
            return error

        def build_checkboxes(frm):
            var = tk.IntVar()
            checkboxes = list()
            checkboxes.append(ttk.Checkbutton(frm, text="File", onvalue=1, variable=var).grid(row=1, column=0))
            checkboxes.append(ttk.Checkbutton(frm, text="TextBox", onvalue=2, variable=var).grid(row=1, column=1))
            checkboxes.append(ttk.Checkbutton(frm, text="DataList", onvalue=3, variable=var).grid(row=1, column=2))
            return var

        def build_file(frm):
            ttk.Button(frm, text="Upload file", command=openfile).grid(column=0, row=3)
            file_label = ttk.Label(frm, text="File uploaded")
            return file_label

        def build_text(frm):
            ttk.Label(frm, text="Text:").grid(column=0, row=2)
            text = tk.Text(frm, height=5, width=25)
            text.grid(columnspan=2, column=1, row=2)
            return text

        def build_entries(frm):
            entries = Entries(self)
            ttk.Label(frm, text="X").grid(column=0, row=4)
            ttk.Label(frm, text="Y").grid(column=1, row=4)
            entries.add()
            entries.add()
            ttk.Button(frm, text="Add", command=entries.add).grid(column=2, row=5)
            ttk.Button(frm, text="Remove", command=entries.remove).grid(column=2, row=6)
            return entries

        self.__root, self.__frm = build_frame()
        build_button(self.__frm)
        self.__error = build_error(self.__frm)
        self.__var = build_checkboxes(self.__frm)
        self.__file_label = build_file(self.__frm)
        self.__file_name = ''
        self.__text = build_text(self.__frm)
        self.__entries = build_entries(self.__frm)

    def get_frame(self):
        return self.__frm

    def get_error(self):
        return self.__error

    def get_var(self):
        return self.__var

    def get_file_label(self):
        return self.__file_label

    def get_file_name(self):
        return self.__file_name

    def set_file_name(self, file_name):
        self.__file_name = file_name

    def get_text(self):
        return self.__text

    def get_entries(self):
        return self.__entries

    def print_error(self, data):
        self.__error.config(text=data)
        interface.get_error().grid(column=2, row=0)

    def hide_error(self):
        self.__error.grid_forget()

    def show(self):
        self.__root.mainloop()


interface = Interface()
interface.show()
