from shiny import App

from shiny_kpi import server as kpi_server
from shiny_kpi import ui as kpi_ui

app = App(kpi_ui.app_ui, kpi_server.app_server)
