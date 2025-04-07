import asyncio
from groq_report import GroqReport  # Import the class

async def test_groq_report():
    # Sample test data
    score = 85
    good_skills = "Python, Django, SQL, REST APIs"
    bad_skills = "Machine Learning, DevOps, AWS"

    # Create an instance of GroqReport
    report_generator = GroqReport(score, good_skills, bad_skills)

    # Run the async function to generate the report
    report_text = await report_generator.generate_llm_report()

    # Print the generated report
    print("\n=== Generated LLM Report ===\n")
    print(report_text)

# Run the test
if __name__ == "__main__":
    asyncio.run(test_groq_report())
