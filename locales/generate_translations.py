import os
import json
from enums.languages_enum import LanguageEnum
from openai_interface import get_response

LOCALES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MESSAGE_FILES = [
    "age_descriptions.json",
    "environment_descriptions.json",
    "general_messages.json",
    "race_class_descriptions.json"
]


def call_gpt_translate(messages_dict, target_language, filename):
    print(f"Sending messages from {filename} to be translated to {target_language}...")

    message_content = json.dumps(messages_dict, ensure_ascii=False, indent=4)
    conversation = [
        {"role": "system", "content": "You are a helpful assistant. Translate the entire content of the given JSON."},
        {"role": "user", "content": f"Translate this JSON content to {target_language}: \n\n{message_content}"}
    ]

    response = get_response(conversation)
    translated_text = response['choices'][0]['message']['content'].strip()

    try:
        translated_messages = json.loads(translated_text)
    except json.JSONDecodeError:
        print("Error decoding the translated JSON!")
        return messages_dict

    return translated_messages


def generate_translations_for_file(filename, lang_code):
    default_lang_path = os.path.join(LOCALES_PATH, LanguageEnum.EN_US.code, filename)
    target_lang_path = os.path.join(LOCALES_PATH, lang_code, filename)

    with open(default_lang_path, 'r', encoding='utf-8') as f:
        messages = json.load(f)

    translations = call_gpt_translate(messages, lang_code, filename)

    os.makedirs(os.path.dirname(target_lang_path), exist_ok=True)
    with open(target_lang_path, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=4)

    print(f"\033[92mGenerated translations for {filename} in {lang_code}\033[0m")


def main():
    print("Starting translation process...")
    for lang in LanguageEnum:
        print(lang.code)  # Printing the language code
        if lang.code == LanguageEnum.EN_US.code:
            continue

        for filename in MESSAGE_FILES:
            generate_translations_for_file(filename, lang.code)


if __name__ == "__main__":
    main()
