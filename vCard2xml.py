############################################################
# Program read vCard from Apple iCloude contacts and create
# XML in AVM Fritz!Box style to import in
# XML_Phone_Book_Database
#
## Author (Pseudonym): Hermann12; Date: 10.01.2021
############################################################

import re
import timeit
from datetime import datetime
# import xml.etree.ElementTree as ET
# from xml.etree import ElementTree
# import xml.dom.minidom

def read_vcard(vcard_file, xml_file):
    """ Translate vCard to XML FritzFon style
    """
    output_file = xml_file # line 41
    global result
    result=[]
    contacts=[]
    result.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    result.append('<phonebooks>\n')
    result.append('<phonebook owner="1" name="vCard-translation">\n')
    
    with open(vcard_file, "r", encoding ="utf-8") as file:   
        contact=[]
        for line in file:
            if line[0] != ' ':
                contact.append(line.strip())
            else:
                line_ext = contact.pop()+line.lstrip()
                contact.append(line_ext)
                
            if re.search (r'END:VCARD', line):
                contacts.append(contact)
                contact =[]
        
                
        f = open(output_file, "w", encoding ="utf-8") # output.xml given from Gui
        for contact_set in contacts:
            numbers_list=[]
            mails_list=[]
            adr_list=[]
            bday_list=[]
            note_list=[]
            for elm in contact_set:
                if re.search (r'BEGIN:VCARD', elm):
                    #print('<contact>')
                    #print('<category></category>')
                    result.append('<contact>\n')
                    result.append('<category></category>\n')
                
                if re.search (r'^FN:', elm):
                    #print(f"<person>\n<realName>{elm.split(':')[1]}</realName>\n</person>")
                    realname = elm.strip('\n')
                    realname = re.sub('&','&amp;',realname)
                    name = realname.split(':')[1]
                    result.append(f"<person>\n<realName>{realname.split(':')[1]}</realName>\n</person>\n")
             # numbers
                if re.search (r'TEL;', elm):
                    numbers_list.append(elm)
             # mails       
                if re.search (r'EMAIL;', elm):
                    mails_list.append(elm)
                    
            # address    
                if re.search (r'.ADR;', elm):
                    adr_list.append(elm)
            
            # Note
                if re.search (r'^NOTE', elm):
                    note_list.append(elm)        
            # bDay
                if re.search (r'^BDAY;', elm):
                    bday_list.append(elm)
                    
            

                
                
                if re.search (r'REV:', elm):
                    numbers_list = write_numbers(numbers_list) # numbers from function
                    write_mails(mails_list)
                    write_adr(adr_list,name)
                    write_note(note_list)
                    write_bday(bday_list)
                    newline=elm.strip('\n') # remove '\n'
                    date_iphone = newline.split(':',1)[1]
                    mod_date = date_to_timestamp(date_iphone)
                    # print('Timestam:',mod_date)
                    # print(f"<mod_time>{newline.split(':',1)[1]}</mod_time>") # split : only one times
                    #print(f"<mod_time>{mod_date}</mod_time>")
                    result.append(f"<mod_time>{mod_date}</mod_time>\n")
                         
                if re.search (r'END:VCARD', elm):
                    #print('</contact>')
                    result.append('</contact>\n')
                    
        
        
        
        #print(contact)
    #print(contacts)
    
    result.append('</phonebook>\n')
    result.append('</phonebooks>\n')
    f.writelines(result)
    print(f"vcard file:{vcard_file} converted to:{xml_file}")
    
    
def write_numbers(numbers_list):
    nid=len(numbers_list)
    result.append(f'<telephony nid="{nid}">\n')
    #print(f"<telephony nid={nid}>\n")
    ph_id=-1
    for num in numbers_list:
        ph_id += 1
        # print(ph_id)
        number = num.split(':')[1].strip('\n')
        number_attrib_raw=num.split(':')[0]
        number_attrib= read_attrib(number_attrib_raw)
        if len(number_attrib) !=0:
            ph_attrib = f'type="{number_attrib[0]}"'
            ph_prio = f'''prio="{number_attrib[-1]}"'''
        else:
            ph_attrib=''
            ph_prio=''
        #print(f'<number {ph_attrib} {ph_prio} id="{ph_id}">{number}</number>')
        result.append(f'<number {ph_attrib} {ph_prio} id="{ph_id}">{number}</number>\n')
    #print(f"</telephony>\n")
    result.append(f"</telephony>\n")
    numbers_list =[]
    return numbers_list

def read_attrib(number_attrib_raw):
    dict_attrib = {"HOME":"home","home":"home","CELL":"mobile","cell":"mobile","WORK":"business","work":"business","MAIN":"Zentrale","main":"main","OTHER":"Andere","other":"andere"}
    dict_fax = {"FAX":"fax_","fax":"fax_"}
    dict_prio={"pref":"1"}
    # print('Type:',string_tel)
    prob=[]
    for key, val in dict_fax.items():
        if key in number_attrib_raw:
            keyval = val
            for ph_key, ph_val in dict_attrib.items():
                if ph_key in number_attrib_raw:
                    keyvalue = keyval+ph_val
                    prob.append(keyvalue)
                    for pri, val in dict_prio.items():
                        if pri in number_attrib_raw:
                            prio = '1'
                            prob.append(prio)
                        else:
                            prio = '0'
                            prob.append(prio)
                else:
                    break
    for ph_key, ph_val in dict_attrib.items():
        if ph_key in number_attrib_raw:
            valuetype = ph_val
            prob.append(valuetype)
            for pri, val in dict_prio.items():
                if pri in number_attrib_raw:
                    prio = '1'
                    prob.append(prio)
                else:
                    prio = '0'
                    prob.append(prio)   
    # print(prob)
    return prob          
    
