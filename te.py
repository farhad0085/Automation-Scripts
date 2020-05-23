import re
import csv

address = "Ayushmann Test Khurrana (@gaber) on TikTok | 32M Likes. 61 Fans. Watch the latest video from Gaber (@gaber)"

#find first @
at = address.find("@")
# get first half
username = address[:at]
uName = re.sub('\W+',' ', username )
fh = re.sub('\W+',' ', username ).split()


print(fh)


username = address.split()[0]
userid = address.split()[1+len(fh)-1]
userid = re.sub('\W+','', userid )

likes = address.split()[5+len(fh)-1]
follower = address.split()[7+len(fh)-1]

print(uName)
print(userid)
print(likes)
print(follower)

data = []

data.append(uName)
data.append(userid)
data.append(likes)
data.append(follower)

print(data)

f = open('numbers.csv', 'a+')

with f:
    writer = csv.writer(f)
    writer.writerow(data)
