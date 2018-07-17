from lxml import etree
from io import open
import json
import csv
import os,requests as req
def vuln(filename):
        os.chdir('D:/project/pkl/ParsingXML/data')
        api_url='http://localhost:3000/vulnerabilities'
        i=0
        report = {}
        reportHostName = []
        reportItem = []
        nessusFile = open(filename, 'r')
        xml_content = nessusFile.read()
        nessusFile.close()
        data=[]
        root = etree.fromstring(xml_content)
        for block in root:
            if block.tag == "Report":
                
                for report_host in block:
                    if report_host.tag=="ReportHost":
                        Hostname = report_host.attrib['name']
                        reportItem = []
                        for report_item in report_host:
                            if report_item.tag=="ReportItem":
                                
                                portProtocol = report_item.attrib['svc_name'] +"/" +report_item.attrib['protocol']
                                severity = report_item.attrib['severity']
                                name = report_item.attrib['pluginName'] +" ("+report_item.attrib['pluginID']+")"
                                for param in report_item:
                                    if param.tag=="solution":
                                        solution = param.text

                                    elif param.tag=="synopsis":
                                        synopsis=param.text

                                    elif param.tag =="risk_factor":
                                        risk_factor=param.text

                                    elif param.tag =="description":
                                        desc=param.text

                                detail = synopsis + desc

                                reportItem.append({
                                    'system': Hostname,
                                    'name': name,
                                    'severity': severity,
                                    'port_protocol': portProtocol,
                                    'solution': solution,
                                    'synopsis': synopsis,
                                    'detail': detail,
                                    'risk_level': risk_factor
                                })
                        reportHostName.append({
                            'item':reportItem
                        })
        report.update({
            'hostname' : reportHostName
        })            

        # x=["System", "Name", "Port/Protocol", "Risk Level", "Synopsis","Detail","Solution","Severity"]
        # data.append(x)

    #Put output to csv file
        # myFile=open('vulnv.csv','wb')
        # with myFile:
        #     writer = csv.writer(myFile)
        #     writer.writerows(data)
        #     for x in range (0,len(reportHostName)):
        #         for y in range (0,len(reportHostName[x])):
        #             writer.writerow([reportHostName[x][y]["hostname"],
        #                         reportHostName[x][y]["name"],
        #                         reportHostName[x][y]["port/protocol"],
        #                         reportHostName[x][y]["risk_level"],
        #                         reportHostName[x][y]["synopsis"],
        #                         reportHostName[x][y]["detail"],
        #                         reportHostName[x][y]["solution"],
        #                         reportHostName[x][y]["severity"],
        #                         ])
        # with open('vulnv.csv', 'wb') as csvfile:
        #     f = csv.writer(csvfile)

        #     f.writerow(["System", "Name", "Port/Protocol", "Risk Level", "Synopsis","Detail","Solution","Severity"])

        #     for x in range (0,len(reportHostName)):
        #         for y in range (0,len(reportHostName[x])):
        #             f.writerow([reportHostName[x][y]["hostname"],
        #                         reportHostName[x][y]["name"],
        #                         reportHostName[x][y]["port/protocol"],
        #                         reportHostName[x][y]["risk_level"],
        #                         reportHostName[x][y]["synopsis"],
        #                         reportHostName[x][y]["detail"],
        #                         reportHostName[x][y]["solution"],
        #                         reportHostName[x][y]["severity"],
        #                         ])
        

        # return f
        Jsondata=json.dumps(report)
        headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
        r=req.post(api_url,data=Jsondata,headers=headers)
        print r
        return Jsondata
