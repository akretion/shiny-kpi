# Shiny Kpi

The shiny-kpi library is a Python project by Akretion tool for creating Key Performance Indicators (KPIs) from an existing database. 

# *WORK IN PROGRESS - early stage*


## Built on top of

[Shiny Python](https://shiny.posit.co/py/gallery)

Current package contains shortcuts to create a KPI dashboard from a database.

Shortcut configuration is contained in kpi-custom/kpi_custom/data



## Installation


in a virtual environment

```bash

git clone https://github.com/akretion/shiny-kpi

cd shiny-kpi

cp -r kpi-custom ..

# inside the copied directory
cd kpi-custom

pip install -e .

```

## Configuration

In https://github.com/akretion/shiny-kpi/tree/main/kpi-custom/kpi_custom/data

- Update `config.toml` to fill your expectations.

- Copy/paste `dsn-sample.toml` as `dsn.toml` and update it


## Start application


```bash

shiny run app.py --port 8009

# You may omit `port`, default one is 8000

# see https://shiny.posit.co/py/get-started/create-run.html

```
