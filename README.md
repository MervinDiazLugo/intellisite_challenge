# Test Intellisite - QA Challenge
Presenting test challenge

## Create a virtual env
```shell
-python -m virtualenv env
```
## Install requerements.txt

```shell
-pip install -r requerements.txt
```

## Run test
```shell
cd .\src\
del /f /q ..\allure-results
behave -f allure_behave.formatter:AllureFormatter --tags=Intellisite --tags=-skip --no-skipped -o ..\allure-results ./features -f pretty
```

## generate Report
```shell
-allure generate ..\allure-results --output ..\allure-report --clean && allure open --port 5000
```