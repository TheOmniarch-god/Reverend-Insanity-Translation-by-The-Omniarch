"""Restore one remotely verified file or the losslessly compressed text index.
Usage: python3 backups/restore_archived_file.py 'editorial/path/to/file.docx'
Does not overwrite existing files. No credentials required for this public repository.
"""
from pathlib import Path
import sys,json,hashlib,gzip,base64,urllib.request
root=Path(__file__).resolve().parent.parent
name=sys.argv[1] if len(sys.argv)>1 else ''
m=json.loads((root/'backups/Workspace-Cleanup-Requested-Ch355.json').read_text())
target=(root/name).resolve()
if root not in target.parents:raise SystemExit('Choose a workspace-relative file path.')
if target.exists():raise SystemExit('File already exists; refusing to overwrite.')
if name=='benchmark/sources/epub-text-index.json':
 item=m['compressed'][0];data=gzip.decompress((root/item['compressed_path']).read_bytes());expected=item['sha256_uncompressed']
else:
 item=next((x for x in m['deleted'] if x['local_path']==name),None)
 if not item or 'git_blob_sha' not in item:raise SystemExit('No single-file restore entry. Chapter285 archive members are listed in Cleanup-285-Remote-Verification.json and available at its pinned commit.')
 url=f"https://api.github.com/repos/{m['repository']}/git/blobs/{item['git_blob_sha']}"
 req=urllib.request.Request(url,headers={'User-Agent':'Omniarch-research-restore'})
 with urllib.request.urlopen(req,timeout=90) as response:blob=json.load(response)
 if blob.get('encoding')!='base64':raise SystemExit('Unexpected GitHub response encoding.')
 data=base64.b64decode(blob['content']);expected=item['sha256']
assert hashlib.sha256(data).hexdigest()==expected,'SHA256 mismatch; not writing'
target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
print('Restored and SHA256-verified:',name)
