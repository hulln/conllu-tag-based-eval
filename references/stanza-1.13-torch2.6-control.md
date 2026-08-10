# Stanza 1.13 PyTorch control

Stanza 1.13.0 was rerun on the SSJ test set with PyTorch 2.6.0+cu118 to control for the different PyTorch versions used in the original 1.13/1.14 comparison.

Docker image: `conllu-stanza:1.13.0-torch2.6.0`  
Image ID: `sha256:fe6414e9339fa6ff1f99f88589bb675edc24240b32f5af02bb748ee5b7224e0d`

Both outputs were byte-for-byte identical to the original Stanza 1.13.0 + PyTorch 2.0.1 outputs:

- `default`: identical
- `default_accurate`: identical

PyTorch 2.0.1 vs 2.6.0 therefore did not affect the Stanza 1.13 predictions in this evaluation.

SHA-256: `default` ca99531992f838ef2b5336769d24091005e0579543e174895b8d4d4cff4d24f6; `default_accurate` d6da5580bdb7e04de18332ebb2228fc46bffcb6d0cea95c669193942cf0a2b91.
