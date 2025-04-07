"""
This module is used to generate a failure message in JSON format.
It will produce the stage of the failure and a description of the failure.

@Author: IFD
@Date: 2025-04-01
"""
from typing import Any

from comparator.compare_utils.stage_enum import Stage


def generate_detail(stage: Stage, description: str) -> dict[Stage, str]:
    return {
        stage.name: {
            "description": description
        }
    }