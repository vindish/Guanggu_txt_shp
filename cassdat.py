# -*- coding: utf-8 -*-
import arcpy
import os
import random
import datetime
import time
today=datetime.date.today()
formatted_today=today.strftime('%y%m%d')
nowtime=time.strftime("%H%M%S")
wkt='PROJCS["Xian_1980_GK3_NO38",GEOGCS["GCS_Xian_1980",DATUM["D_Xian_1980",SPHEROID["Xian_1980",6378140.0,298.257]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",114.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'
print (wkt.split(',')[0][8:-1])
rootpath=os.getcwd()
arcpy.env.workspace=rootpath
envworkspace = arcpy.env.workspace
print (envworkspace)
datType='.dat'
shpType='.shp'
def getZ(lenxyz):
    if lenxyz>2:
      return float(xyz[2])
    elif lenxyz<=2:
      return 0
    else:
      return 99999
def codebmdef(code1):
    if code1:
      return 0
    elif not code1:
      return str(code1)
    else:
      return 9999
def getFileList(envworkspace, datType):
    fileFullPathList = []
    fileNameList = []
    filenameList = os.listdir(envworkspace)
    for fn in filenameList:
        file_name, file_ext = os.path.splitext(fn)
        if file_ext == datType:
            fileNameList.append(file_name)
    return fileNameList
#print getFileList(envworkspace, datType)
fileNameList = []
fileNameList.append(getFileList(envworkspace,datType))
seq=0
for seq in range(len(fileNameList[0])):
    rnd='%d' %(random.randint(10,99))
    fileName1=fileNameList[0][seq]
#    print (fileName1)
    filename2=''.join(fileName1)
    fc = (filename2+'_'+formatted_today+'_'+nowtime+'_'+rnd+shpType)    #xxx.shp
    allpathfc = os.path.join(os.path.join(envworkspace,filename2), fc)    #C:/sff/xxx.shp
    print os.path.join(envworkspace,filename2+datType)
    arcpy.CreateFolder_management(envworkspace, filename2)
    print os.path.join(envworkspace,filename2,filename2+shpType)
    f=open(os.path.join(envworkspace,filename2+datType))    #c:/sff/xxx.dat
    point=arcpy.Point()
    sr = arcpy.SpatialReference()
    sr.loadFromString(wkt)
    arcpy.CreateFeatureclass_management(os.path.join(envworkspace,filename2), fc, 'Point','','','',sr)
    arcpy.AddField_management(allpathfc,'name','TEXT',99)
    arcpy.AddField_management(allpathfc,'codebm','TEXT',99)
    arcpy.AddField_management(allpathfc,'X','double')
    arcpy.AddField_management(allpathfc,'Y','double')
    arcpy.AddField_management(allpathfc,'Z','double')
    cursor = arcpy.InsertCursor(allpathfc, ['SHAPE@'])
    for line in f:
        try:
            Linestr=line.split(',')
            if  len(Linestr)==5:
                xyz = Linestr[2:]
                codebm=codebmdef(Linestr[1])
                name=Linestr[0]
                X = float(xyz[0]);
                Y = float(xyz[1]);
                lenxyz=int(len(xyz))
                Z = getZ(lenxyz)
                point.Y = Y;
                point.X = X;
                point.Z = Z;
                row = cursor.newRow()
                row.shape = point
                row.name = name
                row.codebm = codebm
                row.X = X
                row.Y = Y
                row.Z = Z
##                array.removeAll()
                cursor.insertRow(row)
            elif  len(Linestr)==4:
                xyz = Linestr[1:]
                name=Linestr[0]
                X = float(xyz[0]);
                Y = float(xyz[1]);
                lenxyz=int(len(xyz))
                Z = getZ(lenxyz)
                point.Y = Y;
                point.X = X;
                point.Z = Z;
                row = cursor.newRow()
                row.shape = point
                row.name = name
                row.X = X
                row.Y = Y
                row.Z = Z
##                array.removeAll()
                cursor.insertRow(row)
            else:
                continue
        except OSError:
            pass
        continue