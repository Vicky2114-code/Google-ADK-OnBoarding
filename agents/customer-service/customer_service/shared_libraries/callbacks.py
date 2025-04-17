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

"""Callback functions for FOMC Research Agent."""

import logging
import time
from typing import Any, Dict

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest
from google.adk.tools import BaseTool
from google.adk.agents.invocation_context import InvocationContext
from ..entities.customer import Employee

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

RATE_LIMIT_SECS = 60
RPM_QUOTA = 10


def rate_limit_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> None:
    """Callback function that implements a query rate limit."""

    for content in llm_request.contents:
        for part in content.parts:
            if part.text == "":
                part.text = " "

    now = time.time()
    if "timer_start" not in callback_context.state:
        callback_context.state["timer_start"] = now
        callback_context.state["request_count"] = 1
        logger.debug(
            "rate_limit_callback [timestamp: %i, req_count: 1, elapsed_secs: 0]",
            now,
        )
        return

    request_count = callback_context.state["request_count"] + 1
    elapsed_secs = now - callback_context.state["timer_start"]

    logger.debug(
        "rate_limit_callback [timestamp: %i, request_count: %i, elapsed_secs: %i]",
        now,
        request_count,
        elapsed_secs,
    )

    if request_count > RPM_QUOTA:
        delay = RATE_LIMIT_SECS - elapsed_secs + 1
        if delay > 0:
            logger.debug("Sleeping for %i seconds", delay)
            time.sleep(delay)
        callback_context.state["timer_start"] = time.time()
        callback_context.state["request_count"] = 1
    else:
        callback_context.state["request_count"] = request_count


def lowercase_value(value: Any) -> Any:
    """Recursively lowercases all string values in a nested structure."""
    if isinstance(value, dict):
        return {k.lower() if isinstance(k, str) else k: lowercase_value(v) for k, v in value.items()}
    elif isinstance(value, str):
        return value.lower()
    elif isinstance(value, list):
        return [lowercase_value(i) for i in value]
    elif isinstance(value, tuple):
        return tuple(lowercase_value(i) for i in value)
    elif isinstance(value, set):
        return {lowercase_value(i) for i in value}
    else:
        return value


def before_tool(tool: BaseTool, args: Dict[str, Any], tool_context: CallbackContext):
    """Callback before the onboarding tool is invoked."""

    # Normalize input to lowercase values if needed
    def lowercase_value(input_args):
        return {k: v.lower() if isinstance(v, str) else v for k, v in input_args.items()}

    args.update(lowercase_value(args))

    # Onboarding-specific logic
    if tool.name == "start_onboarding":
        employee_id = args.get("employee_id")
        start_date = args.get("start_date", "TBD")

        logger.info(f"✅ Initiating onboarding for employee {employee_id}, start date: {start_date}")

        # Store onboarding context
        tool_context.state["onboarding_started"] = True
        tool_context.state["onboarding_employee_id"] = employee_id
        tool_context.state["onboarding_start_date"] = start_date

        return {
            "result": f"📦 Onboarding process started for employee `{employee_id}` with start date `{start_date}`."
        }

    return None


def before_agent(callback_context: InvocationContext):
    """Callback before the agent starts."""
    if "customer_profile" not in callback_context.state:
        callback_context.state["customer_profile"] = Employee.get_customer("E001").to_json()

    # Onboarding context load (optional pre-check)
    if "onboarding_started" in callback_context.state:
        logger.debug(
            f"Agent initializing with onboarding already started for: "
            f"{callback_context.state['onboarding_employee_id']}"
        )
