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

## IPFS : ce qui est livré
Le service `ipfs-server.mjs` utilise **Helia/UnixFS**, crée de véritables CIDv1, persiste les blocs dans `.ipfs/blocks`, sauvegarde les JSON sources dans `docs/metadata`, et les restitue par CID. La démonstration fonctionne **hors réseau P2P** ; aucune disponibilité sur une passerelle publique n’est promise. La chaîne conserve uniquement le CID des métadonnées.

Pour Sepolia, épingler les JSON sur un nœud IPFS public ou Pinata, puis saisir le CID obtenu dans le formulaire. Un CID assure l’adressage et l’intégrité, **pas la permanence de disponibilité**. Les secrets Pinata doivent rester hors du front-end. Le format CID est vérifié côté interface ; Core ne vérifie que sa longueur (limite documentée). Ne pas stocker de données personnelles dans les métadonnées publiques.

## Audit reproductible
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-audit.txt
npm run audit
```
Le fichier `slither-new.json` ne doit pas déjà exister ; renommer une précédente sortie avant de relancer. Slither retourne normalement un code non nul lorsqu’il rapporte des findings, même si l’analyse a réussi. Lire `success` dans le JSON et le détail des résultats. Les sorties de la version livrée sont annexées dans `docs/evidence/slither.json` et `slither.txt` ; périmètre : contrats applicatifs, dépendances et contrat adversarial exclus des findings affichés. Il ne s’agit pas d’un audit indépendant ni d’une garantie d’absence de vulnérabilités.

## Sepolia : procédure préparée, non exécutée
Utiliser un wallet de test neuf, quelques ETH de test et trois vrais signataires distincts. Les variables sont décrites dans `.env.example` ; les exporter dans le terminal (le projet ne charge pas automatiquement `.env`). Puis :
```bash
npx hardhat run scripts/deploy.js --network sepolia
npm run build
```
`SEPOLIA_RPC_URL`, `DEPLOYER_PRIVATE_KEY`, `ADMIN_ADDRESS` et `GUARD_SIGNERS` sont requis. Ne jamais committer une vraie clé. Le déploiement exporte l’ABI ; les rôles Admin sont transférés à `ADMIN_ADDRESS` si elle diffère du déployeur. Pour un déploiement public, remplacer le lien local des métadonnées par une passerelle IPFS publique et assurer leur épinglage. Vérifier manuellement toutes les transactions MetaMask. L’énoncé autorise Hardhat local pour la démonstration mais mentionne des captures testnet dans le rapport : demander au professeur si les preuves locales suffisent avant la remise finale.

## Limites à défendre
Gouvernance pondérée ≠ une personne/une voix ; un contributeur majoritaire peut orienter les décisions. Les snapshots empêchent les changements de poids après création, pas toutes les attaques économiques. Les droits historiques d’un scrutin restent figés même si un remboursement ultérieur détruit les CFD. Les dons réussis conservent des CFD, ce qui élargit l’électorat au fil du temps. La perte de deux clés des signataires peut bloquer les gros retraits. Il n’existe pas de rotation des signataires ni de proxy d’upgrade dans ce prototype. Les fonds envoyés de force au contrat ne sont pas attribués à une campagne et ne sont pas récupérables par une fonction Admin. L’interface est un client non fiable : la sécurité repose sur les contrats.

## Bonus IA / blockchain
`analyze.py` utilise des **heuristiques explicables**, pas un modèle entraîné : répétitions, pics de fréquence et montants atypiques. Les événements viennent de `Contribution` sur le contrat déployé. Les adresses liées ne sont pas inférées : sans données additionnelles, ce serait une affirmation injustifiée. Chaque alerte inclut la règle et ses éléments observables ; aucune alerte ne bloque automatiquement les fonds.

## Comprendre avant de soutenir
Lire `docs/SOUTENANCE_10_MIN.md`, exécuter les tests puis modifier vous-même un paramètre et expliquer son effet. `docs/UTILISATION_IA.md` distingue l’assistance de génération du travail de compréhension et validation attendu.

## Recréer le rapport PDF
```bash
pip install reportlab pillow
python3 scripts/build_report.py
```
Les captures de `docs/evidence` doivent être présentes. Sous Ubuntu, les polices DejaVu sont utilisées.
