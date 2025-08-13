from pathlib import Path

from shiny import ui

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
            ui.head_content(
                ui.tags.meta(
                    name="viewport", content="width=device-width, initial-scale=1"
                )
            ),
            ui.output_ui("_navset_tab"),
        ),
    ),
    ui.include_css(app_css),
)
