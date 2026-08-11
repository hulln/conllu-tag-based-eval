# PyTorch control run — Stanza 1.13 under torch 2.6.0

The two arms of this comparison do not share a PyTorch version: Stanza 1.14
cannot load its Slovenian lemmatizer under `torch 2.0.1+cu118` (see the
[experiment README](README.md)). To check that the PyTorch version is not itself
responsible for the observed 1.13-vs-1.14 differences, **Stanza 1.13.0 was rerun
on the same SSJ test set with `torch 2.6.0+cu118`**.

Image: `conllu-stanza:1.13.0-torch2.6.0`
Image ID: `sha256:fe6414e9339fa6ff1f99f88589bb675edc24240b32f5af02bb748ee5b7224e0d`

## Result

Both control outputs were **byte-for-byte identical** to the original Stanza
1.13.0 + PyTorch 2.0.1 predictions:

| Package | SHA-256 of control output | Matches |
|---|---|---|
| `default` | `ca99531992f838ef2b5336769d24091005e0579543e174895b8d4d4cff4d24f6` | `…_stanza-1.13.0-default_aligned_predicted.conllu` |
| `default_accurate` | `d6da5580bdb7e04de18332ebb2228fc46bffcb6d0cea95c669193942cf0a2b91` | `…_stanza-1.13.0-accurate_aligned_predicted.conllu` |

PyTorch 2.0.1 vs 2.6.0 therefore did not affect the Stanza 1.13 predictions in
this evaluation, and the differences reported between 1.13.0 and 1.14.0 **in this
2026-08-10 experiment** are not attributable to the PyTorch version difference
alone.

This statement is scoped to the configuration tested here — Stanza 1.13.0 with
the present-day-resource `combined_*` model set. It does **not** carry over to
the release-time reconstruction in
[`20260811-stanza-release-time-1.13-vs-1.14`](../20260811-stanza-release-time-1.13-vs-1.14/),
whose 1.13 arm resolves to the `ssj_*` model set that this control never ran. For
that experiment, the contribution of the PyTorch-version difference has not been
isolated.

## Repeat on SST

The same control was run again for the
[SST companion experiment](../20260810-stanza-1.13-vs-1.14-sst/), using the same
`conllu-stanza:1.13.0-torch2.6.0` image against the SST gold file. Both SST
control outputs were likewise byte-for-byte identical to the Stanza 1.13.0 +
torch 2.0.1 SST predictions; the two SHA-256 values are recorded under
`control_runs` in
[the SST manifest](../20260810-stanza-1.13-vs-1.14-sst/manifest.json). Those
duplicate control files were also not retained.

## What this control does and does not establish

- It is one-directional: 1.13 was rerun under the *newer* PyTorch. The reverse
  is impossible, because Stanza 1.14 does not load under torch 2.0.1.
- Byte-identical output across two independent runs is also the only evidence in
  this experiment that Stanza inference is deterministic here.

## Retention — read before citing this

**The duplicate control prediction files were not retained**, and no pip-freeze
or Compose service was captured for the control image. What is committed is this
note and the two SHA-256 values above, which do match the committed Stanza 1.13
prediction files.

The control is therefore **documented but not independently reproducible from
this repository**. Reproducing it requires rebuilding the image on the CJVT
server:

```bash
docker build -f docker/Dockerfile.stanza \
  --build-arg STANZA_VERSION=1.13.0 \
  --build-arg TORCH_VERSION=2.6.0+cu118 \
  -t conllu-stanza:1.13.0-torch2.6.0 .
```

and rerunning the two prediction commands from the experiment README against the
1.13 model cache. `docker-compose.stanza.yml` intentionally defines only the two
evaluation services, so this image has no Compose service.
