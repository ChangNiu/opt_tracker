import requests
import re

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
    return raw_html

def extract_info(raw_html):
    print(type(raw_html))
    targ_class_pattern = re.compile('rows text-center">')
    try:
        location1 = targ_class_pattern.search(raw_html).span() #location of 'rows text-center'
        location1_end = location1[-1]

        targ_div_pattern = re.compile('</div>') #location of the first following '</div>'
        location2 = targ_div_pattern.search(raw_html, location1_end).span()
        location2_start = location2[0]

        return raw_html[location1_end + 1: location2_start]
    except:
        return None

def extract_detail(text):
    pass


if __name__ == '__main__':
    t = get_single_page(145100)
    print(extract_info(t))
    # for i in range(100):
    #     get_single_page(i+145000)
