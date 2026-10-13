"""Upload research via GitHub Git Data API, verify remote content, then trim local archives.
Credential is read only from GITHUB_TOKEN in this process environment, never stored.
"""
from pathlib import Path
import os,json,hashlib,base64,requests,concurrent.futures,datetime,time
root=Path('/home/user');repo='TheOmniarch-god/Reverend-Insanity-Translation-by-The-Omniarch';api=f'https://api.github.com/repos/{repo}'
token=os.environ.pop('GITHUB_TOKEN');headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
def call(method,path,**kw):
 for attempt in range(4):
  q=requests.request(method,api+path,headers=headers,timeout=150,**kw)
  if q.status_code not in [429,500,502,503,504]:break
  if attempt<3:time.sleep(2**attempt)
 if not q.ok:
  try:message=q.json().get('message','Request failed')
  except ValueError:message='Non-JSON response'
  raise RuntimeError(f'GitHub {method} {path}: HTTP{q.status_code}; '+message)
 return q.json()
def gitsha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
ref=call('GET','/git/ref/heads/main');head=ref['object']['sha'];commit=call('GET','/git/commits/'+head);tree=call('GET','/git/trees/'+commit['tree']['sha']+'?recursive=1');assert not tree['truncated'];remote={x['path']:x for x in tree['tree'] if x['type']=='blob'}
files=[p for p in (root/'editorial').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
files += [p for p in (root/'benchmark').iterdir() if p.is_file() and p.suffix in ['.md','.docx','.json','.py']]
files += [p for p in (root/'backups').iterdir() if p.is_file() and p.suffix in ['.json','.md','.py']]
files += [root/'backups/Omniarch-Research-Through-Chapter-355.zip',root/'benchmark/sources/epub-text-index.json.gz']
records=[]
for p in sorted(set(files)):
 if p.name=='GitHub-Move-Manifest-Ch355.json':continue
 b=p.read_bytes();local=str(p.relative_to(root));records.append(dict(local_path=local,remote_path='research/'+local,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),git_blob_sha=gitsha(b)))
# Pin deletion candidates in the uploaded manifest before any removal.
cut=[]
for x in records:
 n=x['local_path']
 if n.endswith('.zip') or n=='benchmark/sources/epub-text-index.json.gz' or (n.startswith('editorial/sequential-review/history/') and not Path(n).name.startswith('before-batch018-')) or (n.endswith('.docx') and 'Batch-018-' not in n) or ('/fact-check-' in n and n.endswith('.html')):
  cut.append(x)
manifest=dict(repository=repo,coverage_through=355,next_unread=356,files=records,planned_local_archive_removals=[x['local_path'] for x in cut],epub_unchanged=True,live_site_edits=False,note='Preserves existing remote files. Cleanup occurs only after commit verification and fresh blob downloads. Includes live synopsis comparison.')
mp=root/'backups/GitHub-Move-Manifest-Ch355.json';mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2));b=mp.read_bytes();records.append(dict(local_path=str(mp.relative_to(root)),remote_path='research/backup-records/MOVE-MANIFEST-CH355.json',bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),git_blob_sha=gitsha(b)))
changed=[x for x in records if remote.get(x['remote_path'],{}).get('sha')!=x['git_blob_sha']]
print('Files mapped:',len(records),'Changed/new blobs:',len(changed),'Planned removals:',len(cut),flush=True)
def upload(x):
 b=(root/x['local_path']).read_bytes();q=call('POST','/git/blobs',json={'content':base64.b64encode(b).decode(),'encoding':'base64'});assert q['sha']==x['git_blob_sha'],x['local_path'];return {'path':x['remote_path'],'mode':'100644','type':'blob','sha':q['sha']}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:entries=list(ex.map(upload,changed))
print('All blobs accepted and hashes matched.',flush=True)
t=call('POST','/git/trees',json={'base_tree':commit['tree']['sha'],'tree':entries});c=call('POST','/git/commits',json={'message':'Back up research through Chapter355, fact-check corrections, synopsis audit and workspace move manifest','tree':t['sha'],'parents':[head]});newhead=c['sha'];call('PATCH','/git/refs/heads/main',json={'sha':newhead,'force':False})
print('Committed:',newhead,flush=True)
verified=call('GET','/git/trees/'+t['sha']+'?recursive=1');assert not verified['truncated'];vmap={x['path']:x['sha'] for x in verified['tree'] if x['type']=='blob'}
for x in records:assert vmap.get(x['remote_path'])==x['git_blob_sha']
# Download the actual immutable GitHub blobs of every file to be removed.
# Public raw URLs at the commit avoid API base64 expansion and rate-limit costs.
from urllib.parse import quote
def verify_download(x):
 u=f'https://raw.githubusercontent.com/{repo}/{newhead}/'+quote(x['remote_path'],safe='/');q=requests.get(u,timeout=150);q.raise_for_status();assert hashlib.sha256(q.content).hexdigest()==x['sha256'],x['local_path'];return x['local_path']
critical=[x for x in records if Path(x['local_path']).name in ['proposal-ledger.json','reading-progress.json','Sequential-Reading-and-Proposals.xlsx','Live-Synopsis-Comparison.md']]
checks={x['local_path']:x for x in cut+critical}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:downloads=list(ex.map(verify_download,checks.values()))
print('Fresh remote SHA256 downloads verified:',len(downloads),flush=True)
receipt=dict(repository=repo,branch='main',commit=newhead,coverage_through=355,remote_verified=True,all_mapped_git_blob_hashes_verified=True,mapped_files=len(records),uploaded_changed_files=len(changed),fresh_remote_sha256_files=downloads,deleted_local_files=[],token_written_to_file=False,original_epub_modified=False,site_modified=False)
rp=root/'backups/GitHub-Backup-Receipt-Ch355.json';rp.write_text(json.dumps(receipt,indent=2))
freed=0
for x in cut:
 p=root/x['local_path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256'];p.unlink();freed+=x['bytes'];receipt['deleted_local_files'].append(x)
receipt['bytes_freed_this_move']=freed;receipt['remaining_regular_workspace_bytes']=sum(p.stat().st_size for p in root.rglob('*') if p.is_file());rp.write_text(json.dumps(receipt,indent=2))
print(json.dumps({k:receipt[k] for k in ['commit','coverage_through','mapped_files','uploaded_changed_files','bytes_freed_this_move','remaining_regular_workspace_bytes']},indent=2),flush=True)
