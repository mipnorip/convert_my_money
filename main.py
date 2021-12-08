import config
import json, requests, datetime
from tkinter import *
from tkinter import ttk


class App:
    def __init__(self) -> None:
        self.get_data()
        self.list_d()
        self.window()
        self.draw()

        mainloop()
        pass

    def window(self) -> None:
        self.root = Tk()
        self.root.title('Валютный калькулятор')
        self.root.resizable(width=False, height=False)
        self.canvas = Canvas(self.root, width=300, height=200, bg='white')
        self.scroll_bar = Scrollbar(self.root)
        self.canvas.configure()

    def list_d(self) -> None:
        """
        self.keys_list = []
        for i in self.data.keys():
            self.keys_list.append([i[3:]])
        """
        self.keys_list = ['USD', 'RUB', 'EUR', 'GBP', 'CNY']

    def draw(self) -> None:
        self.canvas.create_text(10, 15, text=f'1 USD = {self.data.get("USDRUB")} RUB', anchor=W)

        self.combo1 = ttk.Combobox(self.root, width=10, height=0)
        self.combo1['values'] = self.keys_list
        self.combo1.place(x=15, y=35)
        self.combo2 = ttk.Combobox(self.root, width=10, height=0)
        self.combo2['values'] = self.keys_list
        self.combo2.place(x=160, y=35)

        self.text = ttk.Entry(self.root)
        self.text.place(x=50, y=120)

        self.convert_buttom = Button(text='Convert', command=self.convert)
        self.convert_buttom.place(x=150, y=90, anchor="c")

        self.canvas.pack()

    def convert(self) -> None:
        data = float(self.text.get())
        self.text.delete(0, last=END)
        self.text.insert(index=0,string=f'{data / self.data.get(f"USD{self.combo1.get()}") * self.data.get(f"USD{self.combo2.get()}")}')


    def get_data(self) -> None:
        try:
            with open('today.txt', 'r') as file:
                self.data = json.load(file)
            if self.data.get('today') == str(datetime.date.today()):
                print("OK")
                self.data.pop('today')
                pass
            else:
                self.api()
                self.get_data()
        except FileNotFoundError:
            self.api()
            self.get_data()

    def api(self) -> None:
        dates = json.loads(requests.get("http://api.currencylayer.com/live?access_key=" + config.KEY + "&format=1").text)
        dates = dates.get('quotes')
        dates['today'] = str(datetime.date.today())
        with open('today.txt', 'w') as file:
            file.write(json.dumps(dates))

App()