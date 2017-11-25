from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, create_engine


Base = declarative_base()


class Student(Base):
    __tablename__ = "Student"
    id = Column(Integer, primary_key=True)
    studentId = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    rollno = Column(Text, nullable=False)
    currentBillAdvance = Column(Integer, default=18000)
    hostelId = Column(Integer, nullable=False)


class Hostel(Base):
    __tablename__ = "Hostel"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    breakfastCharges = Column(Integer, default=30)
    lunchCharges = Column(Integer, default=40)
    dinnerCharges = Column(Integer, default=50)
    breakfastStartTime = Column(Integer, default=8)
    breakfastFinishTime = Column(Integer, default=9)
    lunchStartTime = Column(Integer, default=12)
    lunchEndTime = Column(Integer, default=14)
    dinnerStartTime = Column(Integer, default=20)
    dinnerEndTime = Column(Integer, default=21)


class Attendence(Base):
    __tablename__ = "Attendence"
    id = Column(Integer, primary_key=True)
    studentId = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)
    hostelId = Column(Integer, nullable=False)


engine = create_engine("mysql+pymysql://root:Sahil@1234567@localhost:3306 \
                       /EasyHostel", echo=True)


"""engine = create_engine("mysql+pymysql://uxmjqcj2gqavyh1a:ggmz3mvhw363zx9f@p1us8ottbqwio8hv.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/rmf5o1p3y0eg5kjn", echo=True)"""
Base.metadata.create_all(engine)
