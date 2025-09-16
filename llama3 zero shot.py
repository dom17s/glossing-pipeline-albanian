from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
import argparse

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, required=True, help="Path to input file")
parser.add_argument("--output", type=str, required=True, help="Path to output file")
args = parser.parse_args()

llama_id = "meta-llama/Meta-Llama-3-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(llama_id)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(
    llama_id,
    device_map="auto",
    torch_dtype=torch.float16,
    quantization_config=bnb_config,
)
model.eval()

input_file = args.input
output_file = args.output

def build_prompt_zero_shot(input_sentence):
    instruction = """You are an expert documentary linguist specializing 
	in Albanian. You are working on a documentation 
	project for Albanian text, where you are creating 
	annotated text corpora with full morphological 
	analysis.

    Specifically, you will be provided with a word 
	in Albanian.

    You are to output a morphological analysis for it. The most possible analysis of the word 
	should be outputed on a line.

    The format of the line should be:

	lemma\tsurface_form\tPOS;MorphFeatures

	Where:
	lemma is the base form of the word,
	surface_form is the exact word form from the input text,
	POS is the part of speech (e.g., N for noun, V for verb),

	MorphFeatures is a semicolon-separated list of 
	morphological features such as case, number, definiteness, 
	person, mood, and tense (depending on the word).

    Examples:
	abdikim	abdikime	N;NOM;PL;NDEF
	abdikim	abdikime	N;ACC;PL;NDEF
	abdikim	abdikimesh	N;ABL;PL;NDEF
	dashuroj	dashurofshim	V;1;PL;OPT;PRS
	dashuroj	dashurofshin	V;3;PL;OPT;PRS

    Please analyze the given word morphologically and save 
	the results in a txt file.

    """

    return (
        "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n"
        + instruction + "\n"
        + f"Input: {input_sentence}\n"
        + "<|eot_id|>\n<|start_header_id|>assistant<|end_header_id|>\n"
    )

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for idx, line in enumerate(infile, 1):
        line = line.strip()
        if not line:
            continue

        prompt = build_prompt_zero_shot(line)

        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=False,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.pad_token_id,
            )

        decoded = tokenizer.decode(outputs[0], skip_special_tokens=False)
        response = decoded.split("<|start_header_id|>assistant<|end_header_id|>\n")[-1].split("<|eot_id|>")[0].strip()

        outfile.write(f"{response}\n")
        outfile.flush()

        print(f"[{idx}] Processed sentence with zero-shot prompt")
