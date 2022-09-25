#!/usr/bin/python3

import requests
import os, re

base_url = "https://igracias.telkomuniversity.ac.id/"

rs = requests.Session()

data = {
    "textUsername" : os.getenv("IGRACIAS_USERNAME"),
    "textPassword" : os.getenv("IGRACIAS_PASSWORD"),
    "submit" : ""
}

rs.headers.update({
    "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "Accept-Language" : "en-US,en;q=0.5",
    "Accept-Encoding" : "gzip, deflate, br",
    "X-Requested-With" : "XMLHttpRequest",
    "Connection" : "keep-alive",
    "Sec-Fetch-Dest" : "empty",
    "Sec-Fetch-Mode" : "cors",
    "Sec-Fetch-Site" : "same-origin"
})  

rs.cookies.update({
    "_gcl_au" : "1.1.1274631097.1663075193",
    "_ga" : "GA1.3.213628018.1663075194",
    "_ga_0VSYWXVH4F" : "GS1.1.1663837487.3.0.1663837487.60.0.0",
    "_ga_FKY2TW5PXG" : "GS1.1.1663077157.2.0.1663077157.60.0.0",
    "ajs_anonymous_id" : "e90c3cc1-ceb8-4457-a9ea-3c7e2d100020",
    "_fbp" : "fb.2.1663075195875.44183416",
    "_ga_5GCT5Q5W61" : "GS1.1.1663220043.6.0.1663220043.0.0.0",
    "_clck" : "1hdxta5|1|f53|0",
    "_ga_CMWRTPYNJ0" : "GS1.1.1663837490.1.1.1663837943.0.0.0",
    "_gid" : "GA1.3.1715072394.1664083712",
})

student_id = ''    

while 'i-GRACIAS' in student_id or not student_id:
    response = rs.post(base_url, data = data)
    student_id = re.findall(r'\<title\> \r\n(.*)\</title\>', response.text)[0]
    student_id = student_id.split(' | ')[0]

print(rs.headers)
print(rs.cookies)

for _ in range(5):
    # response = rs.get(f"https://igracias.telkomuniversity.ac.id/libraries/ajax/ajax.schedule.php?act=viewStudentSchedule&studentId={student_id}")
    response = rs.get(f"https://igracias.telkomuniversity.ac.id/libraries/ajax/ajax.schedule.php?act=viewStudentSchedule&studentId={student_id}&sEcho=1&iColumns=7&sColumns=&iDisplayStart=0&iDisplayLength=20&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&mDataProp_5=5&mDataProp_6=6&sSearch=&bRegex=false&sSearch_0=&bRegex_0=false&bSearchable_0=true&sSearch_1=&bRegex_1=false&bSearchable_1=true&sSearch_2=&bRegex_2=false&bSearchable_2=true&sSearch_3=&bRegex_3=false&bSearchable_3=true&sSearch_4=&bRegex_4=false&bSearchable_4=true&sSearch_5=&bRegex_5=false&bSearchable_5=true&sSearch_6=&bRegex_6=false&bSearchable_6=true&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=true&bSortable_4=true&bSortable_5=true&bSortable_6=true&schoolYear=2223%2F1")
    print(response.text)
