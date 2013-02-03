from Tkinter import *
import tkFileDialog as tkFile   

class mFrame(Frame):

    def __init__(self, master, *args, **kw):
        Frame.__init__(self, master, background="#808080", *args, **kw)
        self.master = master
        self.construire()

class mCanvas(Canvas):

    def __init__(self, master, *args, **kw):
        Canvas.__init__(self, master, width=1280, height=800, background="white", *args, **kw)
        self.master = master
        self.stack = 0
        self.bind("<ButtonPress-1>", self.__onPress)
        self.bind("<ButtonRelease-1>", self.__onRelease)
        self.bind("<B1-Motion>", self.__onMotion)
        self.outline = "#000000"
        self.color = ""
        self.taille = 10
        self.outil = "point"

    def undo(self):
        self.delete("obj"+str(self.stack))
        if(self.stack > 1):
            self.stack -= 1

    def __onPress(self, ev):
        x = self.canvasx(ev.x)
        y = self.canvasy(ev.y)
        if(self.outil == "ligne"):
            self.x, self.y = x, y
            self.stack += 1
        elif(self.outil == "rectangle"):
            self.x, self.y = x, y
            self.stack += 1
        elif(self.outil == "cercle"):
            self.x, self.y = x, y
            self.stack += 1
        elif(self.outil == "point"):
            self.stack += 1
            self.create_line(x, y, x, y, capstyle=ROUND, width=self.taille, tags="obj"+str(self.stack), fill=self.outline)
            self.x, self.y = x, y

    def __onRelease(self, ev):
        x = self.canvasx(ev.x)
        y = self.canvasy(ev.y)
        if(self.outil == "ligne"):
            self.create_line(self.x, self.y, x, y, tags="obj"+str(self.stack), width=self.taille, fill=self.outline)
        elif(self.outil == "rectangle"):
            self.create_rectangle(self.x, self.y, x, y, tags="obj"+str(self.stack), width=self.taille, outline=self.outline, fill=self.color)
        elif(self.outil == "cercle"):
            self.create_oval(self.x, self.y, x, y, tags="obj"+str(self.stack), width=self.taille, outline=self.outline, fill=self.color)
        elif(self.outil == "point"):
            self.create_line(self.x, self.y, x, y, capstyle=ROUND, width=self.taille, tags="obj"+str(self.stack), fill=self.color)

    def __onMotion(self, ev):
        x = self.canvasx(ev.x)
        y = self.canvasy(ev.y)
        if(self.outil == "ligne"):
            self.delete("obj"+str(self.stack))
            self.create_line(self.x, self.y, x, y, tags="obj"+str(self.stack), width=self.taille, fill=self.outline)
        elif(self.outil == "rectangle"):
            self.delete("obj"+str(self.stack))
            self.create_rectangle(self.x, self.y, x, y, tags="obj"+str(self.stack), width=self.taille, outline=self.outline, fill=self.color)
        elif(self.outil == "cercle"):
            self.delete("obj"+str(self.stack))
            self.create_oval(self.x, self.y, x, y, tags="obj"+str(self.stack), width=self.taille, outline=self.outline, fill=self.color)
        elif(self.outil == "point"):
            self.create_line(self.x, self.y, x, y, capstyle=ROUND, width=self.taille, tags="obj"+str(self.stack), fill=self.outline)
            self.x, self.y = x, y

class BoiteOutils(mFrame):

    def construire(self):
        Button(self, text="Point", command=lambda a="point":self.master.changerOutil(a)).grid(row=5, column=5)
        Button(self, text="Ligne", command=lambda a="ligne":self.master.changerOutil(a)).grid(row=10, column=5)
        Button(self, text="Rectangle", command=lambda a="rectangle":self.master.changerOutil(a)).grid(row=15, column=5)
        Button(self, text="Cercle", command=lambda a="cercle":self.master.changerOutil(a)).grid(row=20, column=5)

