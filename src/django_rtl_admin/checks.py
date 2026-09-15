"""System checks: catch the three ways this app is usually mis-installed."""

from __future__ import annotations

from django.conf import settings
from django.core.checks import Warning, register

from .conf import SETTINGS_KEY, rtl_settings

APP_NAME = "django_rtl_admin"
ADMIN_APP = "django.contrib.admin"


@register()
def check_app_order(app_configs, **kwargs):
    """``django_rtl_admin`` must shadow the contrib admin templates."""
    installed = list(getattr(settings, "INSTALLED_APPS", []))
    names = [entry.split(".apps.")[0] for entry in installed]
    if APP_NAME not in names or ADMIN_APP not in names:
        return []
    if names.index(APP_NAME) < names.index(ADMIN_APP):
        return []
    return [
        Warning(
            f"{APP_NAME!r} is listed after {ADMIN_APP!r} in INSTALLED_APPS.",
            hint=(
                f"Template overrides are resolved in INSTALLED_APPS order, so "
                f"{APP_NAME!r} must come before {ADMIN_APP!r} for the "
                f"direction-aware admin templates to take effect."
            ),
            id="rtl_admin.W001",
        )
    ]


@register()
def check_settings_keys(app_configs, **kwargs):
    """Typos in ``RTL_ADMIN`` fail silently otherwise."""
    unknown = rtl_settings.unknown_keys()
    if not unknown:
        return []
    return [
        Warning(
            f"Unknown {SETTINGS_KEY} keys: {', '.join(unknown)}.",
            hint=(
                "These keys are ignored. Supported keys are: "
                + ", ".join(sorted(rtl_settings.defaults))
                + "."
            ),
            id="rtl_admin.W002",
        )
    ]


@register()
def check_language_switcher(app_configs, **kwargs):
    """The switcher needs ``set_language`` routed and ``LocaleMiddleware`` on."""
    if not rtl_settings.LANGUAGE_SWITCHER:
        return []
    issues = []

    from django.urls import NoReverseMatch, reverse

    try:
        reverse("set_language")
    except (NoReverseMatch, Exception):
        issues.append(
            Warning(
                "The admin language switcher is enabled but 'set_language' "
                "cannot be reversed.",
                hint=(
                    "Add `path('i18n/', include('django.conf.urls.i18n'))` to "
                    "your root URLconf, or set "
                    f'{SETTINGS_KEY}["LANGUAGE_SWITCHER"] = False.'
                ),
                id="rtl_admin.W003",
            )
        )

    middleware = list(getattr(settings, "MIDDLEWARE", []))
    if "django.middleware.locale.LocaleMiddleware" not in middleware:
        issues.append(
            Warning(
                "django.middleware.locale.LocaleMiddleware is not installed, so "
                "a language chosen in the admin will not stick.",
                hint=(
                    "Add 'django.middleware.locale.LocaleMiddleware' to "
                    "MIDDLEWARE, after SessionMiddleware and before "
                    "CommonMiddleware."
                ),
                id="rtl_admin.W004",
            )
        )
    return issues
