# This script allows one to get commit status of any github repository.
# output will be saved in a csv file




import requests, datetime, csv
from datetime import timedelta


# change this for your need
repo_url = "https://github.com/bitcoin/bitcoin"
file_name_to_save = 'samples.csv'


#slice url and get github api response
slice_url = repo_url.split('/')


# getting the api link
url = "https://api.github.com/repos/"+ slice_url[-2] + "/" + slice_url[-1] + "/stats/commit_activity"

# get the response from github api & reverse the response in order to get date wise
response = requests.get(url).json()[::-1]  # reverse the response

# declare day names
weeks = {'Sunday': 0,
         'Monday': 1,
         'Tuesday': 2,
         'Wednesday': 3,
         'Thursday': 4,
         'Friday': 5,
         'Saturday': 6}



# get today
today_name = datetime.datetime.today().strftime("%A")

# get today number
today_number = weeks[today_name]


# create an empty list, we will add all commit status to this list
dates = []

i = 0

for resp in response:

    # first response is of current week
    if i == 0:
        l1 = []
        #date needed
        j = 0
        for d in resp['days']:
            if j<=today_number:
                l1.append(d)
                j += 1
        dates.append(l1)

    else:
        l2 = []
        for d in resp['days']:
            l2.append(d)
        dates.append(l2)
    i += 1
# 	dates.append(resp['days'])

final_dates = []

for l in dates:
    for p in l[::-1]:
        final_dates.append(p)


today_d = datetime.datetime.date(datetime.datetime.now())

i = 0

for d in final_dates:


    fields=[]

    fields.append(str(today_d - timedelta(days=i)))
    fields.append(str(d))

    with open(file_name_to_save, 'a+') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    i += 1


print(f"{i+1} Data saved to csv!")