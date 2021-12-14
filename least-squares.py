import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
from abc import abstractmethod


class Error:
    def __init__(self, frm):
        self.__error = ttk.Label(frm)

    def print_error(self, data):
        self.__error.config(text=data)
        self.__error.grid(column=2, row=0)

    def hide_error(self):
        self.__error.grid_forget()


class Command:
    def __init__(self, i):
        self._calculator = Calculator()
        self._plot = Plot()
        self._interface = i

    @abstractmethod
    def run(self):
        pass


class ExecuteCommandHandler:
    def __init__(self, i):
        self.__interface = i
        self.__cmds = dict()
        self.__cmds[1] = ExecuteFileCommand(i).run
        self.__cmds[2] = ExecuteTextCommand(i).run
        self.__cmds[3] = ExecuteDataCommand(i).run
        self.__interface.get_error().hide_error()

    def execute(self):
        var = self.__interface.get_var().get()
        if var == 0:
            self.__interface.get_error().print_error("Method not\nselected")
        else:
            self.__cmds[var]()


class ExecuteCommand(Command):

    @abstractmethod
    def run(self):
        pass

    @staticmethod
    def __parse_points(func, data):
        xs = [float(i.get("x")) for i in data.values()]
        ys = [float(i.get("y")) for i in data.values()]
        yfs = [func(x) for x in xs]
        return xs, ys, yfs

    def _create_line(self, data):
        m, b = self._calculator.calculate(data)
        func = self._calculator.make_function()
        xs, ys, yfs = self.__parse_points(func, data)
        self._plot.set_coordinates(xs, ys, yfs)
        self._plot.set_coefficients(m, b)
        self._plot.create_plot()
        self._plot.show()

    @staticmethod
    def parse_data(data):
        pairs = dict()
        temp = data.replace(' ', '').replace('(', '').split('),')
        i = 0
        for t in temp:
            vals = t.replace(')', '').split(',')
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


class ExecuteFileCommand(ExecuteCommand):
    def run(self):
        f = self._interface.get_file_name()
        if f:
            with open(f, 'r') as t:
                txt = t.read()
            values = self.parse_data(txt)
            if not values:
                self._interface.get_error().print_error("Invalid values")
            else:
                self._create_line(values)
        else:
            self._interface.get_error().print_error("File not\nselected")


class ExecuteTextCommand(ExecuteCommand):
    def run(self):
        txt = self._interface.get_text().get("1.0", "end")
        if len(txt) == 1:
            self._interface.get_error().print_error("No data in\nthe textbox")
            return
        values = self.parse_data(txt)
        if not values:
            self._interface.get_error().print_error("Invalid values")
        else:
            self._create_line(values)


class ExecuteDataCommand(ExecuteCommand):
    def run(self):
        entries = self._interface.get_entries()
        data = dict()
        i = 0
        if not entries.check_values():
            self._interface.get_error().print_error("Invalid values")
            return
        for entry in entries.get_entries().values():
            data.update({i: {"x": float(entry.get("x").get()), "y": float(entry.get("y").get())}})
            i += 1
        self._create_line(data)


class FileOpenCommand(Command):
    def run(self):
        filetypes = [('Text files', '*.txt')]
        file_label = self._interface.get_file_label()
        file_label.grid_forget()
        self._interface.set_file_name(fd.askopenfilename(filetypes=filetypes))
        if not self._interface.get_file_name():
            file_label.config(text="File not selected")
        else:
            file_label.config(text="File uploaded")
        file_label.grid(column=1, row=3)


class Calculator:
    def __init__(self):
        self.__m = 0
        self.__b = 0

    def make_function(self):
        def func(x): return self.__m * x + self.__b
        return func

    def calculate(self, data):
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
            self.__m = (n * sumxy - sumx * sumy) / (n * sumx2 - sumx * sumx)
            self.__b = (sumy - self.__m * sumx) / n
        except ZeroDivisionError:
            pass
        return self.__m, self.__b


