from typing import List, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict
import uuid
import datetime

class Address(BaseModel):
    """
    Represents an employee's address.
    """
    street: str
    city: str
    state: str
    zip: str
    model_config = ConfigDict(from_attributes=True)


class JobApplication(BaseModel):
    """
    Represents a job application made by an applicant.
    """
    job_id: str
    position: str
    application_date: str
    status: str  # e.g., "Pending", "Interviewed", "Hired", "Rejected"
    resume: str  # URL or path to the resume
    model_config = ConfigDict(from_attributes=True)


class Interview(BaseModel):
    """
    Represents an interview with an applicant.
    """
    interview_date: str
    interview_panel: List[str]
    feedback: Optional[str] = None
    result: Optional[str] = None  # e.g., "Passed", "Failed"
    marks: Optional[int] = None  # Score out of 100
    model_config = ConfigDict(from_attributes=True)


class Onboarding(BaseModel):
    """
    Represents the onboarding process for a hired employee.
    """
    start_date: str
    orientation_scheduled: bool
    benefits_package: bool
    system_access_granted: bool
    model_config = ConfigDict(from_attributes=True)


class HRQuestions(BaseModel):
    """
    Represents questions asked by an employee to HR.
    """
    question: str
    answered: bool = False
    response: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class Employee(BaseModel):
    """
    Represents an employee.
    """
    employee_id: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    job_applications: List[JobApplication]
    interviews: List[Interview]
    onboarding: Optional[Onboarding] = None
    hr_questions: List[HRQuestions] = []
    address: Address
    status: str  # e.g., "Applicant", "Interviewed", "Hired", "Onboarded", "Agent", "Terminated"
    model_config = ConfigDict(from_attributes=True)


    def to_json(self) -> str:
        """
        Converts the Employee object to a JSON string.
        """
        return self.model_dump_json(indent=4)

    def add_applicant_and_prompt_interview(self) -> None:
        """
        Adds a new applicant and optionally schedules an interview.
        """
        print("👋 Let's start the application process.")

        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()
        email = input("Email: ").strip()
        role = input("Role applying for: ").strip()
        phone = input("Phone number (optional): ").strip() or "000-000-0000"

        employee_id = f"E{uuid.uuid4().hex[:6].upper()}"

        job_application = JobApplication(
            job_id=f"J{uuid.uuid4().hex[:4].upper()}",
            role=role,
            application_date=datetime.now().strftime("%Y-%m-%d"),
            status="Submitted"
        )

        self.current_employee = Employee(
            employee_id=employee_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone,
            job_applications=[job_application],
            interviews=[],
            address=Address(street="", city="", state="", zip=""),
            status="Applicant"
        )

        print(f"\n✅ Applicant `{first_name} {last_name}` added with ID: {employee_id}")
        print(self.current_employee.to_json())

        # Ask to schedule interview
        schedule = input("\nWould you like to schedule an interview now? (yes/no): ").strip().lower()
        if schedule == "yes":
            interview_date = input("Enter interview date (YYYY-MM-DD): ").strip()
            panel_input = input("Enter interview panel members (comma-separated): ").strip()
            interview_panel = [member.strip() for member in panel_input.split(",")]

            self.current_employee.schedule_interview(
                interview_date=interview_date,
                interview_panel=interview_panel
            )

            print("\n📅 Interview scheduled successfully.")
            print(f"Interview Date: {interview_date}")
            print(f"Panel: {', '.join(interview_panel)}")
        else:
            print("✅ You can schedule the interview later.")


    def schedule_interview(self, interview_date: str, interview_panel: List[str]) -> None:
        """
        Schedules a new interview.
        """
        interview = Interview(interview_date=interview_date, interview_panel=interview_panel)
        self.interviews.append(interview)
        self.status = "Interview Scheduled"

    def evaluate_interview(self, interview_index: int, result: str, marks: int, feedback: Optional[str] = None) -> None:
        """
        Records the result and feedback of an interview.
        """
        interview = self.interviews[interview_index]
        interview.result = result
        interview.marks = marks
        interview.feedback = feedback

    def evaluate_candidate(self, start_date: str, passing_marks: int = 60) -> None:
        """
        Evaluates if the candidate has passed at least 3 interviews and promotes to 'Agent' if eligible.
        """
        passed_interviews = [i for i in self.interviews if i.result == "Passed" and (i.marks or 0) >= passing_marks]
        if len(passed_interviews) >= 3:
            print(f"🎉 Congratulations {self.first_name}, you’ve been promoted to Agent after clearing all 3 interviews!")
            self.onboarding = Onboarding(
                start_date=start_date,
                orientation_scheduled=True,
                benefits_package=True,
                system_access_granted=True
            )
            self.status = "Agent"
        else:
            print(f"⚠️ {self.first_name} has not passed all required interview rounds yet.")
            self.status = "Interviewed"

    def onboard_employee(self, start_date: str) -> None:
        """
        Onboards an employee manually if already hired.
        """
        if self.status == "Hired":
            self.onboarding = Onboarding(
                start_date=start_date,
                orientation_scheduled=True,
                benefits_package=True,
                system_access_granted=True
            )
            self.status = "Onboarded"
        else:
            raise ValueError("Employee must be hired before onboarding.")

    def ask_hr_question(self, question: str) -> None:
        """
        Submits a question to HR.
        """
        self.hr_questions.append(HRQuestions(question=question))

    def update_employee_status(self, new_status: str) -> None:
        """
        Updates the employee's current status.
        """
        self.status = new_status

    def get_customer(employee_id: str) -> "Employee":
        # Mock employee data
        return Employee(
            employee_id="E001",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="123-456-7890",
            job_applications=[],
            interviews=[],
            address=Address(
                street="123 Elm St",
                city="Cityville",
                state="CA",
                zip="98765"
            ),
            status="Hired"
        )


# ===== Example Usage =====
if __name__ == "__main__":
    employee = Employee(
        employee_id="E001",
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone_number="123-456-7890",
        job_applications=[],
        interviews=[],
        address=Address(street="123 Elm St", city="Cityville", state="CA", zip="98765"),
        status="Applicant"
    )

    # Schedule and evaluate three interview rounds
    employee.schedule_interview("2025-04-01", ["HR"])
    employee.evaluate_interview(0, result="Passed", marks=85, feedback="Good communication.")

    employee.schedule_interview("2025-04-05", ["Tech Lead"])
    employee.evaluate_interview(1, result="Passed", marks=90, feedback="Strong technical background.")

    employee.schedule_interview("2025-04-10", ["Director"])
    employee.evaluate_interview(2, result="Passed", marks=88, feedback="Leadership potential.")

    # Final evaluation for promotion
    employee.evaluate_candidate(start_date="2025-05-01")

    # Ask HR a question
    employee.ask_hr_question("What is the company's remote work policy?")

    # Show final employee record
    print(employee.to_json())
