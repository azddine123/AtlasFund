// Lance Python avec l'interpréteur disponible (python3 sous Linux/macOS, python ou py sous Windows).
const {spawnSync}=require('node:child_process');
for(const cmd of ['python3','python','py']){
 const r=spawnSync(cmd,process.argv.slice(2),{stdio:'inherit',shell:false});
 if(r.error&&r.error.code==='ENOENT')continue;
 process.exit(r.status??1);
}
console.error('Python 3 introuvable (essayé : python3, python, py).');process.exit(1);
