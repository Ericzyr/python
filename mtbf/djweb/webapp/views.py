from django.shortcuts import render


import os
import re
import datetime
import time
LOG_SUFFIX = "/case.log"
LOG_INFO = "/logstack.log"
FLAG_PASS = "OK (1 test)"


class student(object):
    def __init__(self,SW,phoneData , dataFC , dataTB , dataANR , dataReset , totalExeTime , totalError , dataPass ,
                 dataExce , passRate , mtbfVal):
        self.SW=SW
        self.phoneData = phoneData
        self.dataFC = dataFC
        self.dataTB = dataTB
        self.dataANR = dataANR
        self.dataPass = dataPass
        self.dataExce = dataExce
        self.dataReset = dataReset
        self.totalExeTime = totalExeTime
        self.totalError = totalError
        self.mtbfVal = mtbfVal
        self.passRate = passRate





t=student("x4-50",2,3,4,5,6,7,8,9,10,11,12)



'''获取一个文件打开并读取里面的信息，提取后你赋值'''

r = os.popen("pwd").read()
path = r.rsplit()[0]+"/htmlFolder/648TV/phoneInfo.txt"
phoneInfo = open(path, "r")
lines = phoneInfo.readlines()
def getBuildInfo():
    for line in lines:
        if line.find("buildModel==") != -1:  # get build version
            index = len("buildModel==")
            phoneModel = line[index:].rstrip()
        elif line.find("buildVersion==") != -1:  # get build date
            index = len("buildVersion==")
            phoneVer = line[index:].rstrip()
        elif line.find("buildDate==") != -1:  # get build date
            index = len("buildDate==")
            phoneDate = line[index:].rstrip()
        elif line.find("testStartTime==") != -1:  # get start time
            index = len("testStartTime==")
            startTime = line[index:].rstrip()
        elif line.find("testEndTime==") != -1:  # get end time
            index = len("testEndTime==")
            endTime = line[index:].rstrip()

    startDateTime = time.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    starttime = time.mktime(startDateTime)
    endDateTime = time.strptime(endTime, "%Y-%m-%d %H:%M:%S")
    endtime = time.mktime(endDateTime)
    phoneExeTime = ('%.2f' % ((endtime - starttime) / 3600))
    return phoneModel, phoneVer, phoneDate, startTime, endTime, phoneExeTime


# 这种方法可以获取所需要的值
phoneModel, phoneVer, phoneDate, phoneStartTime, phoneEndTime, phoneExeTime = getBuildInfo()







yy = os.popen("pwd").read()
path1 = yy.rsplit()[0]+"/htmlFolder"
# path = r.rsplit()[0]+"/htmlFolder/648TV/phoneInfo.txt"
# phoneInfo = open(path, "r")
# lines = phoneInfo.readlines()
# print(lines)




def getFolderList(folder):
    pList = []
    for f in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, f)):
            pList.append(os.path.join(folder, f))
    pList.sort(key=lambda x: os.stat(x).st_ctime)
    return pList


a=getFolderList(path1)


Loop = getFolderList(a[0])




print(Loop[0])
p=getFolderList(Loop[0])
print(p[0])


path = p[0]+"/case.log"

print(path)
logcase = open(path, "r")
lines = logcase.readlines()



class LogParser():
    def __init__(self , planned , folderlist):
        # 		print folderlist
        self.resultSheet = []
        # 		self.executed = len(folderlist)
        self.executed = 0
        self.summarySheet = {'pass': 0 , 'plan': planned , 'exed': self.executed , 'tb': 0 , 'anr': 0 , 'fc': 0 ,
                             'reset': 0}
        for folder in folderlist:
            self.resultSheet.append(self.parse_log(folder))

    def parse_log(self , folder):
        # current case properties
        resultdata = {}
        casechname = ""
        caseclass = ""
        casename = ""
        exetime = ""
        failreason = ""
        casestep = ""
        ispass = "fail"
        screencap = ""
        logtrack = ""
        anrCount = ""
        fcCount = ""
        tombstoneCount = ""
        resetCount = ""
        resultdata["anrCount"] = 0
        resultdata["tombstoneCount"] = 0
        resultdata["fcCount"] = 0
        resultdata["resetCount"] = 0
        isFC = False
        isTB = False
        isANR = False
        isRS = False
        stepindex = 0
        try:
            logfile = open(folder + LOG_SUFFIX , "r")
            lines = logfile.readlines()
        except IOError as e:
            lines = ""
            lines_logcat = ""
        # get case dir
        _path = folder.split(os.sep)[1:]
        resultdata["caseurl"] = os.path.join(*_path)
        # print resultdata["caseurl"]
        for line in lines:

            if line.find("INSTRUMENTATION_STATUS: title=") != -1:  # get case chinese name
                index = len("INSTRUMENTATION_STATUS: title=")
                casechname = line[index:].rstrip()
                resultdata["casechname"] = casechname
            elif line.find("INSTRUMENTATION_STATUS: class=") != -1:  # get case class
                index = len("INSTRUMENTATION_STATUS: class=")
                caseclass = line[index:].rstrip()
                resultdata["caseclass"] = caseclass
            elif line.find("INSTRUMENTATION_STATUS: test=") != -1:  # get case name
                index = len("INSTRUMENTATION_STATUS: test=")
                casename = line[index:].rstrip()
                resultdata["casename"] = casename
            elif line.find("Time: ") != -1:  # record execute time
                self.summarySheet['exed'] += 1
                #				self.executed += 1
                index = len("Time: ")
                exetime = line[index:].rstrip()
                resultdata["exetime"] = exetime
            elif line.find("INSTRUMENTATION_STATUS: caseStep=") != -1:  # get case step
                stepindex += 1
                line = re.sub(r'INSTRUMENTATION_STATUS: caseStep=\d?\d?\.?' , str(stepindex) + '.' , line , 1).rstrip()
                casestep += line + "\n"
            elif line.find("INSTRUMENTATION_STATUS: screenshot=") != -1:  # get screenshot info
                index = len("INSTRUMENTATION_STATUS: screenshot=")
                screencap = line[index:].rstrip()
                resultdata["screencap"] = screencap
            elif line.find("INSTRUMENTATION_STATUS: logstack=") != -1:  # get logstack info
                index = len("INSTRUMENTATION_STATUS: logstack=")
                logstack = line[index:].rstrip()
                resultdata["logstack"] = logstack
            elif line.find("INSTRUMENTATION_STATUS: stack=") != -1:  # record fail reason
                index = len("INSTRUMENTATION_STATUS: stack=")
                failreason = line[index:].rstrip()
                if failreason.find("ANR occurred") != -1:
                    if isANR == False:
                        isANR = True
                        resultdata["anrCount"] += 1
                        ispass = "ANR"
                elif failreason.find("FC occurred") != -1:
                    if isFC == False:
                        isFC = True
                        resultdata["fcCount"] += 1
                        ispass = "FC"
                resultdata["failreason"] = "错误原因:\n" + failreason
            elif line.find("INSTRUMENTATION_STATUS: TOMBSTONES=") != -1:  # get tombstone
                if isTB == False:
                    isTB = True
                    resultdata["tombstoneCount"] += 1
                    ispass = "Tombstone"
                resultdata["failreason"] = "错误原因:\n"
            elif line.find("INSTRUMENTATION_STATUS: ANR=") != -1:  # get anr
                if isANR == False:
                    isANR = True
                    resultdata["anrCount"] += 1
                    ispass = "ANR"
                resultdata["failreason"] = "错误原因:\n"
            elif line.find("ANR occurred") != -1:  # get anr
                if isANR == False:
                    isANR = True
                    resultdata["anrCount"] += 1
                    ispass = "ANR"
                resultdata["failreason"] = "错误原因:\n"
            elif line.find("FC occurred") != -1:  # get fc
                if isFC == False:
                    isFC = True
                    resultdata["fcCount"] += 1
                    ispass = "FC"
                resultdata["failreason"] = "错误原因:\n"
            elif line.find("Tombstone occurred") != -1:  # get tombstone
                if isTB == False:
                    isTB = True
                    resultdata["tombstoneCount"] += 1
                    ispass = "Tombstone"
                resultdata["failreason"] = "错误原因:\n"
            elif line.find("Reboot occurred") != -1:  # get reboot
                if isRS == False:
                    isRS = True
                    resultdata["resetCount"] += 1
                    ispass = "Reset"
                resultdata["failreason"] = "错误原因:\n"
            elif line.find(FLAG_PASS) != -1:  # record pass or fail
                ispass = "pass"
        resultdata["ispass"] = ispass
        resultdata["casestep"] = casestep
        if (len(exetime) == 0):
            if ispass == "fail":
                ispass = "notrun"
                resultdata["ispass"] = ispass
        if ispass == 'pass':
            self.summarySheet['pass'] += 1
        if isFC:
            self.summarySheet['fc'] += resultdata["fcCount"]
        if isTB:
            resultdata["failreason"] += "\n Tombstone Occurred"
            self.summarySheet['tb'] += resultdata["tombstoneCount"]
        if isANR:
            resultdata["failreason"] += "\n ANR Occurred"
            self.summarySheet['anr'] += resultdata["anrCount"]
        if isRS:
            resultdata["failreason"] += "\n Reboot Occurred"
            self.summarySheet['reset'] += resultdata["resetCount"]
        if (caseclass == "" and casename == ""):
            resultdata["casename"] = folder
            resultdata["casechname"] = "case.log不存在"
        return resultdata

    def getResultData(self):
        return self.resultSheet

    def getSummaryData(self):
        self.summarySheet['exed'] = self.executed
        self.summarySheet['fail'] = self.executed - self.summarySheet['pass']
        self.summarySheet['notrun'] = int(self.summarySheet['plan']) - self.executed
        return self.summarySheet

def getLoopData(logFolder):
    caseLogList = []
    for folder in os.listdir(logFolder):
        if os.path.isdir(os.path.join(logFolder , folder)):
            caseLogList.append(os.path.join(logFolder , folder))
    caseLogList.sort(key=lambda x: os.stat(x).st_ctime)
    _p = LogParser(4, caseLogList)
    return _p



oo = getLoopData("/home/pc7/pydjango/mtbf/djweb/htmlFolder/648TV/LOOP1/testDesktop_20180509_153433")
z=oo.parse_log("/home/pc7/pydjango/mtbf/djweb/htmlFolder/648TV/LOOP1/testDesktop_20180509_153433")
print(z)
print('ispass:', z['ispass'])
print("caseclass:", z['caseclass'])
print('casename:', z['casename'])
print('casestep:', z['casestep'])

print('fcCount:', z['fcCount'])
print('tombstoneCount', z['tombstoneCount'])
print('anrCount', z['anrCount'])
print('exetime', z['exetime'])
print('resetCount', z['resetCount'])
print('casechname', z['casechname'])












ao = ["a",'b','c','d']

b = 0


def mtbf(request):
    return render(request, 'mtbf.html',
                  {"testresult": phoneModel,"SW": phoneVer, "buildDate": phoneDate, "startTime": phoneStartTime, "EndTime": phoneEndTime, "totalExeTime": phoneExeTime,
                   "totalANR": t.dataANR, "totalTombstone": t.dataTB, "totalFC": t.dataFC, "totalReset": t.dataReset, "totalError":
                    t.totalError, "totalcasePass": t.dataPass, "totalcaseExce": t.dataExce, "passRate": t.passRate,
                   "mtbfValue": t.mtbfVal,
                   "Aexetime":z['exetime'], 'Aispass': z['ispass'],'Acasechname':z['casechname'],'Acaseclass':z['caseclass'],'Acasename':z['casename'],
                   "Acaseurl":z['caseurl'],'Acasestep': z['casestep'], "a": ao, "b": b, "Acasestep": z['casestep']}
                  )












