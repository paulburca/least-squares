from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt


def make_function(m, b):
    def func(x): return m * x + b
    return func


def print_error(data):
    global error
    error.config(text=data)
    error.grid(column=2, row=0)


def hide_error():
    global error
    error.grid_forget()


def calculate(data):
    sumx = 0
    sumy = 0
    sumx2 = 0
    sumxy = 0

    points = data
    for entry in points.values():
        x = float(entry.get("x").get())
        y = float(entry.get("y").get())
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
    xs = [float(i.get("x").get()) for i in data.values()]
    ys = [func(x) for x in xs]
    return xs, ys,


def create_plot(xs, ys):
    plt.xlabel("x")
    plt.ylabel("y")
    plt.plot(xs, ys, color='red', label='Function')
    plt.show()


def create_line():
    global entries
    data = entries.entries
    x = calculate(data)
    m, b = x
    func = make_function(m, b)
    xs, ys = parse_points(func, data)
    create_plot(xs, ys)


class Entries:
    entries = dict()
    length = 0

    def add(self):
        entry1 = ttk.Entry(frm)
        entry2 = ttk.Entry(frm)
        self.entries.update({self.length: {"x": entry1, "y": entry2}})
        self.length += 1
        entry1.grid(column=0, row=self.length)
        entry2.grid(column=1, row=self.length)

    def check_values(self):
        try:
            [float(i.get("x").get()) for i in self.entries.values()]
            [float(i.get("y").get()) for i in self.entries.values()]
            return True
        except ValueError:
            return False


root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
error = ttk.Label(frm)
ttk.Label(frm, text="X").grid(column=0, row=0)
ttk.Label(frm, text="Y").grid(column=1, row=0)
ttk.Button(frm, text="Calculate", command=create_line).grid(column=2, row=0)
entries = Entries()
entries.add()
entries.add()
ttk.Button(frm, text="Add", command=entries.add).grid(column=2, row=1)


root.mainloop()
