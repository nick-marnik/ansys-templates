# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
from dash import html, dash_table
import uuid
import pandas as pd

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.problem_setup_step import ProblemSetupStep
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.definition import {{ cookiecutter.__solution_definition_name }}


class ActorInformationTableAIO(html.Div):

    class ids:
        datatable = lambda aio_id: {
            'component': 'ActorInformationTableAIO',
            'subcomponent': 'datatable',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, problem_setup_step: ProblemSetupStep, aio_id: str = None):
        """ActorInformationTableAIO is an All-in-One component that is composed
        of a parent `html.Div` with a `dcc.Interval` and a `dash_table.DataTable` as children.

        - `problem_setup_step` - The StepModel object of the problem setup step.
        - `datatable_props` - A dictionary of properties passed into the dash_table.DataTable component.
        - `interval_props` - A dictionary of properties passed into the dcc.Interval component.
        - `aio_id` - The All-in-One component ID used to generate the table components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        data = self.get_data(problem_setup_step)

        datatable_props = {
            "data": data.to_dict('records'),
            "columns": [{"name": i, "id": i, "type": "text"} for i in data.columns],
            "fixed_rows": {"headers": True},
            "style_header": {
                "textAlign": "left",
                "font_family": "Roboto",
                "font_size": "15px",
                "fontWeight": "bold",
                "border": "none",
                "display": "none",
            },
            "style_cell": {"textAlign": "left", "font_family": "Roboto", "font_size": "15px", "border": "none"},
            "style_as_list_view": True,
            "style_table": {"border": "none"},  # Hide table borders
        }

        super().__init__([
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H4("Actor information", className="card-title"),
                            dash_table.DataTable(id=self.ids.datatable(aio_id), **datatable_props),
                        ]
                    ),
                ],
                color="warning",
                outline=True,
            )
        ])

    def get_data(self, problem_setup_step) -> pd.DataFrame:

        if problem_setup_step.selected_actor_from_treeview in problem_setup_step.actors_info.keys():
            actor_info = problem_setup_step.actors_info[problem_setup_step.selected_actor_from_treeview]
        else:
            actor_info = {}

        if problem_setup_step.selected_actor_from_treeview in problem_setup_step.actors_status_info.keys():
            actor_status_info = problem_setup_step.actors_status_info[problem_setup_step.selected_actor_from_treeview][0]
        else:
            actor_status_info = {}

        actor_information_data = {
            "column_a": ["Working directory", "Processing state", "Execution duration"],
            "column_b": [None, None, None],
        }

        if actor_info and actor_status_info:
            actor_information_data["column_b"] = [
                actor_status_info["working dir"],
                actor_status_info["state"],
                "-",
            ]
            if actor_info["kind"] == "system":
                succeeded_designs = actor_status_info["succeeded_designs"]
                failed_designs = actor_status_info["failed_designs"]
                pending_designs = actor_status_info["pending_designs"]
                total_designs = actor_status_info["total_designs"]
                processed_designs = total_designs - pending_designs
                status = int(processed_designs / total_designs * 100)
                actor_information_data["column_a"].extend(["Processed", "Status", "Succeeded", "Not succeeded"])
                actor_information_data["column_b"].extend(
                    [f"{processed_designs} / {total_designs}", f"{status}%", succeeded_designs, failed_designs]
                )

        return pd.DataFrame(actor_information_data)
