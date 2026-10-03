from pathlib import Path
import json, sys
root=Path(__file__).resolve().parent
src=json.loads((root/'policy.json').read_text())
base=sys.argv[1].rstrip('/') if len(sys.argv)>1 else 'https://raw.githubusercontent.com/OWNER/REPO/main'
for key in ['ai','cloudflare','direct']:
    lines=src[key]
    (root/f'rules/{key}.list').write_text('\n'.join(lines)+'\n')
    (root/f'rules/{key}.yaml').write_text('payload:\n'+''.join('  - '+json.dumps(x)+'\n' for x in lines))
up='https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule'
providers={k:{'type':'http','behavior':'classical','url':f'{base}/rules/{k}.yaml','path':f'./rules/smart-{k}.yaml','interval':86400} for k in ['ai','cloudflare','direct']}
providers['normal-proxy']={'type':'http','behavior':'classical','url':f'{up}/Clash/Proxy/Proxy.yaml','path':'./rules/normal-proxy.yaml','interval':86400}
providers['china-domain']={'type':'http','behavior':'domain','url':f'{up}/Clash/ChinaMax/ChinaMax_Domain.yaml','path':'./rules/china-domain.yaml','interval':86400}
rules=['RULE-SET,ai,AI','RULE-SET,cloudflare,DIRECT','RULE-SET,direct,DIRECT','RULE-SET,china-domain,DIRECT','RULE-SET,normal-proxy,Normal,no-resolve','GEOIP,CN,DIRECT','MATCH,Unmatched']
config={'mode':'rule','log-level':'info','proxies':[],'proxy-groups':[{'name':'AI','type':'select','proxies':['REJECT']},{'name':'Normal','type':'select','proxies':['REJECT']},{'name':'Unmatched','type':'select','proxies':['Normal','DIRECT']}],'rule-providers':providers,'rules':rules}
(root/'clash.template.yaml').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')
sr=['[General]','ipv6 = false','bypass-system = true','dns-server = 223.5.5.5, 119.29.29.29','','[Proxy Group]','AI = select, DMIT-HY2','Normal = select, PROXY','Unmatched = select, Normal, DIRECT','','[Rule]']
for k,p in [('ai','AI'),('cloudflare','DIRECT'),('direct','DIRECT')]: sr.append(f'RULE-SET,{base}/rules/{k}.list,{p}')
sr += [f'DOMAIN-SET,{up}/Shadowrocket/ChinaMax/ChinaMax_Domain.list,DIRECT',f'RULE-SET,{up}/Shadowrocket/Proxy/Proxy.list,Normal','GEOIP,CN,DIRECT','FINAL,Unmatched','','[URL Rewrite]','','[MITM]','enable = false']
(root/'shadowrocket.conf').write_text('\n'.join(sr)+'\n')
print('Generated public templates and shared rule sets. Repository URL:',base)
