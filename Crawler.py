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
            id = student["id"]
            self.studentIDs.append(id)


    def fetchStudentsInfo(self,
                          url="http://open.test.seiue.com/api/v1/students/:id/transcripts"):
        for id in self.studentIDs:
            student = Student()
            subjects = []

            student.id = id
            response = requests.get(url.replace(":id", str(id)), headers = self.headers)
            studentInfo = response.json()

            for gradeInfo in studentInfo["grade_list"]:
                for subjectInfo in gradeInfo["grade_list"]:
                    subject = Subject(subjectInfo["source_id"], subjectInfo["name"], subjectInfo["evaluation"]["100"], subjectInfo["evaluation"]["abc"], subjectInfo["evaluation"]["gpa"], subjectInfo["evaluation"]["rank"])
                    subjects.append(subject)

            student.subjects = subjects
            print(student.id)
            print(student.subjects[0].name + "---" + str(student.subjects[0].grade))
            self.students.append(student)

crawler = Crawler()

crawler.fetchToken()
crawler.fetchAllStudents()
crawler.fetchStudentsInfo()

print(crawler.students)