from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox,QPushButton
import csv
import datetime

# Load the UI file
ui_path = "interface (2).ui" # this is the path to my XML file
Ui_MainWindow, QtBaseClass = uic.loadUiType(ui_path)
#Ui_MainWindow: classe principale de l'interface utilisateur /QtBaseClass: classe de base de l'interface.

# Create a PyQt application
app = QApplication([])

# Create an instance of the UI
window = QtBaseClass()

# Set up the UI
ui = Ui_MainWindow()
ui.setupUi(window)

import csv

# Path to the CSV file
chemin_fichier_csv = "contacts.csv"

# Check if the file exists, if not, create it
try:
    # Attempt to open the file in read mode
    
    #with statement ensure that the file is properly closed when you're done working with it.
    with open(chemin_fichier_csv, mode='r', newline='', encoding='utf-8') as csvfile:
        pass  # File exists, do nothing
except FileNotFoundError:# this is an exception type
    
    # File doesn't exist, create it
    with open(chemin_fichier_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        pass  # Create an empty file
def verif(ch):
    
    test=True
    if ch.find(".")!=-1:
        pre,nom=ch.split(".")
        if not(pre.isalnum() and nom.isalnum()):
            test=False
    else:
        test=False
    return test
def validate_email(email,nom):
    # Check if the email is empty or does not contain '@' or '.'
    if (not email or '@' not in email or '.' not in email):
        # If any of the conditions are True, return False (invalid email)
        return False
    else:
        
        nom_utilisateur, domaine = email.split('@')
        
        if domaine == "isi.utm.tn":
            
            if nom_utilisateur: # Check if the username is not empty
                    if not (verif(nom_utilisateur)):
                        # If any character is not allowed, return False (invalid email)
                        return False
                
                    return check(nom_utilisateur,nom) # Call the check function to further validate the username
            else:
                # If the username is empty, return False (invalid email)
                return False
        else:
            # If the domain is not 'isi.utm.tn', return False (invalid email)
            return False


def validate_nom(nom_text ):
    test=True
    p=nom_text.find(" ")
    ch1=nom_text[:p]
    ch2=nom_text[p+1:]
    return nom_text==(ch1+" "+ch2)

def validate_phone(phone):
    if (not phone or not phone.isdigit() or len(phone) != 8 ):
        #QMessageBox.warning(window, "Warning", "Numero invalide")
        return "invalide"
    else:
        # Check if the phone number already exists in the CSV file
        existing_phones = [row[2] for row in lire_csv(chemin_fichier_csv)]
        if phone in existing_phones:
        
            return "existant"
        else:
            return "valide"


#check username
def check(nom_utilisateur,nom_text):
    space_pos=nom_text.find(" ")
    nom = nom_text[:space_pos]
    prenom = nom_text[space_pos+1:]
        # Check if either the first name or last name is not contained within the username
    if nom not in nom_utilisateur or prenom not in nom_utilisateur:
            # Show a warning message indicating that the email does not contain the first name or last name
        QMessageBox.warning(window, "Warning", "L'email ne contient pas le nom ou le prénom")
        return False
    else:
        return True


#checks if csv is empty
def is_csv_empty(chemin_fichier_csv):
    
    with open(chemin_fichier_csv, 'r', newline='') as csvfile:
        # Create a CSV reader object or iterator
        csv_reader = csv.reader(csvfile)
        try:
            # Attempt to read the first row of the CSV file
            first_row = next(csv_reader)
        except StopIteration:
            # If StopIteration exception is raised, it means the CSV file is empty
            return True
        # If the first row was successfully read, the CSV file is not empty
        return False


def on_ajouter_clicked():
    chemin_fichier_csv = "contacts.csv"  # THE PATH FOR CSV FILE 
    
    nom = ui.nom.text().strip()
    tel = ui.tel.text()
    if nom!="":
        if tel!="":
            if validate_nom(nom):
                email = generer(nom)
                ui.mail.setText(email) 
                
                validation_result = validate_phone(tel)
                
                #3 cas pour le tel
                if validation_result == "valide": #tel valide
                    if is_csv_empty(chemin_fichier_csv) or not existe(nom, chemin_fichier_csv):# If CSV file is empty or name doesn't exist
                        with open(chemin_fichier_csv, mode='a', newline='', encoding='utf-8') as fichier_csv:
                            
                            writer = csv.writer(fichier_csv)#writer object provides methods for writing data into a CSV file.
                            writer.writerow([nom, email, tel])# Writing name, email, and telephone number to the CSV file
                            
                        # Showing success message and clearing input fields
                        QMessageBox.information(window, "Succès", "Contact ajouté avec succès.")
                        ui.nom.clear()
                        ui.tel.clear()
                        ui.mail.clear()
                    else:
                        reply = QMessageBox.question(window, "Erreur", "Nom déjà existant, voulez-vous le réajouter ?",
                                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            with open(chemin_fichier_csv, mode='a', newline='', encoding='utf-8') as fichier_csv:
                                writer = csv.writer(fichier_csv)
                                writer.writerow([nom, email, tel])
                            QMessageBox.information(window, "Succès", "Contact ajouté avec succès.")
                            ui.nom.clear()
                            ui.tel.clear()
                            ui.mail.clear()
                        else:
                            pass
                elif validation_result == "existant":
                    QMessageBox.warning(window, "Warning", "Numéro de téléphone existant")
                else:
                    QMessageBox.warning(window, "Warning", "Numéro de téléphone invalide")
            else:
                QMessageBox.warning(window, "Erreur", "Nom invalide: veuillez saisir un prénom et un nom séparés par un espace.")
        else:
            QMessageBox.warning(window, "Erreur", "Veuillez tapez le telephone")
    else:
        QMessageBox.warning(window, "Erreur", "Veuillez tapez le nom")



                        
#noun exists in csv file ?
def existe(ch, chemin_fichier_csv):
    # Open the CSV file in read mode
    with open(chemin_fichier_csv, mode='r', newline='', encoding='utf-8') as f:
        # Create a CSV reader object
        lecteur_csv = csv.reader(f)
        
        # Iterate over each row in the CSV file
        for ligne in lecteur_csv:
            # Check if the specified character 'ch' is in the current row
            if ch in ligne:
                return True  # If found, return True
            
    # If 'ch' is not found in any row, return False
    return False

    
def showMessage(self):
        QMessageBox.information(self, 'Message', 'Vous avez cliqué sur le bouton.')
def lire_csv(nom_fichier):
    d=[]
    with open(nom_fichier,'r',newline='') as csvf:
        lecteur=csv.reader(csvf)
        for i in lecteur:
            d.append(i)
    return d
def refresh_nom_list():
    global donnees_csv, nom
    nom=[]
    donnees_csv = lire_csv(chemin_fichier_csv)
    for ligne in donnees_csv:
        nom.append(ligne[0])

from PyQt5.QtWidgets import QInputDialog

def on_modifier_clicked():
    refresh_nom_list()
    nom_a_modif = ui.modif.text()
    nv_mail = ui.nvMail.text()
    nv_nom = ui.nvNom.text().strip()
    if (validate_nom(nom_a_modif)):
        if nom_a_modif in nom:
            if nv_nom!="":
                if nv_mail!="":
                    if validate_nom(nv_nom):
                        if validate_email(nv_mail,nv_nom):
                            
                                # Check if the new email already exists
                                if nv_mail in [row[1] for row in donnees_csv]:
                                    QMessageBox.warning(window, "Warning", "L'email existe déjà.")
                                    return
                                # Get indices of all occurrences of the name
                                indices = [i for i, x in enumerate(nom) if x == nom_a_modif]
                                if len(indices) > 1:
                                    # If there are multiple users with the same name, prompt the user to enter the telephone number
                                    telephone, ok_pressed = QInputDialog.getText(window, "Enter Telephone Number", "Many users with the same name. Please enter the telephone number:")
                                    if ok_pressed:
                                        telephone = telephone.strip()  # Remove leading and trailing spaces
                                        if telephone.isdigit() and len(telephone) == 8:
                                            # Find the index of the user with the entered telephone number
                                            try:
                                                index = [i for i in indices if donnees_csv[i][2] == telephone][0]
                                            except IndexError:
                                                QMessageBox.warning(window, "Warning", "Numéro de téléphone non existent")
                                                return
                                        else:
                                            QMessageBox.warning(window, "Warning", "Numéro de téléphone invalide")
                                            return
                                    else:
                                        # User canceled the input dialog
                                        return
                                else:
                                    index = indices[0]
                                    
                                donnees_csv[index][1] = nv_mail
                                donnees_csv[index][0] = nv_nom
                                
                                with open(chemin_fichier_csv, mode='w', newline='', encoding='utf-8') as csvfile:
                                    writer = csv.writer(csvfile)
                                    writer.writerows(donnees_csv)
                                    
                                QMessageBox.information(window, "Succès", "Contact modifié avec succès.")
                                ui.modif.clear()
                                ui.nvMail.clear()
                                ui.nvNom.clear()
                            
                        else:
                            QMessageBox.warning(window, "Erreur", "L'email est invalide")
                    else:
                        QMessageBox.warning(window, "Erreur", "Le nouveau nom est invalide")
                else:
                    QMessageBox.warning(window, "Erreur", "veuillez entre le nouveau mail")
            else:
                QMessageBox.warning(window, "Erreur", "veuillez entre le nouveau nom")
        else:
            QMessageBox.warning(window, "Erreur", "Le nom à modifier n'existe pas.")
    else:
        QMessageBox.warning(window, "Warning", "Veuillez saisir des informations valides.")




def on_supprimer_contact():
    # Refresh nom list after adding a contact
    refresh_nom_list()
    # Get the name to delete
    nom_a_supprimer = ui.supp.text()
    
    # Check if the name exists
    if nom_a_supprimer!="":
        if nom_a_supprimer in nom:
            indices = [i for i, x in enumerate(nom) if x == nom_a_supprimer]
            if len(indices)>1:
                telephone, ok_pressed = QInputDialog.getText(window, "Enter Telephone Number", "Many users with the same name. Please enter the telephone number:")
                if ok_pressed:
                    telephone = telephone.strip()  # Remove leading and trailing spaces
                    if telephone.isdigit() and len(telephone) == 8:
                        # Find the index of the user with the entered telephone number
                        try:
                            index = [i for i in indices if donnees_csv[i][2] == telephone][0]
                            
                        except IndexError:
                            QMessageBox.warning(window, "Warning", "Numéro de téléphone non existent")
                            return
                    else:
                        QMessageBox.warning(window, "Warning", "Numéro de téléphone invalide")
                        return
                else:
                    #User canceled the input dialog
                    return
                
            else:
                index=indices[0]
            # Remove the contact from the list
            del donnees_csv[index]
            
            # Rewrite the updated data to the CSV file
            with open(chemin_fichier_csv, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(donnees_csv)
            
            QMessageBox.information(window, "Succès", "Contact supprimé avec succès.")
        else:
            QMessageBox.warning(window, "Erreur", "Le nom à supprimer n'existe pas.")
    else:
        QMessageBox.warning(window, "Erreur", "Veuillez tapez le nom à supprimer")
    ui.supp.clear()                  
def on_afficher_clicked():
    ui.list.clear()
    aff = ui.aff.text().strip()  # Get the text entered in the filter line edit and remove leading/trailing spaces
    if not aff:
        # If the filter text is empty, display all contacts
        with open(chemin_fichier_csv, mode='r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                ch = 'Nom Et Prénom : ' + row[0] + '      Email : ' + row[1] + '     Numéro : ' + row[2]
                ui.list.addItem(ch)
    else:
        # If the filter text is not empty, filter contacts based on the entered text
        filtered_contacts = []
        with open(chemin_fichier_csv, mode='r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                # Check if any part of the contact information contains the filter text
                if aff.lower() in ' '.join(row).lower():  # Convert both the filter text and contact info to lowercase for case-insensitive matching
                    filtered_contacts.append(row)
        # Display the filtered contacts
        if not filtered_contacts:
            ch=aff+"n'appartient pas a la list des contact"
            ui.list.addItem(ch)
        for contact in filtered_contacts:
            ch = 'nom=' + contact[0] + ' mail=' + contact[1] + ' num=' + contact[2]
            ui.list.addItem(ch)



def on_reintialiser_clicked():
    ui.nom.clear()
    ui.mail.clear()
    ui.tel.clear()
    ui.modif.clear()
    ui.nvMail.clear()
    ui.nvNom.clear()
    ui.aff.clear()
    ui.list.clear()
    ui.supp.clear()
def on_vider_clicked():
    pw, ok_pressed = QInputDialog.getText(window,"salut","Enter le mot de passe")
    date = datetime.date.today()
    date=str(date)
    p1=date.find("-")
    an=date[:p1]
    ch1=date[p1+1:]
    p2=ch1.find("-")
    mois=ch1[:p2]
    jour=ch1[p2+1:]
    ch=jour+"/"+mois+"/"+an
    if ok_pressed:
        if pw ==ch:
            with open(chemin_fichier_csv, mode='w'):
                pass  # Do something with the file
            QMessageBox.information(window, "Succès", "tous les contacts ont été supprimés.")
        else:
            QMessageBox.information(window, "Echec", "le mot de passe est faux")
    else:
        pass

     

def on_quitter_clicked():
    app.quit()

#tu donne nom composant de 2 chaines elle renvoie l email institutionnel
def generer(nom):
    prenom, nom = nom.split(" ")
    email_base = f"{prenom}.{nom}@isi.utm.tn"

    # Check if the base email already exists in the CSV file
    existing_emails = [row[1] for row in lire_csv(chemin_fichier_csv)]
    if email_base in existing_emails:
        # If the base email exists, find a unique email by adding a number before '@'
        i = 1
        while f"{email_base[:email_base.index('@')]}_{i}@{email_base[email_base.index('@')+1:]}" in existing_emails:
            i += 1
        return f"{email_base[:email_base.index('@')]}_{i}@{email_base[email_base.index('@')+1:]}"
    else:
        return email_base


def existe(ch, chemin_fichier_csv):
    try:
        with open(chemin_fichier_csv, mode='r', newline='', encoding='utf-8') as f:
            lecteur_csv = csv.reader(f)
            for ligne in lecteur_csv:
                if ch in ligne:
                    return True
    except FileNotFoundError:
        pass
    return False

def on_generermail():
    nom = ui.nom.text().strip()
    if validate_nom(nom):
        email = generer(nom)
        ui.mail.setText(email)
    else:
        QMessageBox.warning(window, "Erreur", "Nom invalide: veuillez saisir un prénom et un nom séparés par un espace.")

ui.generatemail.clicked.connect(on_generermail)
ui.ajouter.clicked.connect(on_ajouter_clicked)
ui.modifier.clicked.connect(on_modifier_clicked)
ui.reinitialiser.clicked.connect(on_reintialiser_clicked)
ui.vider.clicked.connect(on_vider_clicked)
ui.quitter.clicked.connect(on_quitter_clicked)
ui.afficher.clicked.connect(on_afficher_clicked)
ui.supprimer.clicked.connect(on_supprimer_contact)


window.show()

app.exec_()
