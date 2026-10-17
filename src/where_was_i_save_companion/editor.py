"""Local editable and printable return-to-game cards."""

from __future__ import annotations

import json
from typing import Any


def render_html(report: dict[str, Any]) -> str:
    payload = json.dumps(report).replace("<", "\\u003c").replace("&", "\\u0026")
    return (
        """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Return to game</title>
<style>body{font:17px system-ui;max-width:900px;margin:auto;padding:22px;background:#f5f1e8;color:#203442}article{background:white;border:1px solid #abc;border-radius:12px;padding:20px;margin:20px 0}label{display:block;margin:14px 0}input,textarea,button{font:inherit;padding:9px;box-sizing:border-box;max-width:100%}input,textarea{width:100%}.print-value{display:none;white-space:pre-wrap;overflow-wrap:anywhere}@media print{body{background:white;padding:0;font-size:12pt}article{break-inside:avoid}input,textarea,button{display:none}.print-value{display:block}article{border:1px solid #888}}</style>
<h1>Return to game</h1><p>Review and edit your local cards, then download a new file. Edits stay in this tab until you download a new JSON file; printing does not save them. Add, duplicate or remove cards here. Screenshot references are labels only: no image or save files are opened.</p><p id="privacy" role="status"></p><button id="add">Add card</button><main id="cards"></main><button id="download">Download edited cards</button><button id="saved" disabled>I saved the download</button><button id="print">Print cards</button>
<script type="application/json" id="data">"""
        + payload
        + r"""</script><script>
const data=JSON.parse(document.getElementById('data').textContent);const omitted=data.share_review?.omitted??{};document.getElementById('privacy').textContent=(data.share_review?.share_safe?'Share-safe export. ':'Local card export. ')+`Omitted ${omitted.private_notes??0} private notes and ${omitted.screenshot_references??0} screenshot references. Review retained text before sharing.`;
let dirty=false,exportPending=false;
function changed(){dirty=true;exportPending=false;document.getElementById('saved').disabled=true;const comparison=document.querySelector('section[aria-label="Snapshot comparison"]');if(comparison){comparison.hidden=true;document.getElementById('privacy').textContent='Cards changed. Download them and regenerate the comparison with the CLI; the original comparison is hidden.';}}
function uniqueId(base='card'){const ids=new Set(data.cards.map(card=>card.id));let id=base,index=2;while(ids.has(id)){id=base+'-'+index++;}return id;}
function renderCards(){document.getElementById('cards').replaceChildren();for(const card of data.cards){const article=document.createElement('article');const title=document.createElement('h2');title.textContent=card.game;article.append(title);
const fields=['id','game','updated','location','next_step','last_played','goals','controls','story_context','loose_ends','spoiler_boundary','save_catalog_id'];
if(!data.share_review?.share_safe)fields.push('screenshot_reference');if(data.share_review?.include_private||'private_note' in card)fields.push('private_note');
for(const key of fields){const list=['goals','controls','story_context','loose_ends'].includes(key);const label=document.createElement('label');label.textContent=key.replaceAll('_',' ')+(list?' (one per line)':'');
const input=document.createElement(list||key==='private_note'?'textarea':'input');input.name=key;if(key==='last_played')input.type='date';input.value=list?(card[key]??[]).join('\n'):(card[key]??'');const printed=document.createElement('span');printed.className='print-value';printed.textContent=input.value;
input.addEventListener('input',()=>{if(list)card[key]=input.value.split('\n').filter(Boolean);else if(input.value===''&&!['id','game','updated','location','next_step'].includes(key))delete card[key];else card[key]=input.value;printed.textContent=input.value;if(key==='game')title.textContent=input.value;changed();});label.append(input,printed);article.append(label);}const duplicate=document.createElement('button');duplicate.textContent='Duplicate card';duplicate.addEventListener('click',()=>{const copy=JSON.parse(JSON.stringify(card));copy.id=uniqueId(card.id+'-copy');data.cards.splice(data.cards.indexOf(card)+1,0,copy);changed();renderCards();});
const remove=document.createElement('button');remove.textContent='Remove card';remove.addEventListener('click',()=>{if(!window.confirm('Remove this card from the edited file? Download first if you want to keep a copy.'))return;data.cards.splice(data.cards.indexOf(card),1);changed();renderCards();});article.append(duplicate,remove);document.getElementById('cards').append(article);}}
renderCards();
document.getElementById('add').addEventListener('click',()=>{data.cards.push({id:uniqueId(),game:'New game',updated:new Date().toISOString().slice(0,10),location:'Add location',next_step:'Add next step'});changed();renderCards();});
function validateCards(){for(const card of data.cards)if(['id','game','updated','location','next_step'].some(key=>!card[key]?.trim())){document.getElementById('privacy').textContent='Required card fields cannot be blank.';return false;}
const seen=new Set();for(const card of data.cards){if(seen.has(card.id)){document.getElementById('privacy').textContent='Card IDs must be unique. Change the duplicate ID before printing or downloading.';return false;}seen.add(card.id);}
return true;}
document.getElementById('download').addEventListener('click',()=>{if(!validateCards())return;
const url=URL.createObjectURL(new Blob([JSON.stringify({version:1,cards:data.cards},null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='edited-return-cards.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);exportPending=true;document.getElementById('saved').disabled=false;document.getElementById('privacy').textContent='Download started. Save the JSON file, then choose I saved the download. Unsaved-edit warnings stay active until you acknowledge this export; the original is unchanged.';});document.getElementById('print').addEventListener('click',()=>{if(validateCards())window.print();});
document.getElementById('saved').addEventListener('click',()=>{if(!exportPending)return;dirty=false;exportPending=false;document.getElementById('saved').disabled=true;document.getElementById('privacy').textContent='You marked the current export as saved. Keep that JSON file; further edits will warn before leaving.';});
window.addEventListener('beforeunload',event=>{if(dirty){event.preventDefault();event.returnValue='';}});</script></html>"""
    )
