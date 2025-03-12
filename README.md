```bash
pyenv install 3.12
pyenv shell $(pyenv latest 3.12)
poetry env use $(which python) &&  poetry install && source .venv/bin/activate

```

```bash
django-admin compilemessages

```