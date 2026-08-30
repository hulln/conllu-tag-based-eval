window.AM_BENCHMARK_RESULTS = {
  "schema_version": 1,
  "source": {
    "path": "reports/authoritative_spacy_stanza_results.tsv",
    "sha256": "388aed50942be46d9e0b96a85b7d904636b6895c297fed69053755868b200e78",
    "row_count": 36
  },
  "dimensions": {
    "language": [
      "EN",
      "NL",
      "SL"
    ],
    "model": [
      "spacy",
      "stanza"
    ],
    "training_condition": [
      "default",
      "writtentrain",
      "writtenandspokentrain"
    ],
    "test_condition": [
      "writtentest",
      "spokentest"
    ]
  },
  "metrics": [
    {
      "name": "Tokens",
      "fields": [
        "precision",
        "recall",
        "f1",
        "aligned_accuracy"
      ]
    },
    {
      "name": "Sentences",
      "fields": [
        "precision",
        "recall",
        "f1",
        "aligned_accuracy"
      ]
    },
    {
      "name": "Words",
      "fields": [
        "precision",
        "recall",
        "f1",
        "aligned_accuracy"
      ]
    },
    {
      "name": "UPOS",
      "fields": [
        "precision",
        "recall",
        "f1",
        "aligned_accuracy"
      ]
    },
    {
      "name": "XPOS",
      "fields": [
        "precision",
        "recall",
        "f1",
        "aligned_accuracy"
      ]
    },
    {
      "name": "UFeats",
      "fields": [
        "precision",
        "recall",
        "f1",
        "aligned_accuracy"
      ]
    },
    {
      "name": "AllTags",
      "fields": [
        "precision",
        "recall",
        "f1",
        "aligned_accuracy"
      ]
    },
    {
      "name": "Lemmas",
      "fields": [
        "precision",
        "recall",
        "f1",
        "aligned_accuracy"
      ]
    },
    {
      "name": "UAS",
      "fields": [
        "precision",
        "recall",
        "f1",
        "aligned_accuracy"
      ]
    },
    {
      "name": "LAS",
      "fields": [
        "precision",
        "recall",
        "f1",
        "aligned_accuracy"
      ]
    },
    {
      "name": "CLAS",
      "fields": [
        "precision",
        "recall",
        "f1",
        "aligned_accuracy"
      ]
    },
    {
      "name": "MLAS",
      "fields": [
        "precision",
        "recall",
        "f1",
        "aligned_accuracy"
      ]
    },
    {
      "name": "BLEX",
      "fields": [
        "precision",
        "recall",
        "f1",
        "aligned_accuracy"
      ]
    }
  ],
  "rows": [
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "EN",
      "model": "spacy",
      "training_condition": "default",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "EN:spokentest",
      "gold_file": "am_benchmark/source/gold/en_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/EN/spacy_default_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "67be8258af599f926bd6191833b34c31dd065fca9d5a6d4d5ccaf8cf8fb03c5a",
      "prediction_sha256": "abcc241bf75eae4fb513548df5987293ee17ced0453ef7cb9d8ee59bacbb9c9d",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 95.707343412527,
          "recall": 95.707343412527,
          "f1": 95.707343412527,
          "aligned_accuracy": 95.707343412527
        },
        "XPOS": {
          "precision": 97.22822174226063,
          "recall": 97.22822174226063,
          "f1": 97.22822174226063,
          "aligned_accuracy": 97.22822174226063
        },
        "UFeats": {
          "precision": 80.09359251259899,
          "recall": 80.09359251259899,
          "f1": 80.09359251259899,
          "aligned_accuracy": 80.09359251259899
        },
        "AllTags": {
          "precision": 78.17674586033118,
          "recall": 78.17674586033118,
          "f1": 78.17674586033118,
          "aligned_accuracy": 78.17674586033118
        },
        "Lemmas": {
          "precision": 96.99424046076314,
          "recall": 96.99424046076314,
          "f1": 96.99424046076314,
          "aligned_accuracy": 96.99424046076314
        },
        "UAS": {
          "precision": 57.35241180705544,
          "recall": 57.35241180705544,
          "f1": 57.35241180705544,
          "aligned_accuracy": 57.35241180705544
        },
        "LAS": {
          "precision": 38.17494600431965,
          "recall": 38.17494600431965,
          "f1": 38.17494600431965,
          "aligned_accuracy": 38.17494600431965
        },
        "CLAS": {
          "precision": 65.5701754385965,
          "recall": 37.13709051389536,
          "f1": 47.417979978194076,
          "aligned_accuracy": 37.13709051389536
        },
        "MLAS": {
          "precision": 38.43201754385965,
          "recall": 21.766806396522277,
          "f1": 27.792645455446525,
          "aligned_accuracy": 21.766806396522277
        },
        "BLEX": {
          "precision": 63.898026315789465,
          "recall": 36.19003260363298,
          "f1": 46.208742194469224,
          "aligned_accuracy": 36.19003260363298
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "EN",
      "model": "spacy",
      "training_condition": "default",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "EN:writtentest",
      "gold_file": "am_benchmark/source/gold/en_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/EN/spacy_default_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "436cd6e67fbc15b5cda785314dc994b51e83c80e67b424b9638f320e9200b880",
      "prediction_sha256": "b3a1704c372ac57cd752a668175374c38356b30d679b73d26156f43e2c49296e",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 96.3841481052936,
          "recall": 96.3841481052936,
          "f1": 96.3841481052936,
          "aligned_accuracy": 96.3841481052936
        },
        "XPOS": {
          "precision": 97.65114260919873,
          "recall": 97.65114260919873,
          "f1": 97.65114260919873,
          "aligned_accuracy": 97.65114260919873
        },
        "UFeats": {
          "precision": 82.3719988429274,
          "recall": 82.3719988429274,
          "f1": 82.3719988429274,
          "aligned_accuracy": 82.3719988429274
        },
        "AllTags": {
          "precision": 81.12236042811686,
          "recall": 81.12236042811686,
          "f1": 81.12236042811686,
          "aligned_accuracy": 81.12236042811686
        },
        "Lemmas": {
          "precision": 96.77176742840614,
          "recall": 96.77176742840614,
          "f1": 96.77176742840614,
          "aligned_accuracy": 96.77176742840614
        },
        "UAS": {
          "precision": 55.82875325426671,
          "recall": 55.82875325426671,
          "f1": 55.82875325426671,
          "aligned_accuracy": 55.82875325426671
        },
        "LAS": {
          "precision": 37.91726930864912,
          "recall": 37.91726930864912,
          "f1": 37.91726930864912,
          "aligned_accuracy": 37.91726930864912
        },
        "CLAS": {
          "precision": 68.62170087976538,
          "recall": 38.102992061876655,
          "f1": 48.99882214369847,
          "aligned_accuracy": 38.102992061876655
        },
        "MLAS": {
          "precision": 40.32258064516129,
          "recall": 22.38957866883778,
          "f1": 28.792042926318544,
          "aligned_accuracy": 22.38957866883778
        },
        "BLEX": {
          "precision": 65.50586510263929,
          "recall": 36.37288825564828,
          "f1": 46.7739824630284,
          "aligned_accuracy": 36.37288825564828
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "EN",
      "model": "spacy",
      "training_condition": "writtenandspokentrain",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "EN:spokentest",
      "gold_file": "am_benchmark/source/gold/en_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/EN/spacy_writtenandspokentrain_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "67be8258af599f926bd6191833b34c31dd065fca9d5a6d4d5ccaf8cf8fb03c5a",
      "prediction_sha256": "0d3341b30dc86ce07fbf19d68e04c6d12abc713d6750be0abbbbd8083c534c7c",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 95.3203743700504,
          "recall": 97.6041282712864,
          "f1": 96.4487342924786,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 98.02915766738661,
          "recall": 98.02915766738661,
          "f1": 98.02915766738661,
          "aligned_accuracy": 98.02915766738661
        },
        "XPOS": {
          "precision": 97.8581713462923,
          "recall": 97.8581713462923,
          "f1": 97.8581713462923,
          "aligned_accuracy": 97.8581713462923
        },
        "UFeats": {
          "precision": 31.785457163426926,
          "recall": 31.785457163426926,
          "f1": 31.785457163426926,
          "aligned_accuracy": 31.785457163426926
        },
        "AllTags": {
          "precision": 31.01151907847372,
          "recall": 31.01151907847372,
          "f1": 31.01151907847372,
          "aligned_accuracy": 31.01151907847372
        },
        "Lemmas": {
          "precision": 98.11915046796257,
          "recall": 98.11915046796257,
          "f1": 98.11915046796257,
          "aligned_accuracy": 98.11915046796257
        },
        "UAS": {
          "precision": 93.1785457163427,
          "recall": 93.1785457163427,
          "f1": 93.1785457163427,
          "aligned_accuracy": 93.1785457163427
        },
        "LAS": {
          "precision": 91.29769618430525,
          "recall": 91.29769618430525,
          "f1": 91.29769618430525,
          "aligned_accuracy": 91.29769618430525
        },
        "CLAS": {
          "precision": 88.67953908439739,
          "recall": 88.41794752367645,
          "f1": 88.54855010495218,
          "aligned_accuracy": 88.41794752367645
        },
        "MLAS": {
          "precision": 5.481158517595765,
          "recall": 5.464989908399317,
          "f1": 5.473062271631813,
          "aligned_accuracy": 5.464989908399317
        },
        "BLEX": {
          "precision": 86.60853316723762,
          "recall": 86.35305076851421,
          "f1": 86.48060328072766,
          "aligned_accuracy": 86.35305076851421
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "EN",
      "model": "spacy",
      "training_condition": "writtenandspokentrain",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "EN:writtentest",
      "gold_file": "am_benchmark/source/gold/en_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/EN/spacy_writtenandspokentrain_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "436cd6e67fbc15b5cda785314dc994b51e83c80e67b424b9638f320e9200b880",
      "prediction_sha256": "1b544c5f24213378b9dd682de67b4bdaae80898a9fd4b15d2fe4471465d05d11",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 98.25282036447787,
          "recall": 99.11871133418934,
          "f1": 98.68386646910136,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 98.47266415967601,
          "recall": 98.47266415967601,
          "f1": 98.47266415967601,
          "aligned_accuracy": 98.47266415967601
        },
        "XPOS": {
          "precision": 98.0676887474689,
          "recall": 98.0676887474689,
          "f1": 98.0676887474689,
          "aligned_accuracy": 98.0676887474689
        },
        "UFeats": {
          "precision": 31.443448076366792,
          "recall": 31.443448076366792,
          "f1": 31.443448076366792,
          "aligned_accuracy": 31.443448076366792
        },
        "AllTags": {
          "precision": 30.916980040497542,
          "recall": 30.916980040497542,
          "f1": 30.916980040497542,
          "aligned_accuracy": 30.916980040497542
        },
        "Lemmas": {
          "precision": 98.16603991900492,
          "recall": 98.16603991900492,
          "f1": 98.16603991900492,
          "aligned_accuracy": 98.16603991900492
        },
        "UAS": {
          "precision": 94.12207115996529,
          "recall": 94.12207115996529,
          "f1": 94.12207115996529,
          "aligned_accuracy": 94.12207115996529
        },
        "LAS": {
          "precision": 92.51952560023142,
          "recall": 92.51952560023142,
          "f1": 92.51952560023142,
          "aligned_accuracy": 92.51952560023142
        },
        "CLAS": {
          "precision": 89.79321585005603,
          "recall": 89.71097089354772,
          "f1": 89.75207453036705,
          "aligned_accuracy": 89.71097089354772
        },
        "MLAS": {
          "precision": 3.004991341550372,
          "recall": 3.0022389578668838,
          "f1": 3.003614519167133,
          "aligned_accuracy": 3.0022389578668838
        },
        "BLEX": {
          "precision": 87.36884995416115,
          "recall": 87.28882556482802,
          "f1": 87.32881942676781,
          "aligned_accuracy": 87.28882556482802
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "EN",
      "model": "spacy",
      "training_condition": "writtentrain",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "EN:spokentest",
      "gold_file": "am_benchmark/source/gold/en_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/EN/spacy_writtentrain_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "67be8258af599f926bd6191833b34c31dd065fca9d5a6d4d5ccaf8cf8fb03c5a",
      "prediction_sha256": "8c4882833f312589f4f8fe06393f6d8f1bbaf7b5d59a140eec91a391bcf72d08",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 95.3203743700504,
          "recall": 97.6041282712864,
          "f1": 96.4487342924786,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 97.6601871850252,
          "recall": 97.6601871850252,
          "f1": 97.6601871850252,
          "aligned_accuracy": 97.6601871850252
        },
        "XPOS": {
          "precision": 97.77717782577395,
          "recall": 97.77717782577395,
          "f1": 97.77717782577395,
          "aligned_accuracy": 97.77717782577395
        },
        "UFeats": {
          "precision": 31.785457163426926,
          "recall": 31.785457163426926,
          "f1": 31.785457163426926,
          "aligned_accuracy": 31.785457163426926
        },
        "AllTags": {
          "precision": 30.97552195824334,
          "recall": 30.97552195824334,
          "f1": 30.97552195824334,
          "aligned_accuracy": 30.97552195824334
        },
        "Lemmas": {
          "precision": 97.41720662347012,
          "recall": 97.41720662347012,
          "f1": 97.41720662347012,
          "aligned_accuracy": 97.41720662347012
        },
        "UAS": {
          "precision": 91.41468682505399,
          "recall": 91.41468682505399,
          "f1": 91.41468682505399,
          "aligned_accuracy": 91.41468682505399
        },
        "LAS": {
          "precision": 88.98488120950324,
          "recall": 88.98488120950324,
          "f1": 88.98488120950324,
          "aligned_accuracy": 88.98488120950324
        },
        "CLAS": {
          "precision": 85.69872393401805,
          "recall": 85.49914609532682,
          "f1": 85.59881868345379,
          "aligned_accuracy": 85.49914609532682
        },
        "MLAS": {
          "precision": 5.275443510737628,
          "recall": 5.263157894736842,
          "f1": 5.269293541618093,
          "aligned_accuracy": 5.263157894736842
        },
        "BLEX": {
          "precision": 82.81979458450047,
          "recall": 82.62692128551467,
          "f1": 82.72324551177431,
          "aligned_accuracy": 82.62692128551467
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "EN",
      "model": "spacy",
      "training_condition": "writtentrain",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "EN:writtentest",
      "gold_file": "am_benchmark/source/gold/en_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/EN/spacy_writtentrain_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "436cd6e67fbc15b5cda785314dc994b51e83c80e67b424b9638f320e9200b880",
      "prediction_sha256": "eec827b182bbdb377eb35a6e1377f5038d2197cf0cf43e5573d23b58d5d4da2b",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 98.25282036447787,
          "recall": 99.11871133418934,
          "f1": 98.68386646910136,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 97.87677176742841,
          "recall": 97.87677176742841,
          "f1": 97.87677176742841,
          "aligned_accuracy": 97.87677176742841
        },
        "XPOS": {
          "precision": 97.37923054671681,
          "recall": 97.37923054671681,
          "f1": 97.37923054671681,
          "aligned_accuracy": 97.37923054671681
        },
        "UFeats": {
          "precision": 31.443448076366792,
          "recall": 31.443448076366792,
          "f1": 31.443448076366792,
          "aligned_accuracy": 31.443448076366792
        },
        "AllTags": {
          "precision": 30.41943881978594,
          "recall": 30.41943881978594,
          "f1": 30.41943881978594,
          "aligned_accuracy": 30.41943881978594
        },
        "Lemmas": {
          "precision": 96.67341625687011,
          "recall": 96.67341625687011,
          "f1": 96.67341625687011,
          "aligned_accuracy": 96.67341625687011
        },
        "UAS": {
          "precision": 91.93520393404685,
          "recall": 91.93520393404685,
          "f1": 91.93520393404685,
          "aligned_accuracy": 91.93520393404685
        },
        "LAS": {
          "precision": 89.50535146080416,
          "recall": 89.50535146080416,
          "f1": 89.50535146080416,
          "aligned_accuracy": 89.50535146080416
        },
        "CLAS": {
          "precision": 86.11196084429488,
          "recall": 85.94545084469775,
          "f1": 86.02862527377376,
          "aligned_accuracy": 85.94545084469775
        },
        "MLAS": {
          "precision": 2.722545120832059,
          "recall": 2.7172806838998578,
          "f1": 2.7199103550145165,
          "aligned_accuracy": 2.7172806838998578
        },
        "BLEX": {
          "precision": 81.77832160701539,
          "recall": 81.6201913291268,
          "f1": 81.69917995212143,
          "aligned_accuracy": 81.6201913291268
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "EN",
      "model": "stanza",
      "training_condition": "default",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "EN:spokentest",
      "gold_file": "am_benchmark/source/gold/en_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/EN/stanza_default_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "67be8258af599f926bd6191833b34c31dd065fca9d5a6d4d5ccaf8cf8fb03c5a",
      "prediction_sha256": "5645cb1840fd50ccdaf338471487a0cbf58e0150f7f6423538eb2a78494f3408",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 97.44420446364292,
          "recall": 97.44420446364292,
          "f1": 97.44420446364292,
          "aligned_accuracy": 97.44420446364292
        },
        "XPOS": {
          "precision": 97.59719222462203,
          "recall": 97.59719222462203,
          "f1": 97.59719222462203,
          "aligned_accuracy": 97.59719222462203
        },
        "UFeats": {
          "precision": 93.7455003599712,
          "recall": 93.7455003599712,
          "f1": 93.7455003599712,
          "aligned_accuracy": 93.7455003599712
        },
        "AllTags": {
          "precision": 92.24262059035277,
          "recall": 92.24262059035277,
          "f1": 92.24262059035277,
          "aligned_accuracy": 92.24262059035277
        },
        "Lemmas": {
          "precision": 98.71310295176386,
          "recall": 98.71310295176386,
          "f1": 98.71310295176386,
          "aligned_accuracy": 98.71310295176386
        },
        "UAS": {
          "precision": 91.26169906407488,
          "recall": 91.26169906407488,
          "f1": 91.26169906407488,
          "aligned_accuracy": 91.26169906407488
        },
        "LAS": {
          "precision": 89.10187185025198,
          "recall": 89.10187185025198,
          "f1": 89.10187185025198,
          "aligned_accuracy": 89.10187185025198
        },
        "CLAS": {
          "precision": 86.5075651224458,
          "recall": 86.10464213631424,
          "f1": 86.3056333644569,
          "aligned_accuracy": 86.10464213631424
        },
        "MLAS": {
          "precision": 76.15036655747933,
          "recall": 75.79568390001552,
          "f1": 75.97261126672892,
          "aligned_accuracy": 75.79568390001552
        },
        "BLEX": {
          "precision": 85.13492434877554,
          "recall": 84.7383946592144,
          "f1": 84.93619670090258,
          "aligned_accuracy": 84.7383946592144
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "EN",
      "model": "stanza",
      "training_condition": "default",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "EN:writtentest",
      "gold_file": "am_benchmark/source/gold/en_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/EN/stanza_default_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "436cd6e67fbc15b5cda785314dc994b51e83c80e67b424b9638f320e9200b880",
      "prediction_sha256": "2e9bd3a0bb8e57349fbb5e548680da1a550ad9e203074f8a5d3a9433193f0681",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 98.07925947353196,
          "recall": 98.07925947353196,
          "f1": 98.07925947353196,
          "aligned_accuracy": 98.07925947353196
        },
        "XPOS": {
          "precision": 97.73213769164015,
          "recall": 97.73213769164015,
          "f1": 97.73213769164015,
          "aligned_accuracy": 97.73213769164015
        },
        "UFeats": {
          "precision": 94.14521261209141,
          "recall": 94.14521261209141,
          "f1": 94.14521261209141,
          "aligned_accuracy": 94.14521261209141
        },
        "AllTags": {
          "precision": 93.08070581428984,
          "recall": 93.08070581428984,
          "f1": 93.08070581428984,
          "aligned_accuracy": 93.08070581428984
        },
        "Lemmas": {
          "precision": 97.74949378073474,
          "recall": 97.74949378073474,
          "f1": 97.74949378073474,
          "aligned_accuracy": 97.74949378073474
        },
        "UAS": {
          "precision": 92.68151576511427,
          "recall": 92.68151576511427,
          "f1": 92.68151576511427,
          "aligned_accuracy": 92.68151576511427
        },
        "LAS": {
          "precision": 90.78970205380388,
          "recall": 90.78970205380388,
          "f1": 90.78970205380388,
          "aligned_accuracy": 90.78970205380388
        },
        "CLAS": {
          "precision": 87.55995509745892,
          "recall": 87.31935680846733,
          "f1": 87.43949044585987,
          "aligned_accuracy": 87.31935680846733
        },
        "MLAS": {
          "precision": 78.20185733238085,
          "recall": 77.98697333604721,
          "f1": 78.09426751592356,
          "aligned_accuracy": 77.98697333604721
        },
        "BLEX": {
          "precision": 85.25359730584753,
          "recall": 85.0193364543049,
          "f1": 85.13630573248408,
          "aligned_accuracy": 85.0193364543049
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "EN",
      "model": "stanza",
      "training_condition": "writtenandspokentrain",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "EN:spokentest",
      "gold_file": "am_benchmark/source/gold/en_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/EN/stanza_writtenandspokentrain_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "67be8258af599f926bd6191833b34c31dd065fca9d5a6d4d5ccaf8cf8fb03c5a",
      "prediction_sha256": "f5cc804fd06442dd1195b2e783a032a8c6a13230ba3b780edef063542482f24a",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 95.3203743700504,
          "recall": 97.6041282712864,
          "f1": 96.4487342924786,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 97.01223902087833,
          "recall": 97.01223902087833,
          "f1": 97.01223902087833,
          "aligned_accuracy": 97.01223902087833
        },
        "XPOS": {
          "precision": 97.0752339812815,
          "recall": 97.0752339812815,
          "f1": 97.0752339812815,
          "aligned_accuracy": 97.0752339812815
        },
        "UFeats": {
          "precision": 97.0842332613391,
          "recall": 97.0842332613391,
          "f1": 97.0842332613391,
          "aligned_accuracy": 97.0842332613391
        },
        "AllTags": {
          "precision": 95.41036717062636,
          "recall": 95.41036717062636,
          "f1": 95.41036717062636,
          "aligned_accuracy": 95.41036717062636
        },
        "Lemmas": {
          "precision": 98.76709863210942,
          "recall": 98.76709863210942,
          "f1": 98.76709863210942,
          "aligned_accuracy": 98.76709863210942
        },
        "UAS": {
          "precision": 89.17386609071274,
          "recall": 89.17386609071274,
          "f1": 89.17386609071274,
          "aligned_accuracy": 89.17386609071274
        },
        "LAS": {
          "precision": 86.35709143268538,
          "recall": 86.35709143268538,
          "f1": 86.35709143268538,
          "aligned_accuracy": 86.35709143268538
        },
        "CLAS": {
          "precision": 82.5713839912623,
          "recall": 82.16115510013972,
          "f1": 82.36575875486382,
          "aligned_accuracy": 82.16115510013972
        },
        "MLAS": {
          "precision": 78.6550163832111,
          "recall": 78.26424468250272,
          "f1": 78.45914396887159,
          "aligned_accuracy": 78.26424468250272
        },
        "BLEX": {
          "precision": 81.32313933530972,
          "recall": 80.91911193913988,
          "f1": 81.12062256809338,
          "aligned_accuracy": 80.91911193913988
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "EN",
      "model": "stanza",
      "training_condition": "writtenandspokentrain",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "EN:writtentest",
      "gold_file": "am_benchmark/source/gold/en_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/EN/stanza_writtenandspokentrain_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "436cd6e67fbc15b5cda785314dc994b51e83c80e67b424b9638f320e9200b880",
      "prediction_sha256": "cf60f1bbc20b023e73fbd0048dea3d45900311f4f704788b857e366c34f52e24",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 98.25282036447787,
          "recall": 99.11871133418934,
          "f1": 98.68386646910136,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 97.7610645067978,
          "recall": 97.7610645067978,
          "f1": 97.7610645067978,
          "aligned_accuracy": 97.7610645067978
        },
        "XPOS": {
          "precision": 97.65692797223025,
          "recall": 97.65692797223025,
          "f1": 97.65692797223025,
          "aligned_accuracy": 97.65692797223025
        },
        "UFeats": {
          "precision": 97.37923054671681,
          "recall": 97.37923054671681,
          "f1": 97.37923054671681,
          "aligned_accuracy": 97.37923054671681
        },
        "AllTags": {
          "precision": 96.48249927682963,
          "recall": 96.48249927682963,
          "f1": 96.48249927682963,
          "aligned_accuracy": 96.48249927682963
        },
        "Lemmas": {
          "precision": 98.53051778999132,
          "recall": 98.53051778999132,
          "f1": 98.53051778999132,
          "aligned_accuracy": 98.53051778999132
        },
        "UAS": {
          "precision": 90.5640728955742,
          "recall": 90.5640728955742,
          "f1": 90.5640728955742,
          "aligned_accuracy": 90.5640728955742
        },
        "LAS": {
          "precision": 88.37720566965577,
          "recall": 88.37720566965577,
          "f1": 88.37720566965577,
          "aligned_accuracy": 88.37720566965577
        },
        "CLAS": {
          "precision": 84.27608740044926,
          "recall": 84.00162833299409,
          "f1": 84.13863404689093,
          "aligned_accuracy": 84.00162833299409
        },
        "MLAS": {
          "precision": 81.1721462119665,
          "recall": 80.90779564420924,
          "f1": 81.03975535168195,
          "aligned_accuracy": 80.90779564420924
        },
        "BLEX": {
          "precision": 82.39738615478865,
          "recall": 82.1290453897822,
          "f1": 82.26299694189603,
          "aligned_accuracy": 82.1290453897822
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "EN",
      "model": "stanza",
      "training_condition": "writtentrain",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "EN:spokentest",
      "gold_file": "am_benchmark/source/gold/en_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/EN/stanza_writtentrain_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "67be8258af599f926bd6191833b34c31dd065fca9d5a6d4d5ccaf8cf8fb03c5a",
      "prediction_sha256": "c79402eaf00b5be7cfee8af5cd319e739dcda1b1d3cc23e327653b71b28a9f7d",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 95.3203743700504,
          "recall": 97.6041282712864,
          "f1": 96.4487342924786,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 96.47228221742262,
          "recall": 96.47228221742262,
          "f1": 96.47228221742262,
          "aligned_accuracy": 96.47228221742262
        },
        "XPOS": {
          "precision": 96.56227501799856,
          "recall": 96.56227501799856,
          "f1": 96.56227501799856,
          "aligned_accuracy": 96.56227501799856
        },
        "UFeats": {
          "precision": 96.508279337653,
          "recall": 96.508279337653,
          "f1": 96.508279337653,
          "aligned_accuracy": 96.508279337653
        },
        "AllTags": {
          "precision": 94.54643628509719,
          "recall": 94.54643628509719,
          "f1": 94.54643628509719,
          "aligned_accuracy": 94.54643628509719
        },
        "Lemmas": {
          "precision": 98.66810655147589,
          "recall": 98.66810655147589,
          "f1": 98.66810655147589,
          "aligned_accuracy": 98.66810655147589
        },
        "UAS": {
          "precision": 87.21202303815694,
          "recall": 87.21202303815694,
          "f1": 87.21202303815694,
          "aligned_accuracy": 87.21202303815694
        },
        "LAS": {
          "precision": 83.90028797696183,
          "recall": 83.90028797696183,
          "f1": 83.90028797696183,
          "aligned_accuracy": 83.90028797696183
        },
        "CLAS": {
          "precision": 80.45053560176434,
          "recall": 79.28893029032758,
          "f1": 79.86550942215966,
          "aligned_accuracy": 79.28893029032758
        },
        "MLAS": {
          "precision": 75.48834278512916,
          "recall": 74.39838534389071,
          "f1": 74.93940104777543,
          "aligned_accuracy": 74.39838534389071
        },
        "BLEX": {
          "precision": 79.25330812854442,
          "recall": 78.10898928737774,
          "f1": 78.67698803659395,
          "aligned_accuracy": 78.10898928737774
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "EN",
      "model": "stanza",
      "training_condition": "writtentrain",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "EN:writtentest",
      "gold_file": "am_benchmark/source/gold/en_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/EN/stanza_writtentrain_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "436cd6e67fbc15b5cda785314dc994b51e83c80e67b424b9638f320e9200b880",
      "prediction_sha256": "5a5ab9e5eadad56710d5e27d1595f13b751a79ddd3b303853debda8b2ed161f0",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 98.25282036447787,
          "recall": 99.11871133418934,
          "f1": 98.68386646910136,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 97.7610645067978,
          "recall": 97.7610645067978,
          "f1": 97.7610645067978,
          "aligned_accuracy": 97.7610645067978
        },
        "XPOS": {
          "precision": 97.63957188313567,
          "recall": 97.63957188313567,
          "f1": 97.63957188313567,
          "aligned_accuracy": 97.63957188313567
        },
        "UFeats": {
          "precision": 97.34451836852762,
          "recall": 97.34451836852762,
          "f1": 97.34451836852762,
          "aligned_accuracy": 97.34451836852762
        },
        "AllTags": {
          "precision": 96.49407000289268,
          "recall": 96.49407000289268,
          "f1": 96.49407000289268,
          "aligned_accuracy": 96.49407000289268
        },
        "Lemmas": {
          "precision": 98.40902516632919,
          "recall": 98.40902516632919,
          "f1": 98.40902516632919,
          "aligned_accuracy": 98.40902516632919
        },
        "UAS": {
          "precision": 90.98640439687591,
          "recall": 90.98640439687591,
          "f1": 90.98640439687591,
          "aligned_accuracy": 90.98640439687591
        },
        "LAS": {
          "precision": 88.85160543824125,
          "recall": 88.85160543824125,
          "f1": 88.85160543824125,
          "aligned_accuracy": 88.85160543824125
        },
        "CLAS": {
          "precision": 85.07615250945517,
          "recall": 84.70384693669855,
          "f1": 84.88959151410067,
          "aligned_accuracy": 84.70384693669855
        },
        "MLAS": {
          "precision": 81.88694674435246,
          "recall": 81.52859759820883,
          "f1": 81.7073792646234,
          "aligned_accuracy": 81.52859759820883
        },
        "BLEX": {
          "precision": 82.9704589594194,
          "recall": 82.6073682067983,
          "f1": 82.78851547758683,
          "aligned_accuracy": 82.6073682067983
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "NL",
      "model": "spacy",
      "training_condition": "default",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "NL:spokentest",
      "gold_file": "am_benchmark/source/gold/nl_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/NL/spacy_default_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "a930b004e6b1a8ae816ee661993e37dec3f8da3321375f5db96ddedbff5083f5",
      "prediction_sha256": "dfbea4425ae03525fd29f7581a8127e630db2365e54425955b9a758743125fa1",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 91.67310482579283,
          "recall": 91.67310482579283,
          "f1": 91.67310482579283,
          "aligned_accuracy": 91.67310482579283
        },
        "XPOS": {
          "precision": 90.46524336241497,
          "recall": 90.46524336241497,
          "f1": 90.46524336241497,
          "aligned_accuracy": 90.46524336241497
        },
        "UFeats": {
          "precision": 75.09657238689253,
          "recall": 75.09657238689253,
          "f1": 75.09657238689253,
          "aligned_accuracy": 75.09657238689253
        },
        "AllTags": {
          "precision": 71.54270854924721,
          "recall": 71.54270854924721,
          "f1": 71.54270854924721,
          "aligned_accuracy": 71.54270854924721
        },
        "Lemmas": {
          "precision": 94.96692984604948,
          "recall": 94.96692984604948,
          "f1": 94.96692984604948,
          "aligned_accuracy": 94.96692984604948
        },
        "UAS": {
          "precision": 70.8021632214664,
          "recall": 70.8021632214664,
          "f1": 70.8021632214664,
          "aligned_accuracy": 70.8021632214664
        },
        "LAS": {
          "precision": 53.08372119316361,
          "recall": 53.08372119316361,
          "f1": 53.08372119316361,
          "aligned_accuracy": 53.08372119316361
        },
        "CLAS": {
          "precision": 56.87154696132597,
          "recall": 44.20949029198604,
          "f1": 49.74745355998188,
          "aligned_accuracy": 44.20949029198604
        },
        "MLAS": {
          "precision": 44.939379987722525,
          "recall": 34.93393778520087,
          "f1": 39.30998607218969,
          "aligned_accuracy": 34.93393778520087
        },
        "BLEX": {
          "precision": 54.66927562922038,
          "recall": 42.49753944346685,
          "f1": 47.82105280821573,
          "aligned_accuracy": 42.49753944346685
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "NL",
      "model": "spacy",
      "training_condition": "default",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "NL:writtentest",
      "gold_file": "am_benchmark/source/gold/nl_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/NL/spacy_default_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "ac1ec430faa1dbb3fe442aaa8ae03c156a39edca1b537240e3a90cbfd7815dd7",
      "prediction_sha256": "d9d6dc89e9c7122fe2ce8e6f85b306067166fe146846c650e11127001bf422b4",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 95.37723833071102,
          "recall": 95.37723833071102,
          "f1": 95.37723833071102,
          "aligned_accuracy": 95.37723833071102
        },
        "XPOS": {
          "precision": 93.48667615693914,
          "recall": 93.48667615693914,
          "f1": 93.48667615693914,
          "aligned_accuracy": 93.48667615693914
        },
        "UFeats": {
          "precision": 94.83529382383057,
          "recall": 94.83529382383057,
          "f1": 94.83529382383057,
          "aligned_accuracy": 94.83529382383057
        },
        "AllTags": {
          "precision": 92.3328588197098,
          "recall": 92.3328588197098,
          "f1": 92.3328588197098,
          "aligned_accuracy": 92.3328588197098
        },
        "Lemmas": {
          "precision": 91.2589595664444,
          "recall": 91.2589595664444,
          "f1": 91.2589595664444,
          "aligned_accuracy": 91.2589595664444
        },
        "UAS": {
          "precision": 86.95587023301117,
          "recall": 86.95587023301117,
          "f1": 86.95587023301117,
          "aligned_accuracy": 86.95587023301117
        },
        "LAS": {
          "precision": 77.55800304687696,
          "recall": 77.55800304687696,
          "f1": 77.55800304687696,
          "aligned_accuracy": 77.55800304687696
        },
        "CLAS": {
          "precision": 75.15605493133583,
          "recall": 66.87105660712699,
          "f1": 70.77190754978722,
          "aligned_accuracy": 66.87105660712699
        },
        "MLAS": {
          "precision": 67.57553058676655,
          "recall": 60.12618857193637,
          "f1": 63.633584914532925,
          "aligned_accuracy": 60.12618857193637
        },
        "BLEX": {
          "precision": 64.9637952559301,
          "recall": 57.802363814094015,
          "f1": 61.17420234652371,
          "aligned_accuracy": 57.802363814094015
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "NL",
      "model": "spacy",
      "training_condition": "writtenandspokentrain",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "NL:spokentest",
      "gold_file": "am_benchmark/source/gold/nl_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/NL/spacy_writtenandspokentrain_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "a930b004e6b1a8ae816ee661993e37dec3f8da3321375f5db96ddedbff5083f5",
      "prediction_sha256": "7cc09d26e1cbe0bc58ff803d7beb4a3474df379cd8e21b944a7fd26d9bd7d2aa",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 97.09811754508281,
          "recall": 97.09811754508281,
          "f1": 97.09811754508281,
          "aligned_accuracy": 97.09811754508281
        },
        "XPOS": {
          "precision": 96.00331643709133,
          "recall": 96.00331643709133,
          "f1": 96.00331643709133,
          "aligned_accuracy": 96.00331643709133
        },
        "UFeats": {
          "precision": 47.116018768018996,
          "recall": 47.116018768018996,
          "f1": 47.116018768018996,
          "aligned_accuracy": 47.116018768018996
        },
        "AllTags": {
          "precision": 45.438956829787635,
          "recall": 45.438956829787635,
          "f1": 45.438956829787635,
          "aligned_accuracy": 45.438956829787635
        },
        "Lemmas": {
          "precision": 97.67849403606625,
          "recall": 97.67849403606625,
          "f1": 97.67849403606625,
          "aligned_accuracy": 97.67849403606625
        },
        "UAS": {
          "precision": 87.72352974429516,
          "recall": 87.72352974429516,
          "f1": 87.72352974429516,
          "aligned_accuracy": 87.72352974429516
        },
        "LAS": {
          "precision": 84.88571482409692,
          "recall": 84.88571482409692,
          "f1": 84.88571482409692,
          "aligned_accuracy": 84.88571482409692
        },
        "CLAS": {
          "precision": 82.2246814619848,
          "recall": 81.99170867010648,
          "f1": 82.10802980750563,
          "aligned_accuracy": 81.99170867010648
        },
        "MLAS": {
          "precision": 26.06328886761979,
          "recall": 25.98944197560321,
          "f1": 26.026313038543673,
          "aligned_accuracy": 25.98944197560321
        },
        "BLEX": {
          "precision": 79.92462762457379,
          "recall": 79.69817173193356,
          "f1": 79.81123904245628,
          "aligned_accuracy": 79.69817173193356
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "NL",
      "model": "spacy",
      "training_condition": "writtenandspokentrain",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "NL:writtentest",
      "gold_file": "am_benchmark/source/gold/nl_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/NL/spacy_writtenandspokentrain_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "ac1ec430faa1dbb3fe442aaa8ae03c156a39edca1b537240e3a90cbfd7815dd7",
      "prediction_sha256": "9462f8d0301c3db92683d02e1e0615d78250134cf7addad1ba15db86c6c39752",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 98.23680727254565,
          "recall": 98.23680727254565,
          "f1": 98.23680727254565,
          "aligned_accuracy": 98.23680727254565
        },
        "XPOS": {
          "precision": 97.19537474089059,
          "recall": 97.19537474089059,
          "f1": 97.19537474089059,
          "aligned_accuracy": 97.19537474089059
        },
        "UFeats": {
          "precision": 42.51142578856672,
          "recall": 42.51142578856672,
          "f1": 42.51142578856672,
          "aligned_accuracy": 42.51142578856672
        },
        "AllTags": {
          "precision": 41.6523063859544,
          "recall": 41.6523063859544,
          "f1": 41.6523063859544,
          "aligned_accuracy": 41.6523063859544
        },
        "Lemmas": {
          "precision": 95.93167003821084,
          "recall": 95.93167003821084,
          "f1": 95.93167003821084,
          "aligned_accuracy": 95.93167003821084
        },
        "UAS": {
          "precision": 94.89023750655579,
          "recall": 94.89023750655579,
          "f1": 94.89023750655579,
          "aligned_accuracy": 94.89023750655579
        },
        "LAS": {
          "precision": 92.702479958043,
          "recall": 92.702479958043,
          "f1": 92.702479958043,
          "aligned_accuracy": 92.702479958043
        },
        "CLAS": {
          "precision": 89.51179423393008,
          "recall": 89.53168044077135,
          "f1": 89.52173623297865,
          "aligned_accuracy": 89.53168044077135
        },
        "MLAS": {
          "precision": 19.594864732797298,
          "recall": 19.59921798631476,
          "f1": 19.597041117799943,
          "aligned_accuracy": 19.59921798631476
        },
        "BLEX": {
          "precision": 83.55470658789037,
          "recall": 83.57326935039545,
          "f1": 83.56398693826776,
          "aligned_accuracy": 83.57326935039545
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "NL",
      "model": "spacy",
      "training_condition": "writtentrain",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "NL:spokentest",
      "gold_file": "am_benchmark/source/gold/nl_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/NL/spacy_writtentrain_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "a930b004e6b1a8ae816ee661993e37dec3f8da3321375f5db96ddedbff5083f5",
      "prediction_sha256": "560c0f3bbfd10284f2720beaa708506568967bf58e94a6b349dfdd6d137ebebd",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 94.21319414347359,
          "recall": 94.21319414347359,
          "f1": 94.21319414347359,
          "aligned_accuracy": 94.21319414347359
        },
        "XPOS": {
          "precision": 92.53613220524223,
          "recall": 92.53613220524223,
          "f1": 92.53613220524223,
          "aligned_accuracy": 92.53613220524223
        },
        "UFeats": {
          "precision": 47.116018768018996,
          "recall": 47.116018768018996,
          "f1": 47.116018768018996,
          "aligned_accuracy": 47.116018768018996
        },
        "AllTags": {
          "precision": 43.1419472761876,
          "recall": 43.1419472761876,
          "f1": 43.1419472761876,
          "aligned_accuracy": 43.1419472761876
        },
        "Lemmas": {
          "precision": 96.39902768094368,
          "recall": 96.39902768094368,
          "f1": 96.39902768094368,
          "aligned_accuracy": 96.39902768094368
        },
        "UAS": {
          "precision": 79.90163749081385,
          "recall": 79.90163749081385,
          "f1": 79.90163749081385,
          "aligned_accuracy": 79.90163749081385
        },
        "LAS": {
          "precision": 74.56895739508941,
          "recall": 74.56895739508941,
          "f1": 74.56895739508941,
          "aligned_accuracy": 74.56895739508941
        },
        "CLAS": {
          "precision": 71.25198388475155,
          "recall": 69.62629365623788,
          "f1": 70.42975879806315,
          "aligned_accuracy": 69.62629365623788
        },
        "MLAS": {
          "precision": 18.94762544255891,
          "recall": 18.515315100360883,
          "f1": 18.72897590997541,
          "aligned_accuracy": 18.515315100360883
        },
        "BLEX": {
          "precision": 68.0136735441338,
          "recall": 66.46186882996808,
          "f1": 67.228817522212,
          "aligned_accuracy": 66.46186882996808
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "NL",
      "model": "spacy",
      "training_condition": "writtentrain",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "NL:writtentest",
      "gold_file": "am_benchmark/source/gold/nl_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/NL/spacy_writtentrain_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "ac1ec430faa1dbb3fe442aaa8ae03c156a39edca1b537240e3a90cbfd7815dd7",
      "prediction_sha256": "126fd8af4c173da477f9ec88c64dce3138288627836124fdcd57cdff51aeaa73",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 98.39914088059739,
          "recall": 98.39914088059739,
          "f1": 98.39914088059739,
          "aligned_accuracy": 98.39914088059739
        },
        "XPOS": {
          "precision": 97.1853849803951,
          "recall": 97.1853849803951,
          "f1": 97.1853849803951,
          "aligned_accuracy": 97.1853849803951
        },
        "UFeats": {
          "precision": 42.51142578856672,
          "recall": 42.51142578856672,
          "f1": 42.51142578856672,
          "aligned_accuracy": 42.51142578856672
        },
        "AllTags": {
          "precision": 41.68227566744087,
          "recall": 41.68227566744087,
          "f1": 41.68227566744087,
          "aligned_accuracy": 41.68227566744087
        },
        "Lemmas": {
          "precision": 95.9716290801928,
          "recall": 95.9716290801928,
          "f1": 95.9716290801928,
          "aligned_accuracy": 95.9716290801928
        },
        "UAS": {
          "precision": 95.1299917584476,
          "recall": 95.1299917584476,
          "f1": 95.1299917584476,
          "aligned_accuracy": 95.1299917584476
        },
        "LAS": {
          "precision": 93.12204989885367,
          "recall": 93.12204989885367,
          "f1": 93.12204989885367,
          "aligned_accuracy": 93.12204989885367
        },
        "CLAS": {
          "precision": 90.24899955535794,
          "recall": 90.18483959832933,
          "f1": 90.21690816961507,
          "aligned_accuracy": 90.18483959832933
        },
        "MLAS": {
          "precision": 19.648732770120052,
          "recall": 19.634764062916553,
          "f1": 19.64174593297182,
          "aligned_accuracy": 19.634764062916553
        },
        "BLEX": {
          "precision": 84.21520675855936,
          "recall": 84.15533635474985,
          "f1": 84.18526091208108,
          "aligned_accuracy": 84.15533635474985
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "NL",
      "model": "stanza",
      "training_condition": "default",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "NL:spokentest",
      "gold_file": "am_benchmark/source/gold/nl_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/NL/stanza_default_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "a930b004e6b1a8ae816ee661993e37dec3f8da3321375f5db96ddedbff5083f5",
      "prediction_sha256": "064c7dd53d10ddf1b46f9705f81bb13e628a272094550d8954980ebffbcafc1b",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 93.96446136162353,
          "recall": 93.96446136162353,
          "f1": 93.96446136162353,
          "aligned_accuracy": 93.96446136162353
        },
        "XPOS": {
          "precision": 92.51917315193427,
          "recall": 92.51917315193427,
          "f1": 92.51917315193427,
          "aligned_accuracy": 92.51917315193427
        },
        "UFeats": {
          "precision": 76.6699956660197,
          "recall": 76.6699956660197,
          "f1": 76.6699956660197,
          "aligned_accuracy": 76.6699956660197
        },
        "AllTags": {
          "precision": 73.85102413838588,
          "recall": 73.85102413838588,
          "f1": 73.85102413838588,
          "aligned_accuracy": 73.85102413838588
        },
        "Lemmas": {
          "precision": 96.32553844994253,
          "recall": 96.32553844994253,
          "f1": 96.32553844994253,
          "aligned_accuracy": 96.32553844994253
        },
        "UAS": {
          "precision": 78.44692758484237,
          "recall": 78.44692758484237,
          "f1": 78.44692758484237,
          "aligned_accuracy": 78.44692758484237
        },
        "LAS": {
          "precision": 73.04264259737323,
          "recall": 73.04264259737323,
          "f1": 73.04264259737323,
          "aligned_accuracy": 73.04264259737323
        },
        "CLAS": {
          "precision": 70.2454840203798,
          "recall": 67.84872796683467,
          "f1": 69.02630700609885,
          "aligned_accuracy": 67.84872796683467
        },
        "MLAS": {
          "precision": 45.97190057125212,
          "recall": 44.40335232187062,
          "f1": 45.17401462511758,
          "aligned_accuracy": 44.40335232187062
        },
        "BLEX": {
          "precision": 67.02485718696927,
          "recall": 64.73798801037908,
          "f1": 65.86157720666323,
          "aligned_accuracy": 64.73798801037908
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "NL",
      "model": "stanza",
      "training_condition": "default",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "NL:writtentest",
      "gold_file": "am_benchmark/source/gold/nl_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/NL/stanza_default_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "ac1ec430faa1dbb3fe442aaa8ae03c156a39edca1b537240e3a90cbfd7815dd7",
      "prediction_sha256": "9044a149d9081e9cde0a1f6d326d93b93120da56a394b298aca6584962e34d50",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 96.70587647661148,
          "recall": 96.70587647661148,
          "f1": 96.70587647661148,
          "aligned_accuracy": 96.70587647661148
        },
        "XPOS": {
          "precision": 95.27484328563223,
          "recall": 95.27484328563223,
          "f1": 95.27484328563223,
          "aligned_accuracy": 95.27484328563223
        },
        "UFeats": {
          "precision": 96.52106590744486,
          "recall": 96.52106590744486,
          "f1": 96.52106590744486,
          "aligned_accuracy": 96.52106590744486
        },
        "AllTags": {
          "precision": 94.63300117379686,
          "recall": 94.63300117379686,
          "f1": 94.63300117379686,
          "aligned_accuracy": 94.63300117379686
        },
        "Lemmas": {
          "precision": 94.77036038060987,
          "recall": 94.77036038060987,
          "f1": 94.77036038060987,
          "aligned_accuracy": 94.77036038060987
        },
        "UAS": {
          "precision": 91.44876501585874,
          "recall": 91.44876501585874,
          "f1": 91.44876501585874,
          "aligned_accuracy": 91.44876501585874
        },
        "LAS": {
          "precision": 87.57024050348393,
          "recall": 87.57024050348393,
          "f1": 87.57024050348393,
          "aligned_accuracy": 87.57024050348393
        },
        "CLAS": {
          "precision": 82.34164209773965,
          "recall": 81.90260375011108,
          "f1": 82.12153613115922,
          "aligned_accuracy": 81.90260375011108
        },
        "MLAS": {
          "precision": 76.65951934244617,
          "recall": 76.25077757042567,
          "f1": 76.4546021562862,
          "aligned_accuracy": 76.25077757042567
        },
        "BLEX": {
          "precision": 75.2881265076387,
          "recall": 74.88669688083178,
          "f1": 75.08687516706762,
          "aligned_accuracy": 74.88669688083178
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "NL",
      "model": "stanza",
      "training_condition": "writtenandspokentrain",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "NL:spokentest",
      "gold_file": "am_benchmark/source/gold/nl_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/NL/stanza_writtenandspokentrain_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "a930b004e6b1a8ae816ee661993e37dec3f8da3321375f5db96ddedbff5083f5",
      "prediction_sha256": "70097694b153c5de791e01b7adcd3d4ffe0bf14daa8c2ef01f8b36e76cc3288d",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 95.94867059865459,
          "recall": 95.94867059865459,
          "f1": 95.94867059865459,
          "aligned_accuracy": 95.94867059865459
        },
        "XPOS": {
          "precision": 94.81995138404719,
          "recall": 94.81995138404719,
          "f1": 94.81995138404719,
          "aligned_accuracy": 94.81995138404719
        },
        "UFeats": {
          "precision": 96.11260811396484,
          "recall": 96.11260811396484,
          "f1": 96.11260811396484,
          "aligned_accuracy": 96.11260811396484
        },
        "AllTags": {
          "precision": 93.41800297725602,
          "recall": 93.41800297725602,
          "f1": 93.41800297725602,
          "aligned_accuracy": 93.41800297725602
        },
        "Lemmas": {
          "precision": 97.61819517986018,
          "recall": 97.61819517986018,
          "f1": 97.61819517986018,
          "aligned_accuracy": 97.61819517986018
        },
        "UAS": {
          "precision": 86.00501234242213,
          "recall": 86.00501234242213,
          "f1": 86.00501234242213,
          "aligned_accuracy": 86.00501234242213
        },
        "LAS": {
          "precision": 82.45491718328968,
          "recall": 82.45491718328968,
          "f1": 82.45491718328968,
          "aligned_accuracy": 82.45491718328968
        },
        "CLAS": {
          "precision": 80.01639742499697,
          "recall": 78.59166691520772,
          "f1": 79.29763319841712,
          "aligned_accuracy": 78.59166691520772
        },
        "MLAS": {
          "precision": 74.7084902222762,
          "recall": 73.37826955769631,
          "f1": 74.03740539564556,
          "aligned_accuracy": 73.37826955769631
        },
        "BLEX": {
          "precision": 77.8574031337301,
          "recall": 76.4711145575472,
          "f1": 77.15803253035615,
          "aligned_accuracy": 76.4711145575472
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "NL",
      "model": "stanza",
      "training_condition": "writtenandspokentrain",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "NL:writtentest",
      "gold_file": "am_benchmark/source/gold/nl_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/NL/stanza_writtenandspokentrain_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "ac1ec430faa1dbb3fe442aaa8ae03c156a39edca1b537240e3a90cbfd7815dd7",
      "prediction_sha256": "78f7ed73e75f240decd7e820f1a3837533450672a841d66ef00f26d6da5563e9",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 96.02157788267026,
          "recall": 96.02157788267026,
          "f1": 96.02157788267026,
          "aligned_accuracy": 96.02157788267026
        },
        "XPOS": {
          "precision": 94.69044229664594,
          "recall": 94.69044229664594,
          "f1": 94.69044229664594,
          "aligned_accuracy": 94.69044229664594
        },
        "UFeats": {
          "precision": 96.23635773332335,
          "recall": 96.23635773332335,
          "f1": 96.23635773332335,
          "aligned_accuracy": 96.23635773332335
        },
        "AllTags": {
          "precision": 93.7863689718039,
          "recall": 93.7863689718039,
          "f1": 93.7863689718039,
          "aligned_accuracy": 93.7863689718039
        },
        "Lemmas": {
          "precision": 96.1389575684923,
          "recall": 96.1389575684923,
          "f1": 96.1389575684923,
          "aligned_accuracy": 96.1389575684923
        },
        "UAS": {
          "precision": 89.08868409879874,
          "recall": 89.08868409879874,
          "f1": 89.08868409879874,
          "aligned_accuracy": 89.08868409879874
        },
        "LAS": {
          "precision": 85.56979096426163,
          "recall": 85.56979096426163,
          "f1": 85.56979096426163,
          "aligned_accuracy": 85.56979096426163
        },
        "CLAS": {
          "precision": 80.6564906119141,
          "recall": 79.5921087709944,
          "f1": 80.12076484401207,
          "aligned_accuracy": 79.5921087709944
        },
        "MLAS": {
          "precision": 74.29420505200595,
          "recall": 73.31378299120234,
          "f1": 73.80073800738008,
          "aligned_accuracy": 73.31378299120234
        },
        "BLEX": {
          "precision": 75.64951145931829,
          "recall": 74.65120412334488,
          "f1": 75.1470423795147,
          "aligned_accuracy": 74.65120412334488
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "NL",
      "model": "stanza",
      "training_condition": "writtentrain",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "NL:spokentest",
      "gold_file": "am_benchmark/source/gold/nl_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/NL/stanza_writtentrain_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "a930b004e6b1a8ae816ee661993e37dec3f8da3321375f5db96ddedbff5083f5",
      "prediction_sha256": "afe82bdd8f9ecd5083423aad3928b193e0cd5398033596dcd71bd262ffaccfe8",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 93.24841244417645,
          "recall": 93.24841244417645,
          "f1": 93.24841244417645,
          "aligned_accuracy": 93.24841244417645
        },
        "XPOS": {
          "precision": 92.00286419566979,
          "recall": 92.00286419566979,
          "f1": 92.00286419566979,
          "aligned_accuracy": 92.00286419566979
        },
        "UFeats": {
          "precision": 76.05193238990748,
          "recall": 76.05193238990748,
          "f1": 76.05193238990748,
          "aligned_accuracy": 76.05193238990748
        },
        "AllTags": {
          "precision": 73.3252934858392,
          "recall": 73.3252934858392,
          "f1": 73.3252934858392,
          "aligned_accuracy": 73.3252934858392
        },
        "Lemmas": {
          "precision": 96.38206862763572,
          "recall": 96.38206862763572,
          "f1": 96.38206862763572,
          "aligned_accuracy": 96.38206862763572
        },
        "UAS": {
          "precision": 76.57766304245416,
          "recall": 76.57766304245416,
          "f1": 76.57766304245416,
          "aligned_accuracy": 76.57766304245416
        },
        "LAS": {
          "precision": 70.54400874333415,
          "recall": 70.54400874333415,
          "f1": 70.54400874333415,
          "aligned_accuracy": 70.54400874333415
        },
        "CLAS": {
          "precision": 67.80216692165985,
          "recall": 64.76483044528617,
          "f1": 66.24870339862102,
          "aligned_accuracy": 64.76483044528617
        },
        "MLAS": {
          "precision": 44.11902457301652,
          "recall": 42.1426228041397,
          "f1": 43.108182317408016,
          "aligned_accuracy": 42.1426228041397
        },
        "BLEX": {
          "precision": 64.94832485090704,
          "recall": 62.03883205583226,
          "f1": 63.46024772713405,
          "aligned_accuracy": 62.03883205583226
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "NL",
      "model": "stanza",
      "training_condition": "writtentrain",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "NL:writtentest",
      "gold_file": "am_benchmark/source/gold/nl_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/NL/stanza_writtentrain_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "ac1ec430faa1dbb3fe442aaa8ae03c156a39edca1b537240e3a90cbfd7815dd7",
      "prediction_sha256": "d1301666d459aae5b14ea5835e144b9cb9c984b9627b2bca6b8058be97ffbfa1",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 96.518568467321,
          "recall": 96.518568467321,
          "f1": 96.518568467321,
          "aligned_accuracy": 96.518568467321
        },
        "XPOS": {
          "precision": 95.42718713318848,
          "recall": 95.42718713318848,
          "f1": 95.42718713318848,
          "aligned_accuracy": 95.42718713318848
        },
        "UFeats": {
          "precision": 96.61347119202817,
          "recall": 96.61347119202817,
          "f1": 96.61347119202817,
          "aligned_accuracy": 96.61347119202817
        },
        "AllTags": {
          "precision": 94.61551909292974,
          "recall": 94.61551909292974,
          "f1": 94.61551909292974,
          "aligned_accuracy": 94.61551909292974
        },
        "Lemmas": {
          "precision": 96.14894732898779,
          "recall": 96.14894732898779,
          "f1": 96.14894732898779,
          "aligned_accuracy": 96.14894732898779
        },
        "UAS": {
          "precision": 90.95427187133188,
          "recall": 90.95427187133188,
          "f1": 90.95427187133188,
          "aligned_accuracy": 90.95427187133188
        },
        "LAS": {
          "precision": 87.85245123748157,
          "recall": 87.85245123748157,
          "f1": 87.85245123748157,
          "aligned_accuracy": 87.85245123748157
        },
        "CLAS": {
          "precision": 83.27802690582959,
          "recall": 82.51577357149205,
          "f1": 82.89514797125385,
          "aligned_accuracy": 82.51577357149205
        },
        "MLAS": {
          "precision": 77.39910313901345,
          "recall": 76.69066026837288,
          "f1": 77.04325313574076,
          "aligned_accuracy": 76.69066026837288
        },
        "BLEX": {
          "precision": 78.01345291479821,
          "recall": 77.29938683017862,
          "f1": 77.65477837789582,
          "aligned_accuracy": 77.29938683017862
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "SL",
      "model": "spacy",
      "training_condition": "default",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "SL:spokentest",
      "gold_file": "am_benchmark/source/gold/sl_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/SL/spacy_default_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "7192fa2003550eb739d7aa3f38fc35fff5c1834829473fd66f9965b72b1e0354",
      "prediction_sha256": "63393faa27b90afcd5e70d7a48734b33dbb009b88ee55980091471cbe64c3be9",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 94.38084418421742,
          "recall": 94.38084418421742,
          "f1": 94.38084418421742,
          "aligned_accuracy": 94.38084418421742
        },
        "XPOS": {
          "precision": 92.82530804858867,
          "recall": 92.82530804858867,
          "f1": 92.82530804858867,
          "aligned_accuracy": 92.82530804858867
        },
        "UFeats": {
          "precision": 94.75661976754348,
          "recall": 94.75661976754348,
          "f1": 94.75661976754348,
          "aligned_accuracy": 94.75661976754348
        },
        "AllTags": {
          "precision": 92.1611465524775,
          "recall": 92.1611465524775,
          "f1": 92.1611465524775,
          "aligned_accuracy": 92.1611465524775
        },
        "Lemmas": {
          "precision": 97.51813335663725,
          "recall": 97.51813335663725,
          "f1": 97.51813335663725,
          "aligned_accuracy": 97.51813335663725
        },
        "UAS": {
          "precision": 79.05269597133618,
          "recall": 79.05269597133618,
          "f1": 79.05269597133618,
          "aligned_accuracy": 79.05269597133618
        },
        "LAS": {
          "precision": 71.5109674036529,
          "recall": 71.5109674036529,
          "f1": 71.5109674036529,
          "aligned_accuracy": 71.5109674036529
        },
        "CLAS": {
          "precision": 67.63136620856912,
          "recall": 62.959060806742926,
          "f1": 65.21162990100552,
          "aligned_accuracy": 62.959060806742926
        },
        "MLAS": {
          "precision": 63.18512530315279,
          "recall": 58.8199879590608,
          "f1": 60.92446800218255,
          "aligned_accuracy": 58.8199879590608
        },
        "BLEX": {
          "precision": 64.96362166531931,
          "recall": 60.47561709813365,
          "f1": 62.63933276171175,
          "aligned_accuracy": 60.47561709813365
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "SL",
      "model": "spacy",
      "training_condition": "default",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "SL:writtentest",
      "gold_file": "am_benchmark/source/gold/sl_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/SL/spacy_default_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "c14d5d2f4f20a7ad43e0f598a2e18c5e41f08364ab36be1c87d6d9eae7f5c8b0",
      "prediction_sha256": "74a2e3716f450b09a5e231d80281b422329264e8d273b178dabb3b138190b23d",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 99.15887115792783,
          "recall": 99.15887115792783,
          "f1": 99.15887115792783,
          "aligned_accuracy": 99.15887115792783
        },
        "XPOS": {
          "precision": 97.62204229227261,
          "recall": 97.62204229227261,
          "f1": 97.62204229227261,
          "aligned_accuracy": 97.62204229227261
        },
        "UFeats": {
          "precision": 97.80677619683988,
          "recall": 97.80677619683988,
          "f1": 97.80677619683988,
          "aligned_accuracy": 97.80677619683988
        },
        "AllTags": {
          "precision": 97.4176558446663,
          "recall": 97.4176558446663,
          "f1": 97.4176558446663,
          "aligned_accuracy": 97.4176558446663
        },
        "Lemmas": {
          "precision": 96.24243377092996,
          "recall": 96.24243377092996,
          "f1": 96.24243377092996,
          "aligned_accuracy": 96.24243377092996
        },
        "UAS": {
          "precision": 94.31648455310118,
          "recall": 94.31648455310118,
          "f1": 94.31648455310118,
          "aligned_accuracy": 94.31648455310118
        },
        "LAS": {
          "precision": 88.05518434085371,
          "recall": 88.05518434085371,
          "f1": 88.05518434085371,
          "aligned_accuracy": 88.05518434085371
        },
        "CLAS": {
          "precision": 90.34875444839857,
          "recall": 82.75637264489211,
          "f1": 86.38606281261697,
          "aligned_accuracy": 82.75637264489211
        },
        "MLAS": {
          "precision": 86.98932384341637,
          "recall": 79.67924897320555,
          "f1": 83.17397665793324,
          "aligned_accuracy": 79.67924897320555
        },
        "BLEX": {
          "precision": 85.61565836298932,
          "recall": 78.42101831931677,
          "f1": 81.86056007349688,
          "aligned_accuracy": 78.42101831931677
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "SL",
      "model": "spacy",
      "training_condition": "writtenandspokentrain",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "SL:spokentest",
      "gold_file": "am_benchmark/source/gold/sl_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/SL/spacy_writtenandspokentrain_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "7192fa2003550eb739d7aa3f38fc35fff5c1834829473fd66f9965b72b1e0354",
      "prediction_sha256": "d46527144344da7d0aa9beb1f5dc0cd3785a954f4d9789c1dc3d8b80a78e8e54",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 98.61050423839902,
          "recall": 98.61050423839902,
          "f1": 98.61050423839902,
          "aligned_accuracy": 98.61050423839902
        },
        "XPOS": {
          "precision": 97.15983570741939,
          "recall": 97.15983570741939,
          "f1": 97.15983570741939,
          "aligned_accuracy": 97.15983570741939
        },
        "UFeats": {
          "precision": 38.86218648955693,
          "recall": 38.86218648955693,
          "f1": 38.86218648955693,
          "aligned_accuracy": 38.86218648955693
        },
        "AllTags": {
          "precision": 38.74857991785371,
          "recall": 38.74857991785371,
          "f1": 38.74857991785371,
          "aligned_accuracy": 38.74857991785371
        },
        "Lemmas": {
          "precision": 98.72411081010225,
          "recall": 98.72411081010225,
          "f1": 98.72411081010225,
          "aligned_accuracy": 98.72411081010225
        },
        "UAS": {
          "precision": 86.271082758018,
          "recall": 86.271082758018,
          "f1": 86.271082758018,
          "aligned_accuracy": 86.271082758018
        },
        "LAS": {
          "precision": 83.34352879489644,
          "recall": 83.34352879489644,
          "f1": 83.34352879489644,
          "aligned_accuracy": 83.34352879489644
        },
        "CLAS": {
          "precision": 79.44896115627823,
          "recall": 79.42504515352198,
          "f1": 79.43700135480958,
          "aligned_accuracy": 79.42504515352198
        },
        "MLAS": {
          "precision": 15.447154471544716,
          "recall": 15.442504515352198,
          "f1": 15.444829143459279,
          "aligned_accuracy": 15.442504515352198
        },
        "BLEX": {
          "precision": 78.04878048780488,
          "recall": 78.02528597230584,
          "f1": 78.037031461689,
          "aligned_accuracy": 78.02528597230584
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "SL",
      "model": "spacy",
      "training_condition": "writtenandspokentrain",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "SL:writtentest",
      "gold_file": "am_benchmark/source/gold/sl_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/SL/spacy_writtenandspokentrain_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "c14d5d2f4f20a7ad43e0f598a2e18c5e41f08364ab36be1c87d6d9eae7f5c8b0",
      "prediction_sha256": "bbe6b065858498458fbee06811540cfa729d4d8256ad724ae6ee25535a2cdb84",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 98.80119487461677,
          "recall": 98.80119487461677,
          "f1": 98.80119487461677,
          "aligned_accuracy": 98.80119487461677
        },
        "XPOS": {
          "precision": 97.2447134659225,
          "recall": 97.2447134659225,
          "f1": 97.2447134659225,
          "aligned_accuracy": 97.2447134659225
        },
        "UFeats": {
          "precision": 24.66787202263973,
          "recall": 24.66787202263973,
          "f1": 24.66787202263973,
          "aligned_accuracy": 24.66787202263973
        },
        "AllTags": {
          "precision": 24.45562455781778,
          "recall": 24.45562455781778,
          "f1": 24.45562455781778,
          "aligned_accuracy": 24.45562455781778
        },
        "Lemmas": {
          "precision": 97.85787280874145,
          "recall": 97.85787280874145,
          "f1": 97.85787280874145,
          "aligned_accuracy": 97.85787280874145
        },
        "UAS": {
          "precision": 94.76063202578415,
          "recall": 94.76063202578415,
          "f1": 94.76063202578415,
          "aligned_accuracy": 94.76063202578415
        },
        "LAS": {
          "precision": 93.38102350444147,
          "recall": 93.38102350444147,
          "f1": 93.38102350444147,
          "aligned_accuracy": 93.38102350444147
        },
        "CLAS": {
          "precision": 91.29275588503056,
          "recall": 91.52487124323619,
          "f1": 91.40866621089299,
          "aligned_accuracy": 91.52487124323619
        },
        "MLAS": {
          "precision": 5.059175445441539,
          "recall": 5.072038594432493,
          "f1": 5.065598854054758,
          "aligned_accuracy": 5.072038594432493
        },
        "BLEX": {
          "precision": 88.54857588763169,
          "recall": 88.77371406219441,
          "f1": 88.66100205098154,
          "aligned_accuracy": 88.77371406219441
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "SL",
      "model": "spacy",
      "training_condition": "writtentrain",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "SL:spokentest",
      "gold_file": "am_benchmark/source/gold/sl_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/SL/spacy_writtentrain_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "7192fa2003550eb739d7aa3f38fc35fff5c1834829473fd66f9965b72b1e0354",
      "prediction_sha256": "998dda55e833ba2d896a3c8b0ebc959f9be931e57e11d99fffe159e5b6e109c7",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 91.4095953858254,
          "recall": 91.4095953858254,
          "f1": 91.4095953858254,
          "aligned_accuracy": 91.4095953858254
        },
        "XPOS": {
          "precision": 89.05881324827405,
          "recall": 89.05881324827405,
          "f1": 89.05881324827405,
          "aligned_accuracy": 89.05881324827405
        },
        "UFeats": {
          "precision": 38.86218648955693,
          "recall": 38.86218648955693,
          "f1": 38.86218648955693,
          "aligned_accuracy": 38.86218648955693
        },
        "AllTags": {
          "precision": 32.60508607882549,
          "recall": 32.60508607882549,
          "f1": 32.60508607882549,
          "aligned_accuracy": 32.60508607882549
        },
        "Lemmas": {
          "precision": 97.47443852136678,
          "recall": 97.47443852136678,
          "f1": 97.47443852136678,
          "aligned_accuracy": 97.47443852136678
        },
        "UAS": {
          "precision": 75.36485187450843,
          "recall": 75.36485187450843,
          "f1": 75.36485187450843,
          "aligned_accuracy": 75.36485187450843
        },
        "LAS": {
          "precision": 69.92047539980774,
          "recall": 69.92047539980774,
          "f1": 69.92047539980774,
          "aligned_accuracy": 69.92047539980774
        },
        "CLAS": {
          "precision": 65.36028390680451,
          "recall": 63.75677302829621,
          "f1": 64.54857142857144,
          "aligned_accuracy": 63.75677302829621
        },
        "MLAS": {
          "precision": 6.449621971917914,
          "recall": 6.291390728476822,
          "f1": 6.36952380952381,
          "aligned_accuracy": 6.291390728476822
        },
        "BLEX": {
          "precision": 63.277272025921924,
          "recall": 61.72486453943408,
          "f1": 62.49142857142858,
          "aligned_accuracy": 61.72486453943408
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "SL",
      "model": "spacy",
      "training_condition": "writtentrain",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "SL:writtentest",
      "gold_file": "am_benchmark/source/gold/sl_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/SL/spacy_writtentrain_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "c14d5d2f4f20a7ad43e0f598a2e18c5e41f08364ab36be1c87d6d9eae7f5c8b0",
      "prediction_sha256": "ff0dfda8ee31f952642d6e95ab761878fdfb0bb169273ab8d98370978d272712",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 98.87587453816525,
          "recall": 98.87587453816525,
          "f1": 98.87587453816525,
          "aligned_accuracy": 98.87587453816525
        },
        "XPOS": {
          "precision": 97.29974058643188,
          "recall": 97.29974058643188,
          "f1": 97.29974058643188,
          "aligned_accuracy": 97.29974058643188
        },
        "UFeats": {
          "precision": 24.66787202263973,
          "recall": 24.66787202263973,
          "f1": 24.66787202263973,
          "aligned_accuracy": 24.66787202263973
        },
        "AllTags": {
          "precision": 24.53423472997406,
          "recall": 24.53423472997406,
          "f1": 24.53423472997406,
          "aligned_accuracy": 24.53423472997406
        },
        "Lemmas": {
          "precision": 97.83822026570238,
          "recall": 97.83822026570238,
          "f1": 97.83822026570238,
          "aligned_accuracy": 97.83822026570238
        },
        "UAS": {
          "precision": 94.84710321515604,
          "recall": 94.84710321515604,
          "f1": 94.84710321515604,
          "aligned_accuracy": 94.84710321515604
        },
        "LAS": {
          "precision": 93.40067604748054,
          "recall": 93.40067604748054,
          "f1": 93.40067604748054,
          "aligned_accuracy": 93.40067604748054
        },
        "CLAS": {
          "precision": 91.37201276290942,
          "recall": 91.47923593454593,
          "f1": 91.42559291112849,
          "aligned_accuracy": 91.47923593454593
        },
        "MLAS": {
          "precision": 5.033535195676239,
          "recall": 5.039441945368016,
          "f1": 5.0364868386760495,
          "aligned_accuracy": 5.039441945368016
        },
        "BLEX": {
          "precision": 88.61105684704043,
          "recall": 88.71504009387834,
          "f1": 88.66301798279906,
          "aligned_accuracy": 88.71504009387834
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "SL",
      "model": "stanza",
      "training_condition": "default",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "SL:spokentest",
      "gold_file": "am_benchmark/source/gold/sl_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/SL/stanza_default_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "7192fa2003550eb739d7aa3f38fc35fff5c1834829473fd66f9965b72b1e0354",
      "prediction_sha256": "7db1eca3d1b9ea74b578a0bc9ec17f7cf71271bef14421a93f65444483f6ee1a",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 95.28969675784322,
          "recall": 95.28969675784322,
          "f1": 95.28969675784322,
          "aligned_accuracy": 95.28969675784322
        },
        "XPOS": {
          "precision": 93.87398409507996,
          "recall": 93.87398409507996,
          "f1": 93.87398409507996,
          "aligned_accuracy": 93.87398409507996
        },
        "UFeats": {
          "precision": 94.5731014594075,
          "recall": 94.5731014594075,
          "f1": 94.5731014594075,
          "aligned_accuracy": 94.5731014594075
        },
        "AllTags": {
          "precision": 93.2098225989688,
          "recall": 93.2098225989688,
          "f1": 93.2098225989688,
          "aligned_accuracy": 93.2098225989688
        },
        "Lemmas": {
          "precision": 98.35707419383029,
          "recall": 98.35707419383029,
          "f1": 98.35707419383029,
          "aligned_accuracy": 98.35707419383029
        },
        "UAS": {
          "precision": 82.24241894608058,
          "recall": 82.24241894608058,
          "f1": 82.24241894608058,
          "aligned_accuracy": 82.24241894608058
        },
        "LAS": {
          "precision": 78.32736170584637,
          "recall": 78.32736170584637,
          "f1": 78.32736170584637,
          "aligned_accuracy": 78.32736170584637
        },
        "CLAS": {
          "precision": 73.93357708714198,
          "recall": 73.04334738109573,
          "f1": 73.48576620230163,
          "aligned_accuracy": 73.04334738109573
        },
        "MLAS": {
          "precision": 68.9061547836685,
          "recall": 68.07645996387718,
          "f1": 68.48879466989703,
          "aligned_accuracy": 68.07645996387718
        },
        "BLEX": {
          "precision": 72.05971968312005,
          "recall": 71.19205298013244,
          "f1": 71.62325863113264,
          "aligned_accuracy": 71.19205298013244
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "SL",
      "model": "stanza",
      "training_condition": "default",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "SL:writtentest",
      "gold_file": "am_benchmark/source/gold/sl_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/SL/stanza_default_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "c14d5d2f4f20a7ad43e0f598a2e18c5e41f08364ab36be1c87d6d9eae7f5c8b0",
      "prediction_sha256": "d295a00a790e85e8980a0182f1bfa2551a3fe14e94a5c502defcd124e9ca7640",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 99.02523386526217,
          "recall": 99.02523386526217,
          "f1": 99.02523386526217,
          "aligned_accuracy": 99.02523386526217
        },
        "XPOS": {
          "precision": 98.01116264444619,
          "recall": 98.01116264444619,
          "f1": 98.01116264444619,
          "aligned_accuracy": 98.01116264444619
        },
        "UFeats": {
          "precision": 98.15659146293531,
          "recall": 98.15659146293531,
          "f1": 98.15659146293531,
          "aligned_accuracy": 98.15659146293531
        },
        "AllTags": {
          "precision": 97.7596100935461,
          "recall": 97.7596100935461,
          "f1": 97.7596100935461,
          "aligned_accuracy": 97.7596100935461
        },
        "Lemmas": {
          "precision": 97.88931687760396,
          "recall": 97.88931687760396,
          "f1": 97.88931687760396,
          "aligned_accuracy": 97.88931687760396
        },
        "UAS": {
          "precision": 96.21492021067526,
          "recall": 96.21492021067526,
          "f1": 96.21492021067526,
          "aligned_accuracy": 96.21492021067526
        },
        "LAS": {
          "precision": 95.04362864554673,
          "recall": 95.04362864554673,
          "f1": 95.04362864554673,
          "aligned_accuracy": 95.04362864554673
        },
        "CLAS": {
          "precision": 93.57594730320224,
          "recall": 93.53934415542082,
          "f1": 93.55764214919145,
          "aligned_accuracy": 93.53934415542082
        },
        "MLAS": {
          "precision": 90.91501989173678,
          "recall": 90.87945759175958,
          "f1": 90.89723526343245,
          "aligned_accuracy": 90.87945759175958
        },
        "BLEX": {
          "precision": 90.5954477271245,
          "recall": 90.56001043092769,
          "f1": 90.57772561293687,
          "aligned_accuracy": 90.56001043092769
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "SL",
      "model": "stanza",
      "training_condition": "writtenandspokentrain",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "SL:spokentest",
      "gold_file": "am_benchmark/source/gold/sl_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/SL/stanza_writtenandspokentrain_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "7192fa2003550eb739d7aa3f38fc35fff5c1834829473fd66f9965b72b1e0354",
      "prediction_sha256": "1907b52b5cdde7fc661300f0c928269298b50eb8e927328685a409a8d33863d6",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 97.71039063182731,
          "recall": 97.71039063182731,
          "f1": 97.71039063182731,
          "aligned_accuracy": 97.71039063182731
        },
        "XPOS": {
          "precision": 95.56934370357423,
          "recall": 95.56934370357423,
          "f1": 95.56934370357423,
          "aligned_accuracy": 95.56934370357423
        },
        "UFeats": {
          "precision": 95.68295027527746,
          "recall": 95.68295027527746,
          "f1": 95.68295027527746,
          "aligned_accuracy": 95.68295027527746
        },
        "AllTags": {
          "precision": 94.54688455824521,
          "recall": 94.54688455824521,
          "f1": 94.54688455824521,
          "aligned_accuracy": 94.54688455824521
        },
        "Lemmas": {
          "precision": 98.39203006204667,
          "recall": 98.39203006204667,
          "f1": 98.39203006204667,
          "aligned_accuracy": 98.39203006204667
        },
        "UAS": {
          "precision": 83.72804334527659,
          "recall": 83.72804334527659,
          "f1": 83.72804334527659,
          "aligned_accuracy": 83.72804334527659
        },
        "LAS": {
          "precision": 80.59075417285678,
          "recall": 80.59075417285678,
          "f1": 80.59075417285678,
          "aligned_accuracy": 80.59075417285678
        },
        "CLAS": {
          "precision": 76.5798690421806,
          "recall": 75.69235400361228,
          "f1": 76.13352509272576,
          "aligned_accuracy": 75.69235400361228
        },
        "MLAS": {
          "precision": 70.74767778285366,
          "recall": 69.92775436484045,
          "f1": 70.3353266217546,
          "aligned_accuracy": 69.92775436484045
        },
        "BLEX": {
          "precision": 75.11801431399421,
          "recall": 74.24744130042143,
          "f1": 74.68019075013247,
          "aligned_accuracy": 74.24744130042143
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "SL",
      "model": "stanza",
      "training_condition": "writtenandspokentrain",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "SL:writtentest",
      "gold_file": "am_benchmark/source/gold/sl_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/SL/stanza_writtenandspokentrain_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "c14d5d2f4f20a7ad43e0f598a2e18c5e41f08364ab36be1c87d6d9eae7f5c8b0",
      "prediction_sha256": "b67903261d58f59f200fe89452b1b0b83e18e8f0037907bfc0c5b3a920d1e756",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 98.05046773052433,
          "recall": 98.05046773052433,
          "f1": 98.05046773052433,
          "aligned_accuracy": 98.05046773052433
        },
        "XPOS": {
          "precision": 95.11044729187958,
          "recall": 95.11044729187958,
          "f1": 95.11044729187958,
          "aligned_accuracy": 95.11044729187958
        },
        "UFeats": {
          "precision": 95.35806933417184,
          "recall": 95.35806933417184,
          "f1": 95.35806933417184,
          "aligned_accuracy": 95.35806933417184
        },
        "AllTags": {
          "precision": 94.46191337159028,
          "recall": 94.46191337159028,
          "f1": 94.46191337159028,
          "aligned_accuracy": 94.46191337159028
        },
        "Lemmas": {
          "precision": 97.77926263658517,
          "recall": 97.77926263658517,
          "f1": 97.77926263658517,
          "aligned_accuracy": 97.77926263658517
        },
        "UAS": {
          "precision": 91.57692005345491,
          "recall": 91.57692005345491,
          "f1": 91.57692005345491,
          "aligned_accuracy": 91.57692005345491
        },
        "LAS": {
          "precision": 89.50947252574483,
          "recall": 89.50947252574483,
          "f1": 89.50947252574483,
          "aligned_accuracy": 89.50947252574483
        },
        "CLAS": {
          "precision": 86.70708651150662,
          "recall": 86.70708651150662,
          "f1": 86.70708651150662,
          "aligned_accuracy": 86.70708651150662
        },
        "MLAS": {
          "precision": 81.04178890410066,
          "recall": 81.04178890410066,
          "f1": 81.04178890410066,
          "aligned_accuracy": 81.04178890410066
        },
        "BLEX": {
          "precision": 84.22974118260643,
          "recall": 84.22974118260643,
          "f1": 84.22974118260643,
          "aligned_accuracy": 84.22974118260643
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "SL",
      "model": "stanza",
      "training_condition": "writtentrain",
      "test_condition": "spokentest",
      "source_test_condition": "spokentest",
      "gold_cohort": "SL:spokentest",
      "gold_file": "am_benchmark/source/gold/sl_gold_test_spoken_final_clean.conllu",
      "prediction_file": "am_benchmark/source/SL/stanza_writtentrain_spokentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "7192fa2003550eb739d7aa3f38fc35fff5c1834829473fd66f9965b72b1e0354",
      "prediction_sha256": "0b71a162219a1f69e377a85393eb3f5c4acd47a337879b8cfa8da8557f80b870",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 92.01258411255789,
          "recall": 92.01258411255789,
          "f1": 92.01258411255789,
          "aligned_accuracy": 92.01258411255789
        },
        "XPOS": {
          "precision": 89.18989775408546,
          "recall": 89.18989775408546,
          "f1": 89.18989775408546,
          "aligned_accuracy": 89.18989775408546
        },
        "UFeats": {
          "precision": 89.61810713973608,
          "recall": 89.61810713973608,
          "f1": 89.61810713973608,
          "aligned_accuracy": 89.61810713973608
        },
        "AllTags": {
          "precision": 88.14122170759417,
          "recall": 88.14122170759417,
          "f1": 88.14122170759417,
          "aligned_accuracy": 88.14122170759417
        },
        "Lemmas": {
          "precision": 97.5967840601241,
          "recall": 97.5967840601241,
          "f1": 97.5967840601241,
          "aligned_accuracy": 97.5967840601241
        },
        "UAS": {
          "precision": 72.8655072970375,
          "recall": 72.8655072970375,
          "f1": 72.8655072970375,
          "aligned_accuracy": 72.8655072970375
        },
        "LAS": {
          "precision": 67.56095429520231,
          "recall": 67.56095429520231,
          "f1": 67.56095429520231,
          "aligned_accuracy": 67.56095429520231
        },
        "CLAS": {
          "precision": 62.003637465898755,
          "recall": 61.57435279951836,
          "f1": 61.78824950913759,
          "aligned_accuracy": 61.57435279951836
        },
        "MLAS": {
          "precision": 56.19884813579873,
          "recall": 55.80975316074653,
          "f1": 56.00362483008608,
          "aligned_accuracy": 55.80975316074653
        },
        "BLEX": {
          "precision": 60.63958775386481,
          "recall": 60.219747140276944,
          "f1": 60.428938226853944,
          "aligned_accuracy": 60.219747140276944
        }
      }
    },
    {
      "result_scope": "BENCHMARK EVALUATION",
      "gold_provenance_notice": "AUTHORITATIVE GOLD CONFIRMED",
      "benchmark_use_notice": "",
      "language": "SL",
      "model": "stanza",
      "training_condition": "writtentrain",
      "test_condition": "writtentest",
      "source_test_condition": "writtentest",
      "gold_cohort": "SL:writtentest",
      "gold_file": "am_benchmark/source/gold/sl_gold_test_written_final_clean.conllu",
      "prediction_file": "am_benchmark/source/SL/stanza_writtentrain_writtentest_clean.conllu",
      "gold_status": "AUTHORITATIVE",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "c14d5d2f4f20a7ad43e0f598a2e18c5e41f08364ab36be1c87d6d9eae7f5c8b0",
      "prediction_sha256": "c4712d50b040d67a08cd85d7cf3bc8a39e224ce1b352e05573ea2624e518b568",
      "error_message": "",
      "metrics": {
        "Tokens": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Sentences": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "Words": {
          "precision": 100,
          "recall": 100,
          "f1": 100,
          "aligned_accuracy": null
        },
        "UPOS": {
          "precision": 98.17231349736656,
          "recall": 98.17231349736656,
          "f1": 98.17231349736656,
          "aligned_accuracy": 98.17231349736656
        },
        "XPOS": {
          "precision": 95.13796085213426,
          "recall": 95.13796085213426,
          "f1": 95.13796085213426,
          "aligned_accuracy": 95.13796085213426
        },
        "UFeats": {
          "precision": 95.51135916987658,
          "recall": 95.51135916987658,
          "f1": 95.51135916987658,
          "aligned_accuracy": 95.51135916987658
        },
        "AllTags": {
          "precision": 94.52873201792312,
          "recall": 94.52873201792312,
          "f1": 94.52873201792312,
          "aligned_accuracy": 94.52873201792312
        },
        "Lemmas": {
          "precision": 97.62990330948826,
          "recall": 97.62990330948826,
          "f1": 97.62990330948826,
          "aligned_accuracy": 97.62990330948826
        },
        "UAS": {
          "precision": 91.86384718182534,
          "recall": 91.86384718182534,
          "f1": 91.86384718182534,
          "aligned_accuracy": 91.86384718182534
        },
        "LAS": {
          "precision": 89.88680135209496,
          "recall": 89.88680135209496,
          "f1": 89.88680135209496,
          "aligned_accuracy": 89.88680135209496
        },
        "CLAS": {
          "precision": 87.20104268491366,
          "recall": 87.23515222635113,
          "f1": 87.21809412071437,
          "aligned_accuracy": 87.23515222635113
        },
        "MLAS": {
          "precision": 81.75953079178886,
          "recall": 81.79151183258361,
          "f1": 81.77551818537349,
          "aligned_accuracy": 81.79151183258361
        },
        "BLEX": {
          "precision": 84.47051156728575,
          "recall": 84.50355303474802,
          "f1": 84.48702907052535,
          "aligned_accuracy": 84.50355303474802
        }
      }
    }
  ]
};
