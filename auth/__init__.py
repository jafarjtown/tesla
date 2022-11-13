
class Anonymous:
    pass

    def __str__(self):
        return 'Anonymous User'

class Authentication:
    def __init__(self):
        self.ANONYMOUS = Anonymous()
        self.user = None
        
        pass
    
    def get_user(self):
        if self.user is None:
            return self.ANONYMOUS
        return self.user
    def set_user(self, obj):
        self.user = obj
        return self.user

    def authenticate(self, cookie:str, session: dict):
       
        if cookie == None:
            return False
        for c in cookie.split(';'):
            key, value = c.split('=')
            # print(2)
            if key.strip() == 'usersession':
                # print(3, session) 
                if value.strip() in session.keys():
                    # print(4)
                    self.set_user(session.get(value.strip()))
     
        
