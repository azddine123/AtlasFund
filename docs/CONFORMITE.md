# Traçabilité énoncé → réalisation

| Exigence | Réalisation | État / preuve |
|---|---|---|
| M1 ERC-20 CFD OpenZeppelin | ERC20 + ERC20Votes ; 1 ETH = 1 000 CFD ; mint Core | Exécuté ; tests M1 |
| M2 créer/contribuer/statuts/refund/withdraw | CrowdfundingCore ; métadonnées via quatrième argument CID | Exécuté ; tests et démo |
| M3 vote pondéré, quorum, majorité, délai | FundingDAO ; quorum 20 %, majorité stricte, snapshot historique | Exécuté ; tests et 3 propositions démo |
| Exécution automatique | conditions automatiques, déclenchement permissionless par transaction | Interprétation technique explicitée |
| M4 front-end + wallet + ABI | HTML/CSS/JS, Ethers.js, ABI générée, MetaMask via EIP-1193 | UI et fournisseur injecté testés ; MetaMask manuel à rejouer |
| Solidity ^0.8.x + bibliothèques imposées | 0.8.28, OpenZeppelin 5.4, AccessControl, ReentrancyGuard, Pausable | Compilation réelle |
| Hardhat ou Foundry | Hardhat 2.29.1 | Tests JavaScript, outil compatible Slither ; version verrouillée |
| Sepolia OU Hardhat local | Hardhat chainId 31337 | Réellement déployé localement ; pas de Sepolia |
| IPFS | Helia/UnixFS, CIDv1, stockage disque hors chaîne | JSON + blocs générés ; P2P désactivé en démo |
| Réentrance | CEI + guard, contrats adversariaux | Attaques refund et withdraw rejetées |
| Contrôle d’accès | rôles Admin, Core minter, DAO exclusive, bénéficiaire seul | tests d’appels non autorisés |
| Pause | contribution/création/retrait/refund suspendus | tests pause/reprise et gel pendant pause |
| 2-sur-3 au-delà d’un seuil | TreasuryGuard > 1 ETH | un retrait de 1,8 ETH démontré |
| Snapshot | dernier bloc terminé à la création | tests solde accru après proposition et même bloc |
| Audit | Slither exécuté, périmètre et findings annexés | 8 findings faible/information, aucun moyen/élevé |
| Fuzzing | 64 contributions pseudo-aléatoires (seed fixe) + **8 séquences aléatoires** (graines 1 à 0xC0FFEE) mêlant contributions, temps, remboursements, votes, exécutions et retraits | 34 tests au total ; invariants de conservation vérifiés après **chaque** opération ; test de mutation : suppression du burn dans refund → échecs détectés |
| Bonus Python | répétition, pic, montant atypique | tests Python + historique réel |
| Rapport 10–15 pages | Rapport_AtlasFund.pdf | rapport de 12 pages avec captures locales |
| Oral 10 minutes | SOUTENANCE_10_MIN.md | déroulé et questions/réponses |
| Binôme/trinôme | Azddine El Hamdaoui et Anas Kerfal (README, interface, rapport) | Répartition des tâches à confirmer par les deux membres |
| Captures testnet (livrables) | captures Hardhat local | Discordance avec option locale de la section technique à clarifier avant remise |

## Touche personnelle directement liée au cours
1. Projets étudiants contextualisés ENSA, au lieu d’un clone générique de financement.
2. Tableau de transparence réunissant séquestre, votes, signataires et règles explicables.
3. Économie CFD cohérente : non-transférabilité et destruction au remboursement.
4. Preuves adversariales et journal d’audit interprété, au lieu d’un simple résultat « tests OK ».

La non-transférabilité et l’annulation définitive sont des choix fonctionnels à expliquer au professeur : le sujet ne prescrit pas un marché secondaire CFD ni un dégel. Une extension vers des CFD négociables exigerait de repenser la récupération des jetons lors des remboursements.
