# Workspace reduction requested after Chapter355

Status: partial cleanup complete; new GitHub upload blocked by missing write credential.

- No usable GitHub credential remains in the current context, environment or Git credential helper. Previous credentials were deliberately not persisted. Connector lookup returned unsupported; direct public GitHub reads work.
- Remote verified research coverage remains315, not355. Do not delete the new355 archive or unuploaded fact-checks/research as though remotely backed up.
- All395 members of the old285 ZIP were freshly matched to GitHub Git-blob hashes at commit9a1c8a25509d54c50754498ea4b0e5e1520a1ce1. Removed the redundant container only after complete verification.
- Fifteen historical binary exports/archives matched the current remote Git tree and were removed locally. Original Chinese EPUB, current cumulative workbook, code, source JSON, registers and recent reports retained.
- The large derived text index is losslessly gzip-compressed. Exact uncompressed SHA256 verified; no text discarded. This was compression, not a new remote upload. No sequential reading progress changed.
- Net cleanup savings:36,150,097 bytes before small receipts/scripts, about36.2MB decimal or34.5MiB. Regular workspace files approximately80MB after cleanup.
- Latest research archive:Omniarch-Research-Through-Chapter-355.zip,21,464,989 bytes; SHA256e6cd99b4124470c4e49199f0ecb26bc6f720368a6b2a92d6b3ba4f5203aa96e1. Still local only.

## Restore

Run `python3 backups/restore_archived_file.py '<local path>'` for a deleted single-file export, or use `benchmark/sources/epub-text-index.json` as the path to decompress the index. Existing files are not overwritten. All restored bytes are checked against SHA256.

Full removal receipt:Workspace-Cleanup-Requested-Ch355.json. The original285 archive's remote member map is Cleanup-285-Remote-Verification.json. It can be rebuilt from research paths at its pinned commit; ZIP-container metadata may differ but member bytes are verified.

## Remaining move

Requires a write-enabled GitHub credential supplied again, or user upload of the355 archive. Existing authorisation to back up research and remove verified local duplicates remains valid; no new permission question is needed. Once authenticated, upload new research and cleanup receipts, verify the actual remote bytes/commit, then remove local archived exports as appropriate while retaining a lean working set for Chapter356 onward. Never persist or print the credential.
