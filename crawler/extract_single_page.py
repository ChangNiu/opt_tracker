import requests
import re
import datetime

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
    filename = 'sample/result' + str(case_num) +'.html'
    # f = open(filename, 'w')
    # f.write(raw_html)
    return raw_html

def extract_info(raw_html):
    #print(type(raw_html))
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

def extract_status(text):
    status_start_pattern = re.compile('<h1>')
    status_end_pattern = re.compile('</h1>')
    
    status_start = status_start_pattern.search(text).span()[-1]
    status_end = status_end_pattern.search(text).span()[0]
    status = text[status_start: status_end]

    return status
    
        
def extract_date(text):
    
    #find date string
    date_pattern = re.compile(r'On\ [a-zA-Z]+\ \d{1,2},\ \d{4}')
    date_str = date_pattern.search(text).group()
    date_str_list = re.split('\W', date_str)
    
    day = int(date_str_list[2])
    year = int(date_str_list[-1])
    month_str = date_str_list[1]

    #month dict: convert name to number
    month_dict = {"January": 1, "February": 2, "March":3 , "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
    month = month_dict[month_str]
    
    #create date
    decision_date = datetime.date(year, month, day)
    
    return decision_date



def extract_form(text) :
    form_pattern = re.compile(r'Form\ I\-[0-9]{3}',re.I)
    form_result = form_pattern.search(text)
    if form_result != None:
        form_result = form_result.group(0)
    return form_result
    

if __name__ == '__main__':
    t = get_single_page(148020)
    info = extract_info(t)
    #print(info)
    status = extract_status(info)
    print(status)
    date = extract_date(info)
    print(date)
    form = extract_form(info)
    print(form)
    # for i in range(100):
    #     get_single_page(i+145000)
