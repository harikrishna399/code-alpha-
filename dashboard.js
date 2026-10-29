/* CodeAlpha browser previews; no external libraries required. */
(() => {
  const cfg = document.body.dataset;
  const $ = id => document.getElementById(id);
  const esc = value => String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
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
  const num = v => {const n=Number(String(v??"").replace(/[₹$,% ,]/g,""));return Number.isFinite(n)&&String(v??"").trim()!==""?n:null;};
  const latestFields = ["ClosingCash","TotalAssets","TotalLiabilities","ShareholdersEquity","ClosingHeadcount","Cash","PlannedHeadcount"];
  const avgField = field => /average|score|pct|rating|satisfaction|utilization|policyRate/i.test(field);
  const fmt = (n,field) => {
    if(n===null||!Number.isFinite(n))return "—";
    if(/revenue|income|profit|expense|cash|assets|liabilities|equity|salary|price|rent|budget|cost|flow/i.test(field))
      return "₹"+new Intl.NumberFormat("en-IN",{maximumFractionDigits:0}).format(n);
    if(/pct|yield|rate/i.test(field))return new Intl.NumberFormat("en-IN",{maximumFractionDigits:2}).format(n)+"%";
    return new Intl.NumberFormat("en-IN",{maximumFractionDigits:2}).format(n);
  };
  function aggregate(rows,field) {
    const vals=rows.map(r=>num(r[field])).filter(v=>v!==null);
    if(!vals.length)return null;
    if(latestFields.includes(field)){
      const dateKey = ["Date","Month","HireDate","AcademicYear"].find(k=>rows.some(r=>r[k]));
      if(dateKey){
        const sorted=rows.filter(r=>num(r[field])!==null).sort((a,b)=>String(a[dateKey]).localeCompare(String(b[dateKey])));
        if(sorted.length)return num(sorted[sorted.length-1][field]);
      }
      return vals[vals.length-1];
    }
    if(avgField(field))return vals.reduce((a,b)=>a+b,0)/vals.length;
    return vals.reduce((a,b)=>a+b,0);
  }
  function renderChart(el, rows, group, metric, label) {
    const groups={};
    rows.forEach(r=>{const k=r[group]||"Unknown",v=num(r[metric]);if(v===null)return;(groups[k]??=[]).push(v);});
    let entries=Object.entries(groups).map(([k,vs])=>[k,vs.reduce((a,b)=>a+b,0)/vs.length]);
    entries.sort((a,b)=> {
      if(/^\d{4}-\d{2}/.test(a[0]) && /^\d{4}-\d{2}/.test(b[0])) return a[0].localeCompare(b[0]);
      return b[1]-a[1];
    });
    if(entries.length>18)entries=entries.slice(0,18);
    if(!entries.length){el.innerHTML='<p class="muted">No numeric values available for this chart.</p>';return;}
    const W=700,H=Math.max(210,Math.min(500,entries.length*28+30)),left=180,right=50,top=12,bottom=18,plot=W-left-right,rowH=(H-top-bottom)/entries.length,max=Math.max(...entries.map(x=>Math.abs(x[1])))||1;
    let svg='<svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="'+esc(label)+'">';
    entries.forEach(([name,value],i)=>{const y=top+i*rowH+rowH*.17,w=plot*Math.abs(value)/max,h=Math.max(5,rowH*.6);svg+='<text x="'+(left-10)+'" y="'+(y+h*.72)+'" text-anchor="end" class="axis">'+esc(name.length>24?name.slice(0,22)+"…":name)+'</text><rect x="'+left+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="4" class="bar"/><text x="'+Math.min(left+w+7,W-58)+'" y="'+(y+h*.72)+'" class="value">'+esc(fmt(value,metric))+'</text>';});
    svg+='</svg><p class="chart-note">'+esc(label||"Average "+metric)+" · grouped by "+esc(group)+'.</p>';el.innerHTML=svg;
  }
  function table(rows,headers){
    const q=$("search").value.toLowerCase();
    const filtered=rows.filter(r=>headers.some(h=>String(r[h]??"").toLowerCase().includes(q))).slice(0,150);
    $("dataTable").innerHTML='<table><thead><tr>'+headers.map(h=>'<th>'+esc(h.replace(/([a-z])([A-Z])/g,"$1 $2"))+'</th>').join("")+'</tr></thead><tbody>'+filtered.map(r=>'<tr>'+headers.map(h=>'<td>'+esc(r[h])+'</td>').join("")+'</tr>').join("")+'</tbody></table><p class="muted">Showing '+filtered.length+' matching rows (maximum 150 shown).</p>';
  }
  function render(rows){
    if(!rows.length){$("status").textContent="No data rows found.";return;}
    $("status").textContent=rows.length+" rows loaded from the synthetic project CSV. Demo data only.";
    const kpis=(cfg.kpis||"").split("|").filter(Boolean);
    $("kpis").innerHTML=kpis.map(field=>{
      const value=aggregate(rows,field);
      const isAverage=avgField(field);
      const label=field.replace(/([a-z])([A-Z])/g,"$1 $2");
      return '<section class="kpi"><div class="kpi-label">'+esc(label)+'</div><div class="kpi-value">'+esc(fmt(value,field))+'</div><div class="kpi-foot">'+(latestFields.includes(field)?"latest sample period":isAverage?"sample average":"sample total")+'</div></section>';
    }).join("");
    renderChart($("chartA"),rows,cfg.group,cfg.metricA,cfg.chartA);
    renderChart($("chartB"),rows,cfg.group,cfg.metricB,cfg.chartB);
    const headers=Object.keys(rows[0]);
    $("search").addEventListener("input",()=>table(rows,headers));
    table(rows,headers);
  }
  fetch(cfg.csv).then(r=>{if(!r.ok)throw new Error("Could not load CSV ("+r.status+"). Serve this page over HTTP(S), for example through GitHub Pages.");return r.text();}).then(parseCSV).then(render).catch(e=>{$("status").textContent=e.message;});
})();