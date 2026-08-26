# Gold clarification requirements

These are the remaining human inputs required before evaluation. For every
provided or confirmed gold file, record the dataset/treebank name, exact release
or version, filename, SHA-256 checksum, and cohort mapping.

## EN gold files

- Identify or provide the authoritative EN written-test gold CoNLL-U for cohort
  EN:writtentest.
- Identify or provide the authoritative EN spoken-test gold CoNLL-U for cohort
  EN:spokentest.

## NL gold files

- Identify or provide the authoritative NL written-test gold CoNLL-U for cohort
  NL:writtentest.
- Identify or provide the authoritative NL spoken-test gold CoNLL-U for cohort
  NL:spokentest.
- Identify or provide the authoritative NL dialect-test gold CoNLL-U for cohort
  NL:dialecttest, and clarify whether spoken and dialect are distinct datasets.

## SL provenance confirmation

- Confirm whether ../data/gold/sl_ssj-ud-test.conllu (SHA-256
  c14d5d2f4f20a7ad43e0f598a2e18c5e41f08364ab36be1c87d6d9eae7f5c8b0)—the local UD Slovenian SSJ r2.17 file that
  exactly matches the written predictions' ID/FORM structure—is the intended
  SL:writtentest gold.
- Confirm whether ../data/gold/sl_sst-ud-test.conllu (SHA-256
  6824234edf98cbbedb2e981644c324a3058c2920ed6cdcd7f467e835cfe25eeb)—the local official standardised UD Slovenian
  SST r2.16/r2.17 file that exactly matches the spoken predictions' ID/FORM
  structure—is the intended SL:spokentest gold.
- If either answer is no, provide the authoritative replacement and exact release
  information. Structural alignment alone is not sufficient confirmation.

## Separate prediction blocker

- Provide a corrected NL Trankit written+spoken-training/spoken-test prediction,
  or confirm that this logical run should remain excluded. The current file is
  byte-identical to EN content.
