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
                    response = {}
                    for r in recordList:
                        time = r.time
                        if getDate(time).day > day:
                            day = getDate(time).day
                            month = getDate(time).month
                            year = getDate(time).year
                            if len(response) > 0:
                                record.append(response)
                            response = {}
                            response["date"] = str(year)+"/"+str(month)+"/"+str(day)
                        if checkDateTime(time, breakfastStartTime,
                                         breakfastFinishTime):
                                            response["breakfast"] = True
                        if checkDateTime(time, lunchStartTime, lunchEndTime):
                            response["lunch"] = True
                        if checkDateTime(time, dinnerStartTime, dinnerEndTime):
                            response["dinner"] = True
                    return record
