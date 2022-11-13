from dataclasses import dataclass
from tesla.modal import Modal



@dataclass
class UserBaseModal(Modal):
    username : str 
    email : str
    password : str

    def save(self):
        # check if no User with this username
        if self.get(username = self.username):
            raise Exception('User with this username already exists')
        # hashes the password
        return super().save()