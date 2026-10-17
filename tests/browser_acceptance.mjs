import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const {chromium,firefox,webkit}=await import(process.env.PLAYWRIGHT_MODULE||'playwright');
const dir=process.env.FIXTURE_DIR;const receipts=[];
for(const [name,engine] of Object.entries({chromium,firefox,webkit})){
 const browser=await engine.launch({headless:true});
 for(const variant of ['normal','share','private','empty']){
 const page=await browser.newPage({acceptDownloads:true});const errors=[];page.on('pageerror',e=>errors.push(e.message));let dialogs=0;let allowRemove=true;page.on('dialog',async d=>{if(d.type()==='beforeunload')dialogs++;if(d.type()==='confirm'&&!allowRemove)await d.dismiss();else await d.accept();});
 await page.goto('file://'+dir+'/where-'+variant+'.html');
 if(variant==='empty')await page.click('#add');
 const first=page.locator('article').first();await first.locator('[name=game]').fill('Renamed Game');assert.equal(await first.locator('h2').textContent(),'Renamed Game');
 await first.locator('[name=goals]').fill('First goal\nSecond goal');assert.equal(await first.locator('[name=goals]').inputValue(),'First goal\nSecond goal');
 await page.emulateMedia({media:'print'});assert.equal(await first.locator('h2').textContent(),'Renamed Game');assert.match(await first.locator('.print-value').allTextContents().then(x=>x.join('|')),/First goal\nSecond goal/);await page.emulateMedia({media:'screen'});
 assert.equal(await page.locator('[name=private_note]').count(),variant==='private'?1:0);assert.equal(await page.locator('[name=screenshot_reference]').count(),variant==='share'?0:1);
 await first.getByRole('button',{name:'Duplicate card',exact:true}).click();assert.equal(await page.locator('article').count(),2);
 const ids=await page.locator('[name=id]').evaluateAll(inputs=>inputs.map(x=>x.value));assert.equal(new Set(ids).size,2);
 let downloads=0;page.on('download',()=>downloads++);await page.locator('article').nth(1).locator('[name=id]').fill(ids[0]);await page.click('#download');assert.equal(downloads,0);assert.match(await page.locator('#privacy').textContent(),/IDs must be unique/);
 let prints=0;await page.evaluate(()=>{window.__prints=0;window.print=()=>window.__prints++;});await page.click('#print');assert.equal(await page.evaluate(()=>window.__prints),0);
 await page.locator('article').nth(1).locator('[name=id]').fill('corrected');await page.locator('article').nth(1).locator('[name=location]').fill(' ');await page.click('#download');assert.equal(downloads,0);assert.match(await page.locator('#privacy').textContent(),/cannot be blank/);await page.locator('article').nth(1).locator('[name=location]').fill('Town');
 await page.click('#add');assert.equal(await page.locator('article').count(),3);allowRemove=false;await page.locator('article').last().getByRole('button',{name:'Remove card',exact:true}).click();assert.equal(await page.locator('article').count(),3);allowRemove=true;await page.locator('article').last().getByRole('button',{name:'Remove card',exact:true}).click();assert.equal(await page.locator('article').count(),2);
 const event=page.waitForEvent('download');await page.click('#download');const path=dir+'/'+name+'-'+variant+'-cards.json';await(await event).saveAs(path);const output=JSON.parse(await fs.readFile(path,'utf8'));assert.equal(output.version,1);assert.equal(output.cards[0].game,'Renamed Game');assert.deepEqual(output.cards[0].goals,['First goal','Second goal']);assert.equal(output.cards.length,2);assert.equal('private_note' in output.cards[0],variant==='private');
 if(variant==='share')for(const card of output.cards){assert.ok(!('screenshot_reference' in card));assert.ok(!('extension' in card));}
 assert.equal(await page.locator('#saved').isDisabled(),false);await first.locator('[name=next_step]').fill('Changed after export');assert.equal(await page.locator('#saved').isDisabled(),true,'editing invalidates pending export acknowledgement');await first.locator('[name=next_step]').fill('Climb');const currentExport=page.waitForEvent('download');await page.click('#download');await(await currentExport).saveAs(dir+'/'+name+'-'+variant+'-current-export.json');assert.equal(await page.locator('#saved').isDisabled(),false);await page.click('#saved');assert.equal(await page.locator('#saved').isDisabled(),true);await page.reload();assert.equal(dialogs,0,'explicit acknowledgement clears dirty warning');await page.locator('article').count();if(variant==='empty')await page.click('#add');await page.evaluate(()=>{window.__prints=0;window.print=()=>window.__prints++;});await page.locator('article').first().locator('[name=next_step]').fill('Unsaved');assert.equal(await page.locator('#saved').isDisabled(),true,'edits disable old export acknowledgement');await page.click('#print');assert.equal(await page.evaluate(()=>window.__prints),1);
 await page.reload();assert.equal(dialogs,1,'printing does not clear dirty warning');
 if(variant==='empty')await page.click('#add');await page.locator('article').first().locator('[name=next_step]').fill('Canceled download');const canceled=page.waitForEvent('download');await page.click('#download');await(await canceled).cancel();assert.equal(await page.locator('#saved').isDisabled(),false);await page.reload();assert.equal(dialogs,2,'canceled download must still warn before reload');
 if(variant==='empty'){await page.click('#add');await page.locator('article').first().getByRole('button',{name:'Remove card',exact:true}).click();const emptyEvent=page.waitForEvent('download');await page.click('#download');await(await emptyEvent).saveAs(dir+'/'+name+'-empty-collection.json');assert.deepEqual(JSON.parse(await fs.readFile(dir+'/'+name+'-empty-collection.json','utf8')).cards,[]);}
 assert.deepEqual(errors,[]);receipts.push({browser:name,variant,passed:true});await page.close();
 }
 const comparison=await browser.newPage();comparison.on('dialog',d=>d.accept());await comparison.goto('file://'+dir+'/where-comparison.html');assert.equal(await comparison.locator('section[aria-label="Snapshot comparison"]').isVisible(),true);await comparison.locator('[name=game]').first().fill('Changed');assert.equal(await comparison.locator('section[aria-label="Snapshot comparison"]').isVisible(),false);await comparison.close();
 await browser.close();
}
await fs.writeFile(dir+'/WHERE-BROWSER.json',JSON.stringify(receipts,null,2));console.log(JSON.stringify(receipts));
