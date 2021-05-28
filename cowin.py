import requests
import datetime
import schedule
import time




#========================================== vacNotif Function starts==============================
def vacNotif():

    theday = datetime.date.today()
    start = theday - datetime.timedelta(days=0)
    dates = [start + datetime.timedelta(days=d) for d in range(3)]

    #=====================================================================

    listOfAllCentresFor45=[]
    listOfAllCentresFor18=[]

    for d in dates:
        todayDate=str(d.strftime("%d-%m-%Y"))
        url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=581&date={0}'.format(todayDate)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}
        x = requests.get(url, headers=headers)
        data = x.json()

        count_1=1
        count_2=1
        centre_detail_1 = ""
        centre_detail_2 = ""

        centre_detail_1 = centre_detail_1 + "Date: "+ todayDate + "\n\n" 
        centre_detail_2 = centre_detail_2 + "Date: "+ todayDate + "\n\n"

        for d in data["sessions"]:
            if d["min_age_limit"] == 45:
                if d["available_capacity_dose1"] > 0:
                    centre_detail_1 =centre_detail_1 + "Centre {0}: ".format(count_1) + "\nCentre Adrress: " + d['name'] + ", " + d["address"] + "\nVaccine: " + d['vaccine'] + "\nAvailable Capacity dose 1: " + str(d["available_capacity_dose1"]) + "\nAvailable Capacity dose 2: " + str(d["available_capacity_dose2"]) + '\n'
                    listOfAllCentresFor45.append(centre_detail_1)
                    centre_detail_1=''
                    count_1=count_1+1

            elif d["min_age_limit"] == 18:
                if d["available_capacity_dose1"] > 0:
                    centre_detail_2 =centre_detail_2 + "Centre {0}: ".format(count_2) + "\nCentre Adrress: " + d['name'] + ", " + d["address"] + "\nVaccine: " + d['vaccine'] + "\nAvailable Capacity dose 1: " + str(d["available_capacity_dose1"]) + "\nAvailable Capacity dose 2: " + str(d["available_capacity_dose2"]) + '\n'
                    listOfAllCentresFor18.append(centre_detail_2)
                    centre_detail_2=''
                    count_2=count_2+1

    #============================Sending TELEGRAM MESSAGE=======================================

    messageFor45 = ""

    if len(listOfAllCentresFor45) >0:
        messageFor45 = messageFor45 + "*Available  vaccination centres for 45 plus:*\n\n"
        for mess in  listOfAllCentresFor45:
            messageFor45 = messageFor45 + mess
            messageFor45 = messageFor45 + "\n"


    base_url = 'https://api.telegram.org/bot1891899278:AAFYbFbZ95cKslyOlLNcuxRYG63BuIzUyTQ/sendMessage?chat_id=-525721389&text={0}'.format(messageFor45)
    print("Response:",requests.get(base_url))
    print("Message Sent for 45+!")

    #----------------------------------------------------------------------------
    messageFor18 = ""

    if len(listOfAllCentresFor18) >0:
        messageFor18 = messageFor18 + "*Available  vaccination centres for 18 and above age:*\n\n"
        for mess in  listOfAllCentresFor18:
            messageFor18 = messageFor18 + mess
            messageFor18 = messageFor18 + "\n"


    base_url = 'https://api.telegram.org/bot1891899278:AAFYbFbZ95cKslyOlLNcuxRYG63BuIzUyTQ/sendMessage?chat_id=-525721389&text={0}'.format(messageFor18)
    print("Response:",requests.get(base_url))
    print("Message Sent for 18+!")

#========================================== vacNotif Function ends==============================


#--------------------------Scheduling the Notifications-------------------------
schedule.every(1).minutes.do(vacNotif)

print("Execution started...")
while 1:
    schedule.run_pending()
    time.sleep(1)
