const results=document.querySelector('#results');
if(results){
 const q=(new URLSearchParams(location.search).get('q')||'').trim();
 fetch('/search-index.json').then(r=>r.json()).then(entries=>{
  const matches=q?entries.filter(e=>q.toLowerCase().split(/\s+/).every(t=>(e.title+' '+e.text).toLowerCase().includes(t))):[];
  results.textContent=q?(matches.length?'Results for '+q:'No results for '+q):'Enter a search term above.';
  const list=document.createElement('ul');
  for(const item of matches){const li=document.createElement('li'),a=document.createElement('a');a.href=item.url;a.textContent=item.title;li.append(a);list.append(li);}
  if(matches.length) results.append(list);
 }).catch(()=>{results.textContent='Search is temporarily unavailable.'});
}
const form=document.querySelector('#contact');
form?.addEventListener('submit',async e=>{
 e.preventDefault();
 const status=document.querySelector('#form-status'),button=form.querySelector('button');
 button.disabled=true;status.textContent='Sending…';
 try{
  const reply=await fetch(form.action,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(form)))});
  const result=await reply.json();status.textContent=result.message;
  if(reply.ok) form.reset();
 }catch{status.textContent='Your message could not be sent. Please try again.';}
 finally{button.disabled=false;}
});
