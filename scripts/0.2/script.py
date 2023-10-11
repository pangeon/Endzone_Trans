import json
from googletrans import Translator
from tqdm import tqdm
import re

# Open the JSON file
with open('English.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Initialize the translator
translator = Translator()

# Get the list of phrases to translate
translations = data.get("translations", [])

# Prepare the progress bar
progress_bar = tqdm(total=len(translations), desc="Translating phrases", unit="phrase")

# Function to translate text while excluding content inside "<< >>"
def translate_except_markers(text):
    markers = re.findall(r'<<[^<>]+>>', text)
    translated_text = text

    placeholders = {}
    for i, marker in enumerate(markers):
        placeholder = f"__MARKER_{i}__"
        placeholders[placeholder] = marker
        translated_text = translated_text.replace(marker, placeholder)

    translation = translator.translate(translated_text, src='en', dest='pl')
    translated_text = translation.text

    for placeholder, marker in placeholders.items():
        translated_text = translated_text.replace(placeholder, marker)

    return translated_text

# Translate phrases in the JSON file
for item in translations:
    if "v" in item:
        english_phrase = item["v"]
        try:
            translation = translate_except_markers(english_phrase)
            item["v"] = translation
        except Exception as e:
            print(f"Translation error: {e}")
        finally:
            progress_bar.update(1)

# Save the modified JSON file
with open('Polish.json', 'w', encoding='utf-8') as updated_file:
    json.dump(data, updated_file, ensure_ascii=False, indent=2)

# Close the progress bar
progress_bar.close()