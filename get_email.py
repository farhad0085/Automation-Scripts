import datetime
import email
import imaplib
import mailbox
import re
from openpyxl import Workbook
import openpyxl, xlsxwriter
import os.path



file_name_to_save = "emails.xlsx"


if not os.path.exists(file_name_to_save):
	print("File not found!, I am creating a file.")
	cr = xlsxwriter.Workbook(file_name_to_save) 
	ex = cr.add_worksheet()
	ex.write('A1','Email')
	cr.close()
	print("File created!")


# Function to search for a key value pair  
def search(key, value, con):  
    result, data = con.search(None, key, '"{}"'.format(value)) 
    return data


EMAIL_ACCOUNT = input("Enter your gmail address : ")
PASSWORD = input("Enter your password : ")

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(EMAIL_ACCOUNT, PASSWORD)

mail_boxs = mail.list()

mail.select('inbox')

search_string = input("Enter you search string here... : ")

print("Please wait while getting data...", end="")

data = search('X-GM-RAW', search_string, mail)
messageIdx = data[0].decode().split()

uids = []


for midx in messageIdx: #I'm just doing the first out of the list in this case
    resp, data = mail.fetch(midx, "(UID)")
    uids.append(data[0].decode().split()[-1][:-1])

datas = uids

print("...done!")

print(f"Number of result : {len(datas)}")


# now its time to save the data

book = openpyxl.load_workbook(file_name_to_save)
sheet = book.active


emails_set = set()



for data in datas:
    latest_email_uid = data
    result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    # result, email_data = conn.store(num,'-FLAGS','\\Seen') 
    # this might work to set flag to seen, if it doesn't already
    raw_email = email_data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    # Header Details
    date_tuple = email.utils.parsedate_tz(email_message['Date'])
    if date_tuple:
        local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))

    email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
    #subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))


    # I no longer need this
    # print(email_from)
    # print(subject)


    #find the email using regex
    clean_email = re.findall(r'[\w\.-]+@[\w\.-]+', email_from)


    #print(clean_email[0])

    # add the emails to email set
    emails_set.add(clean_email[0])


for unique_email in emails_set:
	l = []
	l.append(unique_email)
	sheet.append(tuple(l))

	book.save(file_name_to_save)

#worksheet.write(row, column, clean_email[0]) 

# incrementing the value of row by one 
# with each iteratons. 

