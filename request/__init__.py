import cgi
import cgitb; cgitb.enable()
from dataclasses import dataclass
import os
import tempfile
import string 
import random as r
# from Cookie import SimpleCookie


@dataclass
class TemporaryFile:
    
    
    def __init__(self, file, filename,path, *args, **kwargs) -> None:
        self.file = file
        self.filename = filename
        self.path = path 
        
        # print(self.filename, self.file)
    
    def save(self):
        # print('file obj',self.file)
        def fbuffer(f, chunk_size=10000):
            while True:
                chunk = f.read(chunk_size)
                if not chunk: break
                yield chunk
        fn = os.path.basename(self.filename)
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        with open(self.path+'/'+fn , 'wb+') as f:
            for chunk in fbuffer(self.file.file):
                f.write(chunk)
        return self.path+'/'+fn        

class PostBody:
    def __init__(self, data):
        self.data = data 
    
    def get(self, key):
        value = self.data.get(key)
        # if type(value) == str:
        #     print(dir(cgi))
        #     value = cgi.escape(value)

        return value
    
    def set(self, key, value):
        self.data[key] = value

    def __iter__(self):
        for key, value in self.data:
            yield key, value

    

class Request:
    def __init__(self, environ, start_response, app, csrf, authentication, context, session, auth_model):
        self.app = app
        self.csrf = csrf
        self.environ = environ
        self.start_response = start_response
        self.cookie = []
        self.context = context
        self.session = session
        self.auth_model = auth_model
        # self.headers = [*self.cookie]

        self.http_host = environ['HTTP_HOST']
        self.http_user_agent = environ['HTTP_USER_AGENT']
        self.http_cookie = environ.get("HTTP_COOKIE")
        self.lang = environ.get('LANG')
        self.method = environ.get('REQUEST_METHOD')
        self.path = environ.get('PATH_INFO')
        self.host_address = environ.get('HTTP_HOST')
        self.gateway_interface = environ.get('GATEWAY_INTERFACE')
        self.server_port = environ.get('SERVER_PORT')
        self.remote_host = environ.get('REMOTE_HOST')
        self.content_type = environ.get('CONTENT_TYPE')
        self.content_length = environ.get('CONTENT_LENGTH')
        self.body = environ.get('BODY')
        self.query_string = environ.get('QUERY_STRING')
        self.server_protocol = environ.get('SERVER_PROTOCOL')
        self.server_software = environ.get('SERVER_SOFTWARE')

        # auth request's
        authentication.authenticate(self.http_cookie, self.session.values)

        self.user = authentication.get_user()
        self.is_authenticated = self.user != authentication.ANONYMOUS 

        self.parse_qs()
        self.pass_csrf()
        pass
    def pass_csrf(self):
        
        if self.method == 'POST':
         
            csrf = self.post.get('csrfmiddleware')
            if csrf is not None:
                if csrf in self.app.csrf_tokens:
                    
                    self.app.csrf_tokens.remove(csrf)
                    self.csrf = self.app.csrf_tokens[r.randint(0, len(self.app.csrf_tokens)-1)]
                    
                    self.app.csrf_tokens.append(''.join(r.sample([*string.ascii_letters,  *string.hexdigits],55)))
                    return None
                # self.csrf = self.app.csrf_tokens[r.randint(0, len(self.app.csrf_tokens)-1)]
            # print(self.csrf)
            
            raise Exception('csrf is not provided')    
 
    def parse_qs(self):
        # print(self.environ)
        if self.method != 'POST':
            # self.
            return
        
        self.post = PostBody({})
        environ = self.environ
        field_storage = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=environ,
            keep_blank_values = True 
        )
         
        for item in field_storage.list:
            if not item.filename:
                self.post.set(item.name, item.value)
            else:
                # print(item)
                self.post.set(item.name, TemporaryFile(file=item, filename=item.filename, path=self.app.media_file))
                
    def get_cookie(self):
        return ';'.join(self.cookie)  

    def set_cookie(self, k, v):
        self.cookie.append(f'{k}={v}')
            
