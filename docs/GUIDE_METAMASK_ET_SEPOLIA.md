# Guide : test manuel MetaMask (local) et déploiement Sepolia

Ces deux étapes demandent un navigateur avec l'extension MetaMask et, pour Sepolia, des clés personnelles : elles doivent être faites par un membre de l'équipe (ne jamais partager une clé privée ou une phrase de récupération, même avec un assistant).

## A. Test manuel avec la vraie extension MetaMask (réseau local, ~15 min)
1. Installer MetaMask (Chrome ou Edge) et créer un portefeuille **réservé aux tests**.
2. Ouvrir 4 terminaux dans le dossier du projet : `npm run node`, `npm run ipfs`, puis dans un 3e `npm run deploy:local && npm run demo && npm run analyze`, et dans un 4e `npm run frontend`.
3. MetaMask → Réseaux → Ajouter un réseau manuellement : nom `AtlasFund local`, RPC `http://127.0.0.1:8545`, chainId `31337`, symbole `ETH`.
4. Importer un compte de test : la console `npm run node` affiche les comptes Hardhat avec leurs clés (**publiques, sans valeur**). Importer le compte #1 (Alice) pour contribuer et voter ; le #3 pour le bénéficiaire ; #4 et #5 pour les signataires.
5. Ouvrir http://127.0.0.1:5173 et vérifier, en capturant l'écran à chaque étape :
   - connexion MetaMask (bouton « Connecter MetaMask ») ;
   - contribution à la campagne WaterSense (fenêtre de confirmation MetaMask) ;
   - création d'une proposition puis vote (onglet Gouvernance) ;
   - approbation multisig par #4 puis #5, puis retrait par le bénéficiaire #3 ;
   - pause / reprise avec le compte Admin #0.
6. Noter dans le rapport : date, comptes utilisés, résultats observés, captures.

## B. Déploiement sur Sepolia (~30 min)
**Prérequis (personnels, à créer par vous)**
- Un portefeuille de test **neuf**, avec quelques ETH Sepolia gratuits (faucet Sepolia au choix, par ex. celui d'Alchemy ou de Google Cloud Web3).
- Une URL RPC Sepolia gratuite (Alchemy, Infura ou autre).
- Trois adresses **distinctes** pour les signataires (3 comptes MetaMask de test suffisent) et l'adresse Admin.

**Variables d'environnement (PowerShell)**
```powershell
$env:SEPOLIA_RPC_URL="https://..."
$env:DEPLOYER_PRIVATE_KEY="0x..."     # clé du portefeuille de TEST uniquement
$env:ADMIN_ADDRESS="0x..."
$env:GUARD_SIGNERS="0xAAA...,0xBBB...,0xCCC..."
npx hardhat run scripts/deploy.js --network sepolia
npm run build
```
Ne jamais committer ces valeurs (`.env` est ignoré par Git). Fermer le terminal après usage.

**Après le déploiement**
1. Noter les adresses affichées ; les vérifier sur https://sepolia.etherscan.io (captures pour le rapport : transaction de déploiement de chaque contrat).
2. Les métadonnées IPFS doivent être épinglées sur un service public (Pinata par exemple) : le serveur local n'est pas accessible depuis Internet. Remplacer le champ « CID IPFS existant » par le CID public.
3. Jouer un mini-scénario avec MetaMask sur Sepolia (créer une campagne de test, contribuer, proposer) et capturer chaque étape.
4. Dans le rapport, présenter ces captures **comme Sepolia** et les captures précédentes **comme locales**. Ne jamais mélanger.

## C. Si Sepolia n'est pas réalisé
Envoyer ce message au professeur et conserver sa réponse : « L'énoncé autorise Hardhat local pour la démonstration mais mentionne des captures testnet dans les livrables. Les captures locales de notre démonstration sont-elles acceptées, ou souhaitez-vous un déploiement Sepolia ? »
