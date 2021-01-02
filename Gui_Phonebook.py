############################################################
# Program to read XML Phonebook, exported from
# a AVM Frit!Box Router 7590 and import the
# data to a sqlite3 database with two tables
# contacts: realNam, category, uniqueid, mod_time
# numbers: realName, nid, number, type, prio, id, quickdial
# emails: 
#
# Test files:
# - Phonebook XML Export from AVM Fritz!Box - Base w/wo picture
# - Phonebook XML Export from AVM Fon App - iPhone
# - Phonebook XMM Import from AVM Fon APP and Export
#   from AVM Fritz!Box
#
# "uniqueid" will be used as Primary Key in sqlite database
# XML Export from AVM Fon App doesn't come with "uniqueid"!
#
# This is Open Source - only for private use without any
# - warrenty,
# - no relation with the German Company AVM!
#
# Author (Pseudonym): Hermann12; Date: 24.12.2020
############################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import Menu
from tkinter import filedialog
import sqlite3
import os
import shutil

from xml_pandas_sqlite import read_xml
from create_uid import create_uniqueid
from primary_foreign_key import create_key


############################################################
# 
#
############################################################
class Phonebook:
    """ Address Book Aplication """
    def __init__(self, master):
        self.master = master
        master.title('XML Phone Book Database')
        # master.iconbitmap('vCard.ico')
        
        mainframe = tk.Frame(master,width=1200, height=30) #background="lightgrey"
        mainframe.grid(row=0, column=0)
        mainframe.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1)
        self.read_xml = read_xml
        
###################################################################        
# Tab Phone & Tab Addresss / E-Mail / Pictures SQLite DB     
#
###################################################################
        # Tab Control
        style = ttk.Style(mainframe)
        style.configure('lefttab.TNotebook', tabposition='n,w')
        style.configure('TNotebook.Tab', padding=(30, 10, 30, 5))
        style.configure("TNotebook", background='lightgrey', foreground='white')
        

        tabControl =ttk.Notebook(mainframe, style='lefttab.TNotebook')

        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text=" Phone Book  ")

        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text=" Address (Mail) ")

        tabControl.grid(row=0, column=0, sticky="w")
        
        frame_tab1=tk.Frame(tab1, width=1200, height=30) #background="lightgrey"
        frame_tab1.grid(row=0, column=0, padx=(10,10), pady=(10,10))
        frame_tab1.grid_rowconfigure(0, weight=1)
        frame_tab1.grid_columnconfigure(0, weight=1)

        frame_tab2=tk.Frame(tab2, width=1200, height=100)  # background="lightgrey"
        frame_tab2.grid(row=0, column=0, padx=(10,10), pady=(10,10))
        frame_tab2.grid_rowconfigure(0, weight=1)
        frame_tab2.grid_columnconfigure(0, weight=1)


        # Frames of tab1
        
        frame_rep=tk.Frame(frame_tab1, width=600, height=400) #background="lightgrey"
        frame_rep.grid(row=1, column=0, padx=(5,5), pady=(5,5))
        
        frame_search=tk.Frame(frame_tab1, width=600, height=400) #background="orange"
        frame_search.grid(row=1, column=1, padx=(5,5), pady=(5,5))
        
        frame_db_file=tk.Frame(frame_tab1, width=1200, height=100) #background="red"
        frame_db_file.grid(row=2, columnspan=2, padx=(5,5), pady=(5,5))
        
        frame_xml_file=tk.Frame(frame_tab1, width=1200, height=100) #background="lightgrey"
        frame_xml_file.grid(row=3, columnspan=2, padx=(5,5), pady=(5,5))

        
