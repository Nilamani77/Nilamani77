
#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen
import json, os
USER="Nilamani77"
ROOT=Path(__file__).resolve().parents[1]
TEMPLATE=ROOT/"assets/id-dashboard.template.svg"
OUTPUT=ROOT/"assets/id-dashboard.svg"
def get_json(url):
    h={"Accept":"application/vnd.github+json","User-Agent":"Nilamani77-profile-dashboard"}
    token=os.getenv("GITHUB_TOKEN")
    if token: h["Authorization"]=f"Bearer {token}"
    with urlopen(Request(url,headers=h),timeout=20) as r: return json.load(r)
profile=get_json(f"https://api.github.com/users/{USER}")
repos=get_json(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
stars=sum(int(x.get("stargazers_count",0)) for x in repos)
vals={"__SYNC__":datetime.now(timezone.utc).strftime("%d %b %Y · %H:%M UTC"),"__REPOS__":str(profile.get("public_repos",0)),"__STARS__":str(stars),"__FOLLOWERS__":str(profile.get("followers",0)),"__FOLLOWING__":str(profile.get("following",0))}
s=TEMPLATE.read_text()
for k,v in vals.items(): s=s.replace(k,v)
OUTPUT.write_text(s)
print(vals)
