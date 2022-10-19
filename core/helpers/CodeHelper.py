import json, requests, pytz, random, secrets, string
from datetime import datetime, timedelta
from UserManagement.Controllers import LocationController

class CodeHelper: 


    #generate expiration date based on country
    @staticmethod
    def generateExpirationDate(request):
        response = json.loads(requests.get(f"https://ipinfo.io/{LocationController.getUserIp(request)}/json").content)
        if response["ip"] == "127.0.0.1":
            return datetime.now() + timedelta(minutes=5)
        return datetime.now(pytz.timezone(response["timezone"])) + timedelta(minutes=5)
    

    #generate random confirmation/verification code
    @staticmethod
    def generateCode():
        n = random.randint(6,10)
        res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(n))
        return res