###################################################################
# Frame rep - Value Representation
#
###################################################################        
        address_frame = ttk.LabelFrame(frame_rep, text = "Phone Book Entry")
        address_frame.grid(row=0, column=0, padx = (5,3), pady=(15,15), sticky='nw')

        self.realName = tk.StringVar()
        self.phone_home = ['']
        self.mobile = ['']
        self.business = ['']  # work - combobox
        self.fax = ['']
        self.email =['']
        self.uid_name = tk.StringVar()

        ttk.Label(address_frame, text="Indicated Name: ").grid(row=0, column=0, padx=(20,5), pady=(20,5), sticky='E')
        ttk.Label(address_frame, text = "private: ").grid(row=1, column=0, padx=(20,5), pady=(15,5), sticky='E')
        ttk.Label(address_frame, text= "mobile: ").grid(row=2, column=0, padx=(20,5), pady=(15,5), sticky='E')
        ttk.Label(address_frame, text = "business: ").grid(row=3, column=0,padx=(20,5), pady=(15,5), sticky='E')
        ttk.Label(address_frame, text = "fax: ").grid(row=4, column=0, padx=(20,5), pady=(15,5), sticky='E')
        ttk.Label(address_frame, text = "e-mail: ").grid(row=5, column=0, padx=(20,5), pady=(15,5), sticky='E')
        ttk.Label(address_frame, text = "uniqueid: ").grid(row=6, column=0, padx=(20,5), pady=(15,20), sticky='E')


        self.e_name = ttk.Entry(address_frame, width = 40, textvariable=self.realName)
        self.e_name.grid(row=0, column=1, columnspan=3, padx=(5,20), pady=(32,5), sticky='WE')
        self.e_phone = ttk.Combobox(address_frame, width = 40)
        self.e_phone.grid(row=1, column=1, columnspan=3, padx=(5,20), pady=(15,5), sticky='WE')
        self.e_mobile = ttk.Combobox(address_frame, width = 40)
        self.e_mobile.grid(row=2, column=1, columnspan=3, padx=(5,20), pady=(15,5), sticky='WE')
      
        self.e_business = ttk.Combobox(address_frame, width = 40)
        self.e_business.grid(row=3, column=1, columnspan=3, padx=(5,20), pady=(15,5), sticky='WE')
        self.e_fax = ttk.Combobox(address_frame, width = 40)
        self.e_fax.grid(row=4, column=1, columnspan=3, padx=(5,20), pady=(15,5), sticky='WE')
        self.e_mail = ttk.Combobox(address_frame, width = 40)
        self.e_mail.grid(row=5, column=1, columnspan=3, padx=(5,20), pady=(15,5), sticky='WE')
        
        self.e_uniqueid = ttk.Entry(address_frame, width = 4, textvariable=self.uid_name, state='readonly')
        self.e_uniqueid.grid(row=6, column=1, padx=(5,5), pady=(15,20), sticky='W')
        
        self.e_uniqueid_btn = ttk.Button(address_frame, text="Create uid", command=self.create_uniqueid) # Funktion anpassen
        self.e_uniqueid_btn.grid(row=6, column=2, padx=(5,15), pady=(15,20), sticky='W')
        
        self.e_primarykey_btn = ttk.Button(address_frame, text="Primary Key", command=self.create_primary_key) # Funktion anpassen
        self.e_primarykey_btn.grid(row=6, column=3, padx=(5,15), pady=(15,20), sticky='W')
        
