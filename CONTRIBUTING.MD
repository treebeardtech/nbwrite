
## Developing

nbwrite uses devcontainers to pre-configure a dev environment. We recommend you open the project in vscode with the remote containers extension to contribute.

For non-vscode users, here are some install steps:

### Install local package
```
poetry install # warning, by default this will install without a venv unless you modify poetry.toml
```

### Activate shell
```
poetry shell
```

### Run static checks
```
pre-commit run --all-files
pre-commit install
```

### Run tests
```
pytest
```
