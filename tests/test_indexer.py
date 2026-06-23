import json
from email.message import EmailMessage

from limitless_drive.indexer import build_manifest, cidv1_raw_sha256, main


def test_cid_is_stable_multibase_base32():
    cid = cidv1_raw_sha256(b"family photo bytes")

    assert cid.startswith("b")
    assert cid == cidv1_raw_sha256(b"family photo bytes")
    assert cid != cidv1_raw_sha256(b"different bytes")


def test_manifest_deduplicates_files_and_keeps_locations(tmp_path):
    (tmp_path / "a.txt").write_text("same memory", encoding="utf-8")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "copy.txt").write_text("same memory", encoding="utf-8")

    manifest = build_manifest([tmp_path])

    assert manifest["artifact_count"] == 1
    assert manifest["duplicate_content_groups"] == 1
    assert sorted(manifest["artifacts"][0]["locations"]) == ["a.txt", "nested/copy.txt"]


def test_mbox_messages_are_indexed(tmp_path):
    message = EmailMessage()
    message["From"] = "alice@example.test"
    message["To"] = "family@example.test"
    message["Subject"] = "Picnic"
    message["Message-ID"] = "<picnic@example.test>"
    message.set_content("remember this day")
    mbox = tmp_path / "mail.mbox"
    mbox.write_text("From alice Sat Jan 01 00:00:00 2022\n" + message.as_string() + "\n", encoding="utf-8")

    manifest = build_manifest([tmp_path])

    assert manifest["artifact_count"] == 1
    artifact = manifest["artifacts"][0]
    assert artifact["kind"] == "email"
    assert artifact["subject"] == "Picnic"
    assert artifact["message_id"] == "<picnic@example.test>"


def test_cli_writes_manifest(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "note.txt").write_text("do not lose", encoding="utf-8")
    output = tmp_path / "manifest.json"

    assert main([str(source), "--output", str(output)]) == 0
    manifest = json.loads(output.read_text(encoding="utf-8"))
    assert manifest["schema"] == "limitless-drive.manifest.v1"
    assert manifest["artifact_count"] == 1
