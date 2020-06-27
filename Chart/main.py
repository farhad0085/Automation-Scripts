#!/usr/bin/env python
# coding: utf-8
import csv
import matplotlib.pyplot as plt
from dateutil.parser import parse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from email.mime.base import MIMEBase
from email import encoders


# change this with your info
MY_ADDRESS = 'your_email_address_here' # example@gmail.com
PASSWORD = 'your_password' # note if your actual password doesn't work, try creating a app password from you google account and use that instead.
SERVER = 'smtp.gmail.com'
PORT = 587 # 587 for tls


csv_file_name = 'data.csv'
email_recipient = "enter_recipient_email_here"
report_file_name = "report.png" # supported formats: eps, pdf, pgf, png, ps, raw, rgba, svg, svgz)


# methods
def get_scraper_names(csv_file_name):
    scraper = set()
    with open(csv_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            elif line_count == 1:
                line_count += 1
            else:
                scraper.add(row[0])
                line_count += 1
    return list(scraper)

def get_headers(csv_file_name):
    scraper = list()
    with open(csv_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                scraper = row
                line_count += 1
            elif line_count == 1:
                line_count += 1
            else:
                line_count += 1
    return scraper


def get_rows(csv_file_name):
    rows = []
    with open(csv_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:

            if line_count == 0:
                line_count += 1
            elif line_count == 1:
                line_count += 1
            else:
                rows.append(row)
                line_count += 1

    return rows


def send_mail(email, report_file, server=SERVER, port=PORT):
    print("Trying to login...")
    # set up the SMTP server
    s = smtplib.SMTP(host=server, port=port)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    print("Logged in successfully!")

    print("Sending email...")

    msg = MIMEMultipart()       # create a message

    # setup the parameters of the message
    msg['From'] = MY_ADDRESS
    msg['To'] = email
    msg['Subject'] = "Report"
    
    # add in the message body
    msg.attach(MIMEText("Check the attachment", 'plain'))

    part = MIMEBase('application', "octet-stream")
    with open(report_file.name, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                    'attachment; filename="{}"'.format(Path(report_file.name).name))
    msg.attach(part)
    
    # send the message via the server set up earlier.
    s.send_message(msg)

    print("Email sent!")
        
    # Terminate the SMTP session and close the connection
    s.quit()



scraper_names = get_scraper_names(csv_file_name)
headers = get_headers(csv_file_name)
rows = get_rows(csv_file_name)



i = 1
plt.rcParams["figure.figsize"] = (30,30)

print("Creating Report...hold on")

fig = plt.figure()

scraper_number = len(scraper_names)
ax = [None] * ((scraper_number*5) + 1)
for scraper in scraper_names:
    
    
    dates = []
    durations = []
    rowsScraped = []
    cpu_avg = []
    cpu_max = []
    ram_avg = []
    ram_max = []
    for row in rows:
        if row[0] == scraper:
            # x axis values 
            date = row[2]
            # corresponding y axis values 
            duration = int(row[1])
            rowScrape = int(row[4])
            dates.append(date)
            rowsScraped.append(rowScrape)
            durations.append(duration)
            cpu_avg.append(int(row[5]))
            cpu_max.append(int(row[6]))
            ram_avg.append(float(row[7]))
            ram_max.append(int(row[8]))

    # get larger date
    dt = parse(dates[0])
    for date in dates:
        if dt < parse(date):
            dt = parse(date)
    
    
    c_avg = 0
    c_max = 0
    r_avg = 0
    r_max = 0

    for row in rows:
        if row[0] == scraper:
            if parse(row[2]) == dt:
                keywordScraped = row[3]
                c_avg = int(row[5])
                c_max = int(row[6])
                r_avg = float(row[7])
                r_max = int(row[8])
            
    
    
    # row 1
    ax[i] = fig.add_subplot(scraper_number, 5, i)
    
    #plotting the points  
    ax[i].plot(dates, durations) 
      
    # naming the x axis 
    ax[i].set_xlabel('Date') 
    # naming the y axis 
    ax[i].set_ylabel(scraper, fontsize=20) 
      
    # giving a title to my graph 
    ax[i].title.set_text('Duration')
    
    i += 1
    
    
    
    # row 2
    ax[i] = fig.add_subplot(scraper_number, 5, i)
    #plotting the points  
    ax[i].plot(dates, rowsScraped) 
      
    # naming the x axis 
    ax[i].set_xlabel('Date') 
      
    # giving a title to my graph 
    ax[i].title.set_text('Rows Scraped')
    
    i += 1
    
    
    # row 3
    ax[i] = fig.add_subplot(scraper_number, 5, i)
    #plotting the text  
    ax[i].text(0.5, 0.5,keywordScraped,horizontalalignment='center',verticalalignment='center',fontsize=15,transform = ax[i].transAxes)
    #ax3.plot()
    # naming the x axis 
    ax[i].set_xlabel('Date')
    ax[i].patch.set_visible(False)
    ax[i].axis('off')
      
    # giving a title to my graph 
    ax[i].title.set_text('Keywords Scraped')
    
    i += 1
    
    
    
    
    # row 4
    ax[i] = fig.add_subplot(scraper_number, 5, i)
    #plotting the points  
    ax[i].plot(dates, cpu_max, color='r', label="Max")
    ax[i].plot(dates, cpu_avg, color='g', label="Average")

    ax[i].legend(loc="upper right")
      
    # naming the x axis 
    ax[i].set_xlabel('Date') 
      
    # giving a title to my graph 
    ax[i].title.set_text('CPU')
    
    i += 1
    
    # print(dates)
    # print(cpu_max)
    # print(cpu_avg)
    
    
    # row 5
    ax[i] = fig.add_subplot(scraper_number, 5, i)
    #plotting the points  
    ax[i].plot(dates, ram_max, color='r', label="Max")
    ax[i].plot(dates, ram_avg, color='g', label="Average")
    
    ax[i].legend(loc="upper right")

    # naming the x axis 
    ax[i].set_xlabel('Date') 
      
    # giving a title to my graph 
    ax[i].title.set_text('RAM')
    
    i += 1

    # show max and average CPU and RAM
    print("")
    print("For", scraper)
    print("Average CPU : ", c_avg)
    print("Maximum CPU : ", c_max)
    print("Average RAM : ", r_avg)
    print("Maximum RAM : ", r_max)
    print("")

    # print(dates)
    # print(ram_max)
    # print(ram_avg)
    
    
    # function to show the plot 
    #plt.show()
    #plt.clf()
    #fig.savefig(f'report.png', bbox_inches='tight')
    
    #i += 1

fig.savefig(report_file_name, bbox_inches='tight')
print("Report saved!")
#fig.show()

report_file = open(report_file_name)

# now send email
send_mail(email_recipient, report_file)