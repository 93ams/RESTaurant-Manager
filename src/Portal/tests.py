from portal import app
response = app.get_response('/')
assert response.status_int == 200
assert response.body == '<h1>Wellcome!</h1>'
