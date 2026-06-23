# Limitless Drive Blueprint

Limitless Drive is a local-first preservation layer for personal files and email
that can be published through IPFS and resolved through IPNS. It is designed as a
virtual disk drive that mounts on phones, laptops, desktops, and home servers
while keeping the canonical state in a GitOS-style append-only history.

## Goals

- Preserve family artifacts, memories, files, and email without accidental loss.
- Address every unique object by content using CIDv1-compatible multibase names.
- Deduplicate identical payloads while retaining every original location and
  contextual label.
- Treat deletion as a reversible intent, not destruction, until retention policy,
  quorum, and human review checks pass.
- Use agent-to-agent (A2A) coordination so devices, backup nodes, scanners, and
  recovery agents can negotiate sync without a single privileged automaton.

## Architecture

1. **Local capture agents** watch selected folders, removable drives, camera
   imports, and exported mailboxes. They only append observations to manifests.
2. **Content-addressed object store** chunks and pins payloads in IPFS. The
   included `limitless-index` prototype emits CIDv1-style base32 multibase IDs
   for whole-file and whole-email payloads before publication.
3. **GitOS ledger** commits manifests, policy files, revocation events, and IPNS
   pointer updates. Each commit is a signed checkpoint that devices can audit.
4. **IPNS namespace** publishes the current root manifest and latest safe mount
   view. Old roots remain reachable from the GitOS ledger and local pins.
5. **Virtual drive mount** exposes files through a FUSE/WebDAV/mobile-provider
   adapter. The mounted view is reconstructed from manifests, not from mutable
   path names alone.
6. **Email account vault** imports mbox/Maildir/IMAP exports as immutable
   `message/rfc822` artifacts, preserving message IDs, subjects, dates, and
   mailbox provenance as metadata.

## Security model

- **Quantum-resistant envelope option:** encrypt data keys to post-quantum KEM
  recipients, while retaining conventional authenticated encryption for payloads.
- **Device keys:** every device has its own signing key and revocation record.
- **Movement-based identification:** local unlock policy can combine device-held
  keys with consented motion biometrics, such as gait or familiar gesture
  classifiers, but motion signals must never be the sole recovery factor.
- **A2A least privilege:** scanner, dedupe, pinning, mount, and recovery agents
  exchange signed tasks with bounded capabilities.
- **Tamper evidence:** manifests store hashes, CIDs, sizes, timestamps, and
  source locations so unexpected mutation is detectable.

## Loss-prevention policy

Deletion requests create tombstone proposals. A proposal is eligible for garbage
collection only after all of these checks pass:

1. the content exists in at least the configured number of independent pins;
2. a newer manifest confirms no protected album, mailbox, or artifact collection
   references the content;
3. the retention window has expired;
4. a human recovery contact or owner quorum signs the removal;
5. the GitOS ledger contains the tombstone, approvals, and final collection
   receipt.

Until then, the virtual drive hides the item only in the requested view while the
underlying object remains pinned and recoverable.

## Prototype usage

Create a local manifest without changing source data:

```bash
python -m limitless_drive.indexer ~/Pictures ~/Documents mail-export.mbox \
  --output limitless-manifest.json
```

The manifest reports unique artifacts and duplicate content groups. Duplicate
entries are grouped by CID while retaining every discovered source location.
