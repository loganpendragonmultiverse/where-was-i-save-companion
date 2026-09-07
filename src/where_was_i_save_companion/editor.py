"""Local editable and printable return-to-game cards."""

from __future__ import annotations

import json
from typing import Any


def render_html(report: dict[str, Any]) -> str:
    payload = json.dumps(report).replace("<", "\\u003c").replace("&", "\\u0026")
    return (
        """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Return to game</title>
<style>body{font:17px system-ui;max-width:900px;margin:auto;padding:22px;background:#f5f1e8;color:#203442}article{background:white;border:1px solid #abc;border-radius:12px;padding:20px;margin:20px 0}label{display:block;margin:14px 0}input,textarea,button{font:inherit;padding:9px;box-sizing:border-box;max-width:100%}input,textarea{width:100%}.print-value{display:none;white-space:pre-wrap;overflow-wrap:anywhere}@media print{body{background:white;padding:0;font-size:12pt}article{break-inside:avoid}input,textarea,button{display:none}.print-value{display:block}article{border:1px solid #888}}</style>
<h1>Return to game</h1><p>Review and edit your local cards, then download a new file. Screenshot references are labels only: no image or save files are opened.</p><p id="privacy" role="status"></p><main id="cards"></main><button id="download">Download edited cards</button><button id="print">Print cards</button>
<script type="application/json" id="data">"""
        + payload
        + """</script><script>
const data=JSON.parse(document.getElementById('data').textContent);document.getElementById('privacy').textContent=JSON.stringify(data.share_review??{mode:'local',note:'Review all fields before sharing'});
for(const card of data.cards){const article=document.createElement('article');const title=document.createElement('h2');title.textContent=card.game;article.append(title);
const fields=['id','game','updated','location','next_step','last_played','goals','controls','story_context','loose_ends','spoiler_boundary','save_catalog_id'];
if(!data.share_review?.share_safe)fields.push('screenshot_reference');if('private_note' in card)fields.push('private_note');
for(const key of fields){const list=['goals','controls','story_context','loose_ends'].includes(key);const label=document.createElement('label');label.textContent=key.replaceAll('_',' ')+(list?' (one per line)':'');
const input=document.createElement(list||key==='private_note'?'textarea':'input');if(key==='last_played')input.type='date';input.value=list?(card[key]??[]).join('\n'):(card[key]??'');const printed=document.createElement('span');printed.className='print-value';printed.textContent=input.value;
input.addEventListener('input',()=>{if(list)card[key]=input.value.split('\n').filter(Boolean);else if(input.value===''&&!['id','game','updated','location','next_step'].includes(key))delete card[key];else card[key]=input.value;printed.textContent=input.value;});label.append(input,printed);article.append(label);}document.getElementById('cards').append(article);}
document.getElementById('download').addEventListener('click',()=>{for(const card of data.cards)if(['id','game','updated','location','next_step'].some(key=>!card[key]?.trim())){document.getElementById('privacy').textContent='Required card fields cannot be blank.';return;}
const url=URL.createObjectURL(new Blob([JSON.stringify({version:1,cards:data.cards},null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='edited-return-cards.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});document.getElementById('print').addEventListener('click',()=>window.print());</script></html>"""
    )
