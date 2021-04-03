# OrderListTool
Create an order list from a BOM

Documentation: https://github.com/0815nutzer/OrderListTool/wiki

English description see below.

## German description
Mit Hilfe dieses kleinen Werkzeugs soll eine automatisierte Zuordnung von Bestellnummern zu Bauteilen in einem Schaltplan erfolgen.
Die Bauteile des Schaltplan müssen hierfür in einer entsprechend formatierten csv-Datei zur Verfügung stehen, während die "Bauteildatenbank", welche die zuzuordnenden Bestellnummern enthält, aus entsprechend formatierten Textdateien besteht.

Eine ausführlichere Dokumentation befindet sich im Wiki dieses Projekts: https://github.com/0815nutzer/OrderListTool/wiki

### Anwendung
1. Erzeugen einer Stückliste im csv-Format unter Verwendung des dem CAD-System entsprechenden Skripts im Ordner "BOM-Scripts"
2. Das Programm durch Ausführen der `main.py` mit Python3 starten
3. Mit Klick auf "Stückliste" die zuvor erstellte Stückliste im csv-Fomat wählen
4. Durch Klick auf "Bestelllisten" den Ordner mit den Bestelllisten wählen
5. Paare durch klicken auf "Suche Paare" suchen lassen
6. Die gefundenen Paare prüfen und wenn nötig, Änderungen in der Auswahl vornehmen
7. Mit Klick auf "exp. Bestellliste" die lieferantenspezifischen Bestelllisten generieren lassen


## English description

### Usage
1. Open schematic and create a BOM-file in csv-format using the appropriate script in the "BOM-Scripts"-folder
2. Start the tool by running `main.py` using python3
3. Select the prior created csv-file
4. Select the path to the folder containing the partlist-files
5. Click `Search pairs`
6. Review found matches and adjust, if required
7. Click `Export lists` to create distribtor dependend order lists
