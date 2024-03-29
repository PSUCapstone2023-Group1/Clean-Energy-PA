# Clean-Energy-PA

![CI/CD](https://github.com/PSUCapstone2023-Group1/Clean-Energy-PA/actions/workflows/django-test-stage.yaml/badge.svg)

PaPowerSwitch support application to help connect PA citizens with the best energy suppliers

## Collaboration links

- [Github](https://github.com/PSUCapstone2023-Group1/Clean-Energy-PA)
- [Jira](https://psu-capstone-2023.atlassian.net/jira/software/projects/PC2/boards/1)
- [MS Teams](https://teams.microsoft.com/l/team/19%3aKMnyy48kmrk-UuxkyPXYEEqqOpkXUyXr84Prf3mKq581%40thread.tacv2/conversations?groupId=a9fc0eb9-522d-480d-a52a-68f15a50704f&tenantId=7cf48d45-3ddb-4389-a9c1-c115526eb52e)

## Getting started

### Dependency Installs

- `pip install -r requirements.txt` -- production requirements
- `pip install -r requirements.dev.txt` -- development requirements

### Environment Setup

#### PostgreSQL Setup

Setup PostgreSQL locally

 1. To setup and run PostgreSQL locally follow this guide.
    - Tip: On windows, after installing and setting up PostgreSQL you can also use the very popular pgadmin4 client application to navigate and interact with the server and database.
 2. Create a database within your server
    - [Create db Tutorial](https://www.postgresql.org/docs/15/tutorial-createdb.html)

#### .Env Setup

You also should create a `.env` file in the `src/Clean-Energy-PA-Site/Website` directory, that includes the following variables with the values set:

> Note: Examples provided are not used in production

```YAML
SECRET_KEY=django-insecure-s2n+&9@6-is&v951p)!j)-8=pr_7r1*=@*8z-x)(rlis*wf9%7
DB_USER=postgres
DB_PASSWORD=ExampleDBPassword123
DB_NAME=mydb
DB_HOST=localhost
DB_PORT=5001
SMTP_USER=exampleuser@gmail.com
SMTP_PASSWORD=ExampleEmailPassword123
CURRENT_DOMAIN=https://127.0.0.1:8000
```

> Notes:
>
> - `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_HOST`, and `DB_PORT` are all values defined by your instance of `PostgreSQL`.
> - The `SECRET_KEY` can be any random 50 characters with the django-insecure prefix for local use. You can use the online [django-secret-key-generator](https://django-secret-key-generator.netlify.app/) to generate one for you.
> - The `SMTP_USER` and `SMTP_PASSWORD` values are based on the email service setup for your environment.

### Django Commands

> First be sure your terminal is at the same directory as `manage.py`, which will be under `src/Clean-Energy-PA-Site` (the Django starting point)

- Run server: `python manage.py runserver`
- Run Tests (without coverage):
  - `python manage.py test`
- Run Tests (with coverage):
  - `coverage run manage.py test`
    - > Note: adding the `-v 2` flag will provide a verbose test output
  - `coverage report` (generates report in terminal)
  - `coverage html` (generates html version of report)

### Web Parser Commands

> First change your terminal's directory to `src/web_parser`

- Run Tests (without coverage):
  - `python -m pytest .`
- Run Tests (with coverage):
  - `coverage run pytest .`
- Run Coverage Report
  - `coverage report` (generates report in terminal)
  - `coverage html` (generates html version of report)

## PyTest

### Debugging

To debug tests that are using the pytest framework you can either

1. Use VS Code with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) installed, follow the guide [here](https://code.visualstudio.com/docs/python/testing).
   - This route makes it much easier to debug in the VS Code environment and see your tests pass in a nice interface
2. Using the Python debugger (pdb) - [guide](https://docs.pytest.org/en/7.1.x/how-to/failures.html)
   - This route is more versatile as it can be used in the terminal

## Dependency Documentation

- [django-environ](https://django-environ.readthedocs.io/en/latest/)
- [django-cripsy-forms](https://django-crispy-forms.readthedocs.io/en/latest/)
- [crispy-bootstrap5](https://pypi.org/project/crispy-bootstrap5/)

## Front-End

- [Bootstrap](https://getbootstrap.com/docs/5.0/getting-started/introduction/)

## Other modules

- [uszipcode](https://pypi.org/project/uszipcode/)
