class contextPojo:

    def __init__(self, SafeIssue=0, safeId =0, percentage=0, Intent=0):
        self._safeId = safeId
        self._percentage = percentage
        
        self._Intent = Intent
    
    def getsafeId(self):
        return self._safeId

   
    def setsafeId(self, value):
        self._safeId = value

   
    def getpercentage(self):
        return self._percentage

   
    def setpercentage(self, value):
        self._percentage = value

    def getIntent(self):
        return self._Intent
   
    def setIntent(self, value):
        self._Intent = value

    def showall(self):
        dict = {
        "safeId" : self._safeId,
        "percentage" : self._percentage,
        "Intent" : self._Intent,
        }

        return dict
        