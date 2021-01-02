############################################################
# Program to read XML Phonebook, exported from
# a AVM Frit!Box Router 7590 and import the
# data to a sqlite3 database with three tables
# contacts: realNam, category, uniqueid, mod_time, *mod_date
# numbers: realName, nid, number, type, prio, id, quickdial, *uniqueid
# emails: realName, email, classifier, *uniqueid
#
# Test files:
# - Phonebook XML Export from AVM Fritz!Box - Base w/wo picture
# - Phonebook XML Export from AVM Fon App - iPhone
# - Phonebook XMM Import from AVM Fon APP and Export
#   from AVM Fritz!Box
#
# "uniqueid" will be used as Primary Key in sqlite database
# XML Export from AVM Fon App doesn't come with "uniqueid"
#
# Author (Pseudonym): Hermann12; Date: 24.12.2020
############################################################
import pandas as pd
import xml.etree.ElementTree as ET


def read_xml(xml_file, db_name):
    """ Parse AVM XML-Phonebook, collect data
        for contacts table and
        for numbers table to prepare sqlite3
    """
    
    phonebook_tree = ET.parse(xml_file)
    phonebook_root = phonebook_tree.getroot()
    
    # Dataframe of contacts
    df_contact_column = ["realName", "category", "uniqueid", "mod_time", "mod_date", "imageURL"]
    contacts_row =[]
    
    for contacts in phonebook_root:
        contact = contacts.findall('./contact')
        for contact in contacts:
            real_Name = contact.find('./person/realName').text
            
            image_url = contact.find('./person/imageURL')
            if image_url is not None:
                image_url = image_url.text
                # print(image_url)
            else:
                image_url = None
                    
            category = contact.find('./category')
            if category is not None:
                category = category.text
            else:
                category = None
            
            uniqueid = contact.find('./uniqueid')
            if uniqueid is not None:
                uniqueid = uniqueid.text
            else:
                uniqueid = 0
         
            mod_time = contact.find('./mod_time')
            if mod_time is not None:
                mod_time = mod_time.text
                mod_date = date_conv(mod_time) 
            else:
                mod_time = None
                mod_date = None
                           
            # print(category, real_Name, uniqueid, mod_time, mod_date)       
            contacts_row.append({"realName":real_Name,"category":category, "uniqueid":uniqueid, "mod_time": mod_time,"mod_date": mod_date, "imageURL": image_url})
                         
            df_contacts = pd.DataFrame(contacts_row, columns = df_contact_column)
            df_contacts["realName"] = df_contacts["realName"].astype("string")
            df_contacts["category"] = df_contacts["category"].astype("string").fillna('0')
            df_contacts["uniqueid"] = df_contacts["uniqueid"].astype("int64")
            df_contacts["imageURL"] = df_contacts["imageURL"].astype("string")
            # write sqlite3 table: contacts
    db_record(df_contacts, db_name) 
    
    # print("Liste",contacts_row)
    # print("DF",df_contacts)
    # print ("DF:", df_contacts.info())
    # print(df_contacts.dtypes)
    
    
    # Dataframe of numbers
    df_numbers_column = ["realName", "nid", "number", "type", "prio", "id", "quickdial"]
    numbers_row =[]
    
    for contacts in phonebook_root:
        contact = contacts.findall('./contact')
        for contact in contacts:
            real_Name = contact.find('./person/realName').text
            # print(real_Name)
            
            nid = contact.find('./telephony').attrib.get('nid')
            # print(nid)
            
            for node in contact.findall('./telephony/number'):
                number = node.text    
                number_type = node.attrib.get('type')
                number_prio = node.attrib.get('prio')
                if number_prio is not None:
                    number_prio = node.attrib.get('prio')
                    # print('number_prio',number_prio)
                else:
                    number_prio = None
                    # print('number_prio',number_prio)
                
                number_id = node.attrib.get('id')
                if number_id is not None:
                    number_id = node.attrib.get('id')
                    # print('Number-id',number_id)
                else:
                    number_id = None
                    # print('Number-id',number_id)
                    
                quick_dial = node.attrib.get('quickdial')
                if quick_dial is not None:
                    quick_dial = node.attrib.get('quickdial')
                    # print('quick_dial',quick_dial)
                else:
                    quick_dial = None
                    # print('quick_dial',quick_dial)                  
                # print ('number:', number, 'Type:', number_type, 'prio:', number_prio, 'id:', number_id)
                numbers_row.append({'realName':real_Name, 'nid':nid, 'number': number, 'type': number_type, 'prio': number_prio, 'id': number_id, 'quickdial': quick_dial})
        # print ('numbers list:',numbers_row)
        df_numbers = pd.DataFrame(numbers_row, columns = df_numbers_column)
        df_numbers["realName"] = df_numbers["realName"].astype("string")
        df_numbers["number"] = df_numbers["number"].astype("string")
        df_numbers["prio"] = df_numbers["prio"].astype("string")
        df_numbers["id"] = df_numbers["id"].astype("string")
        df_numbers["quickdial"] = df_numbers["quickdial"].astype("string")
        # write sqlite3 table: numbers 
    db_record(df_numbers, db_name)            
        # print('DF:', df_numbers)
        # print(df_numbers.info())
        
        
    # Dataframe of mails
    df_mails_column = ["realName", "email", "classifier"]
    mails_row =[]
    
    for contacts in phonebook_root:
        contact = contacts.findall('./contact')
        for contact in contacts:
            real_Name = contact.find('./person/realName').text
            # print(real_Name)
            
            for node in contact.findall('./service/email'):
                e_mail = node.text    
                classifier = node.attrib.get('classifier')

                if e_mail is not None:
                    e_mail = node.text
                    classifier = node.attrib.get('classifier')
                    # print('email:',e_mail, classifier)
                else:
                    e_mail = None
                    classifier = None

                  
    
                mails_row.append({'realName':real_Name, 'email':e_mail, 'classifier': classifier})
                            
        df_mails = pd.DataFrame(mails_row, columns = df_mails_column)
        df_mails["realName"] = df_mails["realName"].astype("string")
        df_mails["email"] = df_mails["email"].astype("string")
        df_mails["classifier"] = df_mails["classifier"].astype("string")
        # write sqlite3 table: mails 
    db_record(df_mails, db_name)
        # print(mails_row)
        # print('DF:', df_mails)
        # print(df_mails.info())


