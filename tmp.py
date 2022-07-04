import requests



req = requests.post('http://127.0.0.1:5000/api/employees', name='TestAPI', last_name='WOW', main_technology='Python', status='Free')


print(req.json())
