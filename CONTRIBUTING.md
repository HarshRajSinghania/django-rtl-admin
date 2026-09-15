# Contributing to django-rtl-admin

Bug reports (a screenshot of the admin in the wrong direction helps most), translations and
small, focused pull requests are all welcome.

## Set up

Python 3.10 or later.

```bash
git clone https://github.com/MarwanMaher0/django-rtl-admin.git
cd django-rtl-admin
python -m venv .venv && . .venv/bin/activate
pip install -e ".[test]"
```

To see the admin in both directions, use the example project and log in as `demo` / `demo12345`:

```bash
cd example
python manage.py migrate
python manage.py demodata
python manage.py runserver
```

## Run the checks

```bash
pytest
ruff check .
# the fallback path, without Babel:
pip uninstall -y Babel && pytest && pip install "Babel>=2.12"
# packaging:
pip install build twine && python -m build && python -m twine check dist/*
```

CI runs Python 3.10 and 3.12 against Django 4.2 and 5.2, and Python 3.12 and 3.13 against
Django 6.1, each with and without Babel, and checks that the wheel carries the templates,
static files and translations.

## Style

- ruff, with the rules and line length in `pyproject.toml`.
- HTML output escapes before it isolates. Follow `mark_isolated` and `mark_isolated_runs`, and
  give any new filter or display helper an autoescape test.
- `rtl-admin.css` uses logical properties. Physical rules are only for things that really are
  directional: sprite offsets, mirrored icons, chevrons.
- Every feature is opt-out through `RTL_ADMIN`. A new key goes in `conf.py` and in the README's
  settings table.
- Translations live in `src/django_rtl_admin/locale/`. Edit the `.po` file, run
  `django-admin compilemessages`, and commit both the `.po` and the `.mo`.
- Anything a user would notice gets a line in `CHANGELOG.md` under `## [Unreleased]`.

## Propose a change

1. For anything bigger than a small fix, open an issue first so the approach is agreed before
   you write code. The roadmap lives in the open issues.
2. Branch from `main`, keep the pull request to one change, and fill in the template.
3. CI must be green before review.

Security problems go through [SECURITY.md](SECURITY.md), not a public issue.
