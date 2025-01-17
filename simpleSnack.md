# **1.2 Retrospektive**

## **Lösungsvorgang**

### Anforderungen prüfen und Grundstruktur entwickeln  
Zunächst wurden die Programmanforderungen sorgfältig geprüft, um eine solide Basis zu schaffen. Daraufhin wurde die Grundstruktur des Programms entworfen, einschließlich:  
- der `main()`-Funktion  
- verschiedener Funktionen zur **Input-Validierung**

---

### Planung der User Experience (UX)
Der Fokus lag darauf, einen benutzerfreundlichen Ablauf zu gestalten:  

#### **Allgemeiner Ablauf**  
Aktionsauswahl ->
Aktion durchführen ->
Feedback geben ->
Zurück zur Aktionsauswahl

#### **Bestellvorgang**  
Produktliste anzeigen ->
Eingabe der Produktnummer ->
Eingabe der Produktanzahl ->
Kaufbestätigung

---

### Umsetzung
Beim Erstellen der einzelnen Funktionen und Programmabläufe wurde konsequent darauf geachtet, dass die Anforderungen erfüllt werden, wie:  

- Der Nutzer soll nicht ins Minus gehen können.
- Man darf nur positive Werte einzahlen können.
- Der Nutzer soll nur vorrätige Produkte kaufen können.

Die tabellarische Darstellung der Produkte wurde so implementiert, dass die Tabelle sich **responsive** an die vordefinierten Produkte des `snacks`-Dictionarys anpasst.

---  

## Datenstruktur

Die Wahl der Datenstruktur lag zunächst an der Vorgabe, die neu kennengelernten Strukturen wie Dictionarys zu verwenden.  
Allerdings hätte sich meiner Meinung nach eine Klasse für die einzelnen Snacks besser geeignet, da eine Klasse die Möglichkeit bietet, den Preis und die Anzahl als Eigenschaft zu speichern und so Fehler in der Implementierung vermieden werden. 

Die Historie sollte eine Liste bleiben, da nur Strings dort in schon richtiger Reihenfolge abgelegt werden.

---

## Überarbeitungen

Grundsätzlich wurde bei der Erstellung der `checkProducts()`-Funktion durchgängig die Funktionsweise getestet, um die Resultate direkt zu prüfen. \
Allerdings wurde nach erster "Fertigstellung" eine neue Spalte für die Produktnummer benötigt, die zuerst vergessen wurde.\
Ebenfalls wurde die Breitenanpassung auf den höchsten Preis erst nachträglich eingefügt, als ich realisierte, dass manche Produkte mit formatiertem Preis die kurze Breite vom Titel "Preis" überschreiten.
