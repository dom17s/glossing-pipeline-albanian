import re

# suffix rules for nouns
noun_rules = [
    # Singular, Indefinite
    (r'(.*)im$', 'N;NOM;SG;NDEF;MASC', r'\1im'),           # verbal noun singular
    (r'(.*)ime$', 'N;NOM;PL;NDEF;MASC', r'\1im'),           # verbal noun plural
    (r'(.*)imet$', 'N;NOM;PL;DEF;MASC', r'\1im'),           # verbal noun plural definite
    (r'(.*)imeve$', 'N;GEN;PL;DEF;MASC', r'\1im'),          # verbal noun genitive plural

    # Common feminine endings
    (r'(.*)a$', 'N;NOM;SG;NDEF;FEM', r'\1'),
    (r'(.*)ja$', 'N;NOM;SG;DEF;FEM', r'\1'),
    (r'(.*)ës$', 'N;GEN;SG;NDEF;FEM', r'\1ë'),

    # Common masculine endings
    (r'(.*)i$', 'N;NOM;SG;DEF;MASC', r'\1'),
    (r'(.*)it$', 'N;GEN;SG;DEF;MASC', r'\1'),
    (r'(.*)in$', 'N;ACC;SG;DEF;MASC', r'\1'),

    # Plural endings
    (r'(.*)e$', 'N;NOM;PL;NDEF;FEM', r'\1'),
    (r'(.*)et$', 'N;NOM;PL;DEF;FEM', r'\1'),
    (r'(.*)ve$', 'N;GEN;PL;DEF;FEM', r'\1'),
    (r'(.*)ave$', 'N;GEN;PL;DEF;FEM', r'\1'),
    (r'(.*)ash$', 'N;GEN;PL;DEF;MASC', r'\1'),

    # Default pattern for simple nouns (fallback)
    (r'(.*)$', 'N;NOM;SG;NDEF;UNK', r'\1'),
]

# Verb rules (limited base rules for present, imperfect, aorist, etc.)
verb_rules = [
    (r'(.*)oj$', 'V;1;SG;IND;PRS;ACT', r'\1oj'),
    (r'(.*)on$', 'V;3;SG;IND;PRS;ACT', r'\1oj'),
    (r'(.*)ojnë$', 'V;3;PL;IND;PRS;ACT', r'\1oj'),
    (r'(.*)ova$', 'V;1;SG;IND;AOR;ACT', r'\1oj'),
    (r'(.*)ove$', 'V;2;SG;IND;AOR;ACT', r'\1oj'),
    (r'(.*)uam$', 'V;1;PL;IND;AOR;ACT', r'\1oj'),
    (r'(.*)oja$', 'V;1;SG;IND;IPFV;ACT', r'\1oj'),
    (r'(.*)onte$', 'V;3;SG;IND;IPFV;ACT', r'\1oj'),
    (r'(.*)onin$', 'V;3;PL;IND;IPFV;ACT', r'\1oj'),
    (r'(.*)ofsha$', 'V;1;SG;OPT;PRS;ACT', r'\1oj'),
    (r'(.*)oni$', 'V;2;PL;IMP;PRS;ACT', r'\1oj'),
]

# Adjective rules (very simplified)
adjective_rules = [
    (r'(.*)shëm$', 'ADJ;SG;MASC', r'\1shëm'),
    (r'(.*)shme$', 'ADJ;SG;FEM', r'\1shëm'),
    (r'(.*)shëm$', 'ADJ;PL;MASC', r'\1shëm'),
    (r'(.*)shmet$', 'ADJ;PL;FEM', r'\1shëm'),
]

# POS detector
def detect_pos(word):
    for pattern, tag, lemma_pat in verb_rules:
        if re.match(pattern, word):
            return 'V'
    for pattern, tag, lemma_pat in noun_rules:
        if re.match(pattern, word):
            return 'N'
    for pattern, tag, lemma_pat in adjective_rules:
        if re.match(pattern, word):
            return 'ADJ'
    return 'UNK'

# Analyzer function
def analyze_word(word):
    pos = detect_pos(word)
    rules = []

    if pos == 'N':
        rules = noun_rules
    elif pos == 'V':
        rules = verb_rules
    elif pos == 'ADJ':
        rules = adjective_rules
    else:
        return f"{word}\t{word}\tUNK"

    for pattern, tag, lemma_pat in rules:
        match = re.match(pattern, word)
        if match:
            lemma = re.sub(pattern, lemma_pat, word)
            return f"{lemma}\t{word}\t{tag}"
    return f"{word}\t{word}\tUNK"

# Process input file
def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            word = line.strip()
            if not word:
                continue
            analysis = analyze_word(word)
            outfile.write(analysis + "\n")

# Main execution
if __name__ == "__main__":
    input_file = "UniMorph-test-words.txt"
    output_file = "only_rules_analyzer_test_output.txt"
    process_file(input_file, output_file)
    print(f"Analysis complete. Output saved to: {output_file}")

