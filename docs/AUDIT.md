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

## Risques résiduels et limites fonctionnelles
1. **Gouvernance économique** : majorité de jetons, faible participation et coalition restent possibles. Le quorum global peut rendre une petite campagne dépendante d’anciens contributeurs.
2. **Snapshot historique** : un remboursement ne réécrit pas un scrutin déjà ouvert ; la voix historique reste valable. Pour un design à enjeu financier, un verrouillage temporaire des contributions demanderait une politique explicite compatible avec les remboursements.
3. **Déblocage anticipé** : la DAO peut accepter un projet sous l’objectif avant échéance. C’est une règle annoncée, avec perte du droit de remboursement après autorisation ; ce n’est pas une protection financière absolue.
4. **Pause centralisée** : l’Admin peut bloquer indéfiniment les sorties sans transférer les fonds. Une administration multisig ou une politique de délai maximal serait une extension.
5. **Signataires fixes** : la perte de deux clés bloque les retraits > 1 ETH. Aucune rotation ni récupération n’est implémentée.
6. **Métadonnées** : Core borne la longueur mais ne prouve pas la disponibilité ou la validité complète du CID. Le navigateur vérifie la syntaxe ; l’hébergement local n’apporte pas une réplication publique.
7. **Ordre des décisions** : si une annulation et un retrait sont en concurrence, l’ordre d’inclusion détermine le résultat. Une annulation après paiement échoue. Le délai de gouvernance donne du temps, mais ne supprime pas le risque d’ordonnancement.
8. **Propositions périmées** : plusieurs propositions peuvent viser une campagne. Une exécution devenue incompatible avec l’état échoue et ne déplace aucun fonds ; les propositions inutiles restent dans l’historique. Un seuil minimal de 1 CFD limite seulement les proposants sans participation.
9. **Prototype sans proxy** : une correction implique un nouveau déploiement. Les paramètres retenus sont pédagogiques et ne suffisent pas pour une mise en production.
10. **Transferts forcés** : du solde ETH peut arriver sans contribution. Il n’augmente pas `totalEscrow` et ne donne aucun CFD ; aucune fonction de récupération n’est livrée.

## Vérification manuelle à refaire par l’équipe
Exécuter sur une instance fraîche : contribution, vote avec Alice et Bob, tentative de vote avec un compte sans CFD au snapshot, refus de retrait sans multisig, deux approbations puis retrait, pause/reprise, annulation et remboursement. Capturer les confirmations MetaMask. Décrire fidèlement les résultats observés, sans reprendre une preuve locale comme preuve Sepolia.

## Rejeu de l'audit (Windows) et justification finding par finding
Slither 0.11.6 a été relancé sur la version actuelle (Windows 11, Node 24, Python 3.11) : **37 contrats, 102 détecteurs, 8 findings**, identiques à l'exécution livrée (sorties : `docs/evidence/slither-rerun.json` et `slither-rerun.txt`). Aucun finding moyen ou élevé.

| # | Détecteur | Emplacement | Pourquoi c'est acceptable |
|---|---|---|---|
| 1 | timestamp (faible) | `CrowdfundingCore.status` (l.67-73) | La date limite d'une campagne est comparée à `block.timestamp`. Les durées sont d'au moins 1 h : une dérive de quelques secondes d'un validateur ne change pas le résultat. Aucun aléa n'en dépend. |
| 2 | timestamp | `CrowdfundingCore.authorizeRelease` (l.96-101) | Même raisonnement (comparaison à la date limite). |
| 3 | timestamp | `CrowdfundingCore.cancelByGovernance` (l.103-107) | Le détecteur signale l'usage indirect via les conditions ; pas de logique sensible au temps à la seconde. |
| 4 | timestamp | `CrowdfundingCore.withdrawFunds` (l.108-121) | Idem : le temps n'intervient que via `releaseApproved`, déjà fixé par la DAO. |
| 5 | timestamp | `FundingDAO.vote` (l.51-61) | Fin de scrutin à 1 h minimum ; la précision à la seconde n'est pas requise. |
| 6 | timestamp | `FundingDAO.execute` (l.63-72) | Délai de sécurité de 10 min minimum, sans enjeu à la seconde près. |
| 7 | low-level-calls (info) | `CrowdfundingCore.refund` (l.91) | `call{value:}` est la méthode recommandée pour envoyer de l'ETH (`transfer` limite le gas à 2300 et peut casser avec des contrats). Mitigations : retour booléen vérifié, état mis à jour avant l'appel (CEI), `nonReentrant`, deux tests d'attaque. |
| 8 | low-level-calls (info) | `CrowdfundingCore.withdrawFunds` (l.119) | Même justification que le n° 7. |

**Honnêteté sur les « corrections »** : aucun de ces 8 avertissements n'est une vulnérabilité ; les protections ont été conçues avant l'audit. Un test de mutation complémentaire (suppression de `token.burn` dans `refund`) fait échouer la suite : cela montre que les tests détectent bien une régression de ce type.
