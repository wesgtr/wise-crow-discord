import json

MESSAGE_FILES = [
    "general_messages.json",
    "environment_descriptions.json",
    "race_class_descriptions.json",
    "age_descriptions.json"
]


def load_translations(lang_code):
    messages = {}
    for filename in MESSAGE_FILES:
        filepath = f"locales/{lang_code}/{filename}"
        with open(filepath, "r", encoding="utf-8") as f:
            messages.update(json.load(f))
    return messages


def translate(key, lang_code="en_US"):
    translations = load_translations(lang_code)
    return translations.get(key, key)
