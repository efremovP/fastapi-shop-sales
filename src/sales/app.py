from fastapi import Body
from fastapi import FastAPI
from fastapi import Response

from .models import GreetFrom

app = FastAPI()


#from JSON
@app.post('/post')
def get_form(form: GreetFrom):
    return Response(f'Get from post {form.name}!')


@app.get('/hallo')
def root(name: str = None):
    return 'Hello, '+ str(name)