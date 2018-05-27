import re

text = """                      <h1>Case Was Received</h1>
                      <p>On March 19, 2018, we received your Form I-765, Application for Employment Authorization, Receipt Number YSC1890148020, and sent you the receipt notice that describes how we will process your case. Please follow the instructions in the notice. If you do not receive your receipt notice by April 18, 2018, please call the USCIS Contact Center at 1-800-375-5283. If you move, go to <a href="https://egov.uscis.gov/coa/displayCOAForm.do" target="_blank">www.uscis.gov/addresschange</a> to give us your new mailing address.</p>"""
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

#find FORM type
form_pattern = re.compile('Form I',re.I)
form_start_bool = form_pattern.search(text)
if form_start_bool != None:
    form_start = form_start_bool.span()[0]
    form = text[form_start: form_start + 10]
else:
    form = ''
print(form)