from Tkinter import *
import re
import tkFileDialog as tkFile
import tkMessageBox as tkMsg

class PressePapier(list):

    def __init__(self, *args, **kw):
        list.__init__(self, *args, **kw)
        self.tailleMax = 20

    def copier(self, obj):
        if(obj):
            if(len(self) > 0):
                if(self[0] != obj):
                    self.insert(0, obj)
            else:
                self.insert(0, obj)
        if(len(self) > self.tailleMax):
            self = self[:self.tailleMax]

    def coller(self, index=0):
        try:
            return self[index]
        except IndexError, e:
            return []

class mFrame(Frame):

    def __init__(self, master, *args, **kw):
        Frame.__init__(self, master, background="#808080", *args, **kw)
        self.master = master
        self.modifie = False
        self.construire()

    def construire(self):
        pass

class mCanvas(Canvas):

    def __init__(self, master, *args, **kw):
        Canvas.__init__(self, master, width=1280, height=800, background="white", *args, **kw)
        self.master = master
        self.pressePapier = PressePapier()
        self.stack = 0
        self.bind("<ButtonPress-1>", self.__onPress)
        self.bind("<ButtonRelease-1>", self.__onRelease)
        self.bind("<B1-Motion>", self.__onMotion)
        self.outline = "#000000"
        self.color = ""
        self.fill_select = "#dddddd"
        self.taille = 50
        self.outil = "selectionM"
        self.itemsSelected = []
        self.master.modifie = True

    def changerOutil(self, outil):
        self.outil = outil
        if(self.outil != "selection"):
            self.delete("rectangleSelect")

    def undo(self):
        self.delete("obj"+str(self.stack))
        if(self.stack > 1):
            self.stack -= 1
        self.master.modifie = True

    def copier(self):
        self.pressePapier.copier(self.itemsSelected)

    def couper(self):
        pass #self.pressePapier.copier(self.itemsSelected)

    def coller(self):
        items = self.pressePapier.coller()
        if(len(items) > 0):
            self.master.modifie = True
            self.itemsSelected = items
            self.delete("rectangleSelect")
            for item in self.itemsSelected:
                if(self.gettags(item) != "rectangleSelect"):
                    coords = self.coords(item)
                    if(len(coords) == 4):
                        if(self.type(item) == "line"):
                            self.stack += 1
                            self.create_line(coords[0],coords[1],coords[2],coords[3],fill=self.itemcget(item,"fill"),tag="obj"+str(self.stack),width=self.itemcget(item,"width"))
                        elif(self.type(item) == "rectangle"):
                            self.stack += 1
                            self.create_rectangle(coords[0],coords[1],coords[2],coords[3],outline=self.itemcget(item,"outline"),fill=self.itemcget(item,"fill"),tag="obj"+str(self.stack),width=self.itemcget(item,"width"))
                        elif(self.type(item) == "oval"):
                            self.stack += 1
                            self.create_oval(coords[0],coords[1],coords[2],coords[3],outline=self.itemcget(item,"outline"),fill=self.itemcget(item,"fill"),tag="obj"+str(self.stack),width=self.itemcget(item,"width"))

                        bb = self.bbox("obj"+str(self.stack))
                        self.tag_raise("obj"+str(self.stack))
                        self.create_rectangle(bb[0],bb[1],bb[2],bb[3],outline="grey",dash=(4, 4),tag="rectangleSelect",width=2,fill="")

    def supprimer(self):
        self.delete("rectangleSelect")
        if(len(self.itemsSelected) > 0):
            self.master.modifie = True
            for item in self.itemsSelected:
                self.delete(item)
            
    def __onPress(self, ev):
        x = self.canvasx(ev.x)
        y = self.canvasy(ev.y)
        if(self.outil == "selectionM"):
            self.x, self.y = x, y
            self.stack += 1
            tags = self.gettags(self.find_withtag(CURRENT))
            for tag in tags:
                if(tag == "rectangleSelect"):
                    self.outil = "deplacementM"
            if(self.outil == "selectionM"):
                self.itemsSelected = []
                self.delete("rectangleSelect")
        elif(self.outil == "selection"):
            self.x, self.y = x, y
            if(self.master.master.keysPressed.count("17") == 0):
                self.itemsSelected = []
            self.delete("rectangleSelect")
            tags = self.gettags(self.find_withtag(CURRENT))
            for tag in tags:
                if(re.match(r'obj(.*)',tag)):
                    self.itemsSelected += self.find_withtag(tag)
            for item in self.itemsSelected:
                if(self.gettags(item) != "rectangleSelect"):
                    bb = self.bbox(item)
                    self.tag_raise(item)
                    self.create_rectangle(bb[0],bb[1],bb[2],bb[3],outline="grey",fill=self.fill_select,dash=(4, 4),tag="rectangleSelect",width=2)
            self.tag_lower("rectangleSelect")
        elif(self.outil == "ligne"):
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
        if(self.outil == "deplacementM"):
            self.outil = "selectionM"
        elif(self.outil == "selectionM"):
            self.delete("rect")
        elif(self.outil == "selection"):
            if(len(self.itemsSelected) > 0):
                self.master.modifie = True
                for item in self.itemsSelected:
                    self.move("rectangleSelect", x - self.x, y - self.y)
                    self.move(item, x - self.x, y - self.y)
        elif(self.outil == "ligne"):
            self.master.modifie = True
            pass #self.create_line(self.x, self.y, x, y, tags="obj"+str(self.stack), width=self.taille, fill=self.outline)
        elif(self.outil == "rectangle"):
            self.master.modifie = True
            pass #self.create_rectangle(self.x, self.y, x, y, tags="obj"+str(self.stack), width=self.taille, outline=self.outline, fill=self.color)
        elif(self.outil == "cercle"):
            self.master.modifie = True
            pass #self.create_oval(self.x, self.y, x, y, tags="obj"+str(self.stack), width=self.taille, outline=self.outline, fill=self.color)
        elif(self.outil == "point"):
            self.master.modifie = True
            pass #self.create_line(self.x, self.y, x, y, capstyle=ROUND, width=self.taille, tags="obj"+str(self.stack), fill=self.color)

    def __onMotion(self, ev):
        x = self.canvasx(ev.x)
        y = self.canvasy(ev.y)
        if(self.outil == "deplacementM"):
            for item in self.itemsSelected:
                self.move(item, x - self.x, y - self.y)
            self.move("rectangleSelect", x - self.x, y - self.y)
            self.x, self.y = x, y
        elif(self.outil == "selectionM"):
            self.itemsSelected = []
            #self.tag_lower("obj"+str(self.stack))
            self.itemsSelected = self.find_overlapping(self.x, self.y, x, y)
            self.delete("rectangleSelect")
            self.delete("rect")
            for item in self.itemsSelected:
                t = True
                for tag in self.gettags(item):
                    if(tag == "rect" or tag == "rectangleSelect"):
                        t = False
                if(t):
                    bb = self.bbox(item)
                    self.tag_raise(item)
                    if(bb):
                        self.create_rectangle(bb[0],bb[1],bb[2],bb[3],fill=self.fill_select,outline="grey",dash=(4, 4),tag="rectangleSelect",width=2)
            self.create_rectangle(self.x, self.y, x, y, fill=self.fill_select, dash=(4, 4), tags="rect", width=2, outline="#808080")
            self.tag_lower("rectangleSelect")
            self.tag_lower("rect")
        elif(self.outil == "selection"):
            for item in self.itemsSelected:
                self.move("rectangleSelect", x - self.x, y - self.y)
                self.move(item, x - self.x, y - self.y)
                self.x, self.y = x, y
        elif(self.outil == "ligne"):
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

    def charger(self, filename):
        f = open(filename, "r")
        lines = f.readlines()
        for line in lines:
            line = line.split(" ")
            line[7] = line[7].strip()
            if(line[0] == "line"):
                self.create_line(line[1], line[2], line[3], line[4], width=line[5], capstyle=line[6], fill=line[7])
            elif(line[0] == "rectangle"):
                self.create_rectangle(line[1], line[2], line[3], line[4], width=line[5], outline=line[6], fill=line[7])
            elif(line[0] == "oval"):
                self.create_oval(line[1], line[2], line[3], line[4], width=line[5], outline=line[6], fill=line[7])
        self.master.modifie = False

    def enregistrer(self):
        chaine = ""
        items = self.find_all()
        for item in items:
            tags = self.gettags(item)
            if("rectangleSelect" in tags):
                continue
            coords = self.coords(item)
            if(len(coords) == 4):
                if(self.type(item) == "line"):
                    chaine += "line "+str(coords[0])+" "+str(coords[1])+" "+str(coords[2])+" "+str(coords[3])+" "+self.itemcget(item,"width")+" "+self.itemcget(item,"capstyle")+" "+self.itemcget(item,"fill")
                elif(self.type(item) == "rectangle"):
                    chaine += "rectangle "+str(coords[0])+" "+str(coords[1])+" "+str(coords[2])+" "+str(coords[3])+" "+self.itemcget(item,"width")+" "+self.itemcget(item,"outline")+" "+self.itemcget(item,"fill")
                elif(self.type(item) == "oval"):
                    chaine += "oval "+str(coords[0])+" "+str(coords[1])+" "+str(coords[2])+" "+str(coords[3])+" "+self.itemcget(item,"width")+" "+self.itemcget(item,"outline")+" "+self.itemcget(item,"fill")            
                chaine += "\n"
        self.master.modifie = False
        return chaine

