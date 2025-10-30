from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model = AutoModelForSeq2SeqLM.from_pretrained("/dss/dsshome1/0C/ge86yac2/byt5-UD-STAF")
tokenizer = AutoTokenizer.from_pretrained("/dss/dsshome1/0C/ge86yac2/byt5-UD-STAF")

input_path = "/dss/dsshome1/0C/ge86yac2/UD-TSA-sentences.txt"
output_path = "/dss/dsshome1/0C/ge86yac2/UD-TSA-sentences-byt5-results.txt"

decoded_predictions = []

with open(input_path, "r", encoding="utf-8") as f_in, open(output_path, "w", encoding="utf-8") as f_out:
    for line in f_in:
        line = line.strip()
        if not line:
            continue
        words = line.split()
        for word in words:
            encoded = tokenizer(word, return_tensors="pt", padding=True, truncation=True, max_length=128)
            output = model.generate(
                input_ids=encoded["input_ids"],
                attention_mask=encoded["attention_mask"],
                max_length=128
            )
            decoded = tokenizer.decode(output[0], skip_special_tokens=True)
            f_out.write(f"{decoded}\n")
        # After all words in the sentence, add a line with just ';'
        f_out.write(";\n")
