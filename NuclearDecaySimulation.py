from tkinter import *
import tkinter as tk
import pygubu
import os
import platform

class Application:
    def __init__(self, master):
        self.master = master

        self.builder = builder = pygubu.Builder()

        builder.add_from_file("simulationUI.ui")

        img_path = os.path.join('nuclearGUI.png')

        builder.add_resource_path(img_path)

        self.mainwindow = builder.get_object('MainFrame', master)

        builder.connect_callbacks(self)

    def getData(self):
        num = self.builder.get_object('noOfParticles')
        value = num.get()
        temperature = self.builder.get_object('temperature')
        tempValue = temperature.get()
        file = open('data.txt','w+')
        data = value+","+tempValue
        file.write(data)
        file.close()

    def simulate(self):
        self.getData()
        os.startfile(os.path.join('mainSimulation.exe'))
            
        
if __name__ == '__main__':

    root = Tk()
    app = Application(root)

    root.mainloop()
