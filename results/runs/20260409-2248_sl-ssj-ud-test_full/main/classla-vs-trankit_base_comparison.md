# CLASSLA base vs Trankit base (exact difference report)

## Coverage
- Gold sentences: 1282
- CLASSLA base predicted sentences: 1287
- Trankit base predicted sentences: 1291
- Gold sentences paired with both models: 1255
- Unmatched gold for CLASSLA base: 3
- Unmatched gold for Trankit base: 24
- Unmatched predicted for CLASSLA base: 8
- Unmatched predicted for Trankit base: 33
- Skipped sentence pairs (token count mismatch): 25
- Compared tokens (FORM-aligned): 24364
- Skipped tokens (FORM mismatch): 0

## LAS exact differences
- CLASSLA base correct, Trankit base wrong: 1085 (4.45%)
- Trankit base correct, CLASSLA base wrong: 1292 (5.30%)
- Both correct: 20990 (86.15%)
- Both wrong: 997 (4.09%)

## UAS exact differences
- CLASSLA base correct, Trankit base wrong: 879 (3.61%)
- Trankit base correct, CLASSLA base wrong: 1140 (4.68%)
- Both correct: 21593 (88.63%)
- Both wrong: 752 (3.09%)

## DEPREL exact differences
- CLASSLA base correct, Trankit base wrong: 570 (2.34%)
- Trankit base correct, CLASSLA base wrong: 710 (2.91%)
- Both correct: 22642 (92.93%)
- Both wrong: 442 (1.81%)

## Top LAS mistakes where CLASSLA base wins
gold_deprel	pred_deprel	count
advmod	advmod	268
punct	punct	140
iobj	obj	42
nmod	obl	42
conj	conj	36
orphan	advmod	34
obl	obl	23
obl	nmod	21
nmod	nmod	20
root	parataxis	19
parataxis	parataxis	16
ccomp	root	14
det	nmod	11
conj	parataxis	10
cop	cop	10
nsubj	nsubj	9
nsubj	obj	9
nsubj	root	8
acl	acl	8
obl	obj	8

## Top LAS mistakes where Trankit base wins
gold_deprel	pred_deprel	count
punct	punct	186
advmod	advmod	84
obl	nmod	63
nmod	nmod	50
conj	conj	47
obl	obl	43
nmod	obl	36
acl	acl	29
aux	aux	28
cc	cc	26
nsubj	obj	25
obj	iobj	25
obj	nsubj	24
root	cop	21
mark	mark	21
nsubj	nsubj	21
cop	cop	19
csubj	csubj	15
nsubj	root	15
cc	advmod	13

## Top DEPREL mistakes where CLASSLA base wins
gold_deprel	pred_deprel	count
nmod	obl	48
iobj	obj	44
orphan	advmod	38
obl	nmod	25
root	parataxis	19
conj	parataxis	15
ccomp	root	14
det	nmod	11
advcl	acl	10
nsubj	root	9
nsubj	obj	9
parataxis	conj	9
cc	advmod	8
obl	obj	8
flat	nmod	8
parataxis	nsubj	7
case	advmod	7
advcl	parataxis	7
parataxis	advmod	7
conj	advmod	6

## Top DEPREL mistakes where Trankit base wins
gold_deprel	pred_deprel	count
obl	nmod	64
nmod	obl	40
obj	iobj	27
obj	nsubj	25
nsubj	obj	25
root	cop	21
nsubj	root	16
cc	advmod	13
cop	root	12
parataxis	root	11
nsubj	conj	10
root	parataxis	10
advcl	acl	9
obl	nsubj	8
conj	cop	8
nmod	flat	8
appos	conj	8
nsubj	parataxis	7
conj	appos	7
advmod	nsubj	7
