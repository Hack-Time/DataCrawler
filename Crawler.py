# -*- coding: UTF-8 -*-
import requests, json
from Student import Student
from Subject import Subject

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
                         url="http://open.test.seiue.com/api/v1/reflections?role=1&$per-page=1000&$page=1"):
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
        for i in range(0, len(self.students)):
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
            print(str(self.students[i].graduateYear) + "---" + str(self.students[i].subjects[0].grade))

crawler = Crawler()

crawler.fetchToken()
crawler.fetchAllStudents()
crawler.fetchStudentsInfo()

# crawler.students.to_csv("data/students.csv")