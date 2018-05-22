from html.parser import HTMLParser
class GetIdList(HTMLParser):
    def reset(self): #default
        self.IDlist = []
        self.flag = False
        self.getdata = False
        self.verbatim = 0
        HTMLParser.reset(self) #question?

    def start_div(self, attrs):
        if self.flag == True:
            self.verbatim +=1 #进入子层div了，层数加1
            return
        for k,v in attrs:#遍历div的所有属性以及其值
            if k == 'class' and v == 'rows text-center':#确定进入了<div class='rows text-center>
                self.flag = True
                return

    def end_div(self):#遇到</div>
        if self.verbatim == 0:
            self.flag = False
        if self.flag == True:#退出子层div了，层数减1
            self.verbatim -=1

    def start_p(self, attrs):
        if self.flag == False:
            return
        self.getdata = True

    def end_p(self):#遇到</p>
        if self.getdata:
            self.getdata = False

    def handle_data(self, text):#处理文本
        if self.getdata:
            self.IDlist.append(text)

    def printID(self):
        for i in self.IDlist:
            print(i)


##import urllib2
##import datetime
##vrg = (datetime.date(2012,2,19) - datetime.date.today()).days
##strUrl = 'http://www.nod32id.org/nod32id/%d.html'%(200+vrg)
##req = urllib2.Request(strUrl)#通过网络获取网页
##response = urllib2.urlopen(req)
##the_page = response.read()

htmlfile = open('/home/c/h/changn/Download/result.html','r')
the_page = htmlfile.read()
lister = GetIdList()
lister.feed(the_page)
lister.printID()
