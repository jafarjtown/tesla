from tesla.request import Request
from tesla.template import Template
import os



# from jinja2 import Environment, PackageLoader


class Response:
    def __init__(self, request: Request, status_code: str, content_type: str):
        
        self.status_code = status_code
        self.start_response = request.start_response
        self.content_type = content_type
        # print(request.get_cookie())
        self.headers = [('Content-type', self.content_type), ('Set-cookie', request.get_cookie())]
        self.response_content = []
        self.templates_folders = ['./']

        
        ...

    def make_response(self):
        self.start_response(self.status_code, self.headers)
        return self.response_content

    def parse_cookie(self, cookie):
        cookie = cookie.split(';')
        obj = {}
        for c in cookie:
            c = c.split('=')
            obj[c[0]] = c[1]
        cookie = obj
        return obj.items()

class Render(Response):
    
    def __init__(self, request: Request, content, context = {},  status_code = '200 OK', content_type = 'text/html'):
        
        # request.cookie = self.parse_cookie(request.http_cookie)
        super().__init__(request, status_code, content_type)
        # env = Environment(loader=PackageLoader('jinja2', '/'))

        if self.is_available(content) is not None:
            # template = env.get_template(self.is_available(content))
            with open(self.is_available(content), 'r') as file:
                content = file.read()
                content = Template(content, {'csrf':request.csrf, **request.context.get_objs(), **request.params, **context}).render()
        else:
            content = f'Template {content} not found.'
        # content = template.render(*context)
        self.response_content.append(content.encode()) 

    def is_available(self, filename):
        for path in self.templates_folders:
            if os.path.isfile(path + filename):
                return path + filename
        return None


class HttpResponse(Response):
    
    def __init__(self, request: Request,content,  status_code = '200 OK', content_type = 'text/html'):
        super().__init__(request, status_code, content_type)
        if type(content) == str:
            content = content.encode()
        self.response_content.append(content) 

    
class JsonResponse(Response):
    
    def __init__(self, request: Request,content : str,  status_code = '200 OK', content_type = 'application/json'):
        super().__init__(request, status_code, content_type)
        import json
        content = json.dumps(content).encode()
        self.response_content.append(content) 
    

class ErrorResponse(Response):
    def __init__(self, request: Request, error_code: str):
        super().__init__(request, '404 Not Found', 'text/html')
        # self.response_content.append('Server Error'.encode())


class Http404Response(ErrorResponse):
    def __init__(self, request: Request):
        super().__init__(request, '404 Not Found')
        self.response_content.append('404 Not Found'.encode())
        
class Http500Response(ErrorResponse):
    def __init__(self, request: Request, message):
        super().__init__(request, '500 Server Error')
        self.response_content.append(f'500 Server Error \n {message}'.encode())        
        