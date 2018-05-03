#!/usr/bin/python3
import csv

def writeToCSV(filename,deviceIp,startIp,poolId,item,remarks):
    myData = [["deviceip", "startip", "poolid", "index", "Remarks"]]
    myFile = open(filename, 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(myData)
        writer.writerows([[deviceIp,startIp,poolId,item,remarks]])
#     print("Writing complete")