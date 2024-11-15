
import os
from flask import Flask, request, jsonify
import certifi
import logging
import requests
import time
import json
import language_tool_python
import textstat
#import warnings
import ssl
import urllib.request  # Import urllib.request


app = Flask(__name__)


# Loading all API keys from environment variables
app.config['SAPLING_API_KEY'] = os.getenv('SAPLING_API_KEY')
app.config['COPYLEAKS_API_KEY'] = os.getenv('COPYLEAKS_API_KEY')
app.config['COPYSCAPE_API_KEY'] = os.getenv('COPYSCAPE_API_KEY')
app.config['ZOTERO_API_KEY'] = os.getenv('ZOTERO_API_KEY')
app.config['RAPIDAPI_KEY'] = os.getenv('RAPIDAPI_KEY')

# Suppress InsecureRequestWarning
#warnings.simplefilter('ignore', InsecureRequestWarning)



def sapling_check(text, api_key): 
    url = "https://api.sapling.ai/api/v1/spellcheck"
    api_key="hb-9nJfHhHVwGPo3Q2HnMvTQOmDAoFzlLYZ25ZtvWuDPwOIatv-yJl3HasQPWgDE64IHP2Ozzkerys6VwLonwg%3D%3D"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "text": text
    }

    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)

    try:
        response = requests.post(url, headers=headers, json=payload, verify=False)
        response.raise_for_status()  # This will raise an error for bad responses
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")  # Print the error
        print(response.text)  # Print the response body for more context
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


 
'''
    logging.basicConfig(level=logging.DEBUG)
    response = requests.post(url, headers=headers, json=payload, verify=False)#verify=certifi.where())

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
'''


def check_grammar(text):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
    return corrected_text



#adding here code with url to submit and scan text files or pdf (any file type) etc for copyleaks .

def check_copyleaks(text, api_key):
    # URL for submitting text for plagiarism check
    url = "https://api.copyleaks.com/v3/education/submit/text"
    api_key = "eb3583d9-7fe0-4863-821c-967e72cef7d5"
    # Set up the payload
    payload = {
        'text': text,
        'key': api_key
    }
    
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)


    response = requests.post(url, data=payload, verify=False)
    return response.json()


def get_readability_scores(text):
    scores = {
        'flesch_reading_ease': textstat.flesch_reading_ease(text),
        'smog_index': textstat.smog_index(text),
        'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
        'coleman_liau_index': textstat.coleman_liau_index(text),
        'automated_readability_index': textstat.automated_readability_index(text),
        'dale_chall_readability_score': textstat.dale_chall_readability_score(text),
        'difficult_words': textstat.difficult_words(text),
        'linsear_write_formula': textstat.linsear_write_formula(text),
        'gunning_fog': textstat.gunning_fog(text),
    }
    return scores



def get_zotero_citations(text):
    url = "https://api.zotero.org/users/14615578/items"
    api_key = "yFbQ9VcHqx6eRi0VTZaJMsv1"
    headers = {
        'Zotero-API-Key': api_key
    }
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)

    response = requests.post(url, headers=headers, verify=False)
    return response.json()

def paraphrase_with_rapidapi(text):
    url = "https://paraphrasing-tool.p.rapidapi.com/api/v1/paraphrase"
    api_key = "878c0fdb13mshd35ae3571a99a0ep1a8586jsn6874dd646924"
    payload = {
        'text': text,
        'key': api_key
    }
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)

    response = requests.post(url, data=payload, verify=False)
    return response.json()


@app.route('/api/v1/essay', methods=['POST'])
def edit_essay():
    #api_key = app.config['SAPLING_API_KEY']
    data = request.get_json()
    text = data['text']

    # Retrieving API keys from the Flask config
    sapling_api_key = app.config['SAPLING_API_KEY']
    copyleaks_api_key = app.config['COPYLEAKS_API_KEY']
    zotero_api_key = app.config['ZOTERO_API_KEY']
    rapidapi_key = app.config['RAPIDAPI_KEY']

    # Calling each function with the appropriate API key
    result = {
    'original_text': text,
    'corrected_text': check_grammar(text),
    'sapling': sapling_check(text, sapling_api_key),
    'copyleaks': check_copyleaks(text, copyleaks_api_key),
    'readability_scores': get_readability_scores(text),
    'zotero_citations': get_zotero_citations(text, zotero_api_key),
    'rapidapi': paraphrase_with_rapidapi(text, rapidapi_key)
}

    return jsonify(result)




if __name__ == "__main__":

    sapling_api_key = os.getenv('SAPLING_API_KEY')
    copyleaks_api_key = os.getenv('COPYLEAKS_API_KEY')
    zotero_api_key = os.getenv('ZOTERO_API_KEY')
    rapidapi_key = os.getenv('RAPIDAPI_KEY')

    text_to_check = "hi my namme iss lavi. mice to meet you."
    
    # Testing sapling_check
    result = sapling_check(text_to_check,sapling_api_key)  # Passing the api_key
    print("Sapling check result:")
    #print(json.dumps(result, indent=4)) 
    print(result)
    
    # Testing check_grammer
    corrected_text = check_grammar(text_to_check)
    print("Grammar check result:")
    print(corrected_text)
    
    # Testing check_copyleaks
    copyleaks_result = check_copyleaks(text_to_check)
    print("Copyleaks check result:")
    #print(json.dumps(copyleaks_result, indent=4))
    print(copyleaks_result)
    
    # Testing get_readability_scores
    readability_scores = get_readability_scores(text_to_check)
    print("Readability scores:")
    #print(json.dumps(readability_scores, indent=4)) 
    print(readability_scores)
    
    # Testing get_zotero_citations
    zotero_citations = get_zotero_citations(text_to_check)
    print("Zotero citations result:")
    #print(json.dumps(zotero_citations, indent=4))    
    print(zotero_citations)
    
    # Testing paraphrase_with_rapidapi
    paraphrase_result = paraphrase_with_rapidapi(text_to_check)
    print("Paraphrasing result:")
    #print(json.dumps(paraphrase_result, indent=4))
    print(paraphrase_result)

    app.run(debug=True)



