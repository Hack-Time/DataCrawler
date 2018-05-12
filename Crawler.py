# -*- coding: UTF-8 -*-
import requests
import codecs
import pandas as pd
from Student import Student
from Subject import Subject
import csv

class Crawler:
    clientID = "368912"
    clientSecret = "KuGCMO-WBu6ciGEV_Mchp_44-X2TSCJ3omWxatfj"
    headers = ""
    studentIDs = []
    students = []

    def fetchToken(self, url="http://open.test.seiue.com/api/v1/oauth"):
        data = {
            "grant_type": "client_credentials",
            "client_id": self.clientID,
            "client_secret": self.clientSecret
        }
        response = requests.post(url, data=data)
        jsonResult = response.json()

        # self.token = jsonResult["access_token"]
        self.headers = {
            "X-School-Id": "3",
            "Authorization": "Bearer " + jsonResult["access_token"]
        }

    def fetchAllStudents(self,
                         url="http://open.test.seiue.com/api/v1/reflections?role=1&$per-page=100000&$page=1"):
        response = requests.get(url, headers=self.headers)
        students = response.json()

        for student in students:
            stu = Student()
            stu.id = student["id"]
            stu.gender = student["gender"]
            stu.graduateYear = student["graduates_in"]
            self.students.append(stu)
            # id = student["id"]
            # self.studentIDs.append(id)


    def fetchStudentsInfo(self,
                          url="http://open.test.seiue.com/api/v1/students/:id/transcripts"):
        for i in range(len(self.students)):
            subjects = []
            response = requests.get(url.replace(":id", str(self.students[i].id)), headers=self.headers)
            studentInfo = response.json()

            for gradeInfo in studentInfo["grade_list"]:
                for subjectInfo in gradeInfo["grade_list"]:
                    # print(subjectInfo)
                    subject = Subject(subjectInfo["source_id"], subjectInfo["name"], subjectInfo["evaluation"]["100"],
                                      subjectInfo["evaluation"]["abc"], subjectInfo["evaluation"]["gpa"],
                                      subjectInfo["evaluation"]["rank"])
                    subjects.append(subject)
            self.students[i].subjects = subjects
            # print(str(self.students[i].graduateYear) + "---" + str(self.students[i].subjects[0].grade))

crawler = Crawler()

crawler.fetchToken()
crawler.fetchAllStudents()
crawler.fetchStudentsInfo()

columnName = ["id"]

print(crawler.students)

# data = pd.DataFrame(columns=columnName, data={crawler.students.id})
#
# data.to_csv("./data/students.csv")

# csvFile2 = open("./data/students.csv", "w")

csvFile2 = codecs.open("./data/students.csv", "w", "utf_8_sig")
writer = csv.writer(csvFile2)
m = len(crawler.students)
for i in range(m):
    writer.writerow([crawler.students[i].id, crawler.students[i].gender, crawler.students[i].graduateYear, crawler.students[i].subjects[0].name, crawler.students[i].subjects[0].grade])
csvFile2.close()