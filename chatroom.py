import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ChartRoom():
    def __init__(self,ID,name):
        self.mumber = []
        self.ID = ID
        self.name = name

    def addnewmember(self,user):
        self.mumber.append(user.username)

    def remmember(self,user):
        self.mumber.remove(user.username)

    def getallmumber(self):
        return self.mumber