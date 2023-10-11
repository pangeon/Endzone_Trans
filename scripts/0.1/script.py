import json
from googletrans import Translator
from tqdm import tqdm  # Importuj tqdm

# Otwarcie pliku JSON
with open('English.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Inicjalizacja tłumacza
translator = Translator()

# Pobierz listę fraz do tłumaczenia
translations = data.get("translations", [])

# Przygotuj tqdm do wyjścia postępu
progress_bar = tqdm(total=len(translations), desc="Tłumaczenie fraz", unit="fraza")

# Przetłumacz frazy w pliku JSON
for item in translations:
    if "v" in item:
        english_phrase = item["v"]
        try:
            translation = translator.translate(english_phrase, src='en', dest='pl')
            item["v"] = translation.text
        except Exception as e:
            print(f"Błąd tłumaczenia: {e}")
        finally:
            # Zaktualizuj wyjście postępu niezależnie od wyniku tłumaczenia
            progress_bar.update(1)

# Zapisz zmodyfikowany plik JSON
with open('Polish.json', 'w', encoding='utf-8') as updated_file:
    json.dump(data, updated_file, ensure_ascii=False, indent=2)

# Zamknij pasek postępu
progress_bar.close()