class PaletteCouleurs(mFrame):

    def construire(self):
        couleurs = ("#ffffff","#cccccc","#999999","#666666","#333333","#000000")
        row = 5
        self.couleur = StringVar()
        self.couleur.set(self.master.canvas.outline)
        self.couleur.trace("w", self.changerCouleur)
        for couleur in couleurs:
            Button(self, bg=couleur, width=3, command=lambda a=couleur:self._changerCouleur(a)).grid(row=row, column=5)
            row += 5
        Entry(self, width=8, textvariable=self.couleur).grid(row=row, column=5, padx=10)

    def _changerCouleur(self, couleur, e=None):
        self.couleur.set(couleur)
    
    def changerCouleur(self, *args):
        self.master.changerCouleur(self.couleur.get())

class Parametres(mFrame):

    def construire(self):
        self.taille = StringVar()
        self.taille.set(self.master.canvas.taille)
        self.taille.trace("w", self.changerTaille)
        Label(self, text="Taille").grid(row=5, column=5)
        Entry(self, width=3, textvariable=self.taille).grid(row=5, column=10, padx=10)

    def changerTaille(self, *args):
        self.master.changerTaille(self.taille.get())

class AtelierCreation(mFrame):

    def construire(self):
        self.canvas = mCanvas(self)
        self.canvas.pack(side=RIGHT)
        BoiteOutils(self).pack(side=LEFT)
        PaletteCouleurs(self).pack(side=LEFT)
        Parametres(self).pack(side=LEFT)

    def changerOutil(self, outil):
        self.canvas.outil = outil

    def changerCouleur(self, couleur):
        self.canvas.outline = couleur

    def changerTaille(self, taille):
        self.canvas.taille = taille

    def undo(self):
        self.canvas.undo()

class BarreMenu(Menu):

    def __init__(self, master, *args,**kw):
        Menu.__init__(self, *args,**kw)
        self.master = master
        self.construire()

    def construire(self):
        menuFichier = Menu(self)
        menuFichier.add_command(label="Nouveau", accelerator="Ctrl+N", command=self.master.nouvelleExperience)
        menuFichier.add_command(label="Enregistrer", accelerator="Ctrl+S", command=self.master.controleur.nouvelleExperience)
        menuFichier.add_separator()
        menuFichier.add_command(label="Quitter", accelerator="Ctrl+Q", command=self.master.quitter)
        self.add_cascade(label="Fichier", menu=menuFichier)

        menuEdition = Menu(self)
        menuEdition.add_command(label="Annuler", accelerator="Ctrl+Z", command=self.master.undo)
        #menuEdition.add_command(label="Refaire")
        self.add_cascade(label="Edition", menu=menuEdition)


class Vue(Tk):
    
    def __init__(self, controleur, *args,**kw):
        Tk.__init__(self, *args,**kw)
        self.geometry("+50+50")
        #self.resizable(width=FALSE, height=FALSE)
        self.controleur = controleur
        self.title("Experience Creator - Nouveau *")
        self.bind("<Control-n>", self.nouvelleExperience)
        self.bind("<Control-s>", self.controleur.nouvelleExperience)
        self.bind("<Control-z>", self.undo)
        self.bind("<Control-q>", self.quitter)
        self.construire()

    def construire(self):
        barreMenu = BarreMenu(self)
        self.config(menu=barreMenu)
        self.frame = Frame()
        self.nouvelleExperience()

    def undo(self, e=None):
        self.frame.undo()

    def nouvelleExperience(self, e=None):
        self.frame.destroy()
        self.frame = AtelierCreation(self)
        self.frame.pack()

    def quitter(self, e=None):
        self.quit()
        self.destroy()
        

class Controleur(object):

    def __init__(self):
        self.vue = Vue(self)
        self.filename = ""

    def nouvelleExperience(self, e=None):
        if(self.filename == ""):
            self.filename = tkFile.asksaveasfilename(filetypes=[("Postscript",".ps")],defaultextension=".ps")
        if(self.filename):
            self.vue.title("Experience Creator - " + self.filename)
            self.vue.frame.canvas.update()
            self.vue.frame.canvas.postscript(file=self.filename, colormode='color')


if __name__ == "__main__":
    controleur = Controleur()
    controleur.vue.mainloop()