class Plot:
    def __init__(self):
        self.__m = 0
        self.__b = 0
        self.__xs = []
        self.__ys = []
        self.__yfs = []

    def create_plot(self):
        xs = self.__xs
        ys = self.__ys
        yfs = self.__yfs
        plt.clf()
        if self.__m == self.__b == 0:
            plt.title("x = " + str(xs[0]) + " [note:x, not y]")
        else:
            plt.title("Function: (" + str(round(self.__m, 5)) + ") * x + (" + str(round(self.__b, 5)) + ")")
            for x, y, yf in zip(xs, ys, yfs):
                plt.plot([x, x], [y, yf], color='black', linestyle='dashed')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.plot(xs, yfs, color='red', label='Function')
        plt.scatter(xs, ys)
        labels = [f"({x},{y})" for x, y in zip(xs, ys)]
        for label, x, y in zip(labels, xs, ys):
            plt.annotate(label, xy=(x, y), xytext=(5, -5), textcoords='offset points')
        plt.plot(xs, ys, color="blue")
        mx = max(max(xs), max(ys), max(yfs))
        mn = min(min(xs), min(ys), min(yfs))
        plt.xlim([mn - 0.5, mx + 0.5])
        plt.ylim([mn - 0.5, mx + 0.5])

    def set_coordinates(self, xs, ys, yfs):
        self.__xs = xs
        self.__ys = ys
        self.__yfs = yfs

    def set_coefficients(self, m, b):
        self.__m = m
        self.__b = b

    @staticmethod
    def show():
        plt.show()


class Entries:
    def __init__(self, i):
        self.__interface = i
        self.__entries = dict()
        self.__start = 4
        self.__length = 0

    def add(self):
        self.__interface.get_error().hide_error()
        if self.__length != 35:
            entry1 = ttk.Entry(self.__interface.get_frame())
            entry2 = ttk.Entry(self.__interface.get_frame())
            self.__entries.update({self.__length: {"x": entry1, "y": entry2}})
            self.__length += 1
            entry1.grid(column=0, row=self.__length + self.__start)
            entry2.grid(column=1, row=self.__length + self.__start)
        else:
            self.__interface.get_error().print_error("Maximum set\nof values: 35")

    def remove(self):
        self.__interface.get_error().hide_error()
        if self.__length != 2:
            self.__length -= 1
            entryx = self.__entries.get(self.__length).get("x")
            entryy = self.__entries.get(self.__length).get("y")
            self.__entries.pop(self.__length)
            entryx.destroy()
            entryy.destroy()
        else:
            self.__interface.get_error().print_error("Minimum set\nof values: 2")

    def check_values(self):
        try:
            [float(i.get("x").get()) for i in self.__entries.values()]
            [float(i.get("y").get()) for i in self.__entries.values()]
            return True
        except ValueError:
            return False

    def get_entries(self):
        return self.__entries


class Interface:
    def __init__(self):
        def build_frame():
            root = Tk(className="least squares")
            frm = ttk.Frame(root, padding=10)
            frm.grid()
            return root, frm

        def build_button(frm):
            ttk.Button(frm, text="Calculate", command=ExecuteCommandHandler(self).execute).grid(column=1, row=0)

        def build_error(frm):
            error = Error(frm)
            return error

        def build_checkboxes(frm):
            var = tk.IntVar()
            checkboxes = list()
            checkboxes.append(ttk.Checkbutton(frm, text="File", onvalue=1, variable=var).grid(row=1, column=0))
            checkboxes.append(ttk.Checkbutton(frm, text="TextBox", onvalue=2, variable=var).grid(row=1, column=1))
            checkboxes.append(ttk.Checkbutton(frm, text="DataList", onvalue=3, variable=var).grid(row=1, column=2))
            return var

        def build_file(frm):
            ttk.Button(frm, text="Upload file", command=FileOpenCommand(self).run).grid(column=0, row=3)
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
        self.__error = build_error(self.__frm)
        build_button(self.__frm)
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

    def show(self):
        self.__root.mainloop()


interface = Interface()
interface.show()
