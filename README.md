# XML Phone Book Database 
## (from Fritz!Box Router/App[xml] or iCloud Contacts [vcf to xml])
##### (sqlite3)
Create a SQLite3 database via import of XML file created by Fritz!Box* or Fritz!Fon* App. 
As a second option a vCard.vcf file exported from Apple iCloud* contacts could converted to xml and afterwards imported in a SQLite3 database.
This second option create a database with post address, birthday and notes from your iPhone* contacts.


![XML Phone Book Database](Pictures/XML_Phone_Book_Database_20210307_db_tb.jpg?raw=true)
Fig. 1: Phone Book

![XML Phone Book Database Search](Pictures/XML_Phone_Book_Database_20210307_search_tb.jpg?raw=true)
Fig. 2: Phone Book - Search

With this Gui an xml file import will create a sqlite3 database. 
XML Import from FritzFon app has no uniqueid. This can be created via button *Create uid*. Also the Primary Key and the Foreign Key of the database tables,
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

## Licence
The software useing the MIT-Licence.#

## Notes:
</br>*This is a private project and have nothing to do with the German company AVM or with the US company Apple! 
</br>*The name Fritz!Box and Fritz!Fon are copyright by AVM* and iPhone and iCloude are copyright by Apple*

