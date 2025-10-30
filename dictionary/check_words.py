import re
from collections import Counter

def load_dictionary(dict_file):
    dictionary = {}
    with open(dict_file, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '->' in line:
                alb, eng = map(str.strip, line.split('->'))
                dictionary[alb.lower()] = eng.lower()
    return dictionary

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower(), flags=re.UNICODE)

def check_dictionary_coverage(text_file, dict_file):
    dictionary = load_dictionary(dict_file)

    with open(text_file, encoding='utf-8') as f:
        text = f.read()

    tokens = tokenize(text)
    types = set(tokens)
    token_counter = Counter(tokens)

    # Token-level stats
    token_total = len(tokens)
    token_found = sum(freq for word, freq in token_counter.items() if word in dictionary)
    missing_tokens = [word for word in tokens if word not in dictionary]

    # Type-level stats
    type_total = len(types)
    type_found = sum(1 for word in types if word in dictionary)
    missing_types = sorted([word for word in types if word not in dictionary])

    # Save missing words
    with open("missing_tokens.txt", "w", encoding='utf-8') as f:
        for word in missing_tokens:
            f.write(word + "\n")

    with open("missing_types.txt", "w", encoding='utf-8') as f:
        for word in missing_types:
            f.write(word + "\n")

    # Print stats
    print(f"Dictionary Coverage Stats")
    print(f"Token-level:")
    print(f"  Found: {token_found} / {token_total} ({(token_found / token_total) * 100:.2f}%)")
    print(f"  Missing tokens saved to: missing_tokens.txt")

    print(f"Type-level:")
    print(f"  Found: {type_found} / {type_total} ({(type_found / type_total) * 100:.2f}%)")
    print(f"  Missing types saved to: missing_types.txt")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", required=True)
    parser.add_argument("-d", required=True)
    args = parser.parse_args()

    check_dictionary_coverage(args.t, args.d)
