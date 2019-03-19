

#variable handler

class vhandler:

    def __init__(self):
        self.vars = {}

    def readvar(self, varname):
        return(self.vars[varname])

    def storevar(self, varname, value):
        self.vars[varname] = value

    def checkchange(self, varname, value):
        try:
            if self.vars[varname] == value:
                return False
            else: 
                return True
        except NameError:
            return True

    def changeifnew(self, varname, value):
        if self.checkchange(varname, value):
            self.storevar(varname, value)
        else:
            pass