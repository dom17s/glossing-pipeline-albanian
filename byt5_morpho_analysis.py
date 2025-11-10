import argparse
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run model on Albanian sentences")
    parser.add_argument("-m", "--model", required=True, help="Path to the trained model directory")
    parser.add_argument("-i", "--input", required=True, help="Path to input text file (sentences)")
    parser.add_argument("-o", "--output", required=True, help="Path to save output file")
    args = parser.parse_args()

    # Load model and tokenizer
    model = AutoModelForSeq2SeqLM.from_pretrained(args.model)
    tokenizer = AutoTokenizer.from_pretrained(args.model)

    # Read sentence-wise input
    with open(args.input, "r", encoding="utf-8") as f:
        sentences = [line.strip() for line in f if line.strip()]

    # Generate and save output
    with open(args.output, "w", encoding="utf-8") as out_file:
        for sentence in sentences:
            words = sentence.split()
            for word in words:
                encoded = tokenizer(
                    word,
                    return_tensors="pt",
                    padding=True,
                    truncation=True,
                    max_length=128
                )
                output = model.generate(
                    input_ids=encoded["input_ids"],
                    attention_mask=encoded["attention_mask"],
                    max_length=128
                )
                decoded = tokenizer.decode(output[0], skip_special_tokens=True)
                out_file.write(f"{decoded}\n")
            out_file.write(";\n")  # Sentence separator

if __name__ == "__main__":
    main()
