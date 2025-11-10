# Albanian Morphological Analysis and Glossing Pipeline

This repository contains scripts for word-level morphological analysis of Albanian sentences and for generating glossed sentences with English translations

## Model Releases

- Models are provided as zipped releases.  
- To use a model:
  1. Download the zip file from the releases section
  2. Extract it to a local directory
  3. Use the extracted folder as the `-m` (model) argument in the commands below


## Step 1: Morphological Analysis

This step generates a morphological analysis for each word in input sentences

### Command:

```bash
python byt5_morpho_analysis.py -m /path/to/byt5-model \
                                  -i /path/to/input-sentences.txt \
                                  -o /path/to/morph-analysis-output.txt
```

## Step 2: Generate Glossed Sentences

This step generates glossed sentences with English translations from the morphological analysis output from Step 1

### Command:

```bash
python glossing.py -i /path/to/morph-analysis-output.txt \
                                  -d /path/to/sq-en-dictionary.txt \
                                  -o /path/to/glossed-output.txt
```
