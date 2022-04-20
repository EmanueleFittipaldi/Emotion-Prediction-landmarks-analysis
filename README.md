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
- Per ogni soggetto non è detto che ci siano state rappresentate tutte e 8 le espressioni facciali.
- Non vanno usati gli stessi soggetti in fase di training e di testing (ovviamente per evitare overfitting)

## Pipeline di lavoro

### Features

Le feature che saranno utilizzate per predire la percentuale di espressione sono le distanze tra i landmark in frame consecutivi.

Saranno creati due array di distanze:
- un array di distanze dei landmark rispetto al frame precedente. Questo vettore ci fornisce la variazione parziale.
- un array di distanze dei landmark rispetto al frame iniziale. Questo vettore ci fornisce la variazione globale.

### Passaggi da effettuare

La prima cosa da fare è **Preparare il dataset di caratteristiche (features)**:
1. Per ogni video di espressione facciale di un soggetto, estrapolare i frame (da decidere se tutti i frame o solo un sottoinsieme) ed estrapolare i 468 landmark mediante mediapipe da questi frame ed inserirli in un csv.
2. All'interno dello stesso csv costruire il vettore delle distanze locali(ogni frame dal precedente, il primo avrà distanze 0) e quello delle distanze globali (ogni frame dal primo, i l primo avrà distanze 0). 
3. Associare ad ogni array l'etichettature relativa all'espressione
4. A seconda di come si deciderà di risolvere il problema, si potrebbe associare ad ogni riga una percentuale o una classe di percentuale di espressione.


La seconda cosa da fare è la vera e propria **predizione dell'espressione**
Questa fase della risoluzione può essere affrontata in due modi:
1. Classificazione: costruire delle classi di percentuale (Bucket technique) ovvero delle classi (10-30;30-50;50-70;70-10) per le espressioni. Il problema diventa quindi una classificazione multiclasse, dove le percentuali più basse individuano la micro-espressione e le più alte la macro-espressione.
2. Regressione: il valore percentuale è ottenuto mediante regressione dei valori esistenti. Avendo un numero diverso di frame in ogni cartella del dataset, non avremo tutti i possibili valori percentuali.












