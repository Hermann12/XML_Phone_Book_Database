# XML_Phone_Book_Database
Create a SQLite3 database via import of XML file created by FritzBox or FritzFon App. 
</br>*This is a private project and have nothing to do with the German company AVM! The name Fritz!Box and Fritz!Fon are copyright by AVM*

![XML Phone Book Database](https://github.com/Hermann12/XML_Phone_Book_Database/blob/main/Pictures/XML%20Phone%20Book%20Database_20210102.jpg)

With this gui an xml file can create a sqlite3 database. 
XML Import from FritzFon app has no uniqueid. This can be created via button *Create uid*. Also Primary Key and Foreign Key of the three database tables,
- contacts
- numbers
- mails
can be created by the button *Primary Key*

XML Import from FritzBox router comes with an uniqueid. This will be copied to the other tables.
Caution, if you have double entries in your phone book! This could rise some problems.

Further features are planed:
- add new contacts.
- export to Fritz!Box XML format for re-import to the Fritz!Box router
- analysis of data, double entries, empty content fields
- import vCard format from iPhone
- add a second tab for the postal address, maybe pictures


