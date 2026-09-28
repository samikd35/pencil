// Execute the shipped menu script against a small DOM fixture: no browser or network access.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
class Element {
  constructor(tag){this.tag=tag;this.children=[];this.dataset={};this.attrs={};this.textContent='';this.hidden=false;this.className='';this.value='';this.classList={toggle:(name,on)=>{const names=new Set(this.className.split(' ').filter(Boolean));on?names.add(name):names.delete(name);this.className=[...names].join(' ');}};}
  append(...children){this.children.push(...children);}
  replaceChildren(...children){this.children=children;}
  setAttribute(k,v){this.attrs[k]=v;}
  focus(){this.focused=true;}
  select(){this.selected=true;}
}
const ids=Object.fromEntries(['gallery','count','selection','chosenName','choice','notice','copyChoice'].map(id=>[id,new Element('div')]));
const filters=['All','Character','Finish','Presentation'].map(filter=>{const e=new Element('button');e.dataset.filter=filter;return e;});
const document={createElement:tag=>new Element(tag),getElementById:id=>{assert.ok(ids[id],id);return ids[id];},querySelectorAll:selector=>{if(selector==='[data-filter]')return filters;if(selector==='.card')return ids.gallery.children;throw Error('Unexpected selector '+selector);}};
let copied='';const navigator={clipboard:{writeText:async text=>{copied=text;}}};
const html=fs.readFileSync(path.join(__dirname,'gallery.html'),'utf8');
assert.ok(!html.includes('/* CATALOG_DATA */'));assert.ok(!/<video\b/i.test(html));
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
vm.runInNewContext(script,{document,navigator});
const walk=e=>[e,...e.children.flatMap(walk)];
async function check(){
  assert.equal(ids.gallery.children.length,19);
  for(const image of ids.gallery.children.flatMap(walk).filter(e=>e.tag==='img')){
    assert.ok(image.alt.length>20);assert.ok(fs.existsSync(path.join(__dirname,image.src)));
  }
  const catalog=JSON.parse(fs.readFileSync(path.join(__dirname,'catalog.json'),'utf8'));
  for(const card of ids.gallery.children){
    const ref=catalog.options.find(o=>o.id===card.dataset.id).reference;
    assert.ok(walk(card).some(e=>e.tag==='a'&&e.href===ref.source_url),'Missing source link');
    assert.ok(walk(card).some(e=>e.textContent===ref.credit),'Missing visible credit');
    for(const target of ref.quality_targets)assert.ok(walk(card).some(e=>e.tag==='li'&&e.textContent===target),'Missing quality target');
  }
  filters[1].onclick();assert.equal(ids.gallery.children.length,10);
  filters[2].onclick();assert.equal(ids.gallery.children.length,7);
  filters[3].onclick();assert.equal(ids.gallery.children.length,2);
  let card=ids.gallery.children.find(c=>c.dataset.id==='parallax');walk(card).find(e=>e.tag==='button').onclick();
  assert.equal(ids.selection.hidden,false);assert.ok(ids.choice.value.includes('"parallax"'));
  assert.ok(ids.choice.value.includes('Aim for the visual quality'));
  assert.ok(ids.choice.value.includes('quality targets'));
  assert.ok(card.className.includes('selected'));
  filters[0].onclick();assert.equal(ids.gallery.children.length,19);
  assert.ok(ids.gallery.children.find(c=>c.dataset.id==='parallax').className.includes('selected'));
  await ids.copyChoice.onclick();assert.equal(copied,ids.choice.value);
  navigator.clipboard.writeText=async()=>{throw Error('Clipboard unavailable in local-file context');};
  await ids.copyChoice.onclick();assert.equal(ids.choice.selected,true);
  assert.ok(ids.notice.textContent.includes('Command+C'));
  console.log('PASS: shipped offline menu creates 19 accessible image cards; category filters, selected state, prepared message, clipboard and manual-copy fallback work in a DOM fixture. Browser layout/playback are not covered.');
}
check().catch(error=>{console.error(error);process.exitCode=1;});
