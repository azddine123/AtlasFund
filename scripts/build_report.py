#!/usr/bin/env python3
"""Rapport reproductible, 12 pages. Exécuter après validate-local.py."""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Image,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing,Rect,String,Line,Polygon,Circle
from PIL import Image as PILImage
root=Path(__file__).resolve().parents[1]
out=root/'docs/Rapport_AtlasFund.pdf';ev=root/'docs/evidence'
pdfmetrics.registerFont(TTFont('DejaVu','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuMono','/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVu-Bold')
INK=colors.HexColor('#153B32');GREEN=colors.HexColor('#237957');MUTED=colors.HexColor('#657C70');PALE=colors.HexColor('#EAF1E7');LINE=colors.HexColor('#DAE5D9');WHITE=colors.white
styles={
 'body':ParagraphStyle('body',fontName='DejaVu',fontSize=9.2,leading=14.3,textColor=INK,spaceAfter=10),
 'small':ParagraphStyle('small',fontName='DejaVu',fontSize=7.8,leading=11.7,textColor=MUTED,spaceAfter=8),
 'h1':ParagraphStyle('h1',fontName='DejaVu-Bold',fontSize=23,leading=29,textColor=INK,spaceAfter=16),
 'h2':ParagraphStyle('h2',fontName='DejaVu-Bold',fontSize=12.2,leading=17,textColor=GREEN,spaceBefore=11,spaceAfter=8),
 'kicker':ParagraphStyle('kicker',fontName='DejaVu-Bold',fontSize=8,leading=12,textColor=GREEN,spaceAfter=8),
 'cell':ParagraphStyle('cell',fontName='DejaVu',fontSize=8,leading=11.7,textColor=INK),
 'code':ParagraphStyle('code',fontName='DejaVuMono',fontSize=7.4,leading=11,textColor=INK,spaceAfter=9),
}
story=[]
def p(t,style='body'):return Paragraph(t,styles[style])
def add(t,style='body'):story.append(p(t,style))
def title(n,t):add(f'ATLOSFUND / DOSSIER TECHNIQUE / {n:02}'.replace('ATLOSFUND','ATLASFUND'),'kicker');add(t,'h1')
def h(t):add(t,'h2')
def table(rows,widths=None):
 data=[[p(str(c),'cell') for c in row] for row in rows]
 t=Table(data,colWidths=widths or [499/len(rows[0])]*len(rows[0]),hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,0),.7,LINE),('LINEBELOW',(0,1),(-1,-1),.3,LINE)]))
 story.append(t);story.append(Spacer(1,10))