def date_conv(time):
    """Change timestamp to readable date"""
    import datetime
    date = datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
    return date


def db_record(table, db_name):
    """write pandas dataframe to sqlite3 table: contacts, numbers"""
    import sqlite3
    con = sqlite3.connect(db_name)
    
    with con:
        
        cur = con.cursor()
        cur.execute('SELECT SQLITE_VERSION()')
        data = cur.fetchone()[0]
        print(f"SQLite version: {data}")
    
        if "uniqueid" in table:
            table.to_sql("contacts", con, if_exists="replace")
            print('Writing contacts to sqlite3 table contacts')
        if "nid" in table:
            table.to_sql("numbers", con, if_exists="replace")
            print('Writing numbers to sqlite3 table numbers')
            # Create column uniqueid to the table and copy from contacts
            # Problem:  If the contacts are twice or mulitiple
            cur.execute('ALTER TABLE numbers ADD COLUMN uniqueid INTEGER;')
            cur.execute('UPDATE numbers SET uniqueid =(SELECT uniqueid FROM contacts WHERE contacts.realName = numbers.realName);')
        if "email" in table:
            table.to_sql("emails", con, if_exists="replace")
            print('Writing e-mail addresses to sqlite3 table emails')
            # Create column uniqueid to the table and copy from contacts
            # Problem:  If the contacts are twice or mulitiple
            cur.execute('ALTER TABLE emails ADD COLUMN uniqueid INTEGER;')
            cur.execute('UPDATE emails SET uniqueid =(SELECT uniqueid FROM contacts WHERE contacts.realName = emails.realName);')
        con.commit()
    con.close()
       
if __name__ == '__main__':
    """ Input XML file definition """
    # xmlfile = select_xml
    # xmlfile = '.\\Source\\FRITZ.Box_Telefonbuch_22.12.20_1605.xml'
    # xmlfile = '.\Source\FRITZ.Box_Telefonbuch_23.12.20_2119_mitBild.xml'
    #xmlfile = '.\Source\FRITZ.Box_Telefonbuch_iPhone_import-exportIPHONE-von-Fritz22.12.20_1739.xml'
    # xmlfile = '.\Source\Telefonkontakte iPhone K 22.12.20 16 18.xml'
    read_xml()
    print('Finished')

    