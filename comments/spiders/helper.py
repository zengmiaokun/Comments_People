import requests
import json


api = 'http://liuyan.people.com.cn/threads/queryThreadsList'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Host': 'liuyan.people.com.cn',
    'Origin': 'http://liuyan.people.com.cn',
    'Connection': 'keep-alive',
    'Referer': 'http://liuyan.people.com.cn/threads/list?fid=571',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}

def load_data(api, formdata, headers):
    r = requests.post(api, data=formdata, headers=headers)
    data = json.loads(r.text)
    return data

def getTid(fid, domainName):
    headers['Referer'] = 'http://liuyan.people.com.cn/threads/list?fid=' + str(fid)
    formdata = {'fid': fid, 'lastItem': 0}
    tids = []
    while True:
        data = load_data(api, formdata, headers)
        for line in data['responseData']:
            if line['domainName'] in domainName:
                print("Get `tid`: %s" % str(line['tid']))
                tids.append(str(line['tid']))
        if len(data['responseData']) < 10:
            break
        else:
            formdata['lastItem'] = str(data['responseData'][-1]['tid'])
    return tids

if __name__ == "__main__":
    print(getTid(4489, ['医疗']))