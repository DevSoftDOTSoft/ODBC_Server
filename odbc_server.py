#!/usr/bin/python
# -*- coding: utf-8 -*-

from SOAPpy import SOAPServer
from SOAPpy import WSDL
import pyodbc,base64

def CS_XML_Write_Row(row,on_off,file):
    if on_off == 0:
        file.write("<" + row + ">")
    else:
        file.write("</" + row + ">")

def CS_XML_Write_SubRow(row,text,file):
    isint = False
    into = 0
    try:
        into = int(text)
    except:pass
    if into > 0:
        isint = True
    if isint == True:
        file.write("<" + row + ">" + str(text).encode('utf-8') + "</" + row + ">")
    else:
        try:file.write("<" + row + ">" + text.encode('utf-8') + "</" + row + ">")
        except:file.write("<" + row + ">" + str(text).encode('utf-8') + "</" + row + ">")

def execute_query(CON_STRING,SQL):
    cnxn = pyodbc.connect(CON_STRING)
    cursor = cnxn.cursor()
    cursor.execute(SQL)
    tables = cursor.fetchall()
    _CS_XML_FILE = open("filename_tmp_.xml", 'wb')
    CS_XML_Write_Row("QUERY", 0, _CS_XML_FILE)
    for t in tables:
        CS_XML_Write_Row("Row", 0, _CS_XML_FILE)
        for data in t:
            CS_XML_Write_SubRow("Data", data, _CS_XML_FILE)
        CS_XML_Write_Row("Row", 1, _CS_XML_FILE)
    CS_XML_Write_Row("QUERY", 1, _CS_XML_FILE)
    _CS_XML_FILE.close()
    f = open("filename_tmp_.xml", 'rb')
    XML = f.read()
    f.close()
    print("Sending : " + str(len(base64.b64encode(XML))) + " bytes...")
    return base64.b64encode(XML)

def EXECUTE():
    server = SOAPServer(('0.0.0.0', 8022),log=1)
    server.registerFunction(execute_query)
    print("Started...")
    server.serve_forever()
EXECUTE()
