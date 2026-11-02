# Soutenance AtlasFund — 10 minutes

**0:00–0:45 · Besoin et contribution personnelle**
« AtlasFund finance des initiatives étudiantes. Les contributeurs reçoivent des CFD et décident collectivement du déblocage ou de l’annulation. Notre valeur ajoutée est la transparence : fonds, votes, autorisations et signaux d’activité sont visibles et explicables. »
Ne pas dire « totalement sécurisé », « sans aucun intermédiaire » ni « IA qui détecte la fraude ».

**0:45–2:00 · Architecture et cours**
Afficher le schéma du rapport. Montrer les quatre contrats, MetaMask, Ethers.js et IPFS. Relier registre/transactions au chapitre 1, cas d’usage au 2, signature/clé privée au 3, Solidity/ERC-20/dApp au 4 et contrôles de sécurité au 5. Les métadonnées sont hors chaîne, leur CID est on-chain.

**2:00–3:10 · Démonstration contribution**
Sur WaterSense, utiliser Alice et contribuer 0,01 ETH. Montrer MetaMask, la confirmation et les 10 CFD correspondants. Expliquer que le montant est en wei et que le contrat conserve le séquestre. Les CFD ne se vendent pas.

**3:10–4:30 · Gouvernance**
Montrer une proposition, son snapshot, son quorum et ses délais. Une contribution après la création n’augmente pas son poids pour ce scrutin. Un vote par adresse. Quorum 20 % de l’offre historique, majorité stricte ; égalité = rejet. Le snapshot est le dernier bloc terminé, afin d’exclure une frappe dans le même bloc.

**4:30–5:30 · Trésorerie**
Montrer Solar Campus : autorisation DAO, accord 2-sur-3 puis retrait. Un accord porte sur un montant et un bénéficiaire précis. Aucun signataire ne peut directement détourner les fonds. Au-delà de 1 ETH, une seule approbation est insuffisante.

**5:30–6:20 · Échec et gel**
Montrer la campagne annulée et le remboursement. Les CFD remboursés sont brûlés. Distinguer pause globale, annulation définitive et échec après échéance. Un vote anticipé peut accepter un projet sous l’objectif, mais pas réécrire un échec déjà acquis.

**6:20–7:35 · Sécurité, preuves**
Montrer les tests de réentrance et le test snapshot même bloc. Le contrat attaquant tente effectivement un second appel : il échoue. Expliquer Checks-Effects-Interactions et ReentrancyGuard. Présenter les 26 tests, le fuzzing à seed fixe, puis les findings Slither avec leurs justifications. Ne pas confondre absence de finding élevé et absence de risque.

**7:35–8:35 · Bonus Python**
Afficher REPETITION et BURST sur WaterSense. Montrer les événements sources. « Quatre montants égaux ou cinq transactions rapprochées méritent une vérification ; cela peut aussi être une collecte organisée légitime. » Aucun gel automatique, aucune identification de personnes.

**8:35–9:30 · Limites et arbitrages**
Gros contributeur influent ; rôle Admin capable de suspendre ; perte des signataires ; historique de vote conservé même après remboursement ; IPFS local non répliqué ; pas de proxy. Justifier la réduction de complexité dans un mini-projet.

**9:30–10:00 · Conclusion factuelle**
Rappeler la dApp fonctionnelle, les règles testées, l’analyse explicable et le périmètre local. Présenter comme étape suivante la validation manuelle MetaMask et, si demandé, le déploiement Sepolia avec épinglage public IPFS.
