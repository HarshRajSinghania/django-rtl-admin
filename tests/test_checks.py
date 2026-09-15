"""The system checks."""

from django.test import override_settings

from django_rtl_admin import checks


def ids(warnings):
    return sorted(warning.id for warning in warnings)


def test_a_correct_installation_reports_nothing():
    assert checks.check_app_order(None) == []
    assert checks.check_settings_keys(None) == []
    assert checks.check_language_switcher(None) == []


@override_settings(
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django_rtl_admin",
        "tests.testapp",
    ]
)
def test_the_app_order_is_checked():
    warnings = checks.check_app_order(None)
    assert ids(warnings) == ["rtl_admin.W001"]
    assert "INSTALLED_APPS" in warnings[0].msg


@override_settings(INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.auth"])
def test_the_app_order_check_is_silent_without_the_admin():
    assert checks.check_app_order(None) == []


@override_settings(RTL_ADMIN={"ENABEL_CSS": True})
def test_unknown_settings_keys_are_reported():
    warnings = checks.check_settings_keys(None)
    assert ids(warnings) == ["rtl_admin.W002"]
    assert "ENABEL_CSS" in warnings[0].msg


@override_settings(ROOT_URLCONF="tests.urls_without_i18n")
def test_a_missing_set_language_route_is_reported():
    assert "rtl_admin.W003" in ids(checks.check_language_switcher(None))


@override_settings(MIDDLEWARE=["django.contrib.sessions.middleware.SessionMiddleware"])
def test_missing_locale_middleware_is_reported():
    assert "rtl_admin.W004" in ids(checks.check_language_switcher(None))


@override_settings(
    RTL_ADMIN={"LANGUAGE_SWITCHER": False},
    ROOT_URLCONF="tests.urls_without_i18n",
    MIDDLEWARE=[],
)
def test_the_switcher_checks_are_skipped_when_it_is_disabled():
    assert checks.check_language_switcher(None) == []


def test_the_checks_are_registered_with_django():
    from django.core.checks import registry

    registered = {check.__name__ for check in registry.registry.get_checks()}
    assert {"check_app_order", "check_settings_keys", "check_language_switcher"} <= registered
