# Quantum Chemistry

This repository tracks the evolution of a self-building Quantum Chemistry
textbook and adjacent experiments in durable, agent-coordinated knowledge
preservation. Automated updates occur every 15 minutes via GitHub Actions.

## Limitless Drive prototype

The repository now includes a local-first preservation prototype for a
content-addressed virtual drive that can later be published through IPFS/IPNS.
It is not a production storage network by itself; it provides the manifesting
foundation needed to identify unique files and exported emails, detect duplicate
payloads, and retain every discovered source location before pinning or mounting.

Key pieces:

- `docs/limitless-drive.md` describes the IPFS/IPNS, GitOS, A2A, security, and
  deletion-safety blueprint.
- `src/limitless_drive/indexer.py` builds a CIDv1-style multibase manifest for
  regular files and `.mbox` email archives.
- `tests/test_indexer.py` covers deterministic IDs, deduplication, mailbox
  indexing, and CLI manifest output.

Run the prototype against one or more directories or files:

```bash
python -m limitless_drive.indexer ~/Pictures ~/Documents mail-export.mbox \
  --output limitless-manifest.json
```
