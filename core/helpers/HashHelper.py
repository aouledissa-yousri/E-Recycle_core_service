import string, random, hashlib

class HashHelper: 

    #generate random salt of random length 
    @staticmethod
    def randomSalt(length: int):
        letters = string.ascii_letters 
        return "".join(random.choice(letters) for i in range(length))

    #hash password
    @staticmethod
    def hashPassword(password: str):
        return hashlib.sha512(str(password).encode("UTF-8")).hexdigest()

    #encrypt password using hash and salt
    @staticmethod
    def encryptPassword(hashedPassword: str, salt: str):
        return hashlib.sha512(str(HashHelper.hashPassword(hashedPassword) + salt).encode("UTF-8")).hexdigest()