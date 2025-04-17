"""Tools module for employee onboarding system."""

import logging
import uuid
from datetime import datetime
from typing import Optional

from ..entities.customer import Employee,Address
logger = logging.getLogger(__name__)


def schedule_interview(candidate_id: str, date: str, time: str) -> dict:
    """
    Schedules an interview for a candidate.

    Args:
        candidate_id (str): The ID of the candidate.
        date (str): Interview date in YYYY-MM-DD format.
        time (str): Interview time (e.g., '10:00 AM').

    Returns:
        dict: A dictionary with interview schedule details.
    """
    logger.info("Scheduling interview for %s on %s at %s", candidate_id, date, time)

    return {
        "status": "scheduled",
        "candidate_id": candidate_id,
        "interview_id": str(uuid.uuid4()),
        "date": date,
        "time": time
    }


def evaluate_interview(candidate_id: str, marks: int, feedback: str) -> dict:
    """
    Evaluates an interview and records the result.

    Args:
        candidate_id (str): The ID of the candidate.
        marks (int): Interview score (0-100).
        feedback (str): Interviewer's feedback.

    Returns:
        dict: A dictionary with evaluation result.
    """
    logger.info("Evaluating interview for %s with marks: %s", candidate_id, marks)

    passed = marks >= 60

    return {
        "candidate_id": candidate_id,
        "marks": marks,
        "feedback": feedback,
        "status": "passed" if passed else "failed"
    }


def promote_employee(candidate_id: str) -> dict:
    """
    Promotes a candidate to the next round or final onboarding stage.

    Args:
        candidate_id (str): The ID of the candidate.

    Returns:
        dict: A dictionary indicating the promotion status.
    """
    logger.info("Promoting candidate %s to next stage", candidate_id)

    return {
        "status": "promoted",
        "candidate_id": candidate_id,
        "next_stage": "final_interview"  # or "onboarding"
    }


def start_onboarding(candidate_id: str, role: str) -> dict:
    """
    Starts the onboarding process for a selected candidate.

    Args:
        candidate_id (str): The ID of the candidate.
        role (str): The job role for the candidate.

    Returns:
        dict: A dictionary indicating the onboarding status.
    """
    logger.info("Starting onboarding for %s as %s", candidate_id, role)

    return {
        "status": "onboarding_started",
        "candidate_id": candidate_id,
        "role": role,
        "onboarding_id": str(uuid.uuid4())
    }


def ask_hr_question(candidate_id: str, question: str) -> dict:
    """
    Simulates asking an HR-related question.

    Args:
        candidate_id (str): The ID of the candidate.
        question (str): The question to ask.

    Returns:
        dict: A simulated HR response.
    """
    logger.info("Candidate %s asked HR: %s", candidate_id, question)

    return {
        "candidate_id": candidate_id,
        "question": question,
        "response": "Thank you for your question. Our HR team will get back to you shortly."
    }


def update_employee_status(candidate_id: str, status: str) -> dict:
    """
    Updates the employment status of a candidate.

    Args:
        candidate_id (str): The ID of the candidate.
        status (str): The new status (e.g., 'active', 'onboarding_complete').

    Returns:
        dict: A dictionary with the update result.
    """
    logger.info("Updating status for %s to %s", candidate_id, status)

    return {
        "candidate_id": candidate_id,
        "status": status,
        "updated_at": datetime.utcnow().isoformat()
    }
def add_applicant_and_prompt_interview(name: str, email: str, role: str) -> dict:
    """
    Adds a new applicant and prompts for interview scheduling.

    Args:
        name (str): Full name of the applicant.
        email (str): Email address of the applicant.
        role (str): Role the applicant is applying for.

    Returns:
        dict: A dictionary containing the applicant data and next step prompt.
    """
    candidate_id = f"APP-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"  # Simple ID generation
    logger.info("New applicant added: %s, Email: %s, Role: %s", name, email, role)

    return {
        "candidate_id": candidate_id,
        "name": name,
        "email": email,
        "applied_role": role,
        "status": "Applicant",
        "created_at": datetime.utcnow().isoformat(),
        "next_step": "Would you like to schedule an interview for this applicant?"
    }
def update_employee_info(
    employee_id: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    address: Optional[str] = None
) -> dict:
    """
    Updates the employee's profile fields if provided.

    Args:
        employee_id (str): The unique ID of the employee.
        first_name (Optional[str]): New first name (if any).
        last_name (Optional[str]): New last name (if any).
        email (Optional[str]): New email (if any).
        phone (Optional[str]): New phone number (if any).
        address (Optional[str]): New address (if any).

    Returns:
        dict: Confirmation of updated fields.
    """
    employee = Employee.get_customer(employee_id)
    if not employee:
        return {"error": f"Employee with ID {employee_id} not found."}

    updates = {}

    if first_name:
        employee.first_name = first_name
        updates["first_name"] = first_name
    if last_name:
        employee.last_name = last_name
        updates["last_name"] = last_name
    if email:
        employee.email = email
        updates["email"] = email
    if phone:
        employee.phone_number = phone
        updates["phone_number"] = phone
    if address:
        employee.address.street = address
        updates["address"] = address

    return {
        "employee_id": employee_id,
        "updated_fields": updates,
        "status": "Profile updated successfully"
    }