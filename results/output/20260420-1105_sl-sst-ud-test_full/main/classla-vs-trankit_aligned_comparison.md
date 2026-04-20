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
- Trankit aligned correct, CLASSLA aligned wrong: 956 (8.35%)
- Trankit aligned wrong, CLASSLA aligned correct: 427 (3.73%)
- Both correct: 8965 (78.34%)
- Both wrong: 1095 (9.57%)

## UAS exact differences
- Trankit aligned correct, CLASSLA aligned wrong: 853 (7.45%)
- Trankit aligned wrong, CLASSLA aligned correct: 417 (3.64%)
- Both correct: 9337 (81.60%)
- Both wrong: 836 (7.31%)

## DEPREL exact differences
- Trankit aligned correct, CLASSLA aligned wrong: 499 (4.36%)
- Trankit aligned wrong, CLASSLA aligned correct: 188 (1.64%)
- Both correct: 10297 (89.99%)
- Both wrong: 459 (4.01%)

## Top LAS mistakes where Trankit aligned wins
gold_deprel	pred_deprel	count
punct	punct	146
advmod	advmod	71
discourse	discourse	62
conj	conj	35
cc	cc	34
parataxis	parataxis	29
obl	nmod	20
mark	mark	19
nmod	obl	18
obl	obl	15
nsubj	nsubj	15
advcl	advcl	13
nsubj	root	12
obj	obj	11
acl	acl	11
case	case	10
orphan	advmod	9
iobj	obj	9
obj	nsubj	9
aux	aux	9

## Top LAS mistakes where Trankit aligned loses to CLASSLA aligned
gold_deprel	pred_deprel	count
punct	punct	99
discourse	discourse	48
advmod	advmod	26
conj	conj	26
reparandum	reparandum	16
parataxis	parataxis	12
cc	cc	12
obl	obl	12
nmod	obl	7
reparandum	orphan	6
obl	nmod	5
mark	mark	5
cop	parataxis	5
root	parataxis	4
case	case	4
orphan	advmod	4
obj	iobj	4
nsubj	obj	3
nsubj	nsubj	3
parataxis	conj	3

## Top DEPREL mistakes where Trankit aligned wins
gold_deprel	pred_deprel	count
obl	nmod	20
nmod	obl	19
nsubj	root	15
conj	parataxis	13
appos	conj	11
conj	obl	10
orphan	advmod	9
iobj	obj	9
obj	nsubj	9
nsubj	parataxis	8
parataxis	conj	7
nummod	det	7
root	nsubj	7
advcl	acl	6
cc	advmod	6
root	cop	6
advmod	orphan	6
root	parataxis	6
acl	advcl	6
nsubj	conj	6

## Top DEPREL mistakes where Trankit aligned loses to CLASSLA aligned
gold_deprel	pred_deprel	count
parataxis	conj	9
reparandum	orphan	7
nmod	obl	7
cop	parataxis	6
obl	nmod	5
nsubj	obj	4
root	parataxis	4
orphan	advmod	4
obj	iobj	4
parataxis	nsubj	4
conj	parataxis	3
parataxis	root	3
cc	reparandum	3
conj	appos	3
obj	nmod	3
appos	conj	3
cop	root	3
fixed	advmod	3
advmod	cc	3
root	obl	3