def box(t):
 t=Table([[p(t)]],colWidths=[499]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),.5,LINE),('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.append(t);story.append(Spacer(1,12))
def img(name,width=499,maxh=390):
 path=ev/name
 with PILImage.open(path) as im:w,hh=im.size
 scale=min(width/w,maxh/hh);return Image(str(path),width=w*scale,height=hh*scale)
def page():story.append(PageBreak())
def diagram():
 d=Drawing(499,310)
 def node(x,y,w,t,sub='',dark=False):
  d.add(Rect(x,y,w,47,rx=6,fillColor=INK if dark else PALE,strokeColor=LINE,strokeWidth=.7));d.add(String(x+10,y+28,t,fontName='DejaVu-Bold',fontSize=9,fillColor=WHITE if dark else INK));d.add(String(x+10,y+12,sub,fontName='DejaVu',fontSize=7,fillColor=colors.HexColor('#B6D2BD') if dark else MUTED))
 def arrow(x1,y1,x2,y2):
  d.add(Line(x1,y1,x2,y2,strokeColor=GREEN,strokeWidth=1));
  if y2<y1:d.add(Polygon([x2,y2,x2-3,y2+6,x2+3,y2+6],fillColor=GREEN,strokeColor=None))
  elif x2>x1:d.add(Polygon([x2,y2,x2-6,y2+3,x2-6,y2-3],fillColor=GREEN,strokeColor=None))
  else:d.add(Polygon([x2,y2,x2+6,y2+3,x2+6,y2-3],fillColor=GREEN,strokeColor=None))
 node(0,235,150,'Interface Ethers.js','Lecture RPC + ABI');node(180,235,140,'MetaMask','Signature locale');node(350,235,149,'IPFS / Helia','JSON + CIDv1')
 arrow(150,259,180,259);d.add(Line(75,282,75,297,strokeColor=GREEN));d.add(Line(75,297,425,297,strokeColor=GREEN));arrow(425,297,425,282)
 node(0,130,150,'FundingDAO','Snapshot, quorum, délais',True);node(180,130,140,'CrowdfundingCore','Séquestre et statuts',True);node(350,130,149,'TreasuryGuard','2 approbations sur 3',True)
 arrow(250,235,250,177);arrow(150,153,180,153);arrow(320,153,350,153)
 node(0,25,150,'CFDToken','Votes historiques + burn');node(180,25,140,'Événements','Contribution / vote / retrait');node(350,25,149,'Analyse Python','Alertes explicables')
 arrow(75,130,75,72);arrow(240,130,240,72);arrow(320,49,350,49);arrow(180,143,150,49)
 return d

def footer(c,doc):
 c.setFillColor(INK);c.rect(0,825,595,17,fill=1,stroke=0)
 c.setStrokeColor(LINE);c.line(48,43,547,43);c.setFont('DejaVu',7);c.setFillColor(MUTED)
 c.drawString(48,29,'ATLASFUND  /  ENSA BÉNI MELLAL  /  31 OCTOBRE 2026');c.drawRightString(547,29,f'{doc.page:02}')

# 1
story.append(Spacer(1,32));add('ENSA BÉNI MELLAL · IA & CYBERSÉCURITÉ','kicker');story.append(Spacer(1,28))
story.append(Paragraph('AtlasFund<span color="#237957">.</span>',ParagraphStyle('cover',fontName='DejaVu-Bold',fontSize=51,leading=58,textColor=INK)))
add('Des idées financées.<br/>Des décisions vérifiables.','h1');story.append(Spacer(1,18))
add('Plateforme de financement participatif décentralisée<br/>à gouvernance par jeton CFD','h2')
add('Rapport de conception, réalisation et validation<br/>Module Blockchain · Pr. Hamza Touil')
story.append(Spacer(1,25))
table([['4 contrats','26 tests Hardhat','2 protections de sortie'],['Architecture séparée et traçable','Inclut réentrance et fuzzing','Gouvernance + multisignature']],[166,166,167])
box('<b>La touche personnelle</b><br/>Une plateforme de projets étudiants où chaque campagne relie contributions, votes, autorisations de paiement et signaux d’activité hors chaîne. Les contrôles sont expliqués et démontrés, pas seulement affichés.')
add('<b>Auteur :</b> Azddine El Hamdaoui<br/><b>Équipe :</b> compléter avec les coéquipiers réels avant remise.<br/><b>Version :</b> 1.0 · Démonstration Hardhat local · Solidity 0.8.28')
add('Statut : prototype pédagogique validé dans l’environnement décrit. Aucun déploiement Sepolia ni audit indépendant n’est revendiqué. L’usage de l’assistance IA et les validations à rejouer par l’équipe sont explicités dans les sources.','small')
page()
# 2
title(2,'Du sujet aux choix de réalisation')
add('Le sujet impose une dApp complète et multi-contrats : les contributions en ETH donnent des CFD, puis la communauté décide des opérations sensibles. AtlasFund applique cette logique à des initiatives étudiantes et réunit les preuves dans une interface de transparence.')
table([['Exigence de l’énoncé','Implémentation et preuve'],['M1 · Jeton ERC-20 CFD','OpenZeppelin ERC20Votes ; frappe proportionnelle par Core ; tests de frappe et d’accès.'],['M2 · Campagnes et fonds','Création, contribution, quatre statuts, remboursement individuel, retrait réservé au bénéficiaire.'],['M3 · Gouvernance','Snapshot, quorum 20 %, majorité stricte, délais et exécution ouverte à tous.'],['M4 · Interface','HTML/CSS/JS + Ethers.js ; ABI issue de la compilation ; connexion MetaMask.'],['Sécurité obligatoire','CEI, ReentrancyGuard, AccessControl, Pausable, 2-sur-3, tests adversariaux et Slither.'],['IPFS et bonus','Helia/UnixFS local pour les métadonnées ; Python sur événements Contribution.']],[145,354])
h('Un périmètre volontairement maîtrisé')
add('Le prototype ne crée ni marché de jetons, ni système de rendement, ni oracle de prix. La différenciation vient de la cohérence économique des CFD, de la lisibilité des décisions et des preuves de sécurité. Cela mobilise directement les cinq chapitres sans ajouter de protocole financier inutile.')
h('Choix d’environnement')
add('Hardhat permet des tests JavaScript, une blockchain locale et l’intégration Ethers.js. La version 2.29.1 est verrouillée pour la compatibilité de cette chaîne d’outils avec Slither. Solidity 0.8.28 est fourni par le paquet solc, avec optimiseur 200 runs et cible EVM Paris. OpenZeppelin 5.4.0 fournit les mécanismes standards.')
box('<b>Point à clarifier pour la remise :</b> les exigences techniques autorisent Hardhat local, alors que la liste des livrables mentionne des captures testnet. Les preuves fournies sont locales et identifiées comme telles ; Sepolia reste une étape distincte si le professeur l’exige.')
page()
# 3
title(3,'Une architecture qui sépare les responsabilités')
story.append(diagram());story.append(Spacer(1,8))
add('Figure 1 — Architecture logique. Le wallet signe ; les contrats décident ; les métadonnées et l’analyse restent hors chaîne. Les appels d’analyse n’accordent aucun pouvoir sur les fonds.','small')
table([['Composant','Responsabilité et frontière de confiance'],['CrowdfundingCore','Détient les ETH et les droits de restitution ; appelle Token ; vérifie la DAO et le garde multisig.'],['CFDToken','Seul Core peut frapper ou brûler. Historique de vote fourni par OpenZeppelin ERC20Votes.'],['FundingDAO','Fige les poids, comptabilise un vote par adresse et autorise ou annule ; ne détient pas les ETH.'],['TreasuryGuard','Enregistre deux accords parmi trois signataires pour une opération exacte ; aucun paiement direct.']],[145,354])
add('La configuration de l’adresse DAO n’est possible qu’une fois. L’Admin possède les rôles de pause et d’administration, mais aucune fonction ne lui permet de déplacer les contributions. L’interface peut être contournée sans contourner les vérifications contractuelles.')
add('Lien au cours : chapitre 1 (transactions et consensus du réseau), chapitre 3 (signature locale), chapitre 4 (dApp, ABI, ERC-20 et IPFS), chapitre 5 (contrôle d’accès et séparation des responsabilités).','small')
page()
# 4
title(4,'Les fonds et les CFD suivent des règles cohérentes')
h('Émission et remboursement')
add('Le taux fixe est de 1 ETH pour 1 000 CFD. Avec 18 décimales, le calcul entier est exact : une contribution de 0,01 ETH crée 10 CFD. Seul Core émet les jetons. Au remboursement, les CFD correspondants sont détruits dans la même transaction, avant le transfert ETH.')
box('<b>Pourquoi des CFD non transférables ?</b><br/>Le jeton garde l’interface ERC-20 mais refuse les transferts entre comptes. La délégation est limitée à soi-même. Ainsi, un contributeur ne peut pas vendre ses CFD puis réclamer son ETH en conservant ailleurs le pouvoir de vote. Ce choix exclut volontairement l’usage DEX ; il doit être défendu explicitement.')
table([['État','Condition','Conséquence'],['En cours','Avant échéance ; aucune autorisation de sortie ni annulation','Contributions acceptées.'],['Réussie','Objectif atteint à échéance, ou déblocage anticipé voté','Retrait encore conditionné à la DAO, puis au multisig si nécessaire.'],['Échouée','Échéance atteinte et objectif manqué','Remboursement individuel, CFD détruits.'],['Annulée','Gel définitif décidé par la DAO avant retrait','Nouvelles contributions interdites ; restitutions ouvertes.']],[82,208,209])
h('Déblocage anticipé : une décision engageante')
add('Avant échéance, la DAO peut accepter une campagne sous son objectif. L’autorisation clôt les contributions et supprime le droit au remboursement. Après échéance, une campagne déjà échouée ne peut pas être sauvée rétroactivement. Le gel peut encore annuler une autorisation tant que le retrait n’a pas eu lieu.')
h('Invariant financier')
add('La somme des séquestres est suivie par totalEscrow. Chaque retrait ou remboursement la réduit exactement du montant envoyé. En fonctionnement normal, le solde ETH du contrat lui est égal. Des ETH forcés peuvent créer un excédent ; ils ne donnent aucun CFD et ne sont pas distribuables par l’Admin.')
page()
# 5
title(5,'Une gouvernance sur des voix figées')
add('Une proposition mémorise son action, la campagne, le bloc de snapshot, son quorum, ses échéances et le résultat. Les voix sont lues avec getPastVotes ; l’offre historique sert au quorum. Aucune lecture du solde courant ne détermine le poids du vote.')
table([['Paramètre','Valeur retenue','Justification'],['Snapshot','Dernier bloc terminé à la création','Exclut une frappe du même bloc ; compatible avec les lectures historiques OpenZeppelin.'],['Droit de proposer','Au moins 1 CFD au snapshot','Écarte les comptes sans contribution ; ne constitue pas une protection totale anti-spam.'],['Quorum','20 % de l’offre au snapshot, arrondi supérieur','Participation minimale explicite ; compromis pédagogique.'],['Majorité','Oui strictement supérieur à Non','Une égalité ne permet pas l’exécution.'],['Délais locaux','1 h de vote + 10 min de délai','Vérifiables avec l’horloge Hardhat ; Sepolia configuré à 48 h + 6 h.']],[94,159,246])
h('Exemple chiffré')
add('Si l’offre historique est de 1 000 CFD, le quorum est de 200 CFD. Un résultat 150 Oui / 0 Non échoue malgré 100 % de voix favorables : participation insuffisante. Un résultat 120 Oui / 100 Non passe. Un résultat 150 Oui / 150 Non échoue par absence de majorité stricte.')
h('Ce que le snapshot empêche, et ce qu’il n’empêche pas')
add('Une contribution postérieure ne donne pas de nouvelles voix pour un scrutin déjà ouvert. La non-transférabilité réduit les acquisitions temporaires de CFD. En revanche, un acteur qui finance beaucoup avant le snapshot peut dominer. Les droits d’un ancien scrutin restent figés même après un remboursement : les CFD brûlés n’affectent que les futurs snapshots.')
box('<b>Exécution :</b> une transaction appelle execute après les délais. N’importe quelle adresse peut la soumettre, mais le contrat vérifie quorum, majorité et état de campagne. Les conditions sont automatiques ; le déclenchement ne se produit pas spontanément.')
page()
# 6
title(6,'Sécuriser les chemins qui déplacent de la valeur')
table([['Menace','Protection mise en œuvre','Validation'],['Réentrance','CEI + nonReentrant sur refund/withdraw ; mise à jour des droits avant appel externe','Deux scénarios adversariaux tentent le rappel et échouent.'],['Accès illégitime','AccessControl, DAO exclusive, bénéficiaire seul, Core seul minter','Appels Admin/directs/tiers rejetés dans les tests.'],['Sortie importante non contrôlée','2 signatures transactionnelles sur 3, au-delà de 1 ETH','Une seule signature échoue ; deux montants différents ne s’additionnent pas.'],['Manipulation des voix','Snapshot historique, vote unique, CFD non transférables','Contribution après proposition et proposition dans le bloc de frappe testées.'],['Incident opérationnel','Pause globale contributions et sorties ; annulation DAO permise','Pause/reprise, refus de remboursement pendant pause, gel pendant pause.'],['Échec du destinataire ETH','Résultat booléen vérifié ; revert atomique','Un destinataire refusant l’ETH retrouve ses droits et peut réessayer.']],[100,237,162])
h('La multisignature ne remplace pas la gouvernance')
add('La clé d’approbation lie chainId, adresse Core, identifiant de campagne, bénéficiaire et montant. Deux comptes distincts doivent approuver la même clé ; une approbation peut être révoquée. La DAO autorise d’abord la sortie et seul le bénéficiaire appelle withdrawFunds. Le booléen withdrawn bloque tout second paiement.')
h('Confiance résiduelle')
add('L’Admin ne peut pas voler les fonds mais peut prolonger une pause. La perte de deux clés multisig bloque les retraits importants. Les signataires sont fixes et aucune rotation n’est livrée. Ces limites sont préférables à une récupération Admin implicite qui contournerait la gouvernance sans être annoncée.')
page()
# 7
title(7,'Tests exécutés : des scénarios qui peuvent échouer')
table([['Validation','Résultat observé','Preuve livrée'],['Compilation Solidity','35 fichiers compilés lors du test initial','evidence/tests.txt'],['Tests Hardhat','26 réussites, 0 échec','test/AtlasFund.test.js'],['Fuzzing reproductible','64 contributions, 4 campagnes, 3 contributeurs','Dernier test ; seed 0xC0FFEE'],['Tests Python','5 tests réussis','evidence/python-tests.txt'],['Interface et transaction','Lecture, filtres, formulaires, mobile et contribution EIP-1193','evidence/ui-tests.txt']],[133,205,161])
h('Scénarios adversariaux significatifs')
add('<b>Réentrance :</b> un contrat reçoit l’ETH puis rappelle refund ou withdrawFunds. Le test vérifie que la tentative a eu lieu, que le rappel a échoué et que le montant reçu n’a pas été multiplié. Il vérifie aussi que le séquestre d’autres contributeurs subsiste.')
add('<b>Snapshot même bloc :</b> autominage désactivé, contribution et proposition envoyées dans le même bloc. La proposition ne bénéficie pas des CFD tout juste frappés. L’autominage est restauré même si le test échoue.')
add('<b>Multisig :</b> tests de doublon, non-signataire, révocation, montant erroné, seuil exact de 1 ETH et retrait supérieur au seuil. Une autorisation ne vaut pas pour un montant voisin.')
h('Propriétés vérifiées par le fuzzing')
add('Un générateur pseudo-aléatoire à seed fixe varie les montants et répartit 64 contributions sur quatre campagnes. Après chaque contribution : solde ETH = totalEscrow et offre CFD = 1 000 × apports cumulés. Après l’échec et tous les remboursements : séquestre, solde et offre reviennent à zéro.')
box('<b>Portée :</b> il s’agit d’un fuzzing déterministe de scénario, pas d’une preuve formelle ni d’une exploration exhaustive. Le test UI utilise un fournisseur EIP-1193 injecté vers Hardhat ; la véritable extension MetaMask doit encore être vérifiée manuellement par l’équipe.')
page()
# 8
title(8,'Audit statique : interpréter plutôt que masquer')
add('Slither 0.11.6 a été exécuté sur la version livrée. Il analyse 37 contrats avec 102 détecteurs. Le filtre exclut des findings affichés les dépendances node_modules et le contrat adversarial contracts/test. Le résultat brut indique success = true et rapporte huit findings.')
table([['Détecteur','Niveau / nombre','Analyse et traitement'],['timestamp','Faible · 6','Dates utilisées pour échéances et délais, jamais comme source d’aléa. Horizons en heures/jours. Avertissements acceptés et documentés.'],['low-level-calls','Informatif · 2','Appels ETH de refund et withdrawFunds. Retour vérifié, CEI et guard. Cas de réentrance et refus ETH testés. Avertissements conservés.']],[103,108,288])
box('<b>Résultat exact :</b> aucun finding moyen ou élevé dans ce périmètre. Cela ne prouve pas l’absence de vulnérabilités. Les huit avertissements figurent dans l’annexe JSON originale ; aucun n’a été retiré pour présenter un résultat artificiellement vide.')
h('Corrections et mesures préventives : distinction nécessaire')
add('Aucune vulnérabilité découverte par cet audit n’a exigé de patch après exécution. Les protections CEI, guard, snapshots et burn ont été introduites avant l’audit. Elles sont décrites comme des mesures préventives, pas comme de faux findings corrigés après coup.')
h('Extrait conceptuel du chemin de remboursement')
add('1. Vérifier état de campagne et contribution.<br/>2. Mettre la contribution à zéro et réduire le séquestre.<br/>3. Détruire les CFD correspondants.<br/>4. Émettre l’événement puis effectuer l’appel ETH.<br/>5. Revert si l’appel échoue ; la transaction restaure tout.','code')
h('Risques conservés')
add('Concentration économique des voix ; faible participation ; pause prolongée ; perte des signataires ; ordre concurrent annulation/retrait ; métadonnées indisponibles ; propositions devenues périmées. Le document AUDIT.md détaille ces limites et la procédure de revue manuelle.')
page()
# 9
title(9,'Une interface de transparence, reliée aux contrats')
story.append(img('interface-apercu.png',499,355));story.append(Spacer(1,8))
add('Figure 2 — Capture réelle de l’interface après transactions sur Hardhat. Les valeurs viennent des contrats ; aucun jeu de données statique ne remplace la lecture blockchain. Les ETH sont des ETH de test.','small')
h('Des informations utiles à la décision')
add('Les cartes distinguent la collecte historique du séquestre encore disponible, le statut et l’autorisation DAO. Un projet peut être « réussi » sans avoir encore payé son bénéficiaire. La gouvernance affiche le bloc snapshot, les voix, le quorum et les dates. Le tableau de transparence montre les contrats, les signataires et les alertes Python.')
h('Chemins utilisateur')
add('Un visiteur lit sans wallet via le RPC local. Pour contribuer, voter ou retirer, il connecte MetaMask au réseau attendu. L’interface affiche la transaction envoyée puis confirmée et recharge l’état. Les contenus IPFS sont affichés comme texte échappé. Un mauvais réseau ou l’absence de wallet produit un message explicite.')
add('Les captures complètes, le détail d’une campagne, le détail d’un vote et la version mobile sont présents dans docs/evidence. Le style visuel n’ajoute aucune autorisation : les contrats restent la source des règles.','small')
page()
# 10
title(10,'Bonus Python : des signaux expliqués, pas des accusations')
add('Le script export-events.js lit les événements Contribution à partir du bloc de déploiement, par fenêtres de 1 000 blocs. Il enregistre adresse, campagne, montant en wei, horodatage, bloc et transaction. analyze.py applique des règles déterministes à cet historique vérifiable.')
table([['Règle','Condition','Interprétation prudente'],['REPETITION','Au moins 3 contributions de même montant depuis une même adresse, pour une campagne','Peut correspondre à un test ou à des versements fractionnés légitimes.'],['BURST','Au moins 5 contributions sur une fenêtre de 300 secondes','Peut signaler un lancement collectif ou une activité à examiner.'],['LARGE_AMOUNT','Au moins 5 observations ; montant supérieur à 5 fois la médiane','Heuristique de contraste, sans preuve de manipulation.']],[105,205,189])
h('Résultat de la démonstration')
report=json.loads((root/'frontend/public/anomalies.json').read_text())
add(f"L’export final contient <b>{report['event_count']} contributions</b> sur le contrat local et <b>{len(report['alerts'])} alertes</b>. WaterSense comporte quatre contributions égales de 0,1 ETH provenant du même compte, puis une contribution rapprochée d’un second compte. Les règles REPETITION et BURST sont déclenchées. La contribution du test UI est également incluse dans l’export final.")
box('<b>Aucune action automatique sur les fonds.</b><br/>Les alertes ne déclenchent ni pause ni gel. Un analyste examine les éléments, puis la gouvernance peut décider. Une adresse n’est pas une identité : aucune relation entre personnes n’est inférée.')
h('Lien avec le profil IA & cybersécurité')
add('La valeur ajoutée porte sur la préparation des données, l’explicabilité des règles et la séparation entre observation et décision. Aucun modèle de machine learning n’est revendiqué sans jeu annoté ni mesure de précision/rappel. Les cinq tests Python couvrent l’entrée vide, les cas ordinaires, les répétitions, les pics, les montants atypiques et l’isolement entre campagnes.')
add(f"Périmètre temporel du rapport : blocs {report['source']['fromBlock']} à {report['source']['toBlock']}, chainId {report['source']['chainId']}. Après une nouvelle transaction, il faut relancer l’export et l’analyse ; l’interface affiche cette limite.",'small')
page()
# 11
title(11,'Déploiement, IPFS et démonstration reproductible')
config=json.loads((root/'deployments/localhost.json').read_text())
add(f"Déploiement exécuté sur <b>Hardhat local, chainId 31337</b>. Core : <font size='7'>{config['addresses']['core']}</font>. Les adresses et ABI complètes sont dans deployments/localhost.json ; leur présence seule ne prouve pas un déploiement Sepolia.")
cols=Table([[img('detail-vote.png',238,240),img('detail-campagne.png',238,240)]],colWidths=[249,250]);cols.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')]));story.append(cols)
add('Figure 3 — Détails réels : vote exécuté et campagne encore active. La démo avance l’horloge de Hardhat pour franchir les délais ; ces dates sont celles de la chaîne locale.','small')
h('Scénario exécuté')
add('Quatre campagnes et trois propositions sont créées. Solar Campus reçoit 1,8 ETH : vote favorable, délai écoulé, deux approbations, puis retrait. Green Mobility est annulée par vote ; Alice récupère sa contribution. WaterSense reste ouverte avec une proposition active. Ces opérations sont consignées dans les journaux et événements livrés.')
h('Stockage IPFS réel, disponibilité locale')
add('Helia/UnixFS produit des CIDv1 et persiste les blocs sur disque. Core ne stocke que le CID. Le serveur de démonstration fonctionne sans annonce P2P ; l’accès par une passerelle publique n’est pas garanti. Pour Sepolia, il faut épingler les métadonnées sur une infrastructure accessible et adapter la passerelle du client.')
h('Reproduction')
add('npm ci → npm test → npm run node<br/>npm run ipfs → npm run deploy:local → npm run demo<br/>npm run analyze → npm run frontend','code')
add('Utiliser des terminaux distincts pour les services persistants. Le README donne la configuration MetaMask, le protocole de relance et la préparation Sepolia. Ne jamais utiliser les clés publiques de test Hardhat pour des fonds réels.','small')
page()
# 12
title(12,'Bilan, limites et références')
add('AtlasFund réalise les quatre modules et les contrôles de sécurité du sujet dans une démonstration locale. Sa contribution distinctive est de rendre les règles et leurs preuves accessibles : séquestre, snapshot, multisig, restitutions et analyse explicable partagent la même interface.')
h('Ce qui reste à faire par l’équipe avant remise')
add('Rejouer l’installation et les tests sur Ubuntu ; connecter une véritable extension MetaMask ; compléter les coéquipiers et leurs contributions ; confirmer avec l’enseignant l’acceptation des captures Hardhat ; déployer sur Sepolia et épingler publiquement les métadonnées si demandé. Les sources fournissent le chemin, mais ne remplacent pas ces validations personnelles.')
h('Limites assumées')
add('Aucun audit indépendant, aucune garantie de perfection, aucune rotation des signataires, aucun proxy, aucune protection contre toutes les coalitions économiques. Les CFD des projets réussis restent dans l’offre et peuvent diluer la participation future. Le périmètre est pédagogique ; une mise en production demanderait une revue économique, opérationnelle et de sécurité supplémentaire.')
h('Références du module')
add('Pr. Hamza Touil, supports fournis : chapitre I « Concepts de base et fonctionnement » ; II « Applications et domaines » ; III « Cryptographie dans la blockchain » ; IV « Smart contracts et DApps » ; V « Sécurité de la blockchain ». Énoncé : « Plateforme de financement participatif décentralisée à gouvernance par jeton », 2 pages.','small')
h('Documentation technique utilisée')
add('OpenZeppelin Contracts 5.x : <link href="https://docs.openzeppelin.com/contracts/5.x/api/token/erc20" color="#237957">ERC20 et ERC20Votes</link> ; <link href="https://docs.openzeppelin.com/contracts/5.x/governance" color="#237957">gouvernance et snapshots</link>.<br/>Hardhat : <link href="https://v2.hardhat.org/docs" color="#237957">documentation version 2</link>.<br/>Slither : <link href="https://github.com/crytic/slither" color="#237957">dépôt officiel et documentation des détecteurs</link>.<br/>IPFS : <link href="https://docs.ipfs.tech/concepts/content-addressing/" color="#237957">content addressing et CID</link>.<br/>Helia : implémentation UnixFS utilisée et versions verrouillées dans package-lock.json.','small')
box('<b>Transparence sur l’assistance IA</b><br/>L’IA a assisté conception, code, tests et rédaction. L’équipe doit comprendre chaque décision, rejouer les preuves et respecter les règles de déclaration de l’enseignant. Le document UTILISATION_IA.md précise ce périmètre sans attribuer de travaux fictifs aux étudiants.')
add('Annexes dans le dépôt : code source, 26 tests Hardhat, 5 tests Python, rapport Slither brut, journaux de déploiement, événements JSON, métadonnées, captures, matrice de conformité et guide de soutenance de 10 minutes.','small')

doc=SimpleDocTemplate(str(out),pagesize=(595.28,841.89),leftMargin=48,rightMargin=48,topMargin=45,bottomMargin=59,title='AtlasFund — Rapport de réalisation et validation',author='Azddine El Hamdaoui')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
