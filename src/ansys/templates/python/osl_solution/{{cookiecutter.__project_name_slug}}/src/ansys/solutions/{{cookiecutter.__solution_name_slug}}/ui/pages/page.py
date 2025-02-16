# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Initialization of the frontend layout across all the steps."""

import dash_bootstrap_components as dbc
import json
import webbrowser

from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State, callback_context, dcc, html

from ansys.saf.glow.client.dashclient import DashClient, callback
from ansys.saf.glow.core.method_status import MethodStatus

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.components.logs_table import LogsTable
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.pages import monitoring_page, problem_setup_page
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.utilities.common_functions import extract_dict_by_key

from ansys_web_components_dash import AwcDashTree


layout = html.Div(
    [
        dcc.Location(id="url", refresh=False), # represents the browser address bar and doesn't render anything
        html.Div(
            id="progress_bar",
            style={
                'margin-left': '35%', 'margin-top': '25%'
            },
        ),
        dcc.Interval(
            id="progress_bar_update",
            interval=1000,
            n_intervals=0,
            disabled=False
        ),
        dcc.Store(id='trigger_layout_display'),
        dcc.Store(id='trigger_treeview_display'),
        dcc.Store(id='trigger_body_display'),
        html.Div(id="page_layout")
    ]
)


@callback(
    Output("trigger_layout_display", "data"),
    Input("url", "pathname"),
)
def initialization(pathname):
    """Run methods to initialize the solution."""
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)

    if not project.steps.problem_setup_step.project_initialized:
        long_running = project.steps.problem_setup_step.get_app_metadata()
        long_running.wait()
        long_running = project.steps.problem_setup_step.get_default_placeholder_values()
        long_running.wait()
        project.steps.problem_setup_step.project_initialized = True

    raise PreventUpdate


@callback(
    Output("trigger_layout_display", "data"),
    Output("progress_bar", "children"),
    Output("progress_bar", "style"),
    Output("progress_bar_update", "disabled"),
    Input("progress_bar_update", "n_intervals"),
    State("url", "pathname"),
)
def update_progress_bar(n_intervals, pathname):
    """Track status of solution initialization."""
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    if not problem_setup_step.project_initialized:

        completion_rate = 0
        message = None
        methods = ["get_app_metadata", "get_default_placeholder_values"]

        for method in methods:
            status = problem_setup_step.get_long_running_method_state(method).status
            if status == MethodStatus.Completed:
                completion_rate += 1
            elif status == MethodStatus.Running:
                message = method.replace("_", " ").capitalize()
                break

        completion_rate = round(completion_rate / len(methods) * 100)

        return (
            True,
            [
                dbc.Progress(
                    value=completion_rate,
                    label=f"{completion_rate} %",
                    color="rgba(255,182,35,1)",
                    style={"width": "600px", "height": "30px"},
                ),
                dbc.Label(message),
            ],
            {'margin-left': '35%', 'margin-top': '25%'},
            False
        )

    else:
        return True, [], {"display": "none"}, True


@callback(
    Output("trigger_body_display", "data"),
    Output("page_layout", "children"),
    Input("url", "pathname"),
    Input("trigger_layout_display", "data"),
)
def display_page_layout(pathname, trigger_layout_display):
    """Display page layout."""
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step
    monitoring_step = project.steps.monitoring_step

    if problem_setup_step.project_initialized:
        return (
            True,
            [
                dbc.Stack(
                [
                    html.Div(
                        [
                            html.Img(
                            src = r"/assets/logos/ansys-solutions-horizontal-logo.png",
                            style={'width': '80%'}
                        )
                        ],
                    ),
                    html.Div(
                        [
                            dbc.Button(
                                f"Project Name: {project.project_display_name}",
                                id = "project_name",
                                disabled = True,
                                style={
                                    "color": "rgba(0, 0, 0, 1)",
                                    "background-color": "rgba(255, 255, 255, 1)",
                                    "border-color": "rgba(0, 0, 0, 1)"
                                },
                            )
                        ],
                        className="ms-auto",
                    ),
                    html.Div(
                        [
                            dbc.Button(
                                "Back to Projects",
                                id = "return_to_portal",
                                className = "me-2",
                                n_clicks = 0,
                                href=DashClient.get_portal_ui_url(),
                                style = {"background-color": "rgba(0, 0, 0, 1)", "border-color": "rgba(0, 0, 0, 1)"},
                            ) if DashClient.get_portal_ui_url() else []
                        ],
                    ),
                ],
                direction = "horizontal",
                gap = 3,
            ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                AwcDashTree(
                                    id="navigation_tree",
                                    multi=False,
                                    height=950,
                                    items=problem_setup_step.treeview_items,
                                    selectedItemIds=["problem_setup"]
                                ),

                            ],
                            width=2,
                            style={"background-color": "rgba(242, 242, 242, 0.6)"},  # Ansys grey
                        ),
                        dbc.Col(
                            [
                                dbc.Row(
                                    html.Div(
                                        id="body_content",
                                        style={"padding-right": "2%"}
                                    ),
                                ),
                                html.Br(),
                                dbc.Row(
                                    html.Div(
                                        id="bottom_button_group",
                                        style={"padding-right": "2%"}
                                    ),
                                ),
                            ],
                            width=10
                        ),
                    ],
                ),
            ]
        )
    else:
        raise PreventUpdate


