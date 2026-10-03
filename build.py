from pathlib import Path
import json
root=Path(__file__).resolve().parent
p=json.loads((root/'source/clash-rules.json').read_text())
(root/'clash.template.yaml').write_text('# Rules and groups only; merge with local nodes.\n'+json.dumps(p,ensure_ascii=False,indent=2)+'\n')
(root/'shadowrocket.conf').write_text((root/'source/shadowrocket.template.conf').read_text())
print('Generated complete public rules templates; node credentials are in the private repository.')
