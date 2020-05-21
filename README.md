## apache_log_analyzer

### Setup
- If you haven't pipenv, please intall pipenv like this.
> install pipenv and dependenciees 

```
$ pip install pipenv
$ cd <path_of_repository>
$ pipenv install
```

### Usage
- Analyze log
```
$ pipenv run main
```
- Add custom module
```
$ pipenv run add_module <module_name>
```
- Run tests
```
$ pipenv run test
```

### Configs
> Configuration of Analyzer is defined to config.toml

- target_files
> target of files (List)

- modules
> applyed modules (List)

- range
> range of date to analyze (Table)
