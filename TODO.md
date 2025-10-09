# TODO List - Smart Traffic Light IoT Project (7 giorni)

## Giorno 1 – Setup hardware e ambiente

- [X] Montare il circuito LED su **Arduino Uno R4 WiFi** (2 semafori → 2 LED rossi + 2 LED verdi, opzionale 2 gialli).
- [X] Collegare ogni LED a un **pin digitale** con resistenza da **220 Ω** in serie.
- [X] Scrivere uno **sketch Arduino base** per accendere i LED (test locale).
- [X] Configurare l’**Arduino Uno R4 WiFi** come **Access Point Wi-Fi** oppure come **client** della rete del Raspberry Pi.
- [X] Configurare il **Raspberry Pi** (Python, librerie: `socket`, `numpy`, `matplotlib`).
- [X] Testare la comunicazione **wireless Raspberry ↔ Arduino** inviando un comando semplice (`G1`, `G2`) per accendere un LED rosso o verde.

## Giorno 2 – Modellazione del problema

- [X] Studiare e semplificare il modello MDP dal PDF.
- [X] Definire lo **stato**: `(n1, n2, TL1, TL2, N)`.
- [X] Definire le **azioni**: (TL1 verde, TL2 rosso) oppure (TL1 rosso, TL2 verde).
- [X] Definire la **funzione reward**: +1, 0, -1 in base a low/medium/high traffic.
- [X] Impostare limiti di simulazione ridotti (es. max 10 auto per strada) per debug veloce.

## Giorno 3 – Simulazione software su Raspberry

- [X] Implementare simulatore in Python del traffico (generazione auto casuale, passaggio auto).
- [X] Implementare algoritmo di ottimizzazione (es. Value Iteration o Q-Learning).
- [X] Eseguire test di simulazione solo su Raspberry (senza Arduino).
- [X] Salvare log dei risultati (reward cumulativo, stato traffico).

## Giorno 4 – Integrazione Raspberry ↔ Arduino

- [X] Scrivere sketch Arduino che riceve comandi (`G1`, `G2`) via seriale e accende i LED.
- [X] Modificare codice Raspberry per inviare la decisione ottimale ad Arduino.
- [X] Testare flusso completo: simulazione → decisione → LED.

## Giorno 5 – Visualizzazione e debugging

- [X] Aggiungere grafici in Python (matplotlib) per visualizzare l’andamento del traffico.
- [X] Debug: verificare che i LED seguano correttamente la politica calcolata.
- [X] Salvare i risultati delle simulazioni (file CSV/JSON).

## Giorno 6 – Estensione simulazione (senza webcam)

- [ ] Migliorare il realismo della simulazione (ad esempio traffico variabile o cicli casuali).
- [ ] Eseguire test estesi con Q-table addestrata.
- [ ] Analizzare i risultati con grafici e medie sulle performance.

## Giorno 7 – Rifinitura e report

- [ ] Pulire codice e creare repository GitHub.
- [ ] Preparare mini demo (video o gif: semaforo che reagisce al traffico).
- [ ] Redigere breve relazione per la prof:
  - Obiettivi
  - Architettura (Raspberry ↔ Arduino)
  - Algoritmo usato
  - Risultati e grafici
