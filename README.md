# Clean-Energy-PA

PaPowerSwitch support application to help connect PA citizens with the best energy suppliers

## Collaboration links

- [Github](https://github.com/PSUCapstone2023-Group1/Clean-Energy-PA)
- [Jira](https://psu-capstone-2023.atlassian.net/jira/software/projects/PC2/boards/1)
- [MS Teams](https://teams.microsoft.com/l/team/19%3aKMnyy48kmrk-UuxkyPXYEEqqOpkXUyXr84Prf3mKq581%40thread.tacv2/conversations?groupId=a9fc0eb9-522d-480d-a52a-68f15a50704f&tenantId=7cf48d45-3ddb-4389-a9c1-c115526eb52e)

## Getting started

### Dependenciy Installs

- `pip install -r requirements.txt` -- production requirements
- `pip install -r requirements.dev.txt` -- development requirements

### Django Commands

> First be sure your terminal is at the same directory as `manage.py`, which will be under `src/Clean-Energy-PA-Site` (the Django starting point)

- Run server: `python manage.py runserver`
- Run Tests: `python manage.py test`
- Run coverage report:
  - `coverage run manage.py test -v 2`
  - `coverage report`
  - `coverage html`

### Web Parser Commands

> First change your terminal's directory to `src/web_parser`

- Run Tests: `pytest .`
- Run coverage report:
  - `coverage run -m pytest .`
  - `coverage report`
  - `coverage html`

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
