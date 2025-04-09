from llm_access.groq_api import generate_groq_response_async


class GroqReport:
    """
    GroqReport class

    This class interacts with the LLM to produce a textual report based on the
    comparison score and skill match data.

    Attributes:
        score (int): The similarity score between the resume and job posting.
        good_skills (str): Comma-separated list of skills that match the job requirements.
        bad_skills (str): Comma-separated list of missing skills.

    @Author: BA
    @Date: 2025-04-02
    """

    def __init__(self, score: int, good_skills: str = "", bad_skills: str = ""):
        self.score = score
        self.good_skills = good_skills
        self.bad_skills = bad_skills

    async def generate_llm_report(self) -> str:
        """
        Generates a professional, well-structured report summarizing the applicant's
        resume comparison results using the Groq AI model.

        Returns:
            str: The generated report.
        """

        # Construct a detailed prompt
        prompt = (
            f"You are a hiring assistant that analyzes resumes.\n\n"
            f"Candidate Resume Score: {self.score}/100\n\n"
            f"✅ Matching Skills: {self.good_skills if self.good_skills else 'None'}\n"
            f"❌ Missing Skills: {self.bad_skills if self.bad_skills else 'None'}\n\n"
            f"Based on this information, write a detailed and professional report evaluating the candidate's strengths and areas for improvement. "
            f"If the skills list is empty, mention that the candidate lacks the required skills for the job.\n\n"
            f"If the matching or missing list has more than 3 entries, pick the three that you feel are most relevant to the job posting.\n\n"
            f"The report should only be a paragraph long and should be written in a professional tone. Max 300 words.\n\n"
        )

        try:
            # Call the Groq API asynchronously
            report = await generate_groq_response_async(prompt)
            return report

        except Exception as e:
            return f"Error generating report: {str(e)}"

