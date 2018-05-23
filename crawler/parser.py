import re

htmlfile = open('./result.html','r')
the_page = htmlfile.read()
targ_class_pattern = re.compile('rows text-center')
location1 = targ_class_pattern.search(the_page).span() #location of 'rows text-center'
location1_end = location1[-1]

targ_div_pattern = re.compile('</div>') #location of the first following '</div>'
location2 = targ_div_pattern.search(the_page, location1_end).span()
location2_start = location2[0]

print(the_page[location1_end + 1: location2_start])