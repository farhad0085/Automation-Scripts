import xml.etree.ElementTree as ET
import sqlite3 as db

conn = db.connect("emaildb.db")
curr = conn.cursor()

curr.execute("create table 'emails'")

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
    emaillist.append(email.lower())

emailslist = list(dict.fromkeys(emaillist))

for email in emailslist:
    sql = "INSERT INTO emails (emailid) VALUES ('" + email +"')"
    curr.execute(sql)
    conn.commit()
    print("email added")