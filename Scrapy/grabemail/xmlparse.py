import xml.etree.ElementTree as ET
import sqlite3 as db

conn = db.connect("emaildb.db")
curr = conn.cursor()

curr.execute("""CREATE TABLE IF NOT EXISTS "emails" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"email"	TEXT
)""")

tree = ET.parse('data.xml')
root = tree.getroot()

# all items data
print('Expertise Data:')

emails = []

for elem in root:
   for subelem in elem:
       for subsub in subelem:
           emails.append(subsub.text)

emails = list(dict.fromkeys(emails))
emaillist = []
for email in emails:
	if not len(email) > 60 and not email.endswith(".png") and not email.endswith(".jpg") and not email.endswith(".jpeg") and not email.endswith(".js"):
		emaillist.append(email.lower())

emailslist = list(dict.fromkeys(emaillist))

print("Total Email : " + str(len(emailslist)))

i = 1
for email in emailslist:
    sql = "INSERT INTO emails (email) VALUES ('" + email +"')"
    curr.execute(sql)
    conn.commit()
    print(str(i) + " email added to database")
    i += 1