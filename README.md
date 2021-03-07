# XML_Phone_Book_Database
Create a SQLite3 database via import of XML file created by FritzBox or FritzFon App. 
</br>*This is a private project and have nothing to do with the German company AVM! The name Fritz!Box and Fritz!Fon are copyright by AVM*
As a scond option a vCard.vcf file exported from Apple iCloud contacts could converted to xml and afterwards imported in a SQLite3 database.
This second option create a database with post address, birthday and notes from your iPhone contacts.


![XML Phone Book Database](Pictures/XML_Phone_Book_Database_20210307_db_tb.jpg?raw=true)

With this Gui an xml file import will create a sqlite3 database. 
XML Import from FritzFon app has no uniqueid. This can be created via button *Create uid*. Also the Primary Key and the oreign Key of the database tables,
- contacts
- numbers
- emails
- address
- birthday
- note
can be created by the button *Primary Key*

XML Import from FritzBox router comes with an uniqueid. This will be copied to the other tables.
Caution, if you have double entries in your phone book! This could rise some problems.

Next features for implementation:
- add new contacts to the database
- export as Fritz!Box XML format for re-import to the Fritz!Box router
- analysis of data, double entries, empty content fields
- complete second tab for the postal address, birthdays, maybe pictures

