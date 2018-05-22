import requests

target_url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
userAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

def craw_page(formdata, http_session):
    http_session.headers['User-Agent'] = userAgent
    r = http_session.post(target_url, data=formdata)
    return r.text

def get_single_page():
    s = requests.Session()
    http_form = {
        'appReceiptNum': 'YSC1890125000',
        'initCaseSearch': 'CHECK+STATUS',
        'changeLocale': ''
        }
    raw_html = craw_page(http_form, s)
    f = open('result.html', 'w')
    f.write(raw_html)


if __name__ == '__main__':
    get_single_page()