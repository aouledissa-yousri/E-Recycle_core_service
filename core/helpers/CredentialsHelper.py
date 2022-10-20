from UserManagement.models import GenericUser

class CredentialsHelper: 
    
    def __init__(self, data: dict):
        try:
            self.username = data["username"]
            self.email = data["email"]
        
        except KeyError:
            if "email" in data.keys():
                self.username = GenericUser.objects.get(email = data["email"]).username
                self.email = data["email"]


            elif "username" in data.keys(): 
                self.email = GenericUser.objects.get(username = data["username"]).email
                self.username = data["username"]

            else: 
                self.username = ""
                self.email = ""
        
        self.password = data["password"]



    def getUsername(self):
        return self.username
    
    def getEmail(self):
        return self.email
    
    def getPassword(self):
        return self.password
    
    def getData(self):

        return {
            "username": self.getUsername(),
            "email": self.getEmail(),
            "password": self.getPassword()
        }
