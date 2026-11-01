const {ethers,network}=require('hardhat');const fs=require('fs');
const E=ethers.parseEther;
async function main(){
 if((await ethers.provider.getNetwork()).chainId!==31337n)throw Error('Démonstration réservée à Hardhat local');
 const cfg=JSON.parse(fs.readFileSync('deployments/localhost.json'));const [admin,alice,bob,beneficiary,s1,s2]=await ethers.getSigners();
 const core=await ethers.getContractAt('CrowdfundingCore',cfg.addresses.core),dao=await ethers.getContractAt('FundingDAO',cfg.addresses.dao),guard=await ethers.getContractAt('TreasuryGuard',cfg.addresses.guard);
 if(await core.campaignCount()!==0n)throw Error('Redéployer avant de rejouer la démo');
 const data=[
  {name:'Solar Campus',description:'Prototype de station solaire pour recharger les appareils sur le campus.',category:'Énergie',goal:'3'},
  {name:'WaterSense',description:'Capteurs et tableau de suivi de consommation d’eau pour un jardin pédagogique.',category:'IoT',goal:'2'},
  {name:'Open Lab IA',description:'Ateliers et ressources ouvertes pour apprendre l’IA de manière responsable.',category:'Éducation',goal:'1'},
  {name:'Green Mobility',description:'Campagne de démonstration annulée par gouvernance pour tester la restitution.',category:'Mobilité',goal:'4'}
 ];
 for(const m of data){
  const r=await fetch('http://127.0.0.1:8787/add',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(m)});if(!r.ok)throw Error(await r.text());const {cid}=await r.json();
  await(await core.createCampaign(E(m.goal),86400*7,beneficiary.address,cid)).wait();
 }
 async function contribute(id,who,value){await(await core.connect(who).contribute(id,{value:E(value)})).wait();}
 await contribute(0,alice,'1.2');await contribute(0,bob,'0.6');
 for(let i=0;i<4;i++)await contribute(1,alice,'0.1');await contribute(1,bob,'0.15');
 await contribute(2,bob,'0.25');await contribute(3,alice,'0.2');await contribute(3,bob,'0.1');
 await(await dao.connect(alice).propose(0,0)).wait();await(await dao.connect(alice).vote(0,true)).wait();await(await dao.connect(bob).vote(0,true)).wait();
 await(await dao.connect(alice).propose(3,1)).wait();await(await dao.connect(alice).vote(1,true)).wait();
 await network.provider.send('evm_increaseTime',[4201]);await network.provider.send('evm_mine');
 await(await dao.execute(0)).wait();await(await dao.execute(1)).wait();
 await(await guard.connect(s1).setApproval(core.target,0,beneficiary.address,E('1.8'),true)).wait();
 await(await guard.connect(s2).setApproval(core.target,0,beneficiary.address,E('1.8'),true)).wait();
 await(await core.connect(beneficiary).withdrawFunds(0)).wait();await(await core.connect(alice).refund(3)).wait();
 await(await dao.connect(alice).propose(1,0)).wait();await(await dao.connect(alice).vote(2,true)).wait();
 console.log('4 campagnes, 3 propositions, 1 retrait multisig, 1 remboursement exécutés sur Hardhat.');
 console.log('Comptes démo (clés publiques de test Hardhat uniquement) :',JSON.stringify({admin:admin.address,alice:alice.address,bob:bob.address,beneficiary:beneficiary.address,signers:cfg.signers},null,2));
}
main().catch(e=>{console.error(e);process.exitCode=1});
