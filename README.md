# Emotion_Prediction_Project
 Progetto svolto per il corso di Fondamenti di Visione Artificiale e Biometria tenuto dal professore Michele Nappi presso l'Università degli Studi di Salerno.
 
 Team: Emanuele Fittipaldi, Paolo Plomitallo

## Background
**Paul Elkman** ha elaborato per primo un modello scientifico per interpretare le emozioni di un soggetto in base alle sue espressioni facciali. Durante i suoi studi ha rilevato che c'è una corrispondenza tra determinati stati d'animo e una specifica espressione facciale. Questa corrispondenza vale per ogni individuo a prescindere dalla sua etnia, posizione geografica, sesso, etc...

Elkmann dunque ipotizzò che tali movimenti dei muscoli facciali siano legati a fattori biologici dunque congeniti e non derivanti dall'apprendimento.


## Espressioni primordiali

L'espressione è una biometria _comportamentale_ e in natura ne esistono 8:
1. Disgusto
2. Sorpresa
3. Tristezza
4. Rabbia
5. Paura
6. Gioia
7. Neutralità
8. Disprezzo


## Classificazione delle espressioni

La classificazione di una espressione/emozione può avvenire impiegando diverse tecniche legate all'intelligenza artificiale come:
- Deep Learning
- Machine Learning

Ovviamente più l'espressione si manifesta palesemente (macro-espressione) più è facile classificarla. Col passare degli anni però le espressioni possono diventare più impercettibili. Parliamo quindi di **micro-espressioni**


## Classificazione delle micro-espressioni

Esse sono caratterizzata da:
- Breve durata
- Bassa intensità
- Spontaneità, ovvero sono difficili da nascondere o simulare

Per le prime due ragioni, gli esseri umano non sono particolarmente bravi nel coglierle.


## Obiettivo del progetto

Allo stato dell'arte attuale, sono state avanzate molte tecniche per classificare le macro-espressioni e le micro-espressioni, ma non è stato fatto ancora molto riguardo la **predizione di una espressione**. 
Una espressione infatti è un processo che ha un inizio ed ha una fine, e l'obiettivo di questo progetto è essere in grado di poter dare una stima (in percentuale) di quale espressione/emozione si sta configurando nel soggetto preso in esame, a partire da una espressione neutrale.


## Dataset

Il Dataset che sarà utilizzato è il Cohn-Kanade Espression Dataset (CK+). Esso contiene:
- 593 video a 30 FPS con risoluzione 640x490 oppure 640x480, rappresentanti una specifica espressione facciale a partire da una espressione neutrale.
- 327 di questi video (55%) sono etichettati con una delle otto classi di espressione.
- Ogni soggetto è in una cartella.
- Ogni video legato ad una espressione diversa del soggetto è a sua volta in una            sottocartella il cui nome è l'espressione facciale.

Note: 
- per ogni soggetto non è detto che ci siano state rappresentate tutte e 8 le espressioni facciali.
- Non vanno usati gli stessi soggetti in fase di training e di testing (ovviamente per evitare overfitting)









