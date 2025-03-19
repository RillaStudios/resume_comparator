import os
import subprocess
import tempfile
from django.core.files.base import ContentFile

"""
A utility class to convert DOCX files to PDF using Pandoc.

This is currently NOT being used. It's a placeholder for future functionality.

Author: IFD
Date: 2025-03-17
"""
class DocxConverter:
    def __init__(self, resume_file):
        self.resume_file = resume_file

    def convert_docx_to_pdf(self):
        """Converts a DOCX file to PDF and returns an in-memory Django file."""

        # Ensure the uploaded file pointer is at the beginning
        self.resume_file.seek(0)

        # Save the uploaded DOCX file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx:
            temp_docx.write(self.resume_file.read())
            temp_docx_path = temp_docx.name  # Get temp file path

        # Define the output PDF path
        output_pdf_path = temp_docx_path.replace(".docx", ".pdf")

        try:
            # Run Pandoc for conversion
            result = subprocess.run(["pandoc", temp_docx_path, "-o", output_pdf_path], check=True, capture_output=True,
                                    text=True)

            # Debugging logs
            print("Pandoc Output:", result.stdout)
            print("Pandoc Error (if any):", result.stderr)

            # Check if PDF was successfully created
            if not os.path.exists(output_pdf_path):
                raise Exception("PDF conversion failed.")

            # Read the converted PDF into memory
            with open(output_pdf_path, "rb") as pdf_file:
                pdf_content = pdf_file.read()

            # Clean up temp files
            subprocess.run(["rm", temp_docx_path, output_pdf_path])

            # Return the PDF as an in-memory Django file
            return ContentFile(pdf_content, name=self.resume_file.name.replace(".docx", ".pdf"))

        except Exception as e:
            print(f"Error converting DOCX to PDF: {e}")
            return None  # Return None if conversion fails
