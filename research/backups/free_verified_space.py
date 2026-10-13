from pathlib import Path
import json,hashlib,gzip,shutil
root=Path('/home/user');repo='TheOmniarch-god/Reverend-Insanity-Translation-by-The-Omniarch'
tree=json.loads((root/'backups/GitHub-Remote-Tree-For-Cleanup.json').read_text());assert not tree['truncated'];remote={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
def gitsha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
manifest=dict(repository=repo,remote_tree=tree['sha'],new_work_uploaded=False,new_work_preserved_through=355,deleted=[],compressed=[],note='No new remote upload. Only matching remote-backed historical copies deleted. Current research and original EPUB retained.')
# Historical binary reports and terminology archive; keep all code, all source JSON,
# current workbook, recent reports, working registers, jotters and textual research.
for base in ['editorial','benchmark']:
 for p in sorted((root/base).rglob('*')):
  if not p.is_file() or p.suffix.lower() not in ['.docx','.xlsx','.zip']:continue
  local=str(p.relative_to(root));rp='research/'+local
  if local=='editorial/sequential-review/Sequential-Reading-and-Proposals.xlsx':continue
  b=p.read_bytes();h=gitsha(b)
  if remote.get(rp)!=h:continue
  manifest['deleted'].append(dict(local_path=local,remote_path=rp,git_blob_sha=h,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),tree=tree['sha']))
# Archive contents independently checked against original commit.
v=json.loads((root/'backups/Cleanup-285-Remote-Verification.json').read_text());assert len(v['verified_files'])==395 and not v['unmatched']
p=root/'backups/Omniarch-Research-Through-Chapter-285.zip';manifest['deleted'].append(dict(local_path=str(p.relative_to(root)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),restore_manifest='backups/Cleanup-285-Remote-Verification.json',commit=v['commit'],note='All395 member bytes match GitHub blobs at pinned commit. Container can be rebuilt; no unique file contents removed.'))
# Lossless compression, not a remote move or deletion of source information.
p=root/'benchmark/sources/epub-text-index.json';gz=p.with_suffix('.json.gz');original=p.read_bytes();h=hashlib.sha256(original).hexdigest()
with gzip.GzipFile(filename=str(gz),mode='wb',compresslevel=9,mtime=0) as f:f.write(original)
assert hashlib.sha256(gzip.decompress(gz.read_bytes())).hexdigest()==h
manifest['compressed'].append(dict(original_path=str(p.relative_to(root)),compressed_path=str(gz.relative_to(root)),original_bytes=len(original),compressed_bytes=gz.stat().st_size,sha256_uncompressed=h,restore='gzip.decompress(Path(compressed_path).read_bytes()); write original_path after checking SHA256'))
manifest['bytes_freed']=sum(x['bytes'] for x in manifest['deleted'])+len(original)-gz.stat().st_size
receipt=root/'backups/Workspace-Cleanup-Requested-Ch355.json';receipt.write_text(json.dumps(manifest,indent=2))
for x in manifest['deleted']:
 q=root/x['local_path'];assert hashlib.sha256(q.read_bytes()).hexdigest()==x['sha256'];q.unlink()
p.unlink();print(json.dumps(dict(deleted_files=len(manifest['deleted']),bytes_freed=manifest['bytes_freed'],compressed_index_bytes=gz.stat().st_size,latest_archive_retained=(root/'backups/Omniarch-Research-Through-Chapter-355.zip').exists()),indent=2))
