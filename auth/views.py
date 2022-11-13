from tesla.pyhtml import PYHTML
from tesla.pyhtml.tags import  CT, CSS, CSSGroup
from tesla.response import HttpResponse
from tesla.auth.forms import LoginForm
import uuid
# LoginForm().save()


def login(request, user):
    session = uuid.uuid1(98_457_453)
    request.set_cookie('usersession', session)
    request.session.add_to_session(str(session), user)



def LoginView(request):
    form_data = LoginForm()

    if request.method == 'POST':
        username = request.post.get('username')
        password = request.post.get('password')
        login(request, username)
        print(username, password)
    doc = PYHTML()
    head,body = doc.create_doc()

    # head
    title = CT('title', 'Tesla | Authentication View')
    style = CT('style')

    form_style = CSS(
        display = 'flex',
        flexDirection= 'column',
        alignItems = 'center',
        padding = '10px',
        margin = 'auto',
        marginTop = '30px',
        width = '250px',
        gap = '10px',
        backgroundColor = 'lightgray',
        borderRadius = '5px'
    )

    head.append(title)
    # form
    form = CT('form', method='POST', style=form_style.css())
    h2 = CT('h2', 'User login view')


    login_btn = CT('button', 'login')
    form.append(h2, form_data, login_btn)
    body.append(form)
    return HttpResponse(request, str(doc))