class BoiteOutils(mFrame):

    def construire(self):
        Button(self, text="Selection", command=lambda a="selection":self.master.changerOutil(a)).grid(row=2, column=5)
        Button(self, text="Selection multiple", command=lambda a="selectionM":self.master.changerOutil(a)).grid(row=3, column=5)
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

    def undo(self):
        self.canvas.undo()
    
    def copier(self):
        self.canvas.copier()

    def couper(self):
        self.canvas.couper()

    def coller(self):
        self.canvas.coller()

    def supprimer(self):
        self.canvas.supprimer()

    def changerOutil(self, outil):
        self.canvas.changerOutil(outil)

    def changerCouleur(self, couleur):
        self.canvas.outline = couleur

    def changerTaille(self, taille):
        self.canvas.taille = taille

class BarreMenu(Menu):

    def __init__(self, master, *args,**kw):
        Menu.__init__(self, *args,**kw)
        self.master = master
        self.construire()

    def construire(self):
        menuFichier = Menu(self)
        menuFichier.add_command(label="Nouveau", accelerator="Ctrl+N", command=self.master.nouvelleExperience)
        menuFichier.add_command(label="Ouvrir", accelerator="Ctrl+O", command=self.master.controleur.chargerExperience)
        menuFichier.add_command(label="Enregistrer", accelerator="Ctrl+S", command=self.master.controleur.nouvelleExperience)
        menuFichier.add_separator()
        menuFichier.add_command(label="Quitter", accelerator="Ctrl+Q", command=self.master.quitter)
        self.add_cascade(label="Fichier", menu=menuFichier)

        menuEdition = Menu(self)
        menuEdition.add_command(label="Annuler objet", accelerator="Ctrl+Z", command=self.master.undo)
        menuEdition.add_separator()
        #menuEdition.add_command(label="Couper", accelerator="Ctrl+X", command=self.master.couper)
        menuEdition.add_command(label="Copier", accelerator="Ctrl+C", command=self.master.copier)
        menuEdition.add_command(label="Coller", accelerator="Ctrl+V", state="disabled", command=self.master.coller)
        menuEdition.add_separator()
        menuEdition.add_command(label="Supprimer", accelerator="Retour/Suppr", command=self.master.supprimer)
        #menuEdition.add_command(label="Refaire")
        self.add_cascade(label="Edition", menu=menuEdition)


class Vue(Tk):
    
    def __init__(self, controleur, *args,**kw):
        Tk.__init__(self, *args,**kw)
        self.geometry("+120+100")
        #self.resizable(width=FALSE, height=FALSE)
        self.controleur = controleur
        self.title("Experience Creator - Nouveau *")
        self.bind("<Control-n>", self.nouvelleExperience)
        self.bind("<Control-o>", self.controleur.chargerExperience)
        self.bind("<Control-s>", self.controleur.nouvelleExperience)
        self.bind("<Control-z>", self.undo)
        self.bind("<Control-q>", self.quitter)
        self.bind("<Control-c>", self.copier)
        #self.bind("<Control-x>", self.couper)
        self.bind("<Control-v>", self.coller)
        self.bind("<BackSpace>", self.supprimer)
        self.bind("<Delete>", self.supprimer)
        self.bind("<KeyPress>", self.__onKeyPress)
        self.bind("<KeyRelease>", self.__onKeyRelease)
        self.protocol("WM_DELETE_WINDOW", self.quitter)
        self.keysPressed = []
        self.construire()

    def construire(self):
        barreMenu = BarreMenu(self)
        self.config(menu=barreMenu)
        self.frame = mFrame(self)
        self.nouvelleExperience()

    def __onKeyPress(self, e=None):
        if(str(e.keycode) not in self.keysPressed):
            self.keysPressed.append(str(e.keycode))

    def __onKeyRelease(self, e=None):
        if(str(e.keycode) in self.keysPressed):
            self.keysPressed.remove(str(e.keycode))

    def undo(self, e=None):
        self.frame.undo()

    def copier(self, e=None):
        self.frame.copier()

    def couper(self, e=None):
        self.frame.couper()

    def coller(self, e=None):
        self.frame.coller()

    def supprimer(self, e=None):
        self.frame.supprimer()

    def confirmation(self, action, message):
        if(self.frame.modifie):
            rep = tkMsg.askquestion(action, message, icon="warning")
            if(rep == "yes"):
                return True
            else:
                return False
        return True

    def nouvelleExperience(self, e=None):
        if(self.confirmation("Nouveau", "Etes-vous sur ?")):    
            self.frame.destroy()
            self.frame = AtelierCreation(self)
            self.controleur.filename = ""
            self.title("Experience Creator - Nouveau *")
            self.frame.pack()

    def chargerExperience(self, e=None):
        if(self.confirmation("Ouvrir", "Etes-vous sur ?")):
            self.frame.destroy()
            self.frame = AtelierCreation(self)
            self.title("Experience Creator - "+self.controleur.filename)
            self.frame.pack()
            self.frame.canvas.charger(self.controleur.filename)

    def quitter(self, e=None):
        if(self.confirmation("Quitter", "Etes-vous sur ?")):
            self.quit()
            self.destroy()
        

class Controleur(object):

    def __init__(self):
        self.vue = Vue(self)
        self.filename = ""

    def nouvelleExperience(self, e=None):
        if(self.filename == ""):
            self.filename = tkFile.asksaveasfilename(filetypes=[("Postscript",".ps"),("Experience",".exp")],defaultextension=".exp")
        if(self.filename != ""):
            self.vue.title("Experience Creator - " + self.filename)
            self.vue.frame.canvas.update()
            if(re.match(r'(.*)\.ps',self.filename)):
                self.vue.frame.canvas.postscript(file=self.filename, colormode='color')
            if(re.match(r'(.*)\.exp',self.filename)):
                f = open(self.filename,"w")
                f.write(self.vue.frame.canvas.enregistrer())

    def chargerExperience(self, e=None):
        filename = tkFile.askopenfilename(filetypes=[("Postscript",".ps"),("Experience",".exp")])
        if(filename != ""):
            self.filename = filename
            self.vue.chargerExperience()

if __name__ == "__main__":
    controleur = Controleur()
    controleur.vue.mainloop()
