import csv
import numpy as np
import sklearn.cluster
import distance
import pickle

"""
Kaggle Postings
01 jobpost
02 Title
03 Company
11 Job Description
12 Job Requirement/Responsibilities
13 Required Qualification
14 Salary

GooglePostings
0 Company
1 Title
2 Category
3 Location
4 Responsibilities
5 Minimum Qualifications
6 Preferred Qualifications
"""


def RowCount(FileToCount):
    with open(FileToCount) as in_file:
        return sum(1 for _ in in_file)


def parse_data(paragraph, deliminator=' '):
    data = str.split(str.lower(paragraph), deliminator)
    data = [f for f in data if len(f) > 3]
    return set(data)


def GetSkills(paragraph,skills):
    return_skills = []
    for skill in skills:
        if(skill in paragraph):
            return_skills.append(skill)
    return set(return_skills)


    return skills

def SaveSkillDict():
    PostingFile = 'data job posts.csv'
    SkillsFile = open('AllSkills.txt', 'r')

    data = str.split(str.lower(SkillsFile.read()), '\n')
    Skills = [f for f in data if len(f) > 3 and " " in f]

    RemoveWords = ['working_w','long_term', 'working w' , 'net']
    for remove_word in RemoveWords:
        if remove_word in Skills:
            Skills.remove(remove_word)

    with open(PostingFile) as file:
        reader = csv.reader(file)

        row1 = next(reader)

        MatchingSkills = {}
        for i in range(3000):
            row = next(reader)
            if(i%100 == 0):
                print(i)
            MatchingSkills[row[2]] = ((GetSkills(row[13], Skills)))

        file.close()

    with open('KaggleSkillDict.pickle', 'wb') as handle:
        pickle.dump(MatchingSkills, handle, protocol=pickle.HIGHEST_PROTOCOL)



def GetSkillDict(new=False):
    if(new):
        SaveSkillDict()

    with open('KaggleSkillDict.pickle', 'rb') as handle:
        MatchDict = pickle.load(handle)

    return MatchDict

def SaveMatchDict():

    SkillsFile = open('AllSkills.txt', 'r')

    Skills = parse_data(SkillsFile.read(), deliminator='\n')

    MatchingSkills = GetSkillDict(new=True)

    MatchingArray = []
    JobArray = []

    MatchDict = {}
    for job in MatchingSkills:
        JobArray.append(job)
        MatchDict[job] = []

    i = 0
    matches = []
    match_jobs = []
    unions = []
    for job1 in MatchingSkills:
        MatchingArray.append([])
        JobArray.append(job1)
        for job2 in MatchingSkills:
            if (job1 != job2):
                skills1 = MatchingSkills[job1]
                skills2 = MatchingSkills[job2]
                union = skills1.intersection(skills2)

                MatchingArray[i].append(len(union))
                matches.append("Job1: " + job1 + "\nJob2: " + job2 + '\n')
                match_jobs.append([job1, job2])
                if((len(skills1) + len(skills2)) == 0):
                    match_percent = 0.0
                else:
                    match_percent = len(union) / (len(skills1) + len(skills2))
                if (match_percent > 0.2):
                    MatchDict[job1].append(job2)
                    MatchDict[job2].append(job1)
                unions.append(union)
        i = i + 1

    with open('KaggleMatchDict.pickle', 'wb') as handle:
        pickle.dump(MatchDict, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ =='__main__':

    #SaveMatchDict()


    with open('KaggleMatchDict.pickle', 'rb') as handle:
        MatchDict = pickle.load(handle)

    topvalnum = 100

    topval = []
    topjob = []
    for i in range(topvalnum):
        topval.append(0)
        topjob.append("")

    for job in MatchDict:
        for i in range(topvalnum):
            if(len(MatchDict[job]) > topval[i]):
                topval[i] = len(MatchDict[job])
                topjob[i] = job
                break

    for job in topjob:
        print(job)


SkillDict = GetSkillDict()

countlists = []
CategoryList = ["Software Developer Engineer", "Business Analyst Strategy", "Sales Marketing", "Database Systems", "Sales Agent",
           "Administrative Assistant Secretary","Interpreter Translator"]
SkillLists = []
CategoryDict = {}
for category in CategoryList:
    JobDict = {}
    terms = job.split()
    for term in terms:
        for JobName in SkillDict.keys():
            if term.lower() in JobName.lower():
                JobDict[JobName] = list(SkillDict[JobName])
                CategoryDict[category] = JobDict


import json
file = open('SkillQuest','w')
json_string = json.dumps(CategoryDict)
file.write(json_string)
file.close()





"""
categories: 
- Medical (Medical Doctor)
- Interpreter (English Language Interpreters/ Translators)
- Finance (Finance Assistant)
- Customer Service (Airport Customer Service Agent)
- Engineer (Junior Engineer)
- Sales (Salesman / Trade Agent)
- Administrative (Administrative Secretary)

"""
