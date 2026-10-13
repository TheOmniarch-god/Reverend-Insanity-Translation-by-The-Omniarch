"""Upload current research without recreating bulky local ZIPs.
Usage: GITHUB_TOKEN=<transient credential> python3 backups/push_incremental_checkpoint.py 365
Never deletes remote files or writes the credential to disk.
"""
from pathlib import Path
import os,sys,json,hashlib,base64,time,concurrent.futures,requests
root=Path('/home/user');end=int(sys.argv[1]);repo='TheOmniarch-god/Reverend-Insanity-Translation-by-The-Omniarch';api=f'https://api.github.com/repos/{repo}'
headers={'Authorization':'Bearer '+os.environ.pop('GITHUB_TOKEN'),'Accept':'application/vnd.github+json'}
def call(method,path,data=None):
 for attempt in range(4):
  q=requests.request(method,api+path,headers=headers,json=data,timeout=90)
  if q.status_code not in [429,500,502,503,504]:break
  if attempt<3:time.sleep(2**attempt)
 if not q.ok:raise RuntimeError(f'GitHub {method} {path}: HTTP{q.status_code}')
 return q.json()
def gitsha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def push(files,message):
 head=call('GET','/git/ref/heads/main')['object']['sha'];c=call('GET','/git/commits/'+head);tree=call('GET','/git/trees/'+c['tree']['sha']+'?recursive=1');assert not tree['truncated'];remote={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
 records=[]
 for p in sorted(set(files)):
  b=p.read_bytes();n=str(p.relative_to(root));records.append(dict(local_path=n,remote_path='research/'+n,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),git_blob_sha=gitsha(b)))
 changed=[x for x in records if remote.get(x['remote_path'])!=x['git_blob_sha']]
 def upload(x):
  b=(root/x['local_path']).read_bytes();v=call('POST','/git/blobs',{'content':base64.b64encode(b).decode(),'encoding':'base64'});assert v['sha']==x['git_blob_sha'];return dict(path=x['remote_path'],mode='100644',type='blob',sha=v['sha'])
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:entries=list(ex.map(upload,changed))
 if entries:
  t=call('POST','/git/trees',{'base_tree':c['tree']['sha'],'tree':entries});new=call('POST','/git/commits',{'message':message,'tree':t['sha'],'parents':[head]});head=new['sha'];call('PATCH','/git/refs/heads/main',{'sha':head,'force':False})
  v=call('GET','/git/trees/'+t['sha']+'?recursive=1');assert not v['truncated'];remote={x['path']:x['sha'] for x in v['tree'] if x['type']=='blob'}
 for x in records:assert remote.get(x['remote_path'])==x['git_blob_sha']
 from urllib.parse import quote
 def verify(x):
  u=f'https://raw.githubusercontent.com/{repo}/{head}/'+quote(x['remote_path'],safe='/');q=requests.get(u,timeout=90);q.raise_for_status();assert hashlib.sha256(q.content).hexdigest()==x['sha256'];return x['local_path']
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:verified=list(ex.map(verify,changed))
 print('Commit',head,'mapped',len(records),'new/changed remote downloads verified',len(verified),flush=True)
 return head,records,verified
files=[p for p in (root/'editorial').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
files += [p for p in (root/'benchmark').iterdir() if p.is_file()]
files += [p for p in (root/'backups').iterdir() if p.is_file() and p.suffix in ['.md','.json','.py'] and p.name!=f'GitHub-Backup-Receipt-Ch{end}.json']
head,records,verified=push(files,f'Continue sequential review through Chapter{end}; preserve qualified proposals and same-character synopsis clarification')
receipt=dict(repository=repo,branch='main',commit=head,coverage_through=end,next_unread=end+1,remote_verified=True,mapped_files=len(records),fresh_sha256_downloads=verified,token_written_to_file=False,source_or_site_edits=False,local_deletions=False)
rp=root/f'backups/GitHub-Backup-Receipt-Ch{end}.json';rp.write_text(json.dumps(receipt,indent=2))
sr=root/'editorial/sequential-review';status=sr/'CURRENT-STATUS.md';text=status.read_text();text=text.replace('Current365 upload not yet claimed.',f'Current365 research uploaded and remote verified at commit{head}.');status.write_text(text)
qa=sr/'batch-019-qa.json'
if end==365:
 q=json.loads(qa.read_text());q.update(remote_uploaded=True,remote_verified=True,remote_data_commit=head);qa.write_text(json.dumps(q,ensure_ascii=False,indent=2))
final,_,_=push([rp,status,qa],f'Record verified Chapter{end} backup receipt and current status')
(root/f'backups/GitHub-Finalization-Ch{end}.json').write_text(json.dumps(dict(data_commit=head,receipt_commit=final,coverage_through=end,remote_verified=True),indent=2))
print('Final verification commit:',final,flush=True)
