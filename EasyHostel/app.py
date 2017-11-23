from flask import Flask, request, jsonify, render_template
from model import Student, Attendence, Hostel
from util import getSession, checkTime, currentTime, createRecord
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
        response = {}
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
            response["status"] = True
            response["message"] = "Data Uploaded Successfully"
        except Exception as e:
            response["status"] = False
            response["message"] = "Error Occur While Submitting Data"
            traceback.print_exc()
        finally:
            db.close()
        return jsonify(**response)


@app.route("/hostel", methods=["GET", "POST"])
def hostelDetail():
    if request.method == "GET":
        return render_template("hostelData.html")
    else:
        db = getSession()
        response = {}
        name = request.form["name"]
        try:
            hostel = Hostel(name=name)
            db.add(hostel)
            db.commit()
            response["status"] = True
            response["message"] = "Data Uploaded Successfully"
        except Exception as e:
            response["status"] = False
            response["message"] = "Error Occur While Submitting Data"
            traceback.print_exc()
        finally:
            db.close()
        return jsonify(**response)


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
