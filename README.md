# AtlasFund — financement étudiant à gouvernance CFD

Projet du module Blockchain — ENSA Béni Mellal, IA & Cybersécurité.
Auteur : **Azddine El Hamdaoui**.

Une dApp pédagogique avec quatre contrats Solidity, des fonds séquestrés, des votes sur snapshot et un accord 2-sur-3 pour les retraits supérieurs à 1 ETH. **Démonstration sur Hardhat local ; aucun déploiement Sepolia n’est revendiqué.**

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