def date_to_timestamp(date_iphone):
    datetime_object = datetime.strptime(date_iphone, '%Y-%m-%dT%H:%M:%SZ')
    timestamp = datetime.timestamp(datetime_object)
    timestamp_wo_dec= "{:.0f}".format(timestamp)
    # print(f"timestamp:{timestamp_wo_dec}")
    return timestamp_wo_dec

def write_mails(mails_list):
    result.append(f"<service>\n")
    #print(f"<service>\n")
    #print(mails_list)
    for mail in mails_list:
        mail_attrib_raw=mail.split(':')[0]
        mail_attrib= read_mailattrib(mail_attrib_raw)
        if len(mail_attrib) != 0:
            mail_attrib = f'"{mail_attrib[0]}"'
        else:
            mail_attrib = f'"label"'
        mail_add = mail.split(':')[1].strip('\n')
        #print(f'<email classifier={mail_attrib}>{mail_add}</email>\n')
        result.append(f'<email classifier={mail_attrib}>{mail_add}</email>\n')
    #print(f"</service>\n")
    result.append(f"</service>\n")
    mails_list =[]
    return mails_list

def read_mailattrib(mail_attrib_raw):
    dict_attrib = {"HOME":"private","home":"private","WORK":"business","work":"business"}
    prob_m=[]
    for key, val in dict_attrib.items():
        if key in mail_attrib_raw:
            keyval = val
            prob_m.append(keyval)
    #print(prob_m)
    return prob_m

def xml_to_string(s):
    string1=""
    return (string1.join(s))

def write_adr(adr_list, name):
    #print(adr_list)
    if len(adr_list) != 0:
        add_nid = len(adr_list)
        result.append(f'<adr aid="{add_nid}">\n')
    else:
        result.append(f'<adr>\n')
    
    adr_id=-1    
    for adr_elm in adr_list:
        result.append(f'<parameters>\n')
        adr_id += 1
        adr_content_raw=adr_elm.split(':')[1]
        adr_attrib_raw=adr_elm.split(':')[0]
        #print(adr_attrib_raw)
        if "type=pref" in adr_attrib_raw:
            prio = 1
        else:
            prio = 0
        
        adr_dict_attrib = {"HOME":"home","home":"home","WORK":"work","work":"work"}
        for adr_key, adr_val in adr_dict_attrib.items():
            if adr_key in adr_attrib_raw:
                adr_typ = adr_val
            else:
                adr_typ ='others'

        result.append(f'<label type="{adr_typ}" prio="{prio}" id="{adr_id}">\n')
        adr_content = adr_content_raw.replace(";",",")
        result.append(f'{name},{adr_content}')
        result.append(f'</label>\n')
        result.append(f'</parameters>\n')
        #print(adr_content_raw.split(";"))
        #print(adr_content_raw.split(";")[-1])
    
        addr_elm = adr_content_raw.split(";")
        #print(addr_elm)
        #print (name, len(addr_elm))
        
        if len(addr_elm) >7:
            if addr_elm[-1] =='' or addr_elm[-1] =='\n':
                result.append(f'<pobox>{addr_elm[-8]}</pobox>\n')
        else:
            result.append(f'<pobox>{addr_elm[-7].strip()}</pobox>\n')
        
        if addr_elm[-1] =='' or addr_elm[-1] =='\n':
            result.append(f'<ext>{addr_elm[-7]}</ext>\n')
        else:
            result.append(f'<ext>{addr_elm[-6].strip()}</ext>\n')
        
        if addr_elm[-1] =='' or addr_elm[-1] =='\n':
            result.append(f'<street>{addr_elm[-6]}</street>\n')
        else:
            result.append(f'<street>{addr_elm[-5].strip()}</street>\n')
        
        if addr_elm[-1] =='' or addr_elm[-1] =='\n':
            result.append(f'<locality>{addr_elm[-5]}</locality>\n')
        else:
            result.append(f'<locality>{addr_elm[-4].strip()}</locality>\n')
        
        if addr_elm[-1] =='' or addr_elm[-1] =='\n':
            result.append(f'<region>{addr_elm[-4]}</region>\n')
        else:
            result.append(f'<region>{addr_elm[-3].strip()}</region>\n')
        
        if addr_elm[-1] =='' or addr_elm[-1] =='\n':
            result.append(f'<code>{addr_elm[-3]}</code>\n')
        else:
            result.append(f'<code>{addr_elm[-2].strip()}</code>\n')
        
        if addr_elm[-1] =='' or addr_elm[-1] =='\n':
            result.append(f'<country>{addr_elm[-2]}</country>\n')
        else:
            result.append(f'<country>{addr_elm[-1].strip()}</country>\n')
     
    result.append(f"</adr>\n")
 
def write_note(note_list):
    if len(note_list)>0:
        for elm in note_list:
            note = elm.replace("NOTE:","").strip()
            note = re.sub(r"&(?!amp;)","&amp;", note)
            result.append(f'<note>{note}</note>\n')
    else:
        result.append(f'<note></note>\n')
 
 
def write_bday(bday_list):
    if len(bday_list)>0:
        for elm in bday_list:
            bday=elm.split(':')[1]
            result.append(f'<bday>{bday}</bday>\n')
    else:
        result.append(f'<bday></bday>\n')
    
    
if __name__ == '__main__':
    """ Input vCard file definition """
    starttime=timeit.default_timer()
    vcard_file = r"intern_Source\\vCard_iCloude_Kontakte_iPhone_266_20201224.vcf"
    read_vcard(vcard_file)   
    print('Finished')
    print("Laufzeit:", timeit.default_timer()-starttime)
                