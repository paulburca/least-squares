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


def create_line():
    hide_error()
    global entries
    data = entries.entries
    if not entries.check_values():
        print_error("Invalid values")
        return
    x = calculate(data)
    if not x:
        print_error("Invalid data")
        return
    else:
        m, b = x
    func = make_function(m, b)
    xs, ys = parse_points(func, data)
    plt.title("Function: (" + str(m) + ") * x + (" + str(b) + ")")
    create_plot(xs, ys)
    plt.show()


class Entries:
    entries = dict()
    start = 1
    length = 0

    def add(self):
        entry1 = ttk.Entry(frm)
        entry2 = ttk.Entry(frm)
        self.entries.update({self.length: {"x": entry1, "y": entry2}})
        self.length += 1
        entry1.grid(column=0, row=self.length + self.start)
        entry2.grid(column=1, row=self.length + self.start)

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
ttk.Button(frm, text="Calculate", command=create_line).grid(column=1, row=0)
ttk.Label(frm, text="X").grid(column=0, row=1)
ttk.Label(frm, text="Y").grid(column=1, row=1)
entries = Entries()
entries.add()
entries.add()
ttk.Button(frm, text="Add", command=entries.add).grid(column=2, row=2)

root.mainloop()
