from sqlalchemy.orm import sessionmaker
from model import engine
import datetime


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


def createRecord(recordList, breakfastStartTime, breakfastFinishTime
                 , lunchStartTime, lunchEndTime, dinnerStartTime
                 , dinnerEndTime):
                    day = -1
                    record = []
                    container = {}
                    for r in recordList:
                        time = r.time
                        dt = getDate(time)
                        if dt.day > day:
                            day = dt.day
                            record.append(response)
                            response = {}
                            container = {}
                        else:
                            response = container
                        response["date"] = str(dt.day)+"/"+str(dt.month)+"/"+str(dt.year)
                        if checkDateTime(time, breakfastStartTime,
                                         breakfastFinishTime):
                                            print("Yep breakfast")
                                            response["breakfast"] = True
                        if checkDateTime(time, lunchStartTime, lunchEndTime):
                            response["lunch"] = True
                            print("Yep lunch")
                        if checkDateTime(time, dinnerStartTime, dinnerEndTime):
                            response["dinner"] = True
                            print("Yep dinner")
                        container = response
                    record.append(container)
                    return record
