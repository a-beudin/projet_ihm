from Tkinter import *
from Tix import *
from xml.dom.minidom import *
from tkFileDialog import *
from PIL import Image, ImageTk

class BoutonQuitter(Button):
    
    def __init__(self, master, *args, **kw):
        self.master = master
        Button.__init__(self, master, text="Quitter", command=self.quitter, *args, **kw)

    def quitter(self):
        self.master.quitter()

class FormulaireEntreprise(Frame):

    def __init__(self, master, *args, **kw):
        Frame.__init__(self, master, *args, **kw)
        self.master = master
        self.construire()

    def construire(self):
        Label(self, text="Entreprise").grid(row=5, column=0, columnspan=2)

        Label(self, text="Numero : ").grid(row=6, column=0)
        self.entreeNumero = Entry(self)
        self.entreeNumero.grid(row=6, column=1, ipadx=5, ipady=5, padx=10, pady=10)

        Label(self, text="Nom : ").grid(row=7, column=0)
        self.entreeNom = Entry(self)
        self.entreeNom.grid(row=7, column=1, ipadx=5, ipady=5, padx=10, pady=10)

        Label(self, text="Adresse complementaire : ").grid(row=8, column=0)
        self.entreeAdresse2 = Entry(self)
        self.entreeAdresse2.grid(row=8, column=1, ipadx=5, ipady=5, padx=10, pady=10)

        Label(self, text="Adresse : ").grid(row=9, column=0)
        self.entreeAdresse1 = Entry(self)
        self.entreeAdresse1.grid(row=9, column=1, ipadx=5, ipady=5, padx=10, pady=10)

        Label(self, text="Code postal : ").grid(row=10, column=0)
        self.entreeCodePostal = Entry(self)
        self.entreeCodePostal.grid(row=10, column=1, ipadx=5, ipady=5, padx=10, pady=10)

        Label(self, text="Ville : ").grid(row=11, column=0)
        self.entreeVille = Entry(self)
        self.entreeVille.grid(row=11, column=1, ipadx=5, ipady=5, padx=10, pady=10)

        Label(self, text="Tel : ").grid(row=12, column=0)
        self.entreeTel = Entry(self)
        self.entreeTel.grid(row=12, column=1, ipadx=5, ipady=5, padx=10, pady=10)

        Label(self, text="Fax : ").grid(row=13, column=0)
        self.entreeFax = Entry(self)
        self.entreeFax.grid(row=13, column=1, ipadx=5, ipady=5, padx=10, pady=10)

        Label(self, text="E-mail : ").grid(row=14, column=0)
        self.entreeEmail = Entry(self)
        self.entreeEmail.grid(row=14, column=1, ipadx=5, ipady=5, padx=10, pady=10)

        Label(self, text="Logo : ").grid(row=15, column=0)
        self.entreeLogo = Entry(self)
        self.entreeLogo.grid(row=15, column=1, ipadx=5, ipady=5, padx=10, pady=10)
        self.entreeLogo.bind("<FocusIn>", self.chargerFichier)
        Button(self, text="...", command=self.chargerFichier).grid(row=15, column=2)

        Label(self, text="Numero prochaine facture : ").grid(row=16, column=0)
        self.entreeNumeroFacture = Entry(self)
        self.entreeNumeroFacture.grid(row=16, column=1, ipadx=5, ipady=5, padx=10, pady=10)

    def chargerFichier(self, event=None):
        self.entreeLogo.unbind("<FocusIn>")
        options = {}
        options['filetypes'] = [('Fichier image', ('.bmp','.jpg','.jpeg','.png','.gif'))]
        chemin = askopenfilename(**options)
        if(chemin):
            self.entreeLogo.delete(0,END)
            self.entreeLogo.insert(0,chemin)

    def lireDonnees(self):
        donnees = {}
        numero = self.entreeNumero.get()
        nom = self.entreeNom.get()
        numeroFacture = self.entreeNumeroFacture.get()
        if(numero and nom and numeroFacture):
            donnees = {
                "numero" : numero,
                "nom" : nom,
                "adresse2" : self.entreeAdresse2.get(),
                "adresse1" : self.entreeAdresse1.get(),
                "code_postal" : self.entreeCodePostal.get(),
                "ville" : self.entreeVille.get(),
                "tel" : self.entreeTel.get(),
                "fax" : self.entreeFax.get(),
                "email" : self.entreeEmail.get(),
                "logo" : self.entreeLogo.get(),
                "numero_facture" : numeroFacture
                }
        return donnees
        

