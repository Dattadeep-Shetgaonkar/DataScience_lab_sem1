import datetime

currentDateTime=datetime.datetime.now()
print(currentDateTime)

month={
 "01":"January",
 "02":"February",
 "03":"March",
 "04":"April",
 "05":"May",
 "06":"June",
 "07":"July",
 "08":"August",
 "09":"September",
 "10":"October",
 "11":"November",
 "12":"December",
 }
 

def getMonthName(dt):
	dt_str=str(dt)
	monthNum=dt_str.split('-')
	monthNum=monthNum[1]
	return month[monthNum]

def getDate(dt):
	month=getMonthName(dt)
	dateNum=((((str(dt)).split(" "))[0]).split("-"))[2]
	datesuffix="th"
	# Fix suffix for 11, 12, 13
	if 11 <= int(dateNum) <= 13:
		datesuffix = "th"
	else:
		if int(dateNum) % 10 == 1:
			datesuffix = "st"
		elif int(dateNum) % 10 == 2:
			datesuffix = "nd"
		elif int(dateNum) % 10 == 3:
			datesuffix = "rd"
	return(dateNum + datesuffix +" "+ month)
	
def getTime(dt):
	time=((((str(dt)).split(" "))[1]).split(":"))[0]	
	t=int(time)
	if 6 <= t < 12:
		return "Morning"
	elif 12 <= t < 15:
		return "Afternoon"
	elif 15 <= t < 21:
		return "Evening"
	else:
		return "Night"

print(getDate(currentDateTime),end=" ")
print(getTime(currentDateTime))