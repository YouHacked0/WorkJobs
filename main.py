from pprint import pprint
import tkinter as tk
from tkinter import messagebox
import collections as coll
import pymongo
import config


class GiveSalary:
    def __init__(self):
        self.main = {}

    def create_human(self, name, post, salary, tax_percent):
        self.main = {
            "names": name,
            "post": post,
            "salary": salary,
            "tax_percent": tax_percent,
        }
        collections.insert_one(self.main)
        return self.main

    def get_reward(self, bol, amount=5000):
        if bol:
            return self.main['salary'] + amount
        else:
            return 0

    def get_compensation(self, bol, amount):
        if bol:
            return self.main['salary'] + amount
        else:
            return 0

    def print_check(self, reward=5000, compensation=0):
        salary__tax = self.main['salary'] - (self.main['salary'] / 100 * self.main['tax_percent'])
        return (f"""
==============================
> ФИО: {self.main["names"]}
> ДОЛЖНОСТЬ: {self.main['post']}
> ВАША ЗП: {self.main['salary']}
> ЗП С УЧЁТОМ НАЛОГОВ: {salary__tax}
> ПРЕМИЯ: {reward}
> КОМПЕНСАЦИЯ: {compensation}

>>> ИТОГ <<<
>>> {salary__tax + reward + compensation} <<< 
""")


class Interface:
    def __init__(self):
        self.tax_percent = None
        self.root = tk.Tk()

        tk.Button(self.root, text="Edit Human", font="Times_New_Roman 10", command=self.tk_edithuman).pack()

        tk.Button(self.root, text="Create Human", font="Times_New_Roman 10", command=self.tk_createhuman).pack()

        tk.Button(self.root, text="Delete Human", font="Times_New_Roman 10", command=self.tk_deletehuman).pack()

        tk.Button(self.root, text="Print Check", font="Times_New_Roman 10", command=self.tk_printcheck).pack()

        self.humans = {}

    def start(self):
        self.root.mainloop()

    def createhuman(self):
        human = GiveSalary()
        human.create_human(name=self.create_names.get(), post=self.create_post.get(), salary=int(self.create_salary.get()),
                          tax_percent=int(self.create_tax_percent.get()))
        self.tax_percent = int(self.create_tax_percent.get())
        if self.humans == {}:
            i = 1
            messagebox.showinfo("WorkJobs", "ID: 1")
        else:
            [i] = coll.deque(self.humans, maxlen=1)
            i = i + 1
            messagebox.showinfo("WorkJobs", f"ID: {coll.deque(self.humans, maxlen=1)}")
        self.humans[i] = human
        self.ch.destroy()
        pprint(self.humans)

    def tk_createhuman(self):

        self.ch = tk.Toplevel(self.root)

        tk.Label(self.ch, text="Name", font="Times_New_Roman 10").pack()

        self.create_names = tk.Entry(self.ch, width=15)
        self.create_names.pack()

        tk.Label(self.ch, text="Post", font="Times_New_Roman 10").pack()

        self.create_post = tk.Entry(self.ch, width=15)
        self.create_post.pack()

        tk.Label(self.ch, text="Salary", font="Times_New_Roman 10").pack()

        self.create_salary = tk.Entry(self.ch, width=15)
        self.create_salary.pack()

        tk.Label(self.ch, text="Tax percent", font="Times_New_Roman 10").pack()

        self.create_tax_percent = tk.Entry(self.ch, width=15)
        self.create_tax_percent.pack()

        tk.Button(self.ch, text="Enter", command=self.createhuman).pack()

    def deletehuman(self):
        human = GiveSalary()
        human.main = list(collections.find({}))[int(self.delete_id.get()) - 1]
        collections.delete_one({"names": human.main["names"]})
        self.dh.destroy()

    def tk_deletehuman(self):

        self.dh = tk.Toplevel(self.root)

        tk.Label(self.dh, text="ID", font="Times_New_Roman 10").pack()

        self.delete_id = tk.Entry(self.dh, width=15)
        self.delete_id.pack()

        tk.Button(self.dh, text="Enter", command=self.deletehuman).pack()

    def edithuman(self):
        human = GiveSalary()
        human.main = list(collections.find({}))[int(self.edit_id.get()) - 1]
        if self.edit_type.get() == "ФИО":
            collections.update_one(collections.find_one({"names": human.main["names"]}), {"$set": {"names": self.edit_value.get()}})
        elif self.edit_type.get() == "Должность":
            collections.update_one(collections.find_one({"names": human.main["names"]}), {"$set": {"post": self.edit_value.get()}})
        elif self.edit_type.get() == "Зарплата":
            collections.update_one(collections.find_one({"names": human.main["names"]}), {"$set": {"salary": int(self.edit_value.get())}})
        elif self.edit_type.get() == "Процент комиссии":
            collections.update_one(collections.find_one({"names": human.main["names"]}), {"$set": {"tax_percent": int(self.edit_value.get())}})
        self.eh.destroy()

    def tk_edithuman(self):

        self.eh = tk.Toplevel(self.root)

        tk.Label(self.eh, text="ID", font="Times_New_Roman 10").pack()

        self.edit_id = tk.Entry(self.eh, width=15)
        self.edit_id.pack()

        tk.Label(self.eh, text="Тип", font="Times_New_Roman 10").pack()

        self.edit_type = tk.Entry(self.eh, width=15)
        self.edit_type.pack()

        tk.Label(self.eh, text="Значение", font="Times_New_Roman 10").pack()

        self.edit_value = tk.Entry(self.eh, width=15)
        self.edit_value.pack()

        tk.Button(self.eh, text="Enter", command=self.edithuman).pack()

    def printcheck(self):
        if int(self.print_reward.get()) == 0:
            rw = False
            r_w = 0
        else:
            rw = True
            r_w = int(self.print_reward.get())

        if int(self.print_compensation.get()) == 0:
            cm = False
            c_m = 0
        else:
            cm = True
            c_m = int(self.print_compensation.get())

        human = GiveSalary()
        human.main = list(collections.find({}))[int(self.print_id.get()) - 1]
        messagebox.showinfo("WorkJobs", human.print_check(rw, c_m))
        self.cp.destroy()

    def tk_printcheck(self):

        self.cp = tk.Toplevel(self.root)

        tk.Label(self.cp, text="ID", font="Times_New_Roman 10").pack()

        self.print_id = tk.Entry(self.cp, width=15)
        self.print_id.pack()

        tk.Label(self.cp, text="Reward (to turn off type 0)", font="Times_New_Roman 10").pack()

        self.print_reward = tk.Entry(self.cp, width=15)
        self.print_reward.pack()

        tk.Label(self.cp, text="Compensation (to turn off type 0)", font="Times_New_Roman 10").pack()

        self.print_compensation = tk.Entry(self.cp, width=15)
        self.print_compensation.pack()

        tk.Button(self.cp, text="Enter", command=self.printcheck).pack()


if __name__ == '__main__':
    client = pymongo.MongoClient(config.url)
    database = client["YouHacked0"]
    collections = database["WorkJobs"]
    root = Interface()
    root.start()
