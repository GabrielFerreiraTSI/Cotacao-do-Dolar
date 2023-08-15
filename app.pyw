import tkinter as tk
from tkinter import ttk
import matplotlib
import requests
from datetime import datetime as dt

matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Cotação do dólar")
        self.figure = Figure(figsize=(15, 6), dpi=100)
        
        self.figureCanvas = FigureCanvasTkAgg(self.figure, self)
        NavigationToolbar2Tk(self.figureCanvas, self)
        
        self.chart = self.figure.add_subplot()
        self.currentValue = tk.StringVar(value=10)
        self.cmdExecutar()
        
        self.figureCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.spinRange = ttk.Spinbox(
            self, 
            from_=1, 
            to=60, 
            textvariable=self.currentValue, 
            wrap=True,
            font=("Arial 18 bold")
        )
        self.spinRange.pack(fill="x", side="left", expand=True, padx=5)
        
        ttk.Button(
            self,
            text="Mostrar",
            command=self.cmdExecutar
        ).pack(fill="x", side="left", expand=True, padx=5)
        
    def cmdExecutar(self):
        
        cotacoes = requests.get(f"https://economia.awesomeapi.com.br/json/daily/USD-BRL/{self.currentValue.get()}")
        xData = []
        yData = []
        yData2 = []
        yData3 = []
        yData4 = []
        
        for x in cotacoes.json():
            ts = int(x["timestamp"])
            xEixo = dt.utcfromtimestamp(ts).strftime("%d/%m/\n%Y")
            xData.insert(0, xEixo)
            yData.insert(0, float(x["bid"]))
            yData2.insert(0, float(x["ask"]))
            yData3.insert(0, float(x["low"]))
            yData4.insert(0, float(x["high"]))
        
        self.chart.clear()
            
        self.chart.plot(xData, yData, marker="o", label="compra")
        self.chart.plot(xData, yData2, marker="o", label="venda")
        self.chart.plot(xData, yData3, marker="o", label="mínimo")
        self.chart.plot(xData, yData4, marker="o", label="máximo")
        
        self.chart.set_title(cotacoes.json()[0]["name"])
        self.chart.set_xlabel("Datas")
        self.chart.set_ylabel("BRL")
        self.chart.grid()
        self.chart.legend()
        
        self.figureCanvas.draw()

if __name__ == "__main__":
    app = App()
    app.mainloop()
    