class FormulaireFacture(FormulaireEntreprise):

    def construire(self):
        Label(self, text="Numero de facture : ").grid(row=5, column=0)
        self.entreeNumero = Entry(self)
        self.entreeNumero.insert(0, self.master.presentateur.entreprise["numero_facture"])
        self.entreeNumero.grid(row=5, column=1, ipadx=5, ipady=5, padx=10, pady=10)

        self.entreprises = self.master.presentateur.entreprises
        for e in self.entreprises.keys():
            if(e == self.master.presentateur.selectionEntreprise):
                self.entreprise = self.entreprises[e]
        if(self.entreprise):
            b=7
            n=0
            self.varNumero = StringVar()
            Label(self, textvariable=self.varNumero).grid(row=b+n, column=1)
            if(self.entreprise.has_key("numero")):
                self.varNumero.set(self.entreprise["numero"])
            n+=1
                
            self.varNom = StringVar()
            Label(self, textvariable=self.varNom).grid(row=b+n, column=1)
            if(self.entreprise.has_key("nom")):
                self.varNom.set(self.entreprise["nom"])
            n+=1
                
            self.varAdresse1 = StringVar()
            Label(self, textvariable=self.varAdresse1).grid(row=b+n, column=1)
            if(self.entreprise.has_key("adresse1")):
                self.varAdresse1.set(self.entreprise["adresse1"])
            n+=1
                
            self.varAdresse2 = StringVar()
            Label(self, textvariable=self.varAdresse2).grid(row=b+n, column=1)
            if(self.entreprise.has_key("adresse2")):
                self.varAdresse2.set(self.entreprise["adresse2"])
            n+=1
            
            self.varCodePostalVille = StringVar()
            Label(self, textvariable=self.varCodePostalVille).grid(row=b+n, column=1)
            if(self.entreprise.has_key("code_postal") and self.entreprise.has_key("ville")):
                self.varCodePostalVille.set(self.entreprise["code_postal"]+" "+self.entreprise["ville"])
            n+=1
            
            self.varTel = StringVar()
            Label(self, textvariable=self.varTel).grid(row=b+n, column=1)
            if(self.entreprise.has_key("tel")):
                self.varTel.set("Tel : "+self.entreprise["tel"])
            n+=1
                
            
            self.varFax = StringVar()
            Label(self, textvariable=self.varFax).grid(row=b+n, column=1)
            if(self.entreprise.has_key("fax")):
                self.varFax.set("Fax : "+self.entreprise["fax"])
            n+=1

            self.varEmail = StringVar()
            Label(self, textvariable=self.varEmail).grid(row=b+n, column=1)
            if(self.entreprise.has_key("email")):
                self.varEmail.set(self.entreprise["email"])
            n+=1
                
            if(self.entreprise.has_key("logo")):
                image = Image.open(self.entreprise["logo"])
                photo = ImageTk.PhotoImage(image)
                self.labelLogo = Label(self, image=photo, width=240, height=240)
                self.labelLogo.image = photo
                self.labelLogo.grid(row=b, column=0, rowspan=n)
        
        self.mb = Menubutton(self, text="Entreprise", relief=RAISED)
        self.mb.grid(row=6,column=0)
        self.mb.menu = Menu(self.mb, tearoff=0)
        self.mb["menu"] = self.mb.menu
        for e in self.entreprises.values():
            if(e["numero"] != self.entreprise["numero"]):
                self.mb.menu.add_command(label=e["numero"]+" - "+e["nom"], command=lambda a=e:self.changerEntreprise(a))

        Label(self, text="Client").grid(row=6, column=2, columnspan=2)

        Label(self, text="Numero : ").grid(row=8, column=2, ipadx=30)
        self.varNumeroClient = StringVar()
        Entry(self, textvariable=self.varNumeroClient).grid(row=8, column=3)

        Label(self, text="Nom : ").grid(row=9, column=2, ipadx=30)
        self.varNomClient = StringVar()
        Entry(self, textvariable=self.varNomClient).grid(row=9, column=3)
        

    def changerEntreprise(self, entreprise):
        self.entreprise = entreprise
        self.entreeNumero.delete(0,END)
        self.entreeNumero.insert(0, entreprise["numero_facture"])
        if(entreprise.has_key("numero")):
            self.varNumero.set(entreprise["numero"])
        else:
            self.varNumero.set("")
        if(entreprise.has_key("nom")):
            self.varNom.set(entreprise["nom"])
        else:
            self.varNom.set("")
        if(entreprise.has_key("adresse1")):
            self.varAdresse1.set(entreprise["adresse1"])
        else:
            self.varAdresse1.set("")
        if(entreprise.has_key("adresse2")):
            self.varAdresse2.set(entreprise["adresse2"])
        else:
            self.varAdresse2.set("")
        if(entreprise.has_key("code_postal") and entreprise.has_key("ville")):
            self.varCodePostalVille.set(entreprise["code_postal"]+" "+entreprise["ville"])
        else:
            self.varCodePostalVille.set("")
        if(entreprise.has_key("tel")):
            self.varTel.set("Tel : "+entreprise["tel"])
        else:
            self.varTel.set("")
        if(entreprise.has_key("fax")):
            self.varFax.set("Fax : "+entreprise["fax"])
        else:
            self.varFax.set("")
        if(entreprise.has_key("email")):
            self.varEmail.set(entreprise["email"])
        else:
            self.varEmail.set("")
        if(entreprise.has_key("logo")):
            image = Image.open(entreprise["logo"])
            photo = ImageTk.PhotoImage(image)
            self.labelLogo.configure(image=photo)
            self.labelLogo.image = photo
            
        self.mb.menu = Menu(self.mb, tearoff=0)
        self.mb["menu"] = self.mb.menu
        for e in self.entreprises.values() :
            if(e["numero"] != entreprise["numero"]):
                self.mb.menu.add_command(label=e["numero"]+" - "+e["nom"], command=lambda a=e:self.changerEntreprise(a))

    def lireDonnees(self):
        numero = self.entreeNumero.get()
        client = {
            "numero" : self.varNumeroClient.get(),
            "nom" : self.varNomClient.get()
            }
        donnees = {}
        if(numero):
            donnees = {
                "numero" : numero,
                "entreprise" : self.entreprise,
                "client" : client
                }
        return donnees

class ModeleEntreprise(object):

    def __init__(self, entreprises, donnees):
        self.entreprises = entreprises
        self.donnees = donnees

    def enregistrer(self):
        chaine = "\
<entreprises>\n\
    <selection>"+self.donnees["numero"]+"</selection>\n"
        if(self.entreprises != []):
            for e in self.entreprises.values():
                chaine += "\
    <entreprise>\n"
                for dk in e.keys():
                    chaine += "\
        <"+dk+">"+e[dk]+"</"+dk+">\n"
                chaine += "\
    </entreprise>\n"

        chaine += "\
    <entreprise>\n"
        for dk in self.donnees.keys():
            chaine += "\
        <"+dk+">"+self.donnees[dk]+"</"+dk+">\n"
        chaine += "\
    </entreprise>\n"
        chaine += "</entreprises>"
        f = open("entreprises.xml","w")
        f.write(chaine)
        f.close()      

class ModeleFacture(object):

    def __init__(self, donnees):
        self.donnees = donnees

    def enregistrer(self):
        f = open('factures/facture_'+self.donnees["numero"]+'.html','w')

        chaine = '\
<html>\n\
    <head>\n\
        <title>facture_'+self.donnees["numero"]+'</title>\n\
        <link rel="stylesheet" href="print.css" type="text/css" media="print" />\n\
        <link rel="stylesheet" href="print.css" type="text/css" media="projection, screen, tv" />\n\
    </head>\n\
    <body>\n\
        <div id="facture">\n\
        <div id="entete">\n\
        <h1>Facture</h1>\n'
        
        chaine += '\
        <div id="entreprise">\n'

        if(self.donnees["entreprise"].has_key("logo")):
            chaine += '\
            <div id="logo">\n\
                <img src="'+self.donnees["entreprise"]["logo"]+'" alt="" />\n\
            </div>\n'

        chaine += '\
            <ul>\n\
                <li><strong>Facture n.</strong> '+self.donnees["numero"]+'</li>\n'

        if(self.donnees["entreprise"].has_key("nom")):
            chaine += '\
                <li><strong>'+self.donnees["entreprise"]["nom"]+'</strong></li>\n'

        if(self.donnees["entreprise"].has_key("numero")):
            chaine += '\
                <li><strong>Entreprise n.</strong> '+self.donnees["entreprise"]["numero"]+'</li>\n'
        
        if(self.donnees["entreprise"].has_key("adresse1")):
            chaine += '\
                <li>'+self.donnees["entreprise"]["adresse1"]+'</li>\n'

        if(self.donnees["entreprise"].has_key("adresse2")):
            chaine += '\
                <li>'+self.donnees["entreprise"]["adresse2"]+'</li>\n'

        if(self.donnees["entreprise"].has_key("code_postal") and self.donnees["entreprise"].has_key("ville")):
            chaine += '\
                <li>'+self.donnees["entreprise"]["code_postal"]+' '+self.donnees["entreprise"]["ville"]+'</li>\n'

        if(self.donnees["entreprise"].has_key("tel")):
            chaine += '\
                <li><strong>Tel</strong> '+self.donnees["entreprise"]["tel"]+'</li>\n'

        if(self.donnees["entreprise"].has_key("fax")):
            chaine += '\
                <li><strong>Fax</strong> '+self.donnees["entreprise"]["fax"]+'</li>\n'

        if(self.donnees["entreprise"].has_key("email")):
            chaine += '\
                <li><strong>E-mail</strong> '+self.donnees["entreprise"]["email"]+'</li>\n'

        chaine += '\
            </ul>\n\
        </div>\n'

        chaine += '\
        <div id="client">\n'
        if(self.donnees["client"].has_key("logo")):
            chaine += '\
            <div id="logo">\n\
                <img src="'+self.donnees["client"]["logo"]+'" alt="" />'

        chaine += '\
            <ul>\n'

        if(self.donnees["client"].has_key("nom")):
            chaine += '\
                <li><strong>'+self.donnees["client"]["nom"]+'</strong></li>\n'

        if(self.donnees["client"].has_key("numero")):
            chaine += '\
                <li><strong>N.</strong> '+self.donnees["client"]["numero"]+'</li>\n'
        
        if(self.donnees["client"].has_key("adresse1")):
            chaine += '\
                <li>'+self.donnees["client"]["adresse1"]+'</li>\n'

        if(self.donnees["client"].has_key("adresse2")):
            chaine += '\
                <li>'+self.donnees["client"]["adresse2"]+'</li>\n'

        if(self.donnees["client"].has_key("code_postal") and self.donnees["client"].has_key("ville")):
            chaine += '\
                <li>'+self.donnees["client"]["code_postal"]+' '+self.donnees["client"]["ville"]+'</li>\n'

        if(self.donnees["client"].has_key("tel")):
            chaine += '\
                <li><strong>Tel</strong> '+self.donnees["client"]["tel"]+'</li>\n'

        if(self.donnees["client"].has_key("fax")):
            chaine += '\
                <li><strong>Fax</strong> '+self.donnees["client"]["fax"]+'</li>\n'

        if(self.donnees["client"].has_key("email")):
            chaine += '\
                <li><strong>E-mail</strong> '+self.donnees["client"]["email"]+'</li>\n'

        chaine += '\
            </ul>\n\
        </div>\n'


        chaine += '\
        </div>\n\
        <div id="produits"></div>\n\
        </div>\n\
    </body>\n\
</html>'
        
        f.write(chaine)
        f.close()
        
