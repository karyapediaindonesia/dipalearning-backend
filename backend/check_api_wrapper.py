import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from django.test import Client
from apps.accounts.models import User

c = Client()
user = User.objects.first()
c.force_login(user)

endpoints = [
    '/api/v1/attendance/absence-reasons/',
    '/api/v1/finance/fee-categories/',
    '/api/v1/hr/job-positions/',
    '/api/v1/billing/payment-methods/',
    '/api/v1/academics/academic-periods/'
]

for url in endpoints:
    response = c.get(url)
    if response.status_code == 200:
        content = response.json()
        has_data = 'data' in content
        print(f"{url} -> wrapped in 'data'? {has_data}")
    else:
        print(f"{url} -> status {response.status_code}")
