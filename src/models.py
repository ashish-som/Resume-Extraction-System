from pydantic import BaseModel, Field
from typing import Literal


class ScreenResume(BaseModel):
    name:str = Field(description="Specify the name of the candidate")
    name_reasoning:str = Field(description='A brief explanation of your answer with evidence')
    email:str = Field(description="Specify the email of the candidate")
    email_reasoning:str = Field(description='A brief explanation of your answer with evidence')
    phone:str = Field(description="Specify the phone number of the candidate")
    phone_reasoning:str = Field(description='A brief explanation of your answer with evidence')
    current_location:str = Field(description="Specify the current location of the candidate")
    current_location_reasoning:str = Field(description='A brief explanation of your answer with evidence')
    total_experience: float = Field(description="Mention the total experience of the candidate. Do not add gap period to the experience. If the candidate is a fresher then mention the experience 0.0")
    total_experience_reasoning:str = Field(description='A brief explanation of your answer with evidence')
    releant_experience: float = Field(description="Mention the relevant experience of the candidate. The experience is relevant if it is related to technical fields like Engineering, Data Science, Data Analysis, Business Analysis, Product Management etc. Do not add gap period to the experience. If the candidate is a fresher then mention the experience 0.0")
    relevant_experience_reasoning:str = Field(description='A brief explanation of your answer with evidence')
    current_job_title:str = Field(description="Specify the current job title of the candidate. If he is not working currently then mention the latest title. If the candidate is a fresher then mention Not Appliacble")
    current_job_title_reasoning:str = Field(description='A brief explanation of your answer with evidence')
    current_company:str = Field(description="Specify the current company of the candidate. If he is not working currently then mention the last company. If the candidate is a fresher then mention Not Appliacble")
    current_company_reasoning:str = Field(description='A brief explanation of your answer with evidence')
    highest_education:Literal["Bachelor's Degree", "Master's Degree", "Doctorate", "Diploma", "Other", "Not Specified"] = Field(description="Mention the highest education the candidate has")
    highest_education_reasoning:str = Field(description='A brief explanation of your answer with evidence')
    notice_period:int = Field(description="Mention the notice period in days.")
    notice_period_reasoning:str = Field(description='A brief explanation of your answer with evidence')