# Pilot report: refusal and over-refusal across English, French, MSA and Tunisian Arabic

*[Your name], ISSAT Sousse. [Date]. Code and data: [GitHub link]*

## 1. Question

aiXamine (arXiv:2608.20554, Section 6) evaluates only English. This pilot asks whether two Llama 8B models keep the same refusal behaviour when the same XSTest prompts are written in French, MSA, Tunisian Arabic (Arabic script) and Tunisian Arabizi, and whether an LLM judge stays reliable on those languages.

## 2. Setup

- 100 XSTest prompts (50 safe, 50 unsafe), 5 language versions, 2 models (`llama3.1:8b` [digest], `llama3:latest` [digest]) via Ollama [version], temperature 0, 512 max tokens.
- Tunisian versions written by hand by the author (native speaker). Arabizi convention used: [one line].
- Labels by `llama3.1:8b` judge; [N] responses labelled blind by the author.
- Hardware and runtime: [e.g. laptop CPU / GPU model, total hours].

## 3. Results

[Paste results/summary/main_table.md]

[Insert results/summary/figures/rates_by_language.png]

Paired comparison with English (exact McNemar, same prompts): [2 to 4 sentences from paired_vs_english.csv. Report the differences in points and p-values; say clearly which are not significant.]

Judge vs human agreement (Cohen's kappa per language): [table from judge_vs_human.csv]

## 4. Observations

[3 to 5 short points. Describe only what the numbers show. If there is no difference, say so: a null result is a result.]

## 5. Limitations

Small n (wide CIs), two related models, quantized local inference not comparable with aiXamine's setup, homonyms that do not survive translation ([N] prompts flagged), self-judging, a single annotator who is also the translator.

## 6. What a full study would add

More prompts and tests (e.g. other aiXamine services such as Safety Alignment and Jailbreak), more models including Arabic-centric ones, several annotators with inter-annotator agreement, other Arabic dialects, and a judge trained or validated for Arabic.
