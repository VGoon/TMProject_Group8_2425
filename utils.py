import csv
import re
from collections import defaultdict
import os 

# source: https://github.com/rishabhverma17/sms_slang_translator/blob/master/slang.txt


import os
import csv
import re

def analyze_slangs(user_string):
    import_path = os.path.join(os.path.dirname(__file__), "slang.txt")
    slang_found = []
    casing_info = {"uppercase": 0, "lowercase": 0, "mixed": 0}
    slang_dict = {}

    # Load slang dictionary
    with open(import_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="=")
        for row in reader:
            if len(row) == 2:
                slang_dict[row[0].strip().upper()] = row[1].strip()

    tokens = user_string.split()
    translated_tokens = []

    for token in tokens:
        # Skip URLs and cashtags
        if token.startswith('http') or token.startswith('$'):
            translated_tokens.append(token)
            continue
        
        if token.endswith("…") or token.endswith(".."):
            continue  # skip truncated words

        cleaned = re.sub(r'[^a-zA-Z0-9-_.]', '', token)
        upper_cleaned = cleaned.upper()

        if upper_cleaned in slang_dict:
            slang_found.append(cleaned)

            if cleaned.isupper():
                casing_info["uppercase"] += 1
            elif cleaned.islower():
                casing_info["lowercase"] += 1
            else:
                casing_info["mixed"] += 1

            translated_tokens.append(slang_dict[upper_cleaned])
        else:
            translated_tokens.append(token)

    return {
        "original_text": user_string,
        "translated_text": ' '.join(translated_tokens),
        "slang_count": len(slang_found),
        "slangs": slang_found,
        "casing_info": casing_info
    }
