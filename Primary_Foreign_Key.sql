/* Define Primary Key and Foreign Key to uniqueid column   */
/* Contacts table with Primary Key  */
CREATE TABLE "contacts_backup" (
            "index" INTEGER,
            "realName" TEXT,
            "category" TEXT,
            "uniqueid" INTEGER,
            "mod_time" TEXT,
            "mod_date" TEXT,
            "imageURL" TEXT
            );

INSERT INTO "contacts_backup" SELECT * FROM "contacts";      

DROP TABLE "contacts";

CREATE TABLE "contacts" (
            "index" INTEGER,
            "realName" TEXT,
            "category" TEXT,
            "uniqueid" INTEGER PRIMARY KEY,
            "mod_time" TEXT,
            "mod_date" TEXT,
            "imageURL" TEXT
            );
            
INSERT INTO "contacts" SELECT * FROM "contacts_backup";

DROP TABLE "contacts_backup";

/* Numbers table with Foreign Key on uniqueid column */
CREATE TABLE "numbers_backup" (
            "index" INTEGER,
            "realName" TEXT,
            "nid" TEXT,
            "number" TEXT,
            "type" TEXT,
            "prio" TEXT,
            "id" TEXT,
            "quickdial" TEXT,
            "uniqueid" INTEGER
            );

INSERT INTO "numbers_backup" SELECT * FROM "numbers";      

DROP TABLE "numbers";

CREATE TABLE "numbers" (
          "index" INTEGER,
          "realName" TEXT,
          "nid" TEXT,
          "number" TEXT,
          "type" TEXT,
          "prio" TEXT,
          "id" TEXT,
          "quickdial" TEXT, 
          "uniqueid" INTEGER,
          FOREIGN KEY(uniqueid) REFERENCES contacts(uniqueid)
          );
          
INSERT INTO "numbers" SELECT * FROM "numbers_backup";

DROP TABLE "numbers_backup";

/* Emails table with Foreign Key on uniqueid column */
CREATE TABLE "emails_backup" (
          "index" TEXT,
          "realName" TEXT,
          "email" TEXT,
          "classifier" TEXT, 
          "uniqueid" INTEGER
          );

INSERT INTO "emails_backup" SELECT * FROM "emails";      

DROP TABLE "emails";

CREATE TABLE "emails" (
          "index" TEXT,
          "realName" TEXT,
          "email" TEXT,
          "classifier" TEXT, 
          "uniqueid" INTEGER,
          FOREIGN KEY(uniqueid) REFERENCES contacts(uniqueid)
          );
          
INSERT INTO "emails" SELECT * FROM "emails_backup";

DROP TABLE "emails_backup"; 

/* Address table with Foreign Key on uniqueid column */
CREATE TABLE "address_backup" (
          "index" INTEGER,
          "realName" TEXT,
          "aid" TEXT,
          "pobox" TEXT,
          "ext" TEXT,
          "street" TEXT,
          "locality" TEXT,
          "region" TEXT,
          "code" TEXT,
          "country" TEXT,
          "label" TEXT,
          "type" TEXT,
          "prio" TEXT,
          "id" TEXT, 
          uniqueid INTEGER);
          
INSERT INTO "address_backup" SELECT * FROM "address";      

DROP TABLE "address";

CREATE TABLE "address" (
          "index" INTEGER,
          "realName" TEXT,
          "aid" TEXT,
          "pobox" TEXT,
          "ext" TEXT,
          "street" TEXT,
          "locality" TEXT,
          "region" TEXT,
          "code" TEXT,
          "country" TEXT,
          "label" TEXT,
          "type" TEXT,
          "prio" TEXT,
          "id" TEXT,
		      "uniqueid" INTEGER,
          FOREIGN KEY(uniqueid) REFERENCES contacts(uniqueid)
          );
          
INSERT INTO "address" SELECT * FROM "address_backup";

DROP TABLE "address_backup"; 

/* Birthday table with Foreign Key on uniqueid column */
CREATE TABLE "birthday_backup" (
          "index" INTEGER,
          "realName" TEXT,
          "bday" TIMESTAMP,
          uniqueid INTEGER);
          
INSERT INTO "birthday_backup" SELECT * FROM "birthday";      

DROP TABLE "birthday";

CREATE TABLE "birthday" (
          "index" INTEGER,
          "realName" TEXT,
          "bday" TIMESTAMP,
		      "uniqueid" INTEGER,
          FOREIGN KEY(uniqueid) REFERENCES contacts(uniqueid)
          );
          
INSERT INTO "birthday" SELECT * FROM "birthday_backup";

DROP TABLE "birthday_backup";

/* Note table with Foreign Key on uniqueid column */
CREATE TABLE "note_backup" (
          "index" INTEGER,
          "realName" TEXT,
          "note" TEXT,
          uniqueid INTEGER);
          
INSERT INTO "note_backup" SELECT * FROM "note";      

DROP TABLE "note";

CREATE TABLE "note" (
          "index" INTEGER,
          "realName" TEXT,
          "note" TEXT,
		      "uniqueid" INTEGER,
          FOREIGN KEY(uniqueid) REFERENCES contacts(uniqueid)
          );
          
INSERT INTO "note" SELECT * FROM "note_backup";

DROP TABLE "note_backup"; 