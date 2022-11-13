from tesla.static import staticfiles
from tesla.router import router
# from

# path = f'http://{staticfiles.request.http_host}'

def include():
    ...

def static_url(file_path):
   
    complete_url = f'http://{staticfiles.request.http_host}' + staticfiles.url + file_path
    return complete_url    


def url(addr):
    for route in router.routes:
        if ':' in addr:
            ap, ur = addr.split(':')
            addr = f'{ur}_{ap}'
        if route.name == addr:
            return f'http://{staticfiles.request.http_host}'+ route.path 
    return None
