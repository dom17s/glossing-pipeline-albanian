from uniparser_albanian import AlbanianAnalyzer

a = AlbanianAnalyzer(mode='strict')

input_file = 'UniMorph-test-words.txt'
output_file = 'UniParser-test-output.txt'

with open(input_file, 'r', encoding='utf-8') as fin, open(output_file, 'w', encoding='utf-8') as fout:
    for line in fin:
        word = line.strip()
        if not word:
            continue

        analyses = a.analyze_words(word)

        if not analyses or not analyses[0].lemma:
            fout.write(f"UNK\t{word.lower()}\tUNK\n")
            continue

        ana = analyses[0]
        lemma = ana.lemma.lower()
        wf = ana.wf.lower()
        tags = ana.gramm.upper().split(',')

        if 'NOUN' in tags:
            case = next((t for t in tags if t in {'ACC', 'NOM', 'GEN', 'DAT', 'ABL'}), 'UNK')
            num = next((t for t in tags if t in {'SG', 'PL'}), 'UNK')
            definiteness = next((t for t in tags if t in {'DEF', 'INDEF'}), 'UNK')
            fout.write(f"{lemma}\t{wf}\tN;{case};{num};{definiteness}\n")

        elif 'V' in tags or 'VERB' in tags:
            person = next((t for t in tags if t in {'1', '2', '3'}), '')
            number = next((t for t in tags if t in {'SG', 'PL'}), '')
            mood = next((t for t in tags if t in {'IND', 'SUBJ', 'IMP'}), '')
            tense = next((t for t in tags if t in {'PRS', 'PST', 'FUT', 'PRES', 'AOR'}), '')

            if tense == 'PRES':
                tense = 'PRS'
            elif tense == 'AOR':
                tense = 'PST'

            fout.write(f"{lemma}\t{wf}\tV;{person};{number};{mood};{tense}\n")

        else:
            fout.write(f"UNK\t{wf}\tUNK\n")
