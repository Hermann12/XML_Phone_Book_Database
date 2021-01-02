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