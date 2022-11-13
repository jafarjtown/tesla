from dataclasses import dataclass
from tesla.form import Field, Form


@dataclass
class LoginForm(Form):
    username : str = Field(placeholder = 'Enter username', name='username')
    password : str = Field(placeholder = 'Enter password', name= 'password', type = 'password')
