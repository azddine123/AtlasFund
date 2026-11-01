# AtlasFund — financement étudiant à gouvernance CFD

Projet du module Blockchain — ENSA Béni Mellal, IA & Cybersécurité.
Auteur : **Azddine El Hamdaoui**.

Une dApp pédagogique avec quatre contrats Solidity, des fonds séquestrés, des votes sur snapshot et un accord 2-sur-3 pour les retraits supérieurs à 1 ETH. **Démonstration sur Hardhat local ; aucun déploiement Sepolia n’est revendiqué.**

## Démarrer sous Ubuntu
Prérequis : Node.js 22 LTS ou 24, npm, Python 3.10+. La validation livrée utilise Node 24.22.1, Solidity 0.8.28, Hardhat 2.29.1 et OpenZeppelin 5.4.0. Versions verrouillées dans `package-lock.json`.

```bash
cd AtlasFund
npm ci
npm test
npm run test:python
```

Ouvrir **quatre terminaux**, tous dans le dossier du projet :

```bash
# Terminal 1 : blockchain locale (laisser ouvert)
npm run node
```

```bash
# Terminal 2 : métadonnées IPFS Helia locales (laisser ouvert)
npm run ipfs
```

```bash
# Terminal 3 : déploiement, données de démonstration, analyse
npm run deploy:local
npm run demo
npm run analyze
```

```bash
# Terminal 4 : interface (laisser ouvert)
npm run frontend
```

Ouvrir **http://127.0.0.1:5173**. Les campagnes sont lisibles sans wallet. Dans MetaMask, ajouter un réseau : nom `AtlasFund local`, RPC `http://127.0.0.1:8545`, chainId `31337`, symbole `ETH`. Importer uniquement un compte de test affiché par Hardhat. **Ces clés sont publiques : ne jamais les utiliser sur un réseau contenant de vrais fonds.**

La démo utilise les comptes Hardhat : #0 Admin, #1 Alice, #2 Bob, #3 bénéficiaire, #4/#5/#6 signataires. La connexion MetaMask ne se fait que depuis votre navigateur ; aucune clé n’est saisie dans la dApp.

### Rejouer
Redémarrer Hardhat efface l’état local. Réexécuter `deploy:local`, `demo`, puis `analyze` ; le fichier `frontend/public/config.json` est régénéré avec les ABI. Recharger l’interface. Le script démo refuse de s’exécuter sur une instance contenant déjà des campagnes. Il avance artificiellement l’horloge **du réseau de test uniquement** pour démontrer les délais.

### Tester l’interface automatiquement (facultatif)
```bash
python3 scripts/validate-local.py
```
Fermer les anciens services sur 8545, 8787 et 5173 avant ce test. Le navigateur de test Linux est fourni par @sparticuz/chromium, verrouillé avec Playwright dans les dépendances de développement. Ce script lance un réseau temporaire, déploie, joue la démonstration, capture l’interface, teste une transaction via un fournisseur EIP-1193 injecté puis arrête les services. Il ne pilote pas une véritable extension MetaMask. Une validation manuelle MetaMask reste requise sur votre ordinateur.

## Règles explicites
- 1 ETH = 1 000 CFD, avec 18 décimales. Seul Core frappe/brûle les jetons.
- CFD conserve l’interface ERC-20 mais refuse les transferts ; la délégation est exclusivement vers soi-même. Ce n’est pas un jeton échangeable sur un DEX.
- Échec après échéance ou annulation votée : remboursement individuel intégral, destruction des CFD correspondants.
- Tous les retraits exigent l’autorisation DAO, même quand l’objectif est atteint.
- Un vote de déblocage anticipé peut clore une campagne sous l’objectif **avant** échéance. Il supprime alors le droit au remboursement ; cette règle est affichée dans l’interface.
- Vote : solde historique au dernier bloc terminé à la création, quorum 20 % de l’offre historique (arrondi supérieur), majorité stricte des voix exprimées, un vote par adresse.
- Délais locaux : 1 h de vote + 10 min de délai ; configuration Sepolia : 48 h + 6 h.
- Le résultat n’est pas exécuté spontanément : `execute(id)` est ouvert à tous une fois les conditions remplies. Un keeper peut appeler la même fonction.
- Au-delà de 1 ETH (strictement >), accord 2-sur-3 lié à la chaîne, au contrat, à la campagne, au bénéficiaire et au montant exact. Aucun bypass Admin.
- Pause Admin : suspend création, contribution, retrait et remboursement. Une annulation par DAO reste possible. L’Admin ne peut pas déplacer les fonds mais peut retarder leur restitution.
- Gel = annulation définitive et restitution, pas confiscation ni suspension réversible.

## Arborescence
- `contracts/` : CFDToken, CrowdfundingCore, FundingDAO, TreasuryGuard ; `test/Attackers.sol` : contrat adversarial.
- `test/` : suite Solidity/Hardhat et tests Python.
- `frontend/` : interface Ethers.js et connexion MetaMask.
- `scripts/` : déploiement, démo, IPFS, export d’événements, analyse et validation UI.
- `docs/` : rapport, architecture, traçabilité, audit, soutenance et preuves brutes.
- `deployments/localhost.json` : adresses et ABI de la démonstration, à régénérer pour votre nœud.
