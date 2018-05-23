import requests

target_url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
userAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

def craw_page(formdata, http_session):
    http_session.headers['User-Agent'] = userAgent
    r = http_session.post(target_url, data=formdata)
    return r.text

def get_single_page(case_num):
    s = requests.Session()
    http_form = {
        'appReceiptNum': 'YSC1890',
        'initCaseSearch': 'CHECK+STATUS',
        'changeLocale': ''
        }
    http_form['appReceiptNum'] += str(case_num)
    raw_html = craw_page(http_form, s)
    filename = 'result' + str(case_num) +'.html'
    f = open(filename, 'w')
    f.write(raw_html)


if __name__ == '__main__':
    for i in range(100):
        get_single_page(i+145000)