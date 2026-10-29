/* CodeAlpha Power BI companion previews — vanilla JS, no external libraries. */
(() => {
  const cfg = document.body.dataset;
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  function parseCSV(text) {
    const rows=[]; let row=[], cell="", quoted=false;
    for(let i=0;i<text.length;i++){
      const c=text[i], n=text[i+1];
      if(c === '"' && quoted && n === '"'){cell+='"';i++;}
      else if(c === '"'){quoted=!quoted;}
      else if(c === ',' && !quoted){row.push(cell);cell="";}
      else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&n==='\n')i++;row.push(cell);if(row.some(v=>v.trim()!==""))rows.push(row);row=[];cell="";}
      else cell+=c;
    }
    row.push(cell); if(row.some(v=>v.trim()!=="")) rows.push(row);
    if(!rows.length)return [];
    const headers=rows.shift().map(h=>h.trim());
    return rows.map(r=>Object.fromEntries(headers.map((h,i)=>[h,(r[i]??"").trim()])));
  }
  const num = v => {const n=Number(String(v??"").replace(/[$,%₹,]/g,""));return Number.isFinite(n)&&String(v??"").trim()!==""?n:null;};
  const fmt = (n,field) => {
    if(n===null||!Number.isFinite(n))return "—";
    if(/salary|revenue|expense|cash|price|rent|budget/i.test(field)) return new Intl.NumberFormat("en-IN",{maximumFractionDigits:0,notation:Math.abs(n)>=10000000?"compact":"standard"}).format(n);
    return new Intl.NumberFormat("en-IN",{maximumFractionDigits:1}).format(n);
  };
  function renderChart(el, rows, group, metric, label) {
    const groups={};
    rows.forEach(r=>{const k=r[group]||"Unknown",v=num(r[metric]);if(v===null)return;(groups[k]??=[]).push(v);});
    const entries=Object.entries(groups).map(([k,vs])=>[k,vs.reduce((a,b)=>a+b,0)/vs.length]).sort((a,b)=>b[1]-a[1]).slice(0,10);
    if(!entries.length){el.innerHTML='<p class="muted">No numeric values available for this chart.</p>';return;}
    const W=700,H=300,left=180,right=30,top=18,bottom=24,plot=W-left-right,rowH=(H-top-bottom)/entries.length,max=Math.max(...entries.map(x=>x[1]))||1;
    let svg='<svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="'+esc(label)+'">';
    entries.forEach(([name,value],i)=>{const y=top+i*rowH+rowH*.18,w=plot*value/max,h=rowH*.58;svg+='<text x="'+(left-10)+'" y="'+(y+h*.72)+'" text-anchor="end" class="axis">'+esc(name.length>23?name.slice(0,21)+"…":name)+'</text><rect x="'+left+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="4" class="bar"/><text x="'+Math.min(left+w+7,W-55)+'" y="'+(y+h*.72)+'" class="value">'+esc(fmt(value,metric))+'</text>';});
    svg+='</svg><p class="chart-note">Bars show the average '+esc(metric)+' per '+esc(group)+' in the sample.</p>';el.innerHTML=svg;
  }
  function render(rows){
    if(!rows.length){$("status").textContent="No data rows found.";return;}
    $("status").textContent=rows.length+" rows loaded from the project CSV. Sample data only.";
    const kpis=(cfg.kpis||"").split("|").filter(Boolean);
    $("kpis").innerHTML=kpis.map(field=>{const vals=rows.map(r=>num(r[field])).filter(v=>v!==null);const value=vals.length?vals.reduce((a,b)=>a+b,0)/((/average|score|pct|rating|satisfaction/i.test(field))?vals.length:1):null;return '<section class="kpi"><div class="kpi-label">'+esc(field.replace(/([a-z])([A-Z])/g,"$1 $2"))+'</div><div class="kpi-value">'+esc(fmt(value,field))+'</div><div class="kpi-foot">'+( /average|score|pct|rating|satisfaction/i.test(field)?"average":"sample total / summary")+'</div></section>';}).join("");
    renderChart($("chartA"),rows,cfg.group,cfg.metricA,cfg.chartA);
    renderChart($("chartB"),rows,cfg.group,cfg.metricB,cfg.chartB);
    const headers=Object.keys(rows[0]);
    $("search").addEventListener("input",()=>table(rows,headers));
    table(rows,headers);
  }
  function table(rows,headers){
    const q=$("search").value.toLowerCase();
    const filtered=rows.filter(r=>headers.some(h=>String(r[h]??"").toLowerCase().includes(q))).slice(0,100);
    $("dataTable").innerHTML='<table><thead><tr>'+headers.map(h=>'<th>'+esc(h)+'</th>').join("")+'</tr></thead><tbody>'+filtered.map(r=>'<tr>'+headers.map(h=>'<td>'+esc(r[h])+'</td>').join("")+'</tr>').join("")+'</tbody></table><p class="muted">Showing '+filtered.length+' matching rows (maximum 100 shown).</p>';
  }
  fetch(cfg.csv).then(r=>{if(!r.ok)throw new Error("Could not load CSV ("+r.status+"). Open this through a web server or GitHub Pages.");return r.text();}).then(parseCSV).then(render).catch(e=>{$("status").textContent=e.message;});
})();