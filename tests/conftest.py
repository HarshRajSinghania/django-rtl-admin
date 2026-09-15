import pytest
from django.contrib import admin

from tests.testapp.models import Thing


@pytest.fixture
def thing(db):
    return Thing.objects.create(
        name="Deep Learning",
        name_ar="التعلم العميق",
        reference="978-0-262-03561-3",
        quantity=1234,
        price="349.90",
    )


@pytest.fixture
def thing_admin():
    return admin.site._registry[Thing]