###################################################################
# Frame search - Search Name at database
#
###################################################################         
        # LabelFrames Search, Phone Book Entry
        # s = ttk.Style()
        # s.configure('Bold.TLabelframe.Label', font=('Default',9, 'bold'))
        # s.configure('Bold.TLabelframe.Label', foreground ='blue')
  
       
        search_f = ttk.LabelFrame(frame_search, text = "Search")  # style = "Bold.TLabelframe" 
        search_f.grid(row=0, column=0, padx = (3,5), pady=(15,15), sticky='w')
        search_f.columnconfigure(1, weight=1)
        
        self.name_search=tk.StringVar()
        self.name_search.trace_add('write', self.my_callback)
        
        self.e_name_search_text = tk.Label(search_f, text="Name: ").grid(row=0, column=0, padx=10, pady=5, sticky='E') 
        self.e_name_search = ttk.Entry(search_f, width = 30, textvariable=self.name_search)
        self.e_name_search.grid(row=0, column=1, padx=(5,1), pady=(10,20), sticky='W')

        self.e_name_btn = ttk.Button(search_f, text="A-Z", width=6, command=self.sort_lbox)
        self.e_name_btn.grid(row=0, column=2, padx=(5,5), pady=(10,20), sticky='W')

        self.lbox = tk.Listbox(search_f, width=40, height=8)
        self.lbox.bind("<Double-Button-1>", self.show_name_search) # Double click or
        self.lbox.bind('<Return>', self.show_name_search)          # return key select an item.
        self.lbox.grid(row=1, column=1, columnspan=2, rowspan=3, padx=(5,5), pady=(10,20))
        self.scrollbar = tk.Scrollbar(search_f)
        self.lbox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.grid(row=1, column=3, columnspan=2, rowspan=3, padx=1, pady=1, sticky='ns')
        self.scrollbar.config(command=self.lbox.yview)

        tk.Label(search_f, text="Select and 'return' or 'double click'").grid(row=5, column=1, padx=10, pady=5, sticky='E') # foreground='red'


        self.no_count_var = tk.StringVar()
        self.no_contact_lab = tk.Label(search_f, text="Count: ")
        self.no_contact_lab.grid(row=6, column=0, padx=10, pady=5, sticky='E')
        self.no_contact = ttk.Entry(search_f, width = 4, textvariable=self.no_count_var, state='readonly') 
        self.no_contact.grid(row=6, column=1, padx=5, pady=5, sticky='W')       
        
        
###################################################################        
# Frame db - Open sqlite DB     
#
###################################################################
        
        ### Widget 
        db_frame = ttk.LabelFrame(frame_db_file, text ="Connect SQLite database [Fritz_Phonebook.db]", borderwidth=10, relief="groove")
        db_frame.grid(row=0, columnspan=2, padx=(10,10), pady=(2,2), sticky=("w,e"))
        
        self.phone_db_var = tk.StringVar()
        self.phone_db = ttk.Entry(db_frame, textvariable=self.phone_db_var, width = 65)
        self.phone_db.grid(row=0, columnspan=6, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
        self.phone_db.focus()
        
        self.db_connect_btn = ttk.Button(db_frame, text="Connect", width=3, command=self.search_connect_db) # Funktion anpassen
        self.db_connect_btn.grid(row=0, column=7, ipadx= 75, padx=(15,15), pady=(5,10), sticky="w")

        self.db_close_btn = ttk.Button(db_frame, text="Close", width=3, command=self.close_db) # Funktion anpassen
        self.db_close_btn.grid(row=0, column=8, ipadx= 75, padx=(15,15), pady=(5,10), sticky="w")



###################################################################        
# Frame XML - Import Fritz!Box / Fritz!Fon phone book xml into     
# a new sqlite DB 
###################################################################
        self.xml_frame = ttk.LabelFrame(frame_xml_file, text ="Create SQLite database from Fritz!Box /!Fon [.xml] import - CAUTION, don't overwrite existing database!", borderwidth=10, relief="groove")
        self.xml_frame.grid(row=0, columnspan=2, padx=(10,10), pady=(2,2), sticky=("w,e"))
        
        self.phone_xml_var = tk.StringVar()
        self.phone_xml = ttk.Entry(self.xml_frame, textvariable=self.phone_xml_var, width = 65)
        self.phone_xml.grid(row=0, columnspan=6, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

        self.xml_import_btn = ttk.Button(self.xml_frame, text="Import XML", width=3, command=self.search_import_xml) # Funktion anpassen
        self.xml_import_btn.grid(row=0, column=7, ipadx= 75, padx=(15,15), pady=(5,10), sticky="w")
        
        self.xml_export_btn = ttk.Button(self.xml_frame, text="Export XML", width=3) # Funktion anpassen
        self.xml_export_btn.grid(row=0, column=8, ipadx= 75, padx=(15,15), pady=(5,10), sticky="w")        
        self.xml_export_btn.config(state=tk.DISABLED)



###################################################################
# File Menu
#
###################################################################
        
        self.master = master
        menu = Menu(self.master,tearoff=0)
        master.config(menu=menu)
        self.filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=self.filemenu)
        
        self.filemenu.add_command(label="Connect sqlite3.db", command=self.search_connect_db) # Test: self.open_db
        self.filemenu.add_command(label="Copy as", command=self.copy_as)
        self.filemenu.add_command(label="Create Primary Key", command=self.close_db)
        self.filemenu.add_command(label="Close sqlite3.db", command=self.close_db)
        self.filemenu.add_command(label="Import Phone-Book.xml", command=self.search_import_xml)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=quit, accelerator="Alt+F4")

        optionmenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Options", menu= optionmenu)
        optionmenu.add_command(label="Export Schema", command=self.export_schema)
        
        helpmenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.about_XML_phonebook)
