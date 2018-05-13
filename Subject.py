# -*- coding: UTF-8 -*-

class Subject:
    id = 0
    name = ""
    grade = 0
    level = ""
    gpa = 0
    rank = ""
    subject = ""

    def __init__(self, id, name, grade, level, gpa, rank, subject):
        self.id = id
        self.name = name
        self.grade = grade
        self.level = level
        self.gpa = gpa
        self.rank = rank
        self.subject = subject
