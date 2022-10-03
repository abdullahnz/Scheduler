import requests
import re
import sys

class GetData:
    def __init__(self, u, p):
        self.username = u
        self.password = p
        self.session = requests.Session()
        self.default_headers = {
            'Host': 'igracias.telkomuniversity.ac.id',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://igracias.telkomuniversity.ac.id',
            'Referer': 'https://igracias.telkomuniversity.ac.id/',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Connection': 'close',
        }

    def getCookie(self): # login to igracias
        data = {
            "textUsername" : self.username,
            "textPassword" : self.password,
            "submit" : "Login"
        }
        login = self.session.post('https://igracias.telkomuniversity.ac.id/', headers=self.default_headers, data=data).text

        if re.search('self.location.href=\'index.php\'', login):
            return True
        else:
            return False

    def getStudentID(self):
        response = self.session.get('https://igracias.telkomuniversity.ac.id/registration/?pageid=17985', headers=self.default_headers).text
        student_id = re.findall(r'\<TITLE\> (.*) Registrasi \| Telkom University\</TITLE\>', response.replace('\n', ' '))[0].strip()
        return student_id

    def getJson(self, student_id):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': 'https://igracias.telkomuniversity.ac.id/registration/?pageid=17985',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
        params = {
            'act': 'viewStudentSchedule',
            'studentId': student_id,
            'sEcho': '1',
            'iColumns': '7',
            'sColumns': '',
            'iDisplayStart': '0',
            'iDisplayLength': '20',
            'mDataProp_0': '0',
            'mDataProp_1': '1',
            'mDataProp_2': '2',
            'mDataProp_3': '3',
            'mDataProp_4': '4',
            'mDataProp_5': '5',
            'mDataProp_6': '6',
            'sSearch': '',
            'bRegex': 'false',
            'sSearch_0': '',
            'bRegex_0': 'false',
            'bSearchable_0': 'true',
            'sSearch_1': '',
            'bRegex_1': 'false',
            'bSearchable_1': 'true',
            'sSearch_2': '',
            'bRegex_2': 'false',
            'bSearchable_2': 'true',
            'sSearch_3': '',
            'bRegex_3': 'false',
            'bSearchable_3': 'true',
            'sSearch_4': '',
            'bRegex_4': 'false',
            'bSearchable_4': 'true',
            'sSearch_5': '',
            'bRegex_5': 'false',
            'bSearchable_5': 'true',
            'sSearch_6': '',
            'bRegex_6': 'false',
            'bSearchable_6': 'true',
            'iSortCol_0': '0',
            'sSortDir_0': 'asc',
            'iSortingCols': '1',
            'bSortable_0': 'true',
            'bSortable_1': 'true',
            'bSortable_2': 'true',
            'bSortable_3': 'true',
            'bSortable_4': 'true',
            'bSortable_5': 'true',
            'bSortable_6': 'true',
            'schoolYear': '2223/1',
        }
        result = self.session.get('https://igracias.telkomuniversity.ac.id/libraries/ajax/ajax.schedule.php', params=params, headers=headers).text

        return result

    def saveData(self, filename, data):
        try:
            with open(filename, "w") as f:
                f.write(data)
            return True
        except:
            return False

    def getScheduleJson(self, filename="data.json", verbose=False):
        if verbose: print("[+] Login into igracias")
        cookie = self.getCookie()
        if not cookie:
            print("[-] Login failed")
            return False
        if verbose: print("[+] Get student ID")
        student_id = self.getStudentID()
        if verbose: print("[+] Get schedule json")
        result = self.getJson(student_id)
        if verbose: print("[+] Save result into " + filename)
        save = self.saveData(filename, result)
        if not save: print("[-] Failed to save file")
        print("[+] Result: ")
        print(result)
        return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 " + sys.argv[0] + " [USERNAME] [PASSWORD]")
    else:
        init = GetData(sys.argv[1], sys.argv[2])
        init.getScheduleJson(verbose=True)
