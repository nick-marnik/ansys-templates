# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Frontend of the visualization view."""

import json
import optislang_dash_lib

from dash_extensions.enrich import html

from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.solution.monitoring_step import MonitoringStep


def layout(monitoring_step: MonitoringStep) -> html.Div:
    """Layout of the visualization view."""

    full_project_status_info = json.loads(monitoring_step.full_project_status_info_dump.read_text())

    return html.Div(
        [
            optislang_dash_lib.VisualizationComponent(
                id="visualization-component",
                project_state=full_project_status_info,
                system_id=monitoring_step.selected_actor_from_treeview,
                state_idx=0,
            ),
        ]
    )
