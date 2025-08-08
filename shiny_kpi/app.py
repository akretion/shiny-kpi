from datetime import datetime
from pathlib import Path

from shiny import App, Inputs, Outputs, Session, reactive, render, ui

from shiny_kpi.builder import get_nav_panels
from shiny_kpi.element import elements as elm
from shiny_kpi.main import instance
from shiny_kpi.tool import _

app_dir = Path(__file__).parent
app_css = app_dir / "style/app.css"


app_ui = ui.page_fillable(
    # To improve readability, method names are prefixed by _
    ui.card(
        ui.card_header("Shiny Kpi"),
        ui.layout_sidebar(
            ui.sidebar(
                "",
                # ui.output_ui("_data_source"),
                ui.output_ui("_organizations"),
                ui.output_ui("_date_range"),
                # ui.output_ui("_debug"),
                bg="#f8f8f8",
            ),
            ui.output_ui("_navset_tab"),
        ),
    ),
    ui.include_css(app_css),
)


def app_server(input: Inputs, output: Outputs, session: Session):
    @render.ui
    def _navset_tab():
        # https://shiny.posit.co/py/layouts/navbars/#navbar-at-top
        return ui.navset_tab(*get_nav_panels(ui), id="tab")

    @render.ui
    def _data_source():
        return ui.input_radio_buttons(
            "df_radio_buttons",
            ui.div(ui.span(_("Sources"))),
            instance.source,
        )

    @render.ui
    def _date_range():
        # TODO BUG: manage first day of the year
        elm.min_date.set(
            datetime.strptime(f"{datetime.today().year}-01-01", "%Y-%m-%d")
        )
        elm.max_date.set(datetime.today())
        return ui.input_slider(
            "date_range",
            ui.span(_("Dates")),
            elm.min_date.get(),
            elm.max_date.get(),
            [elm.min_date.get(), elm.max_date.get()],
            # TODO manage localization
            time_format="%d/%m/%y",
            drag_range=True,
        )

    @reactive.effect
    @reactive.event(input.date_range)
    def date_range_handler():
        values = input.date_range()
        elm.selected_min_date.set(values[0])
        elm.selected_max_date.set(values[1])

    @render.ui
    def _organizations():
        orgas = [x["name"] for x in instance.get_organizations()]
        return (
            ui.input_selectize(
                "organization",
                ui.span(_("Organizations")),
                orgas,
                selected=orgas[0],
                multiple=True,
            ),
        )

    @reactive.effect
    @reactive.event(input.organization)
    def organization_handler():
        elm.organizations.set(input.organization())

    @render.ui
    def _debug():
        dbg = [
            instance.get_organizations().__str__(),
            instance.__str__(),
        ]
        return ui.span("debug"), ui.pre("\n- ".join(dbg))


app = App(app_ui, app_server)
