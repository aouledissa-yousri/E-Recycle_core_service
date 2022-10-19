from UserManagement.models import GenericUser

class CredentialsHelper: 
    
    def __init__(self, data: dict):
        try:
            self.username = data["username"]
            self.email = data["email"]
            self.password = data["password"]
        
        except KeyError:
            if "email" in data.keys():
                self.username = GenericUser.objects.get(email = data["email"]).username

            elif "username" in data.keys(): 
                self.email = GenericUser.objects.get(username = data["username"]).email

            else: 
                self.username = ""
                self.email = ""


    def getUsername(self):
        return self.username
    
    def getEmail(self):
        return self.email
    
    def getPassword(self):
        return self.password
