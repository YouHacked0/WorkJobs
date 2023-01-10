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

    def get_tax(self, summ, percent=13):
        return summ - (summ / 100 * percent)

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

    def print_check(self, use_reward=False, reward=5000, use_compensation=False, compensation=0):
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


def get_tax(summ, percent=13):
    return summ - (summ / 100 * percent)


class tkinterz():
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
        test = GiveSalary()
        test.create_human(name=self.first1.get(), post=self.first2.get(), salary=int(self.first3.get()),
                          tax_percent=int(self.first4.get()))
        self.tax_percent = int(self.first4.get())
        if self.humans == {}:
            i = 1
            messagebox.showinfo("WorkJobs", "ID: 1")
        else:
            [i] = coll.deque(self.humans, maxlen=1)
            i = i + 1
            messagebox.showinfo("WorkJobs", f"ID: {coll.deque(self.humans, maxlen=1)}")
        self.humans[i] = test
        self.ch.destroy()
        pprint(self.humans)

    def tk_createhuman(self):

        self.ch = tk.Toplevel(self.root)

        tk.Label(self.ch, text="Name", font="Times_New_Roman 10").pack()

        self.first1 = tk.Entry(self.ch, width=15)
        self.first1.pack()

        tk.Label(self.ch, text="Post", font="Times_New_Roman 10").pack()

        self.first2 = tk.Entry(self.ch, width=15)
        self.first2.pack()

        tk.Label(self.ch, text="Salary", font="Times_New_Roman 10").pack()

        self.first3 = tk.Entry(self.ch, width=15)
        self.first3.pack()

        tk.Label(self.ch, text="Tax percent", font="Times_New_Roman 10").pack()

        self.first4 = tk.Entry(self.ch, width=15)
        self.first4.pack()

        tk.Button(self.ch, text="Enter", command=self.createhuman).pack()

    def deletehuman(self):
        test = GiveSalary()
        test.main = list(collections.find({}))[int(self.third1.get()) - 1]
        collections.delete_one({"names": test.main["names"]})
        self.dh.destroy()

    def tk_deletehuman(self):

        self.dh = tk.Toplevel(self.root)

        tk.Label(self.dh, text="ID", font="Times_New_Roman 10").pack()

        self.third1 = tk.Entry(self.dh, width=15)
        self.third1.pack()

        tk.Button(self.dh, text="Enter", command=self.deletehuman).pack()

    def edithuman(self):
        test1 = int(self.fourth1.get())
        print(test1)
        print(self.fourth3.get())
        test = GiveSalary()
        test.main = list(collections.find({}))[int(self.fourth1.get()) - 1]
        if self.fourth2.get() == "ФИО":
            collections.update_one(collections.find_one({"names": test.main["names"]}), {"$set": {"names": self.fourth3.get()}})
        elif self.fourth2.get() == "Должность":
            collections.update_one(collections.find_one({"names": test.main["names"]}), {"$set": {"post": self.fourth3.get()}})
        elif self.fourth2.get() == "Зарплата":
            collections.update_one(collections.find_one({"names": test.main["names"]}), {"$set": {"salary": int(self.fourth3.get())}})
        elif self.fourth2.get() == "Процент комиссии":
            collections.update_one(collections.find_one({"names": test.main["names"]}), {"$set": {"tax_percent": int(self.fourth3.get())}})
        print()
        print()
        self.eh.destroy()

    def tk_edithuman(self):

        self.eh = tk.Toplevel(self.root)

        tk.Label(self.eh, text="ID", font="Times_New_Roman 10").pack()

        self.fourth1 = tk.Entry(self.eh, width=15)
        self.fourth1.pack()

        tk.Label(self.eh, text="Тип", font="Times_New_Roman 10").pack()

        self.fourth2 = tk.Entry(self.eh, width=15)
        self.fourth2.pack()

        tk.Label(self.eh, text="Значение", font="Times_New_Roman 10").pack()

        self.fourth3 = tk.Entry(self.eh, width=15)
        self.fourth3.pack()

        tk.Button(self.eh, text="Enter", command=self.edithuman).pack()

    def printcheck(self):
        if int(self.second4.get()) == 0:
            rw = False
            r_w = 0
        else:
            rw = True
            r_w = int(self.second4.get())

        if int(self.second5.get()) == 0:
            cm = False
            c_m = 0
        else:
            cm = True
            c_m = int(self.second5.get())

        test = GiveSalary()
        test.main = list(collections.find({}))[int(self.second1.get()) - 1]
        messagebox.showinfo("WorkJobs", test.print_check(rw, r_w, cm, c_m))
        self.cp.destroy()

    def tk_printcheck(self):

        self.cp = tk.Toplevel(self.root)

        tk.Label(self.cp, text="ID", font="Times_New_Roman 10").pack()

        self.second1 = tk.Entry(self.cp, width=15)
        self.second1.pack()

        tk.Label(self.cp, text="Reward (to turn off type 0)", font="Times_New_Roman 10").pack()

        self.second4 = tk.Entry(self.cp, width=15)
        self.second4.pack()

        tk.Label(self.cp, text="Compensation (to turn off type 0)", font="Times_New_Roman 10").pack()

        self.second5 = tk.Entry(self.cp, width=15)
        self.second5.pack()

        tk.Button(self.cp, text="Enter", command=self.printcheck).pack()


# human = GiveSalary()
# pprint(human.create_human("Леонид Олегович Хомутов", "Охранник", 23_508, human.get_tax(23_508)))
# human.print_check(use_reward=False, use_compensation=False, compensation=1000)

if __name__ == '__main__':
    client = pymongo.MongoClient(config.url)
    database = client["YouHacked0"]
    collections = database["WorkJobs"]
    root = tkinterz()
    root.start()

# ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ
#
# ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ
