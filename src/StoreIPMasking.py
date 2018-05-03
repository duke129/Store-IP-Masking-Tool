#!/usr/bin/python3
'''
Created on Mar 19, 2018

@author: amit
'''
import sys
sys.path.insert(0, '../utils/')
sys.path.insert(0, '../properties/')


import properties
import mailConfig 
import pymysql
import ipaddress
import datetime
from logToExcel import writeToCSV
from builtins import str
pymysql.install_as_MySQLdb()

today = datetime.datetime.now()
filename="/home/amit/"+str(today.strftime('%d_%b_%Y_%H_%M_%S'))+".csv"
# Open database connection
db = pymysql.connect(properties.host,properties.username,properties.password,properties.database)

get_pool_ids="select ipPoolId from ipPool where poolTypeId=1;"
get_devices = "select ipAddress, ipPoolId, inet_aton(ipAddress) from device where  devicestateid = 20  and ipPoolId = %s;"
get_length = "select startIp, endIp, inet_ntoa(startIp), inet_ntoa(endIp) from ipPool where ipPoolId = %s ;"
update_ipPool="""update ipPool set ipMask= %s  where ipPoolId = %s;"""
cursor = db.cursor()
print("Starting the analaysis at "+ str(datetime.datetime.now()))
try:
# Execute the SQL command
    cursor.execute(get_pool_ids)
# Fetch all the pool Ids in a list.
    results = cursor.fetchall()
    for row in results:
        poolId = row[0]
        list_of_indices=[]
#         print("deviceIPPoolId is {0}".format(poolId))
        cursor.execute(get_devices,poolId)
        device_pools= cursor.fetchall()
        #print(device_pools)
#For each poolId get the length        
        for dp in device_pools:
            deviceIp=dp[0]
            dp_poolId=dp[1]
            device_long_value=dp[2]
#             last_value_ip=deviceIp.split('.')[3]
#             print("Device IP is " + format(deviceIp))
            cursor.execute(get_length,dp_poolId)
            pool_result=cursor.fetchall()
            for pr in pool_result:
                startIp=pr[2]
                endIp=pr[3]
                startIp_long=pr[0]
                ip1 = int(ipaddress.IPv4Address(str(startIp)))
                ip2 = int(ipaddress.IPv4Address(str(endIp)))
                length=ip2-ip1
#Prepare mask values of length
                ipMask=[0] * length
                index=int(device_long_value)-int(startIp_long)
            list_of_indices.append(index)
#Get list of all indices that have to be masked
            i=0
            ipMask_val=[]
            while i<len(list_of_indices):
                ipMask_val.append(list_of_indices[i])
                i+=1
#For each item in  list of indices, start masking
        for  item in ipMask_val:
            try: 
                if item >= 0:
                    ipMask[item-1] = 1
                else:
#Inn case if index is negative, it means device ip is not sync with pool
                    print("DeviceIP is :" +str(deviceIp) + " StartIP is :" +str(startIp) + " deviceIPPoolId is " + str(poolId)+" Index: "+str(item))
                    remarks="Device IP not in sync with pool"
                    writeToCSV(filename,deviceIp,startIp,poolId,item,remarks) #write into log file
                    mailConfig.mail(filename) #mail
            except  Exception as e:
                print("Non mumeric or Negative value: "+str(e))  
                pass
        str1 = ''.join(str(e) for e in ipMask)
#                    print("------ updated IPMask is ----- " + str(str1))
#                    cursor.execute(update_ipPool,(str1,poolId))
#                    db.commit()
except Exception as e:
    print("unable to fecth data" + str(e))

# disconnect from server
db.close()
print("Ending the analaysis at "+ str(datetime.datetime.now()))
