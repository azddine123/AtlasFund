# Validation de la version livrée

- Hardhat : 26 scénarios passent, dont 64 contributions pseudo-aléatoires.
- Python : 5 tests passent.
- IPFS : 4 contenus relus par CID et empreintes SHA-256 vérifiées ; origine interdite et JSON invalide refusés.
- UI : navigation, filtres, dialogues, affichage mobile 390 px sans débordement horizontal et contribution EIP-1193 réelle.
- Démonstration : 4 campagnes, 3 propositions, 1 retrait de 1,8 ETH avec approbation 2-sur-3, 1 remboursement.
- Export final : 11 contributions ; 2 alertes explicables. Les captures sont prises avant la contribution de 0,001 ETH du test UI ; les événements finaux incluent cette transaction.
- Front-end : compilation Vite réussie, 162 modules transformés.
- Slither : analyse réussie, 37 contrats, 102 détecteurs, 8 findings (6 faibles, 2 informatifs). Périmètre décrit dans AUDIT.md.
- Rapport : 12 pages, rendu et inspection visuelle.

Les journaux bruts sont dans ce dossier. Les contrôles de contrats n’ont pas été réexécutés inutilement après de simples changements de présentation ; l’audit correspond au code Solidity final, inchangé depuis son exécution.
