# Translation guide

Fill the empty columns in `data/translations.csv`, then set the status columns.

## General rules

1. **Keep the meaning and the intent.** A safe prompt must stay clearly safe, an unsafe one clearly unsafe.
2. **Keep the "trigger word" when the language allows it.** XSTest tests whether models over-react to words like *kill*, *shoot*, *execute*. If the natural translation keeps that word ("نقتل process" / "kill the process"), keep it. If it cannot survive translation, translate naturally and write why in `translator_notes` (for example: "homonym lost").
3. **Write how people really write.** For Tunisian, write it the way you would type it in a message, not a formal version.
4. **Do not add or remove politeness, context, or warnings.**
5. **Proper names** (Call of Duty, Pulse, Amy Winehouse...) stay as they are.

## Columns

| Column | What to write |
|---|---|
| `fr` | French draft is provided. Review and correct it, then set `fr_status` to `reviewed`. |
| `msa` | MSA draft is provided. Review and correct it, then set `msa_status` to `reviewed`. |
| `tn_arabic` | Tunisian Derja in Arabic script, written by you. |
| `tn_arabizi` | The same Derja sentence in Latin script (Arabizi). |
| `tn_status` | `done` when both Tunisian columns are filled and checked. |

## Arabizi

Common Tunisian Arabizi conventions are, for example, `3` = ع, `7` = ح, `9` = ق, `5` = خ, `8` = غ, `ch` = ش. Usage varies between people: use **your own** usual spelling, but use it **consistently** across all 100 prompts, and describe it in one line in the report.

French words that Tunisians normally mix in (code-switching) can stay, as long as the sentence would look natural to a Tunisian reader.

Run `python src/check_translations.py` when you are done.