@callback(
    Output("body_content", "children"),
    Output("bottom_button_group", "children"),
    Output("navigation_tree", "focusRequested"),
    Input("navigation_tree", "treeItemClicked"),
    Input("url", "pathname"),
    Input("trigger_body_display", "data"),
)
def display_body_content(value, pathname, trigger_body_display):
    """Display body content."""
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step
    monitoring_step = project.steps.monitoring_step

    if problem_setup_step.project_initialized:
        triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]
        footer_buttons = [
            dbc.Button(
                "optiSLang logs",
                id="optislang_logs_button",
                n_clicks=0,
                style={"background-color": "rgba(242, 242, 242, 0.6)", "borderColor": "rgba(242, 242, 242, 0.6)", "color": "rgba(0, 0, 0, 1)"},
                size="sm",
            ),
        ]
        if DashClient.get_portal_ui_url():
            footer_buttons.append(
                dbc.Button(
                    "Open in browser",
                    id="open_in_browser",
                    style={"background-color": "rgba(242, 242, 242, 0.6)", "borderColor": "rgba(242, 242, 242, 0.6)", "color": "rgba(0, 0, 0, 1)"},
                    n_clicks=0,
                    size="sm"
                )
            )
        if triggered_id == "url" or triggered_id == "trigger_body_display" or trigger_body_display and len(triggered_id) == 0:
            page_layout = problem_setup_page.layout(problem_setup_step)
            focusRequested = ""
        if triggered_id == "navigation_tree":
            focusRequested = value["id"]
            if value["id"] is None:
                page_layout = html.H1("Welcome!")
            elif value["id"] == "problem_setup_step":
                page_layout = problem_setup_page.layout(problem_setup_step)
            else:
                # Get project data
                project_data = json.loads(monitoring_step.project_data_dump.read_text())
                # Record uid of actor selected from treeview
                monitoring_step.selected_actor_from_treeview = extract_dict_by_key(problem_setup_step.project_tree, "uid", value["id"], expect_unique=True, return_index=False)["uid"]
                # Record hid of actor selected from treeview
                if len(project_data["actors"][monitoring_step.selected_actor_from_treeview]["states_ids"]):
                    monitoring_step.selected_state_id = project_data["actors"][monitoring_step.selected_actor_from_treeview]["states_ids"][0]
                else:
                    monitoring_step.selected_state_id = None
                # Get page layout
                page_layout = monitoring_page.layout(problem_setup_step, monitoring_step)
                # Update footer buttons
                footer_buttons.insert(
                    0,
                    dcc.Dropdown(
                        options=[state_id for state_id in project_data["actors"][monitoring_step.selected_actor_from_treeview]["states_ids"]],
                        value=monitoring_step.selected_state_id,
                        id="selected_state_dropdown",
                        disabled=False,
                        clearable=False,
                        searchable=True,
                        style={
                            "textAlign": "left",
                            "width": "30%"
                        },
                    ),
                )
        footer = [
            dbc.ButtonGroup(
                footer_buttons,
                size="md",
                className="me-1",
            ),
            dbc.Collapse(
                id="optislang_logs_collapse",
                is_open=False,
            )
        ]
        return (
            page_layout,
            footer,
            focusRequested
        )
    else:
        raise PreventUpdate


@callback(
    Output("navigation_tree", "items"),
    Input("url", "pathname"),
    Input("trigger_treeview_display", "data"),
)
def display_tree_view(pathname, trigger_treeview_display):
    """Display treeview with all project nodes."""
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    problem_setup_step = project.steps.problem_setup_step

    if problem_setup_step.project_initialized:
        return problem_setup_step.treeview_items
    else:
        raise PreventUpdate


@callback(
    Output("optislang_logs_collapse", "children"),
    Output("optislang_logs_collapse", "is_open"),
    Input("optislang_logs_button", "n_clicks"),
    Input("url", "pathname"),
    State("optislang_logs_collapse", "is_open"),
    prevent_initial_call=True,
)
def display_optislang_logs(n_clicks, pathname, is_open):
    """Display optiSLang logs."""
    project = DashClient[{{ cookiecutter.__solution_definition_name }}].get_project(pathname)
    monitoring_step = project.steps.monitoring_step

    if not n_clicks:
        # Button has never been clicked
        return None, False

    table = LogsTable(monitoring_step.optislang_logs)

    return table.render(), not is_open


@callback(
    Output("open_in_browser", "children"),
    Input("open_in_browser", "n_clicks"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def open_in_browser(n_clicks, pathname):
    """Open the Portal UI in browser view."""
    portal_ui_url = DashClient.get_portal_ui_url()
    webbrowser.open_new(portal_ui_url)

    raise PreventUpdate
