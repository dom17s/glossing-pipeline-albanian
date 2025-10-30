import pandas as pd
from sklearn.model_selection import train_test_split
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer

# Load dataset
df = pd.read_csv("/dss/dsshome1/0C/ge86yac2/UD-STAF-byt5-training.txt", sep="\t", header=None, names=["lemma", "inflected", "features"])

# Morphological Analysis task: Input = inflected form, Output = lemma + inflected + features
df["input_text"] = df["inflected"]
df["target_text"] = df["lemma"] + "\t" + df["inflected"] + "\t" + df["features"]

# Drop missing values
df.dropna(subset=["input_text", "target_text"], inplace=True)

# Sample check
print(df[["input_text", "target_text"]].sample(3))

# Split into train and eval
train_df, eval_df = train_test_split(df[["input_text", "target_text"]], test_size=0.1, random_state=42)

# Convert to Hugging Face datasets
train_dataset = Dataset.from_pandas(train_df)
eval_dataset = Dataset.from_pandas(eval_df)

# Use ByT5 tokenizer (character-level byte tokenizer)
tokenizer = AutoTokenizer.from_pretrained("google/byt5-base", use_fast=False)

max_input_length = 128
max_target_length = 128

def preprocess(example):
    model_input = tokenizer(example["input_text"], max_length=max_input_length, truncation=True, padding="max_length")
    labels = tokenizer(example["target_text"], max_length=max_target_length, truncation=True, padding="max_length")
    model_input["labels"] = labels["input_ids"]
    return model_input

tokenized_train = train_dataset.map(preprocess, batched=False)
tokenized_eval = eval_dataset.map(preprocess, batched=False)

import os
for var in ["WORLD_SIZE", "RANK", "LOCAL_RANK", "MASTER_ADDR", "MASTER_PORT"]:
    if var in os.environ:
        del os.environ[var]

training_args = Seq2SeqTrainingArguments(
    output_dir="./byt5-UD-STAF",
    evaluation_strategy="epoch",
    learning_rate=3e-4,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    weight_decay=0.01,
    save_total_limit=2,
    num_train_epochs=5,
    predict_with_generate=True,
    logging_dir="./logs",
    report_to="none",
)

model = AutoModelForSeq2SeqLM.from_pretrained("google/byt5-base")

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_eval,
    tokenizer=tokenizer,
)

print(df[["input_text", "target_text"]].sample(5))

trainer.train()

model.save_pretrained("/dss/dsshome1/0C/ge86yac2/byt5-UD-STAF")
tokenizer.save_pretrained("/dss/dsshome1/0C/ge86yac2/byt5-UD-STAF")