class ParserEntreprises(object):

    def __init__(self, fichier):
        self.entreprises = {}
        self.selection = 0
        try:
            dom = parse(fichier)
            selectionNode = dom.getElementsByTagName('selection')[0].firstChild
            if(selectionNode):
                self.selection = selectionNode.nodeValue
            entreprisesNodes = dom.getElementsByTagName('entreprise')
            if(entreprisesNodes):
                for entrepriseNode in entreprisesNodes:
                    entreprise = {}
                    if(entrepriseNode):
                        for element in entrepriseNode.getElementsByTagName('*'):
                            if(element):
                                if(element.firstChild):
                                    entreprise[element.tagName] = element.firstChild.nodeValue
                                    if(element.tagName == "numero"):
                                        numero = element.firstChild.nodeValue
                        self.entreprises[numero] = entreprise
        except:
            print "Erreur de parser xml sur le fichier \"" + fichier + "\" (fichier vide ou mal forme)"
                

class Presentateur(object):

    def __init__(self):
        self.chargerEntreprise()
        self.vue = Vue(self)
        self.entreprise = {}
        if(self.entreprises == []):
            self.vue.nouvelleEntreprise()
        else:
            for e in self.entreprises.keys():
                if(e == self.selectionEntreprise):
                    self.entreprise = self.entreprises[e]
                    break

    def chargerEntreprise(self):
        parser = ParserEntreprises("entreprises.xml")
        self.entreprises = parser.entreprises
        self.selectionEntreprise = parser.selection

    def nouvelleFacture(self):
        donnees = self.vue.frame.lireDonnees()
        if(donnees):
            ModeleFacture(donnees).enregistrer()

    def nouvelleEntreprise(self):
        donnees = self.vue.frame.lireDonnees()
        if(donnees):
            ModeleEntreprise(self.entreprises, donnees).enregistrer()
            self.chargerEntreprise()

    def enregistrerModele(self):
        
        if(donnees):
            self.modele.enregistrer(donnees)


