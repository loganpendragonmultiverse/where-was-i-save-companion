import json
import shutil
import subprocess
from pathlib import Path

import pytest

from where_was_i_save_companion.cli import main
from where_was_i_save_companion.core import build_report, load_cards
from where_was_i_save_companion.editor import render_html


@pytest.mark.parametrize("share_safe", [False, True])
def test_editor_blocks_duplicate_ids_then_exports_reimportable_cards(
    tmp_path: Path, share_safe: bool
) -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("Editor event acceptance requires Node.js")
    data = {
        "version": 1,
        "cards": [
            {
                "id": key,
                "game": key,
                "updated": "2026-10-17",
                "location": "Town",
                "next_step": "Explore",
                "private_note": "private",
            }
            for key in ("a", "b")
        ],
    }
    original = json.dumps(data)
    html = tmp_path / "editor.html"
    html.write_text(render_html(build_report(data, share_safe=share_safe)), encoding="utf-8")
    script = tmp_path / "exercise.cjs"
    script.write_text(
        r"""
const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const html=fs.readFileSync(process.argv[2],'utf8');
const payload=html.match(/id="data">([\s\S]*?)<\/script>/)[1];
const js=html.match(/<\/script><script>([\s\S]*?)<\/script>/)[1];
const nodes=[];
class Element {
  constructor(tag){this.tag=tag;this.events={};this.children=[];nodes.push(this);}
  append(...children){for(const child of children){child.parent=this;this.children.push(child);}}
  addEventListener(event,callback){this.events[event]=callback;}
  replaceChildren(){this.children=[];}
  click(){this.events.click?.();}
}
const ids=Object.fromEntries(['data','privacy','cards','download','print','add','saved'].map(id=>[id,new Element(id)]));
ids.data.textContent=payload;
let blob,downloads=0;const windowEvents={};
vm.runInNewContext(js,{
  document:{getElementById:id=>ids[id],createElement:tag=>new Element(tag),querySelector:()=>null},
  Blob:require('buffer').Blob,URL:{createObjectURL:value=>{blob=value;downloads++;return 'blob:test';},
    revokeObjectURL:()=>{}},setTimeout:()=>{},window:{print:()=>{},addEventListener:(name,callback)=>{windowEvents[name]=callback;}}
});
const inputs=nodes.filter(node=>node.tag==='input'&&node.parent?.textContent==='id');
const edit=value=>{inputs[1].value=value;inputs[1].events.input();};
edit('a');ids.download.click();
assert.equal(downloads,0,'duplicate IDs must not create a download');
assert.match(ids.privacy.textContent,/IDs must be unique/);
edit('   ');ids.download.click();
assert.equal(downloads,0,'blank IDs must still block download');
assert.match(ids.privacy.textContent,/Required card fields/);
edit('corrected');ids.download.click();
assert.equal(downloads,1,'corrected unique ID should download');
let prevented=false;windowEvents.beforeunload({preventDefault:()=>{prevented=true;}});
assert.equal(prevented,true,'download initiation must keep unsaved warning');
assert.equal(ids.saved.disabled,false);
edit('newer');assert.equal(ids.saved.disabled,true,'editing invalidates the pending export');
ids.saved.events.click();prevented=false;windowEvents.beforeunload({preventDefault:()=>{prevented=true;}});
assert.equal(prevented,true,'stale export acknowledgement cannot clear warning');
edit('corrected');ids.download.click();assert.equal(ids.saved.disabled,false);ids.saved.click();
prevented=false;windowEvents.beforeunload({preventDefault:()=>{prevented=true;}});
assert.equal(prevented,false,'explicit saved acknowledgement clears warning');
edit('newer');assert.equal(ids.saved.disabled,true,'later edits invalidate acknowledgement');
prevented=false;windowEvents.beforeunload({preventDefault:()=>{prevented=true;}});
assert.equal(prevented,true,'later edits rearm warning');
blob.text().then(text=>fs.writeFileSync(process.argv[3],text)).catch(error=>{throw error;});
""",
        encoding="utf-8",
    )
    exported = tmp_path / "edited.json"
    result = subprocess.run(
        [node, str(script), str(html), str(exported)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    cards = load_cards(exported)
    assert [card["id"] for card in cards["cards"]] == ["a", "corrected"]
    assert all("private_note" not in card for card in cards["cards"])
    report = tmp_path / "report.json"
    assert main([str(exported), "--format", "json", "--output", str(report)]) == 0
    assert json.loads(report.read_text(encoding="utf-8"))["card_count"] == 2
    assert json.dumps(data) == original
