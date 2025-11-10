import argparse

def parse_features(feat_str):
    parts = feat_str.split(';')
    if len(parts) > 1:
        filtered = [f for f in parts[1:] if f not in {"MASC", "F", "NEUT"}]
        return ';'.join(filtered)
    return ''

def longest_common_prefix(s1, s2):
    min_len = min(len(s1), len(s2))
    i = 0
    while i < min_len and s1[i].lower() == s2[i].lower():
        i += 1
    return i

def convert_line_to_gloss(word, lemma):
    if word.lower() == lemma.lower():
        return word
    prefix_len = longest_common_prefix(word, lemma)
    extra_word = word[prefix_len:]
    return f"{lemma}-{extra_word}"

def load_dictionary(dict_path):
    dictionary = {}
    with open(dict_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '->' in line:
                alb, eng = line.strip().split('->')
                dictionary[alb.strip().lower()] = eng.strip()
    return dictionary

def process_sentence_file(input_path, dict_path, output_path):
    dictionary = load_dictionary(dict_path)
    orig_sentence = []
    gloss_line = []
    translation_line = []

    def write_sentence(f_out):
        if not orig_sentence:
            return
        sentence_str = ''
        for w in orig_sentence:
            if w in {'.', ',', '!', '?', ';', ':', '-', '—'}:
                sentence_str += w
            else:
                if sentence_str:
                    sentence_str += ' ' + w
                else:
                    sentence_str = w

        f_out.write(sentence_str + '\n')
        f_out.write(' '.join(gloss_line) + '\n')
        f_out.write(' '.join(translation_line) + '\n\n')

    with open(input_path, 'r', encoding='utf-8') as f_in, \
         open(output_path, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            line = line.strip()
            if line == ';':
                write_sentence(f_out)
                orig_sentence.clear()
                gloss_line.clear()
                translation_line.clear()
                continue
            parts = line.split('\t')
            if len(parts) != 3:
                continue
            lemma, word, feats = parts
            orig_sentence.append(word)
            gloss_line.append(convert_line_to_gloss(word, lemma))
            translation = dictionary.get(lemma.lower(), lemma)
            if lemma.lower() != word.lower():
                feats_only = parse_features(feats).replace(";", ".")
                if feats_only:
                    translation = f"{translation}-{feats_only}"
            translation_line.append(translation)

        # Write any remaining sentence (optional safety)
        write_sentence(f_out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate glossed Albanian sentences with English translations")
    parser.add_argument("-i", "--input", required=True, help="Path to the input file (morphological analyses)")
    parser.add_argument("-d", "--dict", required=True, help="Path to the Albanian-English dictionary file")
    parser.add_argument("-o", "--output", required=True, help="Path to the output glossed file")
    args = parser.parse_args()

    process_sentence_file(args.input, args.dict, args.output)

