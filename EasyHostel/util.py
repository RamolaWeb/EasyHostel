from sqlalchemy.orm import sessionmaker
from EasyHostel.model import engine
import datetime
import csv


def getSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def checkTime(startHour, endHour):
    dt = datetime.datetime.now()
    startDate = datetime.datetime(dt.year, dt.month, dt.day,
                                  startHour, 0, 0)
    endDate = datetime.datetime(dt.year, dt.month, dt.day,
                                endHour, 0, 0)
    nowTime = int(dt.timestamp())
    startTime = int(startDate.timestamp())
    endTime = int(endDate.timestamp())
    if nowTime >= startTime and nowTime <= endTime:
        print("True for "+str(nowTime)+" "+str(startTime)+" "+str(endTime))
        return True
    else:
        return False


def checkDateTime(time, startHour, endHour):
    dt = datetime.datetime.fromtimestamp(float(time))
    startDate = datetime.datetime(dt.year, dt.month, dt.day,
                                  startHour, 0, 0)
    endDate = datetime.datetime(dt.year, dt.month, dt.day,
                                endHour, 0, 0)
    nowTime = int(dt.timestamp())
    startTime = int(startDate.timestamp())
    endTime = int(endDate.timestamp())
    if nowTime >= startTime and nowTime <= endTime:
        return True
    else:
        return False


def currentTime():
    dt = datetime.datetime.now()
    return int(dt.timestamp())


def getDate(timestamp):
    return datetime.datetime.fromtimestamp(float(timestamp))


def checkEmpty(word):
    if not word:
        return -1
    return word


def createRecord(recordList, breakfastStartTime, breakfastFinishTime
                 , lunchStartTime, lunchEndTime, dinnerStartTime
                 , dinnerEndTime):
                    day = -1
                    record = []
                    container = {}
                    for r in recordList:
                        time = r.time
                        dt = getDate(time)
                        if day == -1:
                            response = {}
                        if dt.day > day:
                            day = dt.day
                            if len(response) != 0:
                                record.append(response)
                            response = {}
                            container = {}
                        else:
                            response = container
                        if checkDateTime(time, breakfastStartTime,
                                         breakfastFinishTime):
                                            response["date"] = str(dt.day)+"/"+str(dt.month)+"/"+str(dt.year)
                                            response["breakfast"] = True
                        if checkDateTime(time, lunchStartTime, lunchEndTime):
                            response["lunch"] = True
                            response["date"] = str(dt.day)+"/"+str(dt.month)+"/"+str(dt.year)
                        if checkDateTime(time, dinnerStartTime, dinnerEndTime):
                            response["dinner"] = True
                            response["date"] = str(dt.day)+"/"+str(dt.month)+"/"+str(dt.year)
                        container = response
                    if len(container) != 0:
                        record.append(container)
                    return record


def convertStringToDate(date):
    dt = datetime.datetime.strptime(date, "%Y-%m-%d")
    return int(dt.timestamp())


def sortAttendenceData(attendenceList, breakfastStartTime
                       , breakfastFinishTime
                       , lunchStartTime, lunchEndTime, dinnerStartTime
                       , dinnerEndTime):
    response = []
    recordList = []
    checkList = [False for x in attendenceList]
    print(len(checkList))
    for count, attendence in enumerate(attendenceList):
        print("Now in"+str(count))
        for c, a in enumerate(attendenceList):
            if a.studentId == attendence.studentId and not checkList[c]:
                recordList.append(attendence)
                checkList[c] = True
                print("YEP1")
        print("YEP")
        print(len(recordList))
        result = createRecord(recordList, breakfastStartTime
                              , breakfastFinishTime
                              , lunchStartTime, lunchEndTime, dinnerStartTime
                              , dinnerEndTime)
        print(len(result))
        record = result[0]
        r = {}
        r["rollNo"] = attendence.studentId
        if "breakfast" in record:
            r["breakfast"] = record["breakfast"]
        else:
            r["breakfast"] = False
        if "lunch" in record:
            r["lunch"] = record["lunch"]
        else:
            r["lunch"] = False
        if "dinner" in record:
            r["dinner"] = record["dinner"]
        else:
            r["dinner"] = False
        response.append(r)
        recordList = []
    return response


def generateCSV(attendenceList, hostelName, date):
    with open(hostelName+"-"+date+".csv", "w") as csvfile:
        field = ["rollNo", "breakfast", "lunch", "dinner"]
        writer = csv.DictWriter(csvfile, fieldnames=field)
        writer.writeheader()
        for attendence in attendenceList:
            writer.writerow(attendence)
