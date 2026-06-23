"""Build a content-addressed manifest for files and exported email archives.

The manifest is intentionally local-first: it never deletes source data and it
can be generated before IPFS/IPNS publication.  Each payload receives a CID-like
multibase identifier derived from a SHA-256 multihash so duplicate bytes can be
recognized across drives, folders, email exports, and historical archives.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mailbox
import mimetypes
import os
import stat
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from email.message import Message
from pathlib import Path
from typing import Iterable, Iterator

CIDV1_RAW_SHA256_PREFIX = bytes([0x01, 0x55, 0x12, 0x20])


@dataclass(frozen=True)
class Artifact:
    """A single preserved object in a local archive."""

    cid: str
    kind: str
    size: int
    sha256: str
    locations: list[str]
    mime_type: str | None = None
    subject: str | None = None
    message_id: str | None = None
    modified_utc: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


def cidv1_raw_sha256(payload: bytes) -> str:
    """Return a CIDv1-style base32 multibase string for raw SHA-256 content."""

    digest = hashlib.sha256(payload).digest()
    cid_bytes = CIDV1_RAW_SHA256_PREFIX + digest
    return "b" + base64.b32encode(cid_bytes).decode("ascii").lower().rstrip("=")


def _utc_timestamp(epoch_seconds: float) -> str:
    return datetime.fromtimestamp(epoch_seconds, tz=timezone.utc).isoformat()


def _safe_location(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def iter_files(roots: Iterable[Path]) -> Iterator[Path]:
    """Yield regular files under roots without following symlinked files."""

    for root in roots:
        if root.is_file() and not root.is_symlink():
            yield root
            continue
        for directory, dirnames, filenames in os.walk(root, followlinks=False):
            dirnames[:] = [name for name in dirnames if not (Path(directory) / name).is_symlink()]
            for filename in filenames:
                path = Path(directory) / filename
                try:
                    mode = path.lstat().st_mode
                except OSError:
                    continue
                if stat.S_ISREG(mode):
                    yield path


def artifact_from_file(path: Path, root: Path) -> Artifact:
    payload = path.read_bytes()
    guessed_mime, _ = mimetypes.guess_type(path.name)
    digest = hashlib.sha256(payload).hexdigest()
    return Artifact(
        cid=cidv1_raw_sha256(payload),
        kind="file",
        size=len(payload),
        sha256=digest,
        locations=[_safe_location(path, root)],
        mime_type=guessed_mime,
        modified_utc=_utc_timestamp(path.stat().st_mtime),
    )


def _message_payload(message: Message) -> bytes:
    return message.as_bytes(unixfrom=False)


def artifacts_from_mbox(path: Path, root: Path) -> Iterator[Artifact]:
    archive = mailbox.mbox(path)
    for index, message in enumerate(archive):
        payload = _message_payload(message)
        location = f"{_safe_location(path, root)}#message-{index}"
        yield Artifact(
            cid=cidv1_raw_sha256(payload),
            kind="email",
            size=len(payload),
            sha256=hashlib.sha256(payload).hexdigest(),
            locations=[location],
            mime_type="message/rfc822",
            subject=message.get("subject"),
            message_id=message.get("message-id"),
            metadata={"from": message.get("from", ""), "date": message.get("date", "")},
        )


def build_manifest(paths: Iterable[Path]) -> dict[str, object]:
    roots = [path.resolve() for path in paths]
    by_cid: dict[str, Artifact] = {}
    for file_path in iter_files(roots):
        root = next((candidate for candidate in roots if candidate == file_path.resolve() or candidate in file_path.resolve().parents), file_path.parent.resolve())
        artifacts: Iterable[Artifact]
        if file_path.suffix.lower() == ".mbox":
            artifacts = artifacts_from_mbox(file_path, root)
        else:
            artifacts = [artifact_from_file(file_path, root)]
        for artifact in artifacts:
            existing = by_cid.get(artifact.cid)
            if existing is None:
                by_cid[artifact.cid] = artifact
            else:
                locations = sorted({*existing.locations, *artifact.locations})
                by_cid[artifact.cid] = Artifact(**{**asdict(existing), "locations": locations})

    artifacts_list = sorted((asdict(item) for item in by_cid.values()), key=lambda item: item["cid"])
    duplicates = [item for item in artifacts_list if len(item["locations"]) > 1]
    return {
        "schema": "limitless-drive.manifest.v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "artifact_count": len(artifacts_list),
        "duplicate_content_groups": len(duplicates),
        "artifacts": artifacts_list,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a content-addressed preservation manifest.")
    parser.add_argument("paths", nargs="+", type=Path, help="Files or directories to index")
    parser.add_argument("--output", "-o", type=Path, default=Path("limitless-manifest.json"), help="Manifest path")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    manifest = build_manifest(args.paths)
    args.output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"indexed {manifest['artifact_count']} unique artifacts; duplicate groups: {manifest['duplicate_content_groups']}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
