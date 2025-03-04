from django.shortcuts import render
from django.http import JsonResponse
import spacy
import docx

# Load spaCy's English model
nlp = spacy.load('en_core_web_sm')

def process_text(request):
    if request.method == 'POST':
        # Get the text input from the POST request
        text1 = request.POST.get('text', '')
        text2 = request.POST.get('text2', '')
        
        # Process the text with spaCy
        doc = nlp(text1)
        
        # Extract token data (text, lemma, and part of speech)
        data = [{'text': token.text, 'lemma': token.lemma_, 'pos': token.pos_} for token in doc]
        
        # Return the extracted data as a JSON response
        return JsonResponse({'data': data})
    
    # If GET request, render the form page
    return render(request, 'comparison/process_text.html')