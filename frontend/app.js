import {BrowserProvider,JsonRpcProvider,Contract,formatEther,parseEther,isAddress} from 'ethers';
import {CID} from 'multiformats/cid';
const $=id=>document.getElementById(id), fmt=v=>Number(formatEther(v)).toLocaleString('fr-FR',{maximumFractionDigits:4});
const short=v=>v?`${v.slice(0,6)}…${v.slice(-4)}`:'—';
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const labels=['En cours','Réussie','Échouée','Annulée'];
let cfg,provider,contracts,account,signer,walletProvider,chainTime=0,filter='all',campaignLimit=24,proposalLimit=24,busy=false;
let campaignData=[];const metaCache=new Map();
function notice(message,error=false){$('notice').hidden=false;$('notice').className=`notice${error?' error':''}`;$('notice').textContent=message;}
function switchTab(tab){document.querySelectorAll('.view').forEach(e=>e.classList.toggle('active',e.id===tab));document.querySelectorAll('.nav').forEach(e=>e.classList.toggle('active',e.dataset.tab===tab));$('page-label').textContent=document.querySelector(`[data-tab="${tab}"] span`).textContent;}
document.querySelectorAll('.nav').forEach(b=>b.onclick=()=>switchTab(b.dataset.tab));
document.querySelectorAll('[data-close]').forEach(b=>b.onclick=()=>b.closest('dialog').close());
document.querySelectorAll('.filter').forEach(b=>b.onclick=()=>{filter=b.dataset.filter;document.querySelectorAll('.filter').forEach(x=>x.classList.toggle('selected',x===b));renderCampaigns();});
async function connect(){
 if(!window.ethereum)throw Error('Installez MetaMask pour signer. La lecture reste accessible sans portefeuille.');
 walletProvider=new BrowserProvider(window.ethereum);await walletProvider.send('eth_requestAccounts',[]);
 const net=await walletProvider.getNetwork();if(Number(net.chainId)!==cfg.chainId)throw Error(`Choisissez le réseau ${cfg.network}, chainId ${cfg.chainId}, dans MetaMask.`);
 signer=await walletProvider.getSigner();account=await signer.getAddress();$('connect').textContent=short(account);$('campaign-beneficiary').value=account;await refresh();
}
$('connect').onclick=()=>connect().catch(e=>notice(e.message,true));
window.ethereum?.on?.('accountsChanged',()=>location.reload());window.ethereum?.on?.('chainChanged',()=>location.reload());
async function write(key,method,args=[],options={}){
 if(busy)return;busy=true;
 const buttons=[...document.querySelectorAll('button')];buttons.forEach(b=>b.disabled=true);
 try{
  if(!signer)await connect();
  const net=await walletProvider.getNetwork();if(Number(net.chainId)!==cfg.chainId)throw Error('Réseau du portefeuille incorrect.');
  notice('Vérifiez puis confirmez la transaction dans MetaMask.');
  const tx=await contracts[key].connect(signer)[method](...args,options);notice(`Transaction envoyée : ${tx.hash}`);
  await tx.wait();notice(`Transaction confirmée : ${tx.hash}`);await refresh();return true;
 }catch(e){notice(e.shortMessage||e.reason||e.message,true);return false;}
 finally{busy=false;buttons.forEach(b=>b.disabled=false);}
}
async function metadata(cid){
 if(metaCache.has(cid))return metaCache.get(cid);
 let data={name:'Métadonnées indisponibles',description:'Le CID reste vérifiable sur la blockchain. Démarrez le nœud IPFS local ou vérifiez sa disponibilité publique.',category:'Projet'};
 try{
  CID.parse(cid);
  for(const base of ['http://127.0.0.1:8787/ipfs/','https://ipfs.io/ipfs/']){
   try{const r=await fetch(base+encodeURIComponent(cid),{signal:AbortSignal.timeout(3500)});if(!r.ok)continue;
    const text=await r.text();if(text.length>65536)continue;const m=JSON.parse(text);
    data={name:String(m.name||'Sans titre').slice(0,80),description:String(m.description||'').slice(0,2000),category:String(m.category||'Projet étudiant').slice(0,50)};break;
   }catch{}
  }
 }catch{}
 metaCache.set(cid,data);return data;
}
async function refresh(){
 const block=await provider.getBlock('latest');chainTime=block.timestamp;
 const [count,escrow,paused,pcount]=await Promise.all([contracts.core.campaignCount(),contracts.core.totalEscrow(),contracts.core.paused(),contracts.dao.proposalCount()]);
 campaignData=await Promise.all(Array.from({length:Math.min(Number(count),campaignLimit)},async(_,id)=>{
  const [c,status]=await Promise.all([contracts.core.campaigns(id),contracts.core.status(id)]);
  const m=await metadata(c.metadataCID);const contribution=account?await contracts.core.contributions(id,account):0n;
  const approvals=await contracts.guard.approvals(await contracts.guard.withdrawalKey(cfg.addresses.core,id,c.beneficiary,c.escrow));
  return {id,c,status:Number(status),m,contribution,approvals:Number(approvals)};
 }));
 $('stat-raised').textContent=fmt(campaignData.reduce((a,x)=>a+x.c.raised,0n))+' ETH';
 if(Number(count)>campaignLimit)$('stat-raised').title='Somme des campagnes chargées uniquement';
 $('stat-escrow').textContent=fmt(escrow)+' ETH';$('stat-count').textContent=count.toString();$('stat-votes').textContent=account?fmt(await contracts.token.getVotes(account)):'—';
 $('network').textContent=`● ${cfg.network==='localhost'?'Hardhat local':cfg.network} · ${cfg.chainId}`;
 $('more-campaigns').hidden=Number(count)<=campaignLimit;renderCampaigns();
 $('system-state').innerHTML=`<p><span class="pill${paused?' cancel':''}">${paused?'En pause':'Opérationnel'}</span> Bloc ${block.number} · ${new Date(chainTime*1000).toLocaleString('fr-FR')} (horloge de la chaîne)</p><p>Solde : <b>${fmt(await provider.getBalance(cfg.addresses.core))} ETH</b> · Engagements : <b>${fmt(escrow)} ETH</b></p><p>La pause suspend contributions, retraits et remboursements. Un gel voté reste possible.</p>`;
 $('addresses').innerHTML=Object.entries(cfg.addresses).map(([k,a])=>`<div><b>${esc(k)}</b> ${esc(a)}</div>`).join('');
 $('signers').innerHTML=cfg.signers.map((a,i)=>`<div>Signataire ${i+1} : ${esc(a)}</div>`).join('');
 await renderProposals(Number(pcount));
}
function renderCampaigns(){
 const data=campaignData.filter(x=>filter==='all'||String(x.status)===filter);
 $('campaign-list').innerHTML=data.length?data.map(({id,c,status,m,contribution,approvals})=>{
  const percent=Number(c.raised*10000n/c.goal)/100;const days=Math.max(0,Math.ceil((Number(c.deadline)-chainTime)/86400));
  return `<article class="card"><div class="card-art art-${id%4}"><span class="pill ${status===3?'cancel':''}">${labels[status]}${c.withdrawn?' · Versée':''}</span><span class="art-symbol">${['☼','≈','◈','↗'][id%4]}</span><span class="tag-id">INITIATIVE / ${String(id+1).padStart(2,'0')}</span></div><div class="card-body"><span class="category">${esc(m.category)}</span><h3>${esc(m.name)}</h3><p class="description">${esc(m.description)}</p><div class="progress"><span style="width:${Math.min(100,percent)}%"></span></div><div class="funding-row"><span><b>${fmt(c.raised)} ETH</b> collectés</span><span>sur ${fmt(c.goal)} ETH</span></div><div class="card-bottom"><span>${status===0?`${days} j restants`:`Campagne #${id}`}</span><span>${percent.toLocaleString('fr-FR',{maximumFractionDigits:1})} % de l’objectif</span></div><div class="card-actions">${status===0?`<input aria-label="Montant campagne ${id}" class="amount" id="amount-${id}" placeholder="ETH" type="number" min="0.000001" step="any"><button class="primary" data-contribute="${id}">Contribuer ↗</button>`:''}${[2,3].includes(status)&&contribution>0n?`<button class="primary" data-refund="${id}">Récupérer ${fmt(contribution)} ETH</button>`:''}${c.releaseApproved&&!c.withdrawn&&!c.cancelled?`<button class="primary" data-withdraw="${id}">Retirer les fonds</button>`:''}</div><div class="card-bottom" style="margin-top:12px"><span>Séquestre : ${fmt(c.escrow)} ETH</span><span>DAO : ${c.releaseApproved?'accordée':'requise'}</span></div>${c.escrow>parseEther('1')?`<small>Multisig : ${approvals}/2 approbations sur le montant actuel</small>`:''}<div class="card-actions"><button class="text-button" data-propose="${id}">Proposer une décision →</button><a class="text-button" href="http://127.0.0.1:8787/ipfs/${encodeURIComponent(c.metadataCID)}" target="_blank" rel="noopener">Métadonnées IPFS ↗</a></div><small class="mono" title="${esc(c.beneficiary)}">Bénéficiaire ${short(c.beneficiary)}</small></div></article>`;
 }).join(''):'<div class="empty">Aucune campagne dans cette catégorie.</div>';
 document.querySelectorAll('[data-contribute]').forEach(b=>b.onclick=()=>{try{const amount=parseEther($(`amount-${b.dataset.contribute}`).value);if(amount<=0n)throw Error('Saisissez un montant strictement positif.');write('core','contribute',[b.dataset.contribute],{value:amount});}catch(e){notice(e.message,true);}});
 document.querySelectorAll('[data-refund]').forEach(b=>b.onclick=()=>write('core','refund',[b.dataset.refund]));
 document.querySelectorAll('[data-withdraw]').forEach(b=>b.onclick=()=>write('core','withdrawFunds',[b.dataset.withdraw]));
 document.querySelectorAll('[data-propose]').forEach(b=>b.onclick=()=>{$('proposal-campaign').value=b.dataset.propose;$('propose-dialog').showModal();});
}
async function renderProposals(count){
 $('more-proposals').hidden=count<=proposalLimit;
 const all=await Promise.all(Array.from({length:Math.min(count,proposalLimit)},async(_,id)=>{
  const p=await contracts.dao.proposals(id);const voted=account?await contracts.dao.hasVoted(id,account):false;
  const weight=account?await contracts.token.getPastVotes(account,p.snapshotBlock):0n;
  const total=p.yes+p.no;const passed=total>=p.quorum&&p.yes>p.no;const closed=chainTime>=Number(p.deadline);
  const state=p.executed?'Exécutée':!closed?'Vote ouvert':!passed?'Rejetée':chainTime<Number(p.executableAt)?'Délai de sécurité':'Exécutable';
  const yes=total?Number(p.yes*100n/total):0;
  return `<article class="proposal"><span class="pill">${state}</span><h3>${p.action===0n?'Débloquer les fonds':'Geler la campagne'} #${p.campaignId}</h3><p>Proposition #${id} · Snapshot au bloc ${p.snapshotBlock}<br>Clôture : ${new Date(Number(p.deadline)*1000).toLocaleString('fr-FR')}<br>Exécution au plus tôt : ${new Date(Number(p.executableAt)*1000).toLocaleString('fr-FR')}</p><div class="vote-bar"><span class="yes" style="width:${yes}%"></span><span class="no" style="width:${total?100-yes:0}%"></span></div><div class="vote-detail"><span>Pour : ${fmt(p.yes)} CFD</span><span>Contre : ${fmt(p.no)} CFD</span></div><p>Participation : ${fmt(total)} / ${fmt(p.quorum)} CFD requis<br>Vos voix figées : ${account?fmt(weight):'connectez-vous'} ${voted?'· Vote enregistré':''}</p><div class="actions">${!closed&&!voted?`<button class="primary" data-vote="${id}" data-support="true">Voter pour</button><button class="secondary" data-vote="${id}" data-support="false">Voter contre</button>`:''}${state==='Exécutable'?`<button class="primary" data-execute="${id}">Exécuter la décision</button>`:''}</div></article>`;
 }));
 $('proposal-list').innerHTML=all.join('')||'<div class="empty">Aucune proposition. Les détenteurs d’au moins 1 CFD peuvent en créer une.</div>';
 document.querySelectorAll('[data-vote]').forEach(b=>b.onclick=()=>write('dao','vote',[b.dataset.vote,b.dataset.support==='true']));
 document.querySelectorAll('[data-execute]').forEach(b=>b.onclick=()=>write('dao','execute',[b.dataset.execute]));
}
$('open-create').onclick=()=>$('create-dialog').showModal();$('open-propose').onclick=()=>$('propose-dialog').showModal();
$('more-campaigns').onclick=()=>{campaignLimit+=24;refresh().catch(e=>notice(e.message,true));};$('more-proposals').onclick=()=>{proposalLimit+=24;refresh().catch(e=>notice(e.message,true));};
$('create-form').onsubmit=async e=>{
 e.preventDefault();try{
  const beneficiary=$('campaign-beneficiary').value.trim();if(!isAddress(beneficiary))throw Error('Adresse du bénéficiaire invalide.');
  let cid=$('campaign-cid').value.trim();
  if(!cid){notice('Enregistrement des métadonnées sur le nœud IPFS local…');const r=await fetch('http://127.0.0.1:8787/add',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:$('campaign-name').value,description:$('campaign-description').value,category:'Projet étudiant'}),signal:AbortSignal.timeout(10000)});if(!r.ok)throw Error(await r.text());cid=(await r.json()).cid;}
  CID.parse(cid);if(await write('core','createCampaign',[parseEther($('campaign-goal').value),Number($('campaign-days').value)*86400,beneficiary,cid]))$('create-dialog').close();
 }catch(e){notice(e.message,true);}
};
$('propose-form').onsubmit=async e=>{e.preventDefault();if(await write('dao','propose',[$('proposal-campaign').value,Number($('proposal-action').value)]))$('propose-dialog').close();};
$('approval-form').onsubmit=async e=>{e.preventDefault();try{const id=$('approval-id').value,c=await contracts.core.campaigns(id);if(Number(id)>=Number(await contracts.core.campaignCount()))throw Error('Campagne inconnue');await write('guard','setApproval',[cfg.addresses.core,id,c.beneficiary,c.escrow,e.submitter.value==='approve']);}catch(e){notice(e.message,true);}};
$('pause').onclick=()=>write('core','pause');$('unpause').onclick=()=>write('core','unpause');
async function anomalies(){
 try{const r=await fetch('/anomalies.json');if(!r.ok)throw Error();const d=await r.json();
  const matches=d.source.chainId===cfg.chainId&&d.source.core.toLowerCase()===cfg.addresses.core.toLowerCase();if(!matches)throw Error('Rapport d’un autre déploiement : relancez l’export.');
  $('anomalies').innerHTML=`<div class="panel"><h2>${d.event_count} contributions analysées</h2><p>Historique limité aux blocs ${d.source.fromBlock}–${d.source.toBlock}. Relancez l’export après de nouvelles transactions.</p></div>`+d.alerts.map(a=>`<div class="panel"><span class="pill cancel">${esc(a.level)} · Campagne #${a.campaign}</span><h2 style="margin-top:15px">${esc(a.rule)}</h2><p>${esc(a.message)}</p><div class="mono">${Object.entries(a.evidence).map(([k,v])=>`${esc(k)} : ${esc(v)}`).join('<br>')}</div></div>`).join('');
 }catch{$('anomalies').innerHTML='<div class="empty">Aucun rapport compatible disponible. Exécutez l’export des événements et le script Python.</div>';}
}
async function init(){
 const r=await fetch('/config.json');if(!r.ok)throw Error('Déployez les contrats pour générer config.json.');cfg=await r.json();
 if(cfg.readRpc)provider=new JsonRpcProvider(cfg.readRpc);else{if(!window.ethereum)throw Error('Sur ce réseau, MetaMask est nécessaire pour lire les contrats.');provider=new BrowserProvider(window.ethereum);}
 if(Number((await provider.getNetwork()).chainId)!==cfg.chainId)throw Error('Réseau RPC incompatible avec le déploiement.');
 if(await provider.getCode(cfg.addresses.core)==='0x')throw Error('Contrats absents : le nœud a peut-être redémarré. Relancez le déploiement.');
 contracts=Object.fromEntries(Object.keys(cfg.addresses).map(k=>[k,new Contract(cfg.addresses[k],cfg.abis[k],provider)]));
 await refresh();await anomalies();setInterval(()=>{if(!busy)refresh().catch(e=>notice('Lecture impossible : '+e.message,true));},20000);
}
init().catch(e=>{notice(e.message,true);$('network').textContent='Réseau indisponible';$('campaign-list').innerHTML='<div class="empty">Le nœud blockchain doit être démarré et les contrats déployés. Consultez le README du projet.</div>';});
