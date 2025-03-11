# """
# views.py - Handles API endpoint for processing resumes.
#
# This module includes:
# - `process_resume`: API to handle file uploads, process resumes, and return structured results.
# """
#
# import os
# import os
# import logging
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .processor import ResumeProcessor
#
# # Configure Django logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# @csrf_exempt
# def process_resume(request):
#     """
#     API to handle resume uploads, process the resume, and return structured results.
#
#     Returns:
#     - JSON response containing:
#         - `cleaned_text`: Processed text output
#         - `sections`: Extracted resume sections
#         - `word_frequency`: Word count analysis
#         - `keywords`: Extracted keywords
#         - `contacts`: Emails, phone numbers, and links
#     - Error messages if any issues occur.
#
#     author: shobhitrajain
#     date: 2025-03-05
#     """
#
#     logger.info("Received API request: process_resume")
#
#     if request.method != "POST":
#         logger.warning("Invalid request method")
#         return JsonResponse({"error": "Invalid request method"}, status=405)
#
#     if "resume" not in request.FILES:
#         logger.error("No file found in the request")
#         return JsonResponse({"error": "No resume file found in request"}, status=400)
#
#     uploaded_resume = request.FILES["resume"]
#     temp_dir = os.path.join(os.getcwd(), "temp_files")
#     os.makedirs(temp_dir, exist_ok=True)  # Ensure temp directory exists
#
#     temp_path = os.path.join(temp_dir, uploaded_resume.name)
#     logger.info(f"Saving uploaded file to temporary path: {temp_path}")
#
#     try:
#         # Save the uploaded file to disk
#         with open(temp_path, "wb") as temp_file:
#             for chunk in uploaded_resume.chunks():
#                 temp_file.write(chunk)
#
#         # Process the saved resume
#         processor = ResumeProcessor(temp_path)
#         result = processor.process()
#
#         return JsonResponse(result, status=200)
#
#     except Exception as e:
#         logger.error(f"Error processing resume: {str(e)}", exc_info=True)
#         return JsonResponse({"error": str(e)}, status=500)
#
#     finally:
#         # Cleanup: Remove temp file after processing
#         if os.path.exists(temp_path):
#             os.remove(temp_path)
#             logger.info(f"Temp file removed: {temp_path}")