class BarreMenu(Menu):

    def __init__(self, master, *args,**kw):
        Menu.__init__(self, *args,**kw)
        self.master = master
        self.construire()

    def construire(self):
        menuFacture = Menu(self, tearoff=0)
        menuFacture.add_command(label="Nouvelle", command=self.master.nouvelleFacture)
        #menuFacture.add_command(label="Ouvrir")
        menuFacture.add_command(label="Enregistrer", command=self.master.presentateur.nouvelleFacture)
        #menuFacture.add_command(label="Enregistrer sous", command=asksaveasfile)
        menuFacture.add_separator()
        menuFacture.add_command(label="Quitter", command=self.master.quitter)
        self.add_cascade(label="Facture", menu=menuFacture)

        menuEntreprise = Menu(self, tearoff=0)
        menuEntreprise.add_command(label="Nouvelle", command=self.master.nouvelleEntreprise)
        menuEntreprise.add_command(label="Enregistrer", command=self.master.presentateur.nouvelleEntreprise)
        if(self.master.presentateur.entreprises != []) :
            menuEntreprise.add_separator()
        for p in self.master.presentateur.entreprises.keys():
            menuEntreprise.add_command(label=p+" - "+self.master.presentateur.entreprises[p]["nom"])
        self.add_cascade(label="Entreprise", menu=menuEntreprise)


class Vue(Tk):
    
    def __init__(self, presentateur, *args,**kw):
        Tk.__init__(self, *args,**kw)
        self.geometry("800x600")
        #self.resizable(width=FALSE, height=FALSE)
        self.presentateur = presentateur
        self.title("Facturier")
        self.__construire()

    def __construire(self):
        barreMenu = BarreMenu(self)
        self.config(menu=barreMenu)
        self.frame = Frame()
        #self.boutonQuitter = BoutonQuitter(self)
        #self.boutonQuitter.pack(side=RIGHT, ipadx=5, ipady=5, padx=10, pady=10)     

    def nouvelleEntreprise(self):
        self.frame.destroy()
        self.frame = FormulaireEntreprise(self)
        self.frame.pack()
        self.presentateur.nouvelleEntreprise()

    def nouvelleFacture(self):
        self.frame.destroy()
        self.frame = FormulaireFacture(self)
        self.frame.pack()
        self.presentateur.nouvelleFacture()

    def quitter(self):
        self.quit()
        self.destroy()
        
        
if __name__ == "__main__":
    presentateur = Presentateur()
    presentateur.vue.mainloop()