###################################################################
# Menu Funktions of command
# 
###################################################################

 
    def menu():
        # Dummy for development
        pass
    
 
    # File Menu
            
    def search_connect_db(self):
        # search and connect sqlite.db to represent values #
        global select_connect_db
        select_connect_db = filedialog.askopenfilename(initialdir = "D:\\Daten\\Programmieren\\Python\\python_programme\\Fritz",title = "Choose your database file [sqlite3.db]", filetypes =(("sqlite3 file", "*.db"),("All Files","*.*")))
        print('Database selected',self.search_connect_db)
        # set path in entry
        self.phone_db_var.set(select_connect_db)
        # Disable XML entry, if working with a existing database  
        self.xml_import_btn.config(state=tk.DISABLED)
        self.xml_export_btn.config(state=tk.DISABLED)
        self.phone_xml.config(state=tk.DISABLED)
        self.open_db(select_connect_db)
        
              
    def open_db(self, select_connect_db):
        connection = sqlite3.connect(select_connect_db)
            
        with connection:
            cursor = connection.cursor()
            cursor.execute('SELECT SQLITE_VERSION()')
           
            data = cursor.fetchone()[0]
            print(f"SQLite version: {data}")
            print(f'Database connected.')
                
            for row in connection.execute('SELECT realName FROM contacts ORDER BY realName ASC;'):
                self.lbox.insert('end', row[0])
                    
            cursor.execute('SELECT * FROM contacts;')
            data= cursor.fetchall()
            print(f'Row in table contacts: {len(data)}')
            self.no_count_var.set(len(data))
            
            cursor.execute('SELECT COUNT(DISTINCT(realName)) FROM contacts;')
            print(f'Unique entries in realName column:',cursor.fetchone()[0])
            self.e_name_search.focus()
            
        return select_connect_db


    def sort_lbox(self):
        # update lbox with a sorted list '
        # print('sort A-Z')
        connection = sqlite3.connect(select_connect_db)
        with connection:
            cursor = connection.cursor()
            cursor.execute('SELECT SQLITE_VERSION()')
           
            data = cursor.fetchone()[0]
            print(f"SQLite version: {data}")
            print(f'Database connected.')
            
            self.lbox.delete(0,'end')
            for row in connection.execute('SELECT realName FROM contacts ORDER BY realName ASC;'):
                self.lbox.insert('end', row[0])
                # print(row[0])
        
    
    def search_import_xml(self):
        # search a AVM XML file and create a sqlite3 database #
        global select_connect_db
        global select_xml
        
        select_xml = filedialog.askopenfilename(initialdir = "D:\\Daten\\Programmieren\\Python\\python_programme\\Fritz",title = "Select XML export file from AVM Fritz!Box or Fritz!Fon [Phone_Book.xml]", filetypes =(("xml file", "*.xml"),("All Files","*.*")))
        print('XMLselected',select_xml)
        # set path in entry
        self.phone_xml_var.set(select_xml)
        # Disable DB entry, if import XML to sqlite3  
        self.phone_db.config(state=tk.DISABLED)
        self.db_connect_btn.config(state=tk.DISABLED)       
        
        print('Choose your database file name, then import xml file into database')
        # select_connect_db = filedialog.asksaveasfilename(initialdir = "D:\\Daten\\Programmieren\\Python\\python_programme\\Fritz",title = "NEW database name ? [*.db]", filetypes =(("sqlite3 file", "*.db"),("All Files","*.*")))
        select_connect_db = filedialog.asksaveasfilename(defaultextension=".db", initialdir = "D:\\Daten\\Programmieren\\Python\\python_programme\\Fritz",title = "NEW database name ? [*.db]", filetypes =(("sqlite3 file", "*.db"),("All Files","*.*")))
        print('Database name given:',self.search_connect_db)
        # set path in entry
        self.phone_db_var.set(select_connect_db)
        
        # Create SQLITE3 database
        print("XML will be imported to SQLite3 database!")
        self.read_xml(select_xml, select_connect_db)
        
        # Open Database
        self.open_db(select_connect_db)
        
        self.xml_import_btn.config(state=tk.DISABLED)
        self.xml_export_btn.config(state=tk.DISABLED)
        self.phone_xml.config(state=tk.DISABLED)
        self.phone_db.config(state=tk.NORMAL)
        self.db_connect_btn.config(state=tk.NORMAL)
        
        return select_connect_db
        
    def create_uniqueid(self):
        create_uniqueid(select_connect_db)
        
    def create_primary_key(self):    
        create_key(select_connect_db)
            

    def my_callback(self, *args):      
        # update listbox resilt if searching name
        self.clear_field()
        print (("Traced variable {}").format(self.name_search.get()))
        search_item = self.name_search.get()
        # print(type(search_item))
        
        self.lbox.delete(0, 'end')
        
        connection = sqlite3.connect(select_connect_db)
        with connection: 
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM contacts WHERE realName LIKE '%"+search_item+"%';")
            data = cursor.fetchall()
            for row in data:
                # print(row[1])
                self.lbox.insert('end', row[1])
                
    def show_name_search(self, event):
        self.clear_field()
        widget = event.widget
        selection = widget.curselection()
        
        indName = widget.get(selection[0])
        print(indName)
        print("selktierter Wert: {}".format(indName))
        
        self.realName.set(indName)
        
        
        connection = sqlite3.connect(select_connect_db)
        print('Database connected.')
        with connection: 
            cursor = connection.cursor()
            cursor.execute("SELECT number, type, prio, id, uniqueid FROM numbers WHERE realName=?;",(indName,))
            data = cursor.fetchall()
            print(data)
            
            for row in data:
                if row[1] == 'home':
                    self.phone_home.append(row[0])
                    print('HOME:',self.phone_home)
                    if len(self.phone_home) >1 and '' in self.phone_home:
                        self.phone_home.remove('')
                                       
                if row[1] == 'mobile':
                    self.mobile.append(row[0])
                    print('Mobile:',self.mobile)
                    if len(self.mobile) >1 and '' in self.mobile:
                        self.mobile.remove('')
                
                if row[1] == 'work':
                    self.business.append(row[0])
                    print(row[0])
                    print('WORK:',self.business)
                    if len(self.business) >1 and '' in self.business:
                        self.business.remove('')
                    
                if row[1] == 'fax_work':
                    self.fax.append(row[0])
                    print(row[0])
                    print('FAX_WORK:',self.fax)
                    if len(self.fax) >1 and '' in self.fax:
                        self.fax.remove('')
                    
                self.uid_name.set(row[4])
            
            
                self.e_phone['values'] = self.phone_home
                self.e_phone.current(0)
           
                self.e_mobile['values'] = self.mobile
                self.e_mobile.current(0)
        
                self.e_business['values'] = self.business # Set the value to the new list
                self.e_business.current(0) # Set the first item of the list as current item
           
                self.e_fax['values'] = self.fax
                self.e_fax.current(0)
                
            cursor.execute("SELECT email, classifier FROM emails WHERE realName=?;",(indName,))
            data = cursor.fetchall()
            print(data)
            
            for row in data:
                if row[1] == 'private' or row[1] == 'business' or row[1] == 'other' or row[1] == 'label:':
                    self.email.append(row[0])
                    print('HOME:',self.phone_home)
                    if len(self.email) >1 and '' in self.email:
                        self.email.remove('')
                        
                self.e_mail['values'] = self.email
                self.e_mail.current(0)
            
    def copy_as(self):
        try:
            files = [('Database', '*.db'), ('XML File', '*.*'), ('All Files', '*.*')] 
            filename = filedialog.asksaveasfilename(filetypes = files, defaultextension = files) 
            print("Source: ",select_connect_db)
            file_new = shutil.copy(select_connect_db, filename)
            print("Destination of copy:",filename)
        except:
            print ("No copy, because no source selected.")

    
    def close_db(self):
        self.xml_import_btn.config(state=tk.NORMAL)
        self.phone_xml.config(state=tk.NORMAL)
        self.e_name_search.delete(0,'end')
        self.phone_db.delete(0, 'end')
        self.lbox.delete(0, 'end')
        self.no_contact.configure(state=tk.NORMAL)
        self.no_contact.delete(0, 'end')
        self.no_contact.configure(state='readonly')
        self.clear_field()
        try:
            connection = sqlite3.connect(select_connect_db)
            connection.commit()
            connection.close()
            print('Database closed.')
        except:
            print("No open database to close.")
               
        
    def clear_field(self):
        self.e_name.delete(0,'end')
        self.e_phone.delete(0,'end')
        self.phone_home = ['']
        self.e_phone['values'] = self.phone_home
        self.e_mobile.delete(0,'end')
        self.mobile = ['']
        self.e_mobile['values'] = self.mobile
        self.e_business.delete(0,'end')
        self.business = ['']
        self.e_business['values'] =self.business
        self.e_fax.delete(0,'end')
        self.fax = ['']
        self.e_fax['values'] = self.fax
        self.e_mail.delete(0,'end')
        self.email = ['']
        self.e_mail['values'] = self.email
        self.e_uniqueid.configure(state=tk.NORMAL)
        self.e_uniqueid.delete(0,'end')
        self.e_uniqueid.configure(state='readonly')
        self.phone_xml.delete(0,'end')
        
    def export_schema(self):
        try:
            dbfile = select_connect_db
            connection = sqlite3.connect(dbfile)
            cursor = connection.cursor()
            cursor.execute("SELECT SQL FROM sqlite_master WHERE SQL NOT NULL") # SQL NOT NULL or type='table'
            sql_schema = open(select_connect_db+"SQL_SCHEMA_XML_READER.txt", mode="w", encoding="utf-8")
            for row in cursor.fetchall():
                print(row[0])
                sql_schema.write(f"{row[0]}\n")
            self._show_info_1()
            sql_schema.close()
            connection.close()    
        except NameError:
            self._msgBox_error_1()
            print("Database not selected or unknown")
        finally:
            print("SCHEMA writting finished!")
            


    def quit(self):
        # File | Exit 
        self.root.destroy()
        exit()
        
    def about_XML_phonebook(self):
        msg.showinfo('XML Phone Book Database','This is a beta version V0.2 (Corona): \nDate: Jan 2021 \nAuthor: Hermann12')    
        
    def _msgBox_error_1(self):
        msg.showerror('Database NameError!','Database name error!, Select a valid sqlite3 db file, please. ')
        
    def _show_info_1(self):
        msg.showinfo("SQL SCHEMA","Database Schema was written: \nSee program directory \nSQL_SCHEMA.sql")


###################################################################
# Main Program
#
###################################################################

def main():
    root = tk.Tk()
    root.geometry('1350x850+300+300')
    root.resizable(True, True)
    address_manager = Phonebook(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
    


        