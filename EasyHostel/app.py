from flask import Flask, request, jsonify, render_template
from model import Student, Attendence, Hostel
from util import getSession, checkTime, currentTime, createRecord, checkEmpty
import traceback


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello"


@app.route("/update", methods=["POST"])
def update():
    hostelId = request.form["hostelId"]
    studentId = request.form["studentId"]
    db = getSession()
    response = {}
    try:
        student = db.query(Student).filter(Student.studentId == studentId) \
                         .first()
        hostel = db.query(Hostel).filter(Hostel.id == hostelId).first()
        charges = 0
        if checkTime(hostel.breakfastStartTime, hostel.breakfastFinishTime):
            charges = hostel.breakfastCharges
        elif checkTime(hostel.lunchStartTime, hostel.lunchEndTime):
            charges = hostel.lunchCharges
        elif checkTime(hostel.dinnerStartTime, hostel.dinnerEndTime):
            charges = hostel.dinnerCharges
        student.currentBillAdvance -= charges
        attendence = Attendence(hostelId=hostelId, studentId=studentId
                                , time=currentTime())
        db.add(attendence)
        db.commit()
        response["status"] = True
        response["message"] = "Attendence Recorded Sucessfully"
    except Exception as e:
            response["status"] = False
            response["message"] = "Student Does Not Exist"
            traceback.print_exc()
    finally:
        db.close()
    return jsonify(**response)


@app.route("/student", methods=["GET", "POST"])
def studentDetail():
    if request.method == "GET":
        return render_template("studentData.html")
    else:
        db = getSession()
        name = request.form["name"]
        email = request.form["email"]
        rollno = int(request.form["rollno"])
        hostelId = int(request.form["hostelId"])
        studentId = rollno
        try:
            student = Student(name=name, email=email, rollno=rollno,
                              hostelId=hostelId, studentId=studentId)
            db.add(student)
            db.commit()
        except Exception as e:
            traceback.print_exc()
        finally:
            db.close()
        return render_template("responseStudentData.html")


@app.route("/hostel", methods=["GET", "POST"])
def hostelDetail():
    if request.method == "GET":
        return render_template("hostelDetail.html")
    else:
        db = getSession()
        name = request.form["name"]
        breakfastStartTime = int(request.form["breakfastStartTime"])
        breakfastFinishTime = int(request.form["breakfastFinishTime"])
        lunchStartTime = int(request.form["lunchStartTime"])
        lunchEndTime = int(request.form["lunchEndTime"])
        dinnerStartTime = int(request.form["dinnerStartTime"])
        dinnerEndTime = int(request.form["dinnerEndTime"])
        breakfastCharges = int(request.form["breakfastCharges"])
        lunchCharges = int(request.form["lunchCharges"])
        dinnerCharges = int(request.form["dinnerCharges"])
        currentBillAdvance = int(request.form["currentBillAdvance"])
        try:
            hostel = Hostel(name=name, breakfastStartTime=breakfastStartTime
                            , breakfastFinishTime=breakfastFinishTime
                            , lunchStartTime=lunchStartTime
                            , lunchEndTime=lunchEndTime
                            , dinnerStartTime=dinnerStartTime
                            , dinnerEndTime=dinnerEndTime
                            , breakfastCharges=breakfastCharges
                            , lunchCharges=lunchCharges
                            , dinnerCharges=dinnerCharges
                            )
            db.add(hostel)
            db.commit()
        except Exception as e:
            traceback.print_exc()
        finally:
            db.close()
        return render_template("responseHostelData.html")


@app.route("/student/<int:rollno>/<int:fromDate>/<int:toDate>")
def studentRecord(rollno, fromDate, toDate):
    response = {}
    db = getSession()
    try:
        student = db.query(Student).filter(Student.rollno == rollno).first()
        studentId = student.studentId
        hostelId = student.hostelId
        currentBillAdvance = student.currentBillAdvance
        hostel = db.query(Hostel).filter(Hostel.id == hostelId).first()
        hostelBreakfastStartTime = hostel.breakfastStartTime
        hostelBreakfastEndTime = hostel.breakfastFinishTime
        hostelLunchStartTime = hostel.lunchStartTime
        hostelLunchEndTime = hostel.lunchEndTime
        hostelDinnerStartTime = hostel.dinnerStartTime
        hostelDinnerEndTime = hostel.dinnerEndTime
        record = db.query(Attendence) \
            .filter(Attendence.studentId == studentId) \
            .order_by(Attendence.time).all()
        response["name"] = student.name
        response["rollno"] = student.rollno
        response["hostel"] = hostel.name
        response["currentBillAdvance"] = student.currentBillAdvance
        response["record"] = createRecord(record, hostelBreakfastStartTime
                                          , hostelBreakfastEndTime
                                          , hostelLunchStartTime
                                          , hostelLunchEndTime
                                          , hostelDinnerStartTime
                                          , hostelDinnerEndTime)
    except Exception as e:
        response["status"] = False
        response["message"] = "Error While Getting Data"
        traceback.print_exc()
    finally:
        db.close()
    return jsonify(**response)


@app.route("/updateInput")
def updateCheck():
    return render_template("updateCheck.html")


@app.route("/hostel/update")
def hostelUpdate():
    return render_template("hostelUpdate.html")


@app.route("/update/hostel", methods=["POST"])
def updateHostel():
    db = getSession()
    response = {}
    hostelId = int(request.form["id"])
    breakfastStartTime = int(checkEmpty(request.form["breakfastStartTime"]))
    breakfastFinishTime = int(checkEmpty(request.form["breakfastFinishTime"]))
    lunchStartTime = int(checkEmpty(request.form["lunchStartTime"]))
    lunchEndTime = int(checkEmpty(request.form["lunchEndTime"]))
    dinnerStartTime = int(checkEmpty(request.form["dinnerStartTime"]))
    dinnerEndTime = int(checkEmpty(request.form["dinnerEndTime"]))
    breakfastCharges = int(checkEmpty(request.form["breakfastCharges"]))
    lunchCharges = int(checkEmpty(request.form["lunchCharges"]))
    dinnerCharges = int(checkEmpty(request.form["dinnerCharges"]))
    currentBillAdvance = int(checkEmpty(request.form["currentBillAdvance"]))
    try:
        hostel = db.query(Hostel).filter(Hostel.id == hostelId).first()
        if breakfastStartTime != -1:
            hostel.breakfastStartTime = breakfastStartTime
        if breakfastFinishTime != -1:
            hostel.breakfastFinishTime = breakfastFinishTime
        if lunchStartTime != -1:
            hostel.lunchStartTime = lunchStartTime
        if lunchEndTime != -1:
            hostel.lunchEndTime = lunchEndTime
        if dinnerEndTime != -1:
            hostel.dinnerEndTime = dinnerEndTime
        if dinnerStartTime != -1:
            hostel.dinnerStartTime = dinnerStartTime
        if breakfastCharges != -1:
            hostel.breakfastCharges = breakfastCharges
        if lunchCharges != -1:
            hostel.lunchCharges = lunchCharges
        if dinnerCharges != -1:
            hostel.dinnerCharges = dinnerCharges
        if currentBillAdvance != -1:
            hostel.currentBillAdvance = currentBillAdvance
        db.commit()
        response["status"] = True
        response["message"] = "Successfully Updated Hostel Data"
    except Exception as e:
        response["status"] = False
        response["message"] = "Error While Updating"
        traceback.print_exc()
    finally:
        db.close()
    return jsonify(**response)
