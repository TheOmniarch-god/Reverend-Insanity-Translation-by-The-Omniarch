"""Restore a verified archived file without overwriting an existing file.
Usage: python3 backups/restore_archived_file.py 'workspace/relative/path'
Supports the Chapter355 move, earlier binary cleanup and decompression of the index.
"""
from pathlib import Path
import sys,json,hashlib,gzip,base64,urllib.request,urllib.parse
root=Path(__file__).resolve().parent.parent
name=sys.argv[1] if len(sys.argv)>1 else ''
old=json.loads((root/'backups/Workspace-Cleanup-Requested-Ch355.json').read_text())
new=json.loads((root/'backups/GitHub-Backup-Receipt-Ch355.json').read_text())
def get_remote(path):
 item=next((x for x in new['deleted_local_files'] if x['local_path']==path),None)
 if item:
  url=f"https://raw.githubusercontent.com/{new['repository']}/{new['commit']}/"+urllib.parse.quote(item['remote_path'],safe='/')
  with urllib.request.urlopen(url,timeout=150) as response:data=response.read()
 else:
  item=next((x for x in old['deleted'] if x['local_path']==path),None)
  if not item or 'git_blob_sha' not in item:raise SystemExit('No single-file restore entry. The older285 ZIP member map is in Cleanup-285-Remote-Verification.json.')
  url=f"https://api.github.com/repos/{old['repository']}/git/blobs/{item['git_blob_sha']}"
  req=urllib.request.Request(url,headers={'User-Agent':'Omniarch-research-restore'})
  with urllib.request.urlopen(req,timeout=90) as response:blob=json.load(response)
  if blob.get('encoding')!='base64':raise SystemExit('Unexpected GitHub encoding.')
  data=base64.b64decode(blob['content'])
 assert hashlib.sha256(data).hexdigest()==item['sha256'],'Remote SHA256 mismatch'
 return data
path=(root/name).resolve()
if root not in path.parents:raise SystemExit('Choose a workspace-relative file path.')
if path.exists():raise SystemExit('File already exists; refusing to overwrite.')
if name=='benchmark/sources/epub-text-index.json':
 item=old['compressed'][0];compressed=root/item['compressed_path'];b=compressed.read_bytes() if compressed.exists() else get_remote(item['compressed_path']);data=gzip.decompress(b);assert hashlib.sha256(data).hexdigest()==item['sha256_uncompressed']
else:data=get_remote(name)
path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
print('Restored and SHA256-verified:',name)
