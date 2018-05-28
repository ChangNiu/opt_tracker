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
    filename = 'sample/result' + str(case_num) +'.html'
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

def extract_status(text):
    status_start_pattern = re.compile('<h1>')
    status_end_pattern = re.compile('</h1>')
    try:
        status_start = status_start_pattern.search(text).span()[-1]
        status_end = status_end_pattern.search(text).span()[0]
        status = text[status_start: status_end]

        return status
    except:
        return None
        
def extract_date(text):
    try :
        #find date string
        date_start_pattern = re.compile('On')
        date_end_pattern = re.compile(',')

        date_start = date_start_pattern.search(text).span()[-1]
        date_end = date_end_pattern.search(text).span()[0]
        date = text[date_start + 1: date_end]
        print(date)

        #find year int
        year_str = text[date_end + 2: date_end + 6]
        year = int(year_str)
        print(year)

        #find month int
        month_list = re.findall(r'[a-zA-Z]', date)
        month_str = ''
        for letter in month_list:
            month_str = month_str + letter

        ##month dict: convert name to number
        month_dict = {"January": 1, "February": 2, "March":3 , "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}

        month = month_dict['March']
        print(month)

        #find day int
        day_list = re.findall(r'[0-9]', date)
        day_str = ''
        for letter in day_list:
            day_str = day_str + letter 
        day = int(day_str)
        print(day)

        decision_date = datetime.date(year, month, day)
        """ decision_date.day = day
        decision_date.month = month
        decision_date.year = year """
        print(decision_date)
        return decision_date
    except :
        return None


def extract_form(text) :
    try :
        #find FORM type
        form_pattern = re.compile('Form I',re.I)
        form_start_bool = form_pattern.search(text)
        if form_start_bool != None:
            form_start = form_start_bool.span()[0]
            form = text[form_start: form_start + 10]
        else:
            form = ''
    

        return form
    except :
        return None

if __name__ == '__main__':
    t = get_single_page(148020)
    info = extract_info(t)
    print(info)
    status = extract_status(info)
    print(status)
    date = extract_date(info)
    print(date)
    form = extract_form(info)
    print(form)
    # for i in range(100):
    #     get_single_page(i+145000)
