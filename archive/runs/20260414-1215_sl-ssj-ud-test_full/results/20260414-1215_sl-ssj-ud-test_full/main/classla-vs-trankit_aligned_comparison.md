# CLASSLA aligned vs Trankit aligned (exact difference report)

## Coverage
- Gold sentences: 1282
- CLASSLA aligned predicted sentences: 1282
- Trankit aligned predicted sentences: 1282
- Gold sentences paired with both models: 1282
- Unmatched gold for CLASSLA aligned: 0
- Unmatched gold for Trankit aligned: 0
- Unmatched predicted for CLASSLA aligned: 0
- Unmatched predicted for Trankit aligned: 0
- Skipped sentence pairs (token count mismatch): 0
- Compared tokens (FORM-aligned): 25442
- Skipped tokens (FORM mismatch): 0

## LAS exact differences
- CLASSLA aligned correct, Trankit aligned wrong: 1195 (4.70%)
- Trankit aligned correct, CLASSLA aligned wrong: 1345 (5.29%)
- Both correct: 21826 (85.79%)
- Both wrong: 1076 (4.23%)

## UAS exact differences
- CLASSLA aligned correct, Trankit aligned wrong: 970 (3.81%)
- Trankit aligned correct, CLASSLA aligned wrong: 1190 (4.68%)
- Both correct: 22467 (88.31%)
- Both wrong: 815 (3.20%)

## DEPREL exact differences
- CLASSLA aligned correct, Trankit aligned wrong: 636 (2.50%)
- Trankit aligned correct, CLASSLA aligned wrong: 739 (2.90%)
- Both correct: 23587 (92.71%)
- Both wrong: 480 (1.89%)

## Top LAS mistakes where CLASSLA aligned wins
gold_deprel	pred_deprel	count
advmod	advmod	271
punct	punct	171
iobj	obj	45
nmod	obl	43
conj	conj	40
orphan	advmod	35
obl	obl	23
nmod	nmod	23
obl	nmod	22
root	parataxis	21
parataxis	parataxis	17
ccomp	root	15
cop	cop	11
det	nmod	11
list	conj	11
nsubj	nsubj	10
conj	parataxis	10
acl	acl	10
nsubj	obj	9
cc	cc	9

## Top LAS mistakes where Trankit aligned wins
gold_deprel	pred_deprel	count
punct	punct	196
advmod	advmod	86
obl	nmod	65
nmod	nmod	53
conj	conj	51
obl	obl	45
nmod	obl	37
acl	acl	32
aux	aux	30
obj	iobj	26
cc	cc	26
obj	nsubj	25
nsubj	obj	25
root	cop	22
mark	mark	22
nsubj	nsubj	21
cop	cop	19
csubj	csubj	16
nsubj	root	16
cc	advmod	13

## Top DEPREL mistakes where CLASSLA aligned wins
gold_deprel	pred_deprel	count
nmod	obl	50
iobj	obj	47
orphan	advmod	39
obl	nmod	27
root	parataxis	21
conj	parataxis	15
ccomp	root	15
list	conj	12
det	nmod	11
advcl	acl	10
nsubj	root	10
nsubj	obj	9
parataxis	conj	9
parataxis	nsubj	8
cc	advmod	8
case	advmod	8
obl	obj	8
advcl	parataxis	8
flat	nmod	8
parataxis	advmod	8

## Top DEPREL mistakes where Trankit aligned wins
gold_deprel	pred_deprel	count
obl	nmod	66
nmod	obl	41
obj	iobj	28
obj	nsubj	26
nsubj	obj	25
root	cop	22
nsubj	root	17
cc	advmod	13
cop	root	12
root	parataxis	11
parataxis	root	11
nmod	flat	11
nsubj	conj	10
advcl	acl	10
obl	nsubj	8
conj	cop	8
appos	conj	8
nsubj	parataxis	7
conj	appos	7
advmod	nsubj	7
