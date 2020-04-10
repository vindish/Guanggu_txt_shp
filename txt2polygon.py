# -*- coding: utf-8 -*-
import arcpy
import os
import random
import datetime
import time
import codecs
import string
import linecache
rootpath=os.getcwd()
print (rootpath)
today=datetime.date.today()
formatted_today=today.strftime('%y%m%d')
nowtime=time.strftime("%H%M%S")
txtType='.txt'
shpType='.shp'
wkt='PROJCS["Xian_1980_3_Degree_GK_Zone_38",GEOGCS["GCS_Xian_1980",DATUM["D_Xian_1980",SPHEROID["Xian_1980",6378140.0,298.257]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",38500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",114.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0],AUTHORITY["EPSG",2362]]'
print (wkt.split(',')[0][8:-1])

def getFileList(envworkspace1, txtType):
    fileFullPathList = []
    fileNameList = []
    filenameList = os.listdir(envworkspace1)
    for fn in filenameList:
        file_name, file_ext = os.path.splitext(fn)
        if file_ext == txtType:
            fileNameList.append(file_name)
    return fileNameList

fileNameList = getFileList(rootpath,txtType)
print (fileNameList)
print (len(fileNameList))
for seq in range(len(fileNameList)):
    rnd='%d' %(random.randint(10,99))
    fileName1=fileNameList[seq]
    print (fileName1)
    filename2=''.join(fileName1)
    arcpy.CreateFolder_management(rootpath, filename2)
    envworkspace=os.path.join(rootpath,filename2)
    shpfile = (filename2+'_'+formatted_today+'_'+nowtime+'_'+rnd+shpType)    #xxx.shp
    allpathfc = os.path.join(envworkspace, shpfile)    #C:/sff/xxx/xxx.shp
    sr = arcpy.SpatialReference()
    sr.loadFromString(wkt)
    arcpy.CreateFeatureclass_management(envworkspace, shpfile, 'POLYGON','','','',sr)
    arcpy.AddField_management(allpathfc,'FFIDDD', "LONG", 9 )
    arcpy.AddField_management(allpathfc,'MJ_mu','double')
    arcpy.AddField_management(allpathfc,'codebm', "LONG", 9)
    arcpy.AddField_management(allpathfc,'name','TEXT',99)
    arcpy.AddField_management(allpathfc,'shapetype_','TEXT',99)    
    arcpy.AddField_management(allpathfc,'fenfu','TEXT',99)
    cursor = arcpy.InsertCursor(allpathfc, ['SHAPE@'])
    txtfile=os.path.join(rootpath,filename2+txtType)    #c:/sff/xxx.txt
    contentrows=file(txtfile,"r").readlines()[12]
    print contentrows
    f = open(txtfile) # 打开txt文件，以‘utf-8'编码读取
    line_number=len(f.readlines())
    print line_number
    array=arcpy.Array()
    point=arcpy.Point()
    for i in range(line_number)[13:]:
        pt=linecache.getline(txtfile, line_number).strip().split(',')
        yx=pt[2:]
##        print yx
        point.X = float(yx[1]);
        point.Y = float(yx[0])
##        print('float(yx[1])+':'+float(yx[0]))
        array.add(point)
    row = cursor.newRow()
#    polygon = arcpy.Polygon(array)
    row.shape = array
    contentrow=contentrows.split(',')
    row.name = ''.join(contentrow[3])
    row.FFIDDD = ''.join(contentrow[0])
    row.MJ_mu = ''.join(contentrow[1])
    row.codebm =string.atoi(''.join(contentrow[2]))
    row.shapetype_ = ''.join(contentrow[4])
    row.fenfu = ''.join(contentrow[5])
    array.removeAll() 
    cursor.insertRow(row)
    seq+=seq