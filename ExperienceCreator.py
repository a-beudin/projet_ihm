from Tkinter import *
#from PIL import *

class Vue(Tk):
    
    def __init__(self, controleur, *args,**kw):
        Tk.__init__(self, *args,**kw)
        self.geometry("800x600")
        #self.resizable(width=FALSE, height=FALSE)
        self.controleur = controleur
        self.title("Experience Creator")
        

class Controleur(object):

    def __init__(self):
        self.vue = Vue(self)


if __name__ == "__main__":
    controleur = Controleur()
    controleur.vue.mainloop()
