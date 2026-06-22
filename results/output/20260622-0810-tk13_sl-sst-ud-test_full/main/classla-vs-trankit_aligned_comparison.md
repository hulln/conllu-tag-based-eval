# Trankit aligned vs CLASSLA aligned (exact difference report)

## Coverage
- Gold sentences: 432
- Trankit aligned predicted sentences: 432
- CLASSLA aligned predicted sentences: 432
- Gold sentences paired with both models: 432
- Unmatched gold for Trankit aligned: 0
- Unmatched gold for CLASSLA aligned: 0
- Unmatched predicted for Trankit aligned: 0
- Unmatched predicted for CLASSLA aligned: 0
- Skipped sentence pairs (token count mismatch): 0
- Compared tokens (FORM-aligned): 11443
- Skipped tokens (FORM mismatch): 0

## LAS exact differences
- Trankit aligned correct, CLASSLA aligned wrong: 975 (8.52%)
- Trankit aligned wrong, CLASSLA aligned correct: 428 (3.74%)
- Both correct: 8964 (78.34%)
- Both wrong: 1076 (9.40%)

## UAS exact differences
- Trankit aligned correct, CLASSLA aligned wrong: 853 (7.45%)
- Trankit aligned wrong, CLASSLA aligned correct: 400 (3.50%)
- Both correct: 9354 (81.74%)
- Both wrong: 836 (7.31%)

## DEPREL exact differences
- Trankit aligned correct, CLASSLA aligned wrong: 506 (4.42%)
- Trankit aligned wrong, CLASSLA aligned correct: 193 (1.69%)
- Both correct: 10292 (89.94%)
- Both wrong: 452 (3.95%)

## Top LAS mistakes where Trankit aligned wins
gold_deprel	pred_deprel	count
punct	punct	153
advmod	advmod	75
discourse	discourse	63
conj	conj	43
cc	cc	33
parataxis	parataxis	27
obl	nmod	21
nmod	obl	18
mark	mark	16
appos	conj	14
nsubj	root	13
obl	obl	12
nsubj	nsubj	12
acl	acl	12
advcl	advcl	12
case	case	10
obj	obj	10
orphan	advmod	9
obj	nsubj	9
nmod	nmod	9

## Top LAS mistakes where Trankit aligned loses to CLASSLA aligned
gold_deprel	pred_deprel	count
punct	punct	91
discourse	discourse	51
advmod	advmod	27
conj	conj	27
reparandum	reparandum	13
parataxis	parataxis	12
cc	cc	10
obl	obl	9
nmod	obl	7
nsubj	nsubj	6
mark	mark	6
obl	nmod	5
cop	parataxis	5
orphan	advmod	4
obj	nsubj	4
cop	cop	4
fixed	advmod	4
root	parataxis	3
cc	advmod	3
reparandum	orphan	3

## Top DEPREL mistakes where Trankit aligned wins
gold_deprel	pred_deprel	count
obl	nmod	21
nmod	obl	19
nsubj	root	15
appos	conj	15
conj	obl	10
orphan	advmod	9
obj	nsubj	9
iobj	obj	8
parataxis	root	8
nummod	det	8
root	nsubj	8
conj	parataxis	8
parataxis	conj	7
root	parataxis	7
advmod	cc	7
root	cop	6
reparandum	case	6
acl	advcl	6
nsubj	conj	6
obj	iobj	5

## Top DEPREL mistakes where Trankit aligned loses to CLASSLA aligned
gold_deprel	pred_deprel	count
parataxis	conj	7
nmod	obl	7
parataxis	acl	6
obl	nmod	5
cop	parataxis	5
appos	conj	4
conj	parataxis	4
orphan	advmod	4
obj	nsubj	4
parataxis	nsubj	4
fixed	advmod	4
root	parataxis	3
cc	advmod	3
reparandum	orphan	3
orphan	reparandum	3
advmod	discourse	3
cc	discourse	3
advmod	orphan	3
conj	appos	3
root	obl	3
