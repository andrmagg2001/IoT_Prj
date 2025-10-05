# TODO List - Smart Traffic Light IoT Project (7 giorni)

## Giorno 1 – Setup hardware e ambiente
- [X] Montare il circuito LED su **Arduino Uno R4 WiFi** (2 semafori → 2 LED rossi + 2 LED verdi, opzionale 2 gialli).  
- [X] Collegare ogni LED a un **pin digitale** con resistenza da **220 Ω** in serie.  
- [X] Scrivere uno **sketch Arduino base** per accendere i LED (test locale).  
- [ ] Configurare l’**Arduino Uno R4 WiFi** come **Access Point Wi-Fi** oppure come **client** della rete del Raspberry Pi.  
- [ ] Configurare il **Raspberry Pi** (Python, librerie: `socket`, `numpy`, `matplotlib`).  
- [ ] Testare la comunicazione **wireless Raspberry ↔ Arduino** inviando un comando semplice (`G1`, `G2`) per accendere un LED rosso o verde.  

## Giorno 2 – Modellazione del problema
- [ ] Studiare e semplificare il modello MDP dal PDF.
- [ ] Definire lo **stato**: `(n1, n2, TL1, TL2, N)`.
- [ ] Definire le **azioni**: (TL1 verde, TL2 rosso) oppure (TL1 rosso, TL2 verde).
- [ ] Definire la **funzione reward**: +1, 0, -1 in base a low/medium/high traffic.
- [ ] Impostare limiti di simulazione ridotti (es. max 10 auto per strada) per debug veloce.

## Giorno 3 – Simulazione software su Raspberry
- [ ] Implementare simulatore in Python del traffico (generazione auto casuale, passaggio auto).
- [ ] Implementare algoritmo di ottimizzazione (es. Value Iteration o Q-Learning).
- [ ] Eseguire test di simulazione solo su Raspberry (senza Arduino).
- [ ] Salvare log dei risultati (reward cumulativo, stato traffico).

## Giorno 4 – Integrazione Raspberry ↔ Arduino
- [ ] Scrivere sketch Arduino che riceve comandi (`G1`, `G2`) via seriale e accende i LED.
- [ ] Modificare codice Raspberry per inviare la decisione ottimale ad Arduino.
- [ ] Testare flusso completo: simulazione → decisione → LED.

## Giorno 5 – Visualizzazione e debugging
- [ ] Aggiungere grafici in Python (matplotlib) per visualizzare l’andamento del traffico.
- [ ] Debug: verificare che i LED seguano correttamente la politica calcolata.
- [ ] Salvare i risultati delle simulazioni (file CSV/JSON).

## Giorno 6 – Modulo video (opzionale/extra)
- [ ] Collegare webcam al Raspberry.
- [ ] Usare OpenCV per contare auto (anche semplificato, es. movimento/contorno).
- [ ] Sostituire i dati random con input dal video.
- [ ] Collegare conteggio reale al modello MDP.

## Giorno 7 – Rifinitura e report
- [ ] Pulire codice e creare repository GitHub.
- [ ] Scrivere README con istruzioni (installazione, schema hardware, esecuzione).
- [ ] Preparare mini demo (video o gif: semaforo che reagisce al traffico).
- [ ] Redigere breve relazione per la prof: 
  - Obiettivi
  - Architettura (Raspberry ↔ Arduino)
  - Algoritmo usato
  - Risultati e grafici