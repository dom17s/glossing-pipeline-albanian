from simalign import SentenceAligner
from collections import defaultdict, Counter
from tqdm import tqdm
import os

# Load sentence files
def load_sentences(en_path, sq_path):
    with open(en_path, "r", encoding="utf-8") as f_en, open(sq_path, "r", encoding="utf-8") as f_sq:
        en_sents = [line.strip() for line in f_en]
        sq_sents = [line.strip() for line in f_sq]
    return en_sents, sq_sents

# Align and build dictionary with frequency filtering
def build_bilingual_dict(en_sents, sq_sents, min_freq=5):
    # Using xlm-roberta-base with correct matching method
    aligner = SentenceAligner(
        model="xlm-roberta-base",
        token_type="bpe",
        matching_methods="mai"  # 'm' = mwmf, 'a' = inter, 'i' = itermax
    )

    lexicon = defaultdict(Counter)

    for en_sent, sq_sent in tqdm(zip(en_sents, sq_sents), total=len(en_sents), desc="Aligning"):
        en_tokens = en_sent.strip().split()
        sq_tokens = sq_sent.strip().split()

        # Skip empty sentences
        if not en_tokens or not sq_tokens:
            continue

        try:
            alignments = aligner.get_word_aligns(en_tokens, sq_tokens)
            alignment = alignments.get("itermax", [])

            if not alignment:
                continue

            for i, j in alignment:
                en_word = en_tokens[i].lower()
                sq_word = sq_tokens[j].lower()
                lexicon[sq_word][en_word] += 1

        except ValueError as e:
            print(f"Skipped a sentence pair due to alignment error: {e}")
            continue

    # Keep only the most frequent translation per Albanian word, and only if it appears more than min_freq times
    filtered_dict = {}
    for en_word, counter in lexicon.items():
        most_common = counter.most_common(1)
        if most_common and most_common[0][1] > min_freq:
            filtered_dict[en_word] = most_common[0]

    return filtered_dict

# Save dictionary to TXT
def save_dictionary_txt(dictionary, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        for en_word, (sq_word, count) in sorted(dictionary.items()):
            f.write(f"{en_word} -> {sq_word} ({count})\n")

# Main execution
if __name__ == "__main__":
    en_file = "XLEnt.en-sq.en"
    sq_file = "XLEnt.en-sq.sq"
    output_file = "sq-en-dictionary.txt"

    if not os.path.exists(en_file) or not os.path.exists(sq_file):
        print("Error: Sentence files not found.")
    else:
        print("Loading sentences...")
        en_sents, sq_sents = load_sentences(en_file, sq_file)

        print("Building word alignments...")
        dictionary = build_bilingual_dict(en_sents, sq_sents, min_freq=5)

        print(f"Saving dictionary to {output_file}...")
        save_dictionary_txt(dictionary, output_file)

        print("Dictionary saved successfully!")
