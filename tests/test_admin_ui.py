import re

import pytest
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse

from tests.testapp.models import Company

pytestmark = pytest.mark.django_db

CHANGELIST = reverse("admin:testapp_company_changelist")


def login(client: Client, next_url: str) -> HttpResponse:
    return client.post(
        reverse("admin:login"),
        {"username": "admin", "password": "password", "next": next_url},
        follow=True,
    )


@pytest.fixture
def form_admin_client(client: Client, admin_user: User) -> Client:
    assert login(client, reverse("admin:index")).status_code == 200
    return client


def header_href(html: str, label: str) -> str:
    match = re.search(rf'<a [^>]*href="([^"]+)"[^>]*>{re.escape(label)}</a>', html)
    assert match, f"no sort link for {label!r}"
    return match.group(1)


def changelist_tbody(html: str) -> str:
    return html.split("<tbody>")[1].split("</tbody>")[0]


def test_login_form_reaches_changelist(client: Client, admin_user: User) -> None:
    response = login(client, reverse("admin:index"))

    assert response.status_code == 200
    assert "Site administration" in response.content.decode()


def test_changelist_renders_decorated_columns(form_admin_client: Client) -> None:
    Company.objects.create(name="Acme", owner_name="zoe", is_active=True)
    Company.objects.create(name="Globex", owner_name="amy", is_active=False)

    response = form_admin_client.get(CHANGELIST)
    html = response.content.decode()

    assert response.status_code == 200
    for heading in (
        "Company owner",
        "Name length",
        "Active",
        "Nickname",
        "Owner (lower)",
    ):
        assert heading in html
    rows = changelist_tbody(html)
    assert "Acme" in rows
    assert re.search(r'class="field-name_length">4</td>', rows)
    assert "(none)" in rows
    assert 'alt="True"' in rows
    assert 'alt="False"' in rows


def test_clicking_owner_header_orders_by_admin_order_field(
    form_admin_client: Client,
) -> None:
    Company.objects.create(name="Acme", owner_name="zoe", is_active=True)
    Company.objects.create(name="Globex", owner_name="amy", is_active=False)

    response = form_admin_client.get(CHANGELIST)
    href = header_href(response.content.decode(), "Company owner")

    response = form_admin_client.get(f"{CHANGELIST}{href}")
    html = response.content.decode()

    assert response.status_code == 200
    assert [company.owner_name for company in response.context["cl"].result_list] == [
        "amy",
        "zoe",
    ]
    rows = changelist_tbody(html)
    assert rows.index("Globex") < rows.index("Acme")
    ordered_names = Company.objects.order_by("owner_name").values_list(
        "name", flat=True
    )
    assert list(ordered_names) == ["Globex", "Acme"]


def test_clicking_expression_header_orders_case_insensitively(
    form_admin_client: Client,
) -> None:
    Company.objects.create(name="Acme", owner_name="Zoe", is_active=True)
    Company.objects.create(name="Globex", owner_name="amy", is_active=False)

    response = form_admin_client.get(CHANGELIST)
    href = header_href(response.content.decode(), "Owner (lower)")

    response = form_admin_client.get(f"{CHANGELIST}{href}")

    assert response.status_code == 200
    assert [company.name for company in response.context["cl"].result_list] == [
        "Globex",
        "Acme",
    ]


def test_add_company_through_admin_form(form_admin_client: Client) -> None:
    response = form_admin_client.post(
        reverse("admin:testapp_company_add"),
        {"name": "Initech", "owner_name": "peter", "is_active": "on"},
    )

    assert response.status_code == 302
    assert response.url == CHANGELIST

    response = form_admin_client.get(response.url)

    assert Company.objects.get().name == "Initech"
    assert "Initech" in response.content.decode()
