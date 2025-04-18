# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Agent module for the onboarding assistant."""

import logging
import warnings
from google.adk import Agent
from .config import Config
from .prompts import GLOBAL_INSTRUCTION, INSTRUCTION
from .shared_libraries.callbacks import (
    rate_limit_callback,
    before_agent,
    before_tool,
)
from .tools.tools import (
    add_applicant_and_prompt_interview,
    schedule_interview,
    evaluate_interview,
    promote_employee,
    start_onboarding,
    ask_hr_question,
    update_employee_status,
)

warnings.filterwarnings("ignore", category=UserWarning, module=".*pydantic.*")

# Load configuration
configs = Config()

# Setup logger
logger = logging.getLogger(__name__)

# Create the onboarding-focused agent
root_agent = Agent(
    model=configs.agent_settings.model,
    global_instruction=GLOBAL_INSTRUCTION,
    instruction=INSTRUCTION,
    name=configs.agent_settings.name,
    tools=[
        add_applicant_and_prompt_interview,
        schedule_interview,
        evaluate_interview,
        promote_employee,
        start_onboarding,
        ask_hr_question,
        update_employee_status,
    ],
    before_tool_callback=before_tool,
    before_agent_callback=before_agent,
    before_model_callback=rate_limit_callback,
)
