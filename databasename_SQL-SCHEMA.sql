CREATE TABLE "contacts" (
            "index" INTEGER,
            "realName" TEXT,
            "category" TEXT,
            "uniqueid" INTEGER PRIMARY KEY,
            "mod_time" TEXT,
            "mod_date" TEXT,
            "imageURL" TEXT
            )
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
          )
CREATE TABLE "emails" (
          "index" TEXT,
          "realName" TEXT,
          "email" TEXT,
          "classifier" TEXT, 
          "uniqueid" INTEGER,
          FOREIGN KEY(uniqueid) REFERENCES contacts(uniqueid)
          )
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
          )
CREATE TABLE "birthday" (
          "index" INTEGER,
          "realName" TEXT,
          "bday" TIMESTAMP, 
          "uniqueid" INTEGER,
          FOREIGN KEY(uniqueid) REFERENCES contacts(uniqueid)
          )
CREATE TABLE "note" (
          "index" INTEGER,
          "realName" TEXT,
          "note" TEXT, 
          "uniqueid" INTEGER,
          FOREIGN KEY(uniqueid) REFERENCES contacts(uniqueid)
          )
