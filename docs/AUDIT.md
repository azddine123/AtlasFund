# Audit statique et analyse de sécurité

## Périmètre réellement analysé
Slither 0.11.6, Solidity 0.8.28, optimiseur activé (200 runs), cible EVM Paris. Commande initiale :

```bash
python -m slither . --filter-paths 'node_modules|contracts/test' --json docs/evidence/slither.json
```

La compilation inclut les dépendances mais le filtre exclut leurs résultats et ceux du contrat d’attaque. **37 contrats analysés, 102 détecteurs, 8 findings rapportés** : 6 de sévérité faible et 2 informatifs. Aucun finding élevé ou moyen dans ce résultat. Les sorties brutes `slither.json` et `slither.txt` sont conservées sans retrait manuel de findings.

| Détecteur | Occurrences | Interprétation | Traitement |
|---|---:|---|---|
| timestamp | 6 | Comparaisons d’échéances et de délais dans Core/DAO | Accepté/documenté : usage nécessaire ; horizons en heures/jours ; aucun aléa ni calcul de récompense basé sur l’horodatage |
| low-level-calls | 2 | Transferts ETH dans refund et withdrawFunds | Accepté/documenté : retour booléen vérifié, état mis à jour avant appel, nonReentrant ; tests adversariaux sur les deux chemins |

Un avertissement accepté n’est pas un avertissement « corrigé ». Aucun patch de vulnérabilité découvert par Slither n’a été nécessaire après cette exécution. Les protections ci-dessous ont été introduites **dès la conception**, et non présentées comme des findings corrigés après coup.

## Protections préventives et preuves
- CEI : soldes, droit de remboursement et indicateur de retrait changent avant le transfert ETH.
- `ReentrancyGuard` : protège contribution, refund, withdraw et exécution de proposition (défense complémentaire).
- Retour booléen des appels vérifié ; un destinataire refusant l’ETH restaure atomiquement l’état initial.
- Accès DAO exclusif aux décisions, rôle Admin limité à la pause et à l’administration des rôles ; le routage DAO n’est configurable qu’une fois.
- Frappe/destruction uniquement par Core. Pas de fonction Admin de récupération des fonds de campagne.
- Snapshot ERC20Votes : bloc précédent, offre et poids historiques, pas de poids lu au moment du vote.
- CFD non transférables, délégation à soi-même et burn au remboursement.
- Deux approbations distinctes, révocables, liées à l’opération exacte. Un retrait ne peut être rejoué.
