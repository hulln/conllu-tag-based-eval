window.AM_BENCHMARK_RESULTS = {
  "schema_version": 1,
  "source": {
    "path": "reports/smoke_test/sl_spacy_stanza_results.tsv",
    "sha256": "53941f923b3d7dd060825604df8b39f7dbcca670a1d8430c98ff9d90d6a514c4",
    "row_count": 12
  },
  "dimensions": {
    "language": [
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
      "result_scope": "PROVISIONAL ENGINEERING SMOKE TEST",
      "gold_provenance_notice": "GOLD PROVENANCE NOT YET CONFIRMED",
      "benchmark_use_notice": "DO NOT TREAT AS BENCHMARK RESULT",
      "language": "SL",
      "model": "spacy",
      "training_condition": "default",
      "test_condition": "spokentest",
      "gold_cohort": "SL:spokentest",
      "gold_file": "data/gold/sl_sst-ud-test.conllu",
      "prediction_file": "am_benchmark/source/SL/spacy_default_spokentest_clean.conllu",
      "gold_status": "CANDIDATE — NEEDS PROVENANCE CONFIRMATION",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "6824234edf98cbbedb2e981644c324a3058c2920ed6cdcd7f467e835cfe25eeb",
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
      "result_scope": "PROVISIONAL ENGINEERING SMOKE TEST",
      "gold_provenance_notice": "GOLD PROVENANCE NOT YET CONFIRMED",
      "benchmark_use_notice": "DO NOT TREAT AS BENCHMARK RESULT",
      "language": "SL",
      "model": "spacy",
      "training_condition": "default",
      "test_condition": "writtentest",
      "gold_cohort": "SL:writtentest",
      "gold_file": "data/gold/sl_ssj-ud-test.conllu",
      "prediction_file": "am_benchmark/source/SL/spacy_default_writtentest_clean.conllu",
      "gold_status": "CANDIDATE — NEEDS PROVENANCE CONFIRMATION",
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
      "result_scope": "PROVISIONAL ENGINEERING SMOKE TEST",
      "gold_provenance_notice": "GOLD PROVENANCE NOT YET CONFIRMED",
      "benchmark_use_notice": "DO NOT TREAT AS BENCHMARK RESULT",
      "language": "SL",
      "model": "spacy",
      "training_condition": "writtenandspokentrain",
      "test_condition": "spokentest",
      "gold_cohort": "SL:spokentest",
      "gold_file": "data/gold/sl_sst-ud-test.conllu",
      "prediction_file": "am_benchmark/source/SL/spacy_writtenandspokentrain_spokentest_clean.conllu",
      "gold_status": "CANDIDATE — NEEDS PROVENANCE CONFIRMATION",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "6824234edf98cbbedb2e981644c324a3058c2920ed6cdcd7f467e835cfe25eeb",
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
      "result_scope": "PROVISIONAL ENGINEERING SMOKE TEST",
      "gold_provenance_notice": "GOLD PROVENANCE NOT YET CONFIRMED",
      "benchmark_use_notice": "DO NOT TREAT AS BENCHMARK RESULT",
      "language": "SL",
      "model": "spacy",
      "training_condition": "writtenandspokentrain",
      "test_condition": "writtentest",
      "gold_cohort": "SL:writtentest",
      "gold_file": "data/gold/sl_ssj-ud-test.conllu",
      "prediction_file": "am_benchmark/source/SL/spacy_writtenandspokentrain_writtentest_clean.conllu",
      "gold_status": "CANDIDATE — NEEDS PROVENANCE CONFIRMATION",
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
      "result_scope": "PROVISIONAL ENGINEERING SMOKE TEST",
      "gold_provenance_notice": "GOLD PROVENANCE NOT YET CONFIRMED",
      "benchmark_use_notice": "DO NOT TREAT AS BENCHMARK RESULT",
      "language": "SL",
      "model": "spacy",
      "training_condition": "writtentrain",
      "test_condition": "spokentest",
      "gold_cohort": "SL:spokentest",
      "gold_file": "data/gold/sl_sst-ud-test.conllu",
      "prediction_file": "am_benchmark/source/SL/spacy_writtentrain_spokentest_clean.conllu",
      "gold_status": "CANDIDATE — NEEDS PROVENANCE CONFIRMATION",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "6824234edf98cbbedb2e981644c324a3058c2920ed6cdcd7f467e835cfe25eeb",
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
      "result_scope": "PROVISIONAL ENGINEERING SMOKE TEST",
      "gold_provenance_notice": "GOLD PROVENANCE NOT YET CONFIRMED",
      "benchmark_use_notice": "DO NOT TREAT AS BENCHMARK RESULT",
      "language": "SL",
      "model": "spacy",
      "training_condition": "writtentrain",
      "test_condition": "writtentest",
      "gold_cohort": "SL:writtentest",
      "gold_file": "data/gold/sl_ssj-ud-test.conllu",
      "prediction_file": "am_benchmark/source/SL/spacy_writtentrain_writtentest_clean.conllu",
      "gold_status": "CANDIDATE — NEEDS PROVENANCE CONFIRMATION",
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
      "result_scope": "PROVISIONAL ENGINEERING SMOKE TEST",
      "gold_provenance_notice": "GOLD PROVENANCE NOT YET CONFIRMED",
      "benchmark_use_notice": "DO NOT TREAT AS BENCHMARK RESULT",
      "language": "SL",
      "model": "stanza",
      "training_condition": "default",
      "test_condition": "spokentest",
      "gold_cohort": "SL:spokentest",
      "gold_file": "data/gold/sl_sst-ud-test.conllu",
      "prediction_file": "am_benchmark/source/SL/stanza_default_spokentest_clean.conllu",
      "gold_status": "CANDIDATE — NEEDS PROVENANCE CONFIRMATION",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "6824234edf98cbbedb2e981644c324a3058c2920ed6cdcd7f467e835cfe25eeb",
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
      "result_scope": "PROVISIONAL ENGINEERING SMOKE TEST",
      "gold_provenance_notice": "GOLD PROVENANCE NOT YET CONFIRMED",
      "benchmark_use_notice": "DO NOT TREAT AS BENCHMARK RESULT",
      "language": "SL",
      "model": "stanza",
      "training_condition": "default",
      "test_condition": "writtentest",
      "gold_cohort": "SL:writtentest",
      "gold_file": "data/gold/sl_ssj-ud-test.conllu",
      "prediction_file": "am_benchmark/source/SL/stanza_default_writtentest_clean.conllu",
      "gold_status": "CANDIDATE — NEEDS PROVENANCE CONFIRMATION",
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
      "result_scope": "PROVISIONAL ENGINEERING SMOKE TEST",
      "gold_provenance_notice": "GOLD PROVENANCE NOT YET CONFIRMED",
      "benchmark_use_notice": "DO NOT TREAT AS BENCHMARK RESULT",
      "language": "SL",
      "model": "stanza",
      "training_condition": "writtenandspokentrain",
      "test_condition": "spokentest",
      "gold_cohort": "SL:spokentest",
      "gold_file": "data/gold/sl_sst-ud-test.conllu",
      "prediction_file": "am_benchmark/source/SL/stanza_writtenandspokentrain_spokentest_clean.conllu",
      "gold_status": "CANDIDATE — NEEDS PROVENANCE CONFIRMATION",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "6824234edf98cbbedb2e981644c324a3058c2920ed6cdcd7f467e835cfe25eeb",
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
      "result_scope": "PROVISIONAL ENGINEERING SMOKE TEST",
      "gold_provenance_notice": "GOLD PROVENANCE NOT YET CONFIRMED",
      "benchmark_use_notice": "DO NOT TREAT AS BENCHMARK RESULT",
      "language": "SL",
      "model": "stanza",
      "training_condition": "writtenandspokentrain",
      "test_condition": "writtentest",
      "gold_cohort": "SL:writtentest",
      "gold_file": "data/gold/sl_ssj-ud-test.conllu",
      "prediction_file": "am_benchmark/source/SL/stanza_writtenandspokentrain_writtentest_clean.conllu",
      "gold_status": "CANDIDATE — NEEDS PROVENANCE CONFIRMATION",
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
      "result_scope": "PROVISIONAL ENGINEERING SMOKE TEST",
      "gold_provenance_notice": "GOLD PROVENANCE NOT YET CONFIRMED",
      "benchmark_use_notice": "DO NOT TREAT AS BENCHMARK RESULT",
      "language": "SL",
      "model": "stanza",
      "training_condition": "writtentrain",
      "test_condition": "spokentest",
      "gold_cohort": "SL:spokentest",
      "gold_file": "data/gold/sl_sst-ud-test.conllu",
      "prediction_file": "am_benchmark/source/SL/stanza_writtentrain_spokentest_clean.conllu",
      "gold_status": "CANDIDATE — NEEDS PROVENANCE CONFIRMATION",
      "result_status": "success",
      "repeat_deterministic": "true",
      "evaluator_file": "scripts/conll18_ud_eval_tag-based.py",
      "evaluator_sha256": "e7eb23ce69747e5c9176f55fffe47dcddc8c1774c9703c1f2f16e6848f96fa95",
      "gold_sha256": "6824234edf98cbbedb2e981644c324a3058c2920ed6cdcd7f467e835cfe25eeb",
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
      "result_scope": "PROVISIONAL ENGINEERING SMOKE TEST",
      "gold_provenance_notice": "GOLD PROVENANCE NOT YET CONFIRMED",
      "benchmark_use_notice": "DO NOT TREAT AS BENCHMARK RESULT",
      "language": "SL",
      "model": "stanza",
      "training_condition": "writtentrain",
      "test_condition": "writtentest",
      "gold_cohort": "SL:writtentest",
      "gold_file": "data/gold/sl_ssj-ud-test.conllu",
      "prediction_file": "am_benchmark/source/SL/stanza_writtentrain_writtentest_clean.conllu",
      "gold_status": "CANDIDATE — NEEDS PROVENANCE CONFIRMATION",
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
