## ⚡lightning⚡ payable e-scooter mit [streamr](https://www.streamr.com/) support 

Der lightning-scooter ist ein e-scooter dessen elektrischen Antrieb man für einen bestimmten Zeitraum buchen kann. 
Für die Bezahlung wird Bitcoin Lightning verwendet. Man wählt am Display aus wie lange man fahren möchte, bekommt einen qr-code generiert den man z.B. mit einer Handy lightning APP scannt und bezahlt. Dann wird der Strom für den gewählten Zeitraum eingeschaltet und man kann den scooter benutzen. Das besondere an diesem System, es ist mobil, d.h. die Kommunikation wird vollständig über das Mobilfunknetzt realisiert.

![1scooter](img/1scooter.png)
![2scooter](img/2scooter.png)


Zusätzlich zu meinen vorherigen Projekt, dem [lightning-bike](https://github.com/leblitzdick/lightning-bike), gibt es beim lightning-scooter eine Integration mit [streamr](https://www.streamr.com/), einer open-source Plattform für den weltweiten Austausch von Echtzeitdaten. Es werden nun bei jedem Buchungsvorgang Daten über den lightning-scooter an das [streamr](https://www.streamr.com/) Netzwerk übermittelt u.a. Datum, Standort, Akku Ladezuustand und noch einiges mehr.

Es ist somit möglich die Nutzung des lightning-scooters zu dokumentieren und sich jederzeit online über die [streamr](https://www.streamr.com/) Platform über den Zustand des scooters zu informieren.


## Wie funktioniert es?

Der Client startet nach dem Bootvorgang automatisch das Programm auf dessen Startbildschirm man momentan zwischen drei unterschiedlichen Nutzungszeiten, 1,3 und 5 Minuten, wählen kann. Pro Minute werden 250 satoshi verlangt das sind ca. 0,01€. 


![main](img/main.png)


Der Kunde wählt nun die gewünschte Zeit der Miete und das Programm ermittel als erstes die genaue Position des scooters per GPS.  Danach werden die aktuellen Status Daten des scooters per bluetooth ausgelesen. Es wird dann eine Internetverbindung hergestellt und die Informationen werden an die [streamr](https://www.streamr.com/) Plattform übermittelt. 


Im zweiten Schritt wird eine Zahlungaufforderung (invoice) über den geforderten Betrag generiert, dieser wird mittels lightning-charge an den lightning node übermittelt. Der Client bekommt die Zahlunginformationen vom lightning Node zurück und  generiert daraus einen qr-code welcher dem Kunden auf dem Display angezeigt wird. 
Der Kunde hat nun 60 Sek. Zeit den qr-code mit seiner lightning APP im Handy zu scannen und zu bezahlen. Solange testet der Client beim lightning node ob die Rechnung als bezahlt markiert ist. 
Hat die Bezahlung innhalb der 60 Sek. nicht funktioniert werden die Daten verworfen und das Programm kehrt zum Startbildschirm zurück, man kann es dann nochmal probieren.


![qr](img/qr.png)
![payed](img/payed.png)
![enjoy](img/enjoy.png)


Hat die Bezahlung funktioniert wird der Strom vom System für die gewählt Zeit eingeschaltet und man kann los fahren!!! Nach dem Ende der bezahlten Zeit wird die Stromzufuhr unterbrochen und die Miete ist beendet - man kann natürlich weiter rollern, aber nur noch mit Muskelkraft. Das Programm kehrt zum Startbildschirm zurück und und ist bereit von neuem zu starten. 

## streamr:

Bei jeder neuen Miete wird nun Informationen zu stream übertragen, dieser beinhaltet die folgenden Daten:

![stream](img/stream.png)

In einem Testlauf habe ich insgesamt 4x hintereinander den scooter gemietet und jedes mal wurden  die Statusinformationen an streamr übermittelt. Aus diesen Daten läßt sich mit dem streamr Editor ein canvas anlegen welches die Daten aus dem stream sammelt. Es nun möglich z.B. über das Map Modul die GPS Daten zu visualisieren, sodas man die Orte der Miete zuordnen kann. 

![canvas](img/canvas.png)


## Systemaufbau:

Herz des System ist ein Raspberry Pi 3 A+, welcher durch einen GSM/GPRS/GNSS HAT ergänzt wird. Dieses Modul besitzt ein GSM und ein GPS Modul und und ist somit für die Ortung als auch die Internetvebindung zuständig. 
Die Relais zur Steuerung der Stromzufuhr werden durch die GPIOs des raspberrypi angegesteuert und das bluetooth Modul für das Auslesen der Informationen aus dem scooter. Hier habe ich als Vorlage diesen Programmcode [ReadM365](https://github.com/Emeryth/ReadM365) angepasst. 
Als Monitor kommt ein e-paper Display zum Einsatz, welches praktischweise auch gleich 4 Druckschalter für die Menüsteuerung zur Verfügung stellt. Diese werden ebenfalls über die GPIOs des raspberrypi abgefragt. Das e-paper Display hat den Vorteil das es im Anzeigemodus so gut wie keinen Strom verbraucht sondern nur wenn sich der Bildinhalt ändert. Es hat einen hohen Kontrast ist auch an sonnigen Tage gut ablesbar. Der Bildaufbau ist zwar mit ca. 6 Sek. relativ zäh, aber es werden eigenlich nur 2 Schritte/Bilder benötigt um den Bezahlvorgang zu erledigen.
Die Stromzufuhr des 


Auf der Serverseite gibt es einen Raspberry Pi 3B auf dem der pseudo Node [sPRUNED](https://github.com/gdassori/spruned) die Bitcoin Blockchain vorhält und ein auf [c-lightning](https://github.com/ElementsProject/lightning) basierender lightning node. Für die Steuerung des lightning nodes wird [lightning-charge API](https://github.com/ElementsProject/lightning-charge) verwendet mit der sich sehr einfach die Programmierung der Bezahlungvorgänge umzusetzen ließ.

Auf beide Raspberry Pi Systeme die aktuellen raspbian strech lite Distribution. Das eigentlich Programm zur Steuerung des lightning-scooter ist in python2.7 geschrieben.

### Bauteile Server:
- Raspberry Pi 3 A+
- 16GB microSD Karte
- Standardgehäuse schwarz
- microUSB Kabel
- Netzteil
- Netzwerkkabel

### Bauteile Client:
- Raspberry A+ Zero WH
- 16GB microSD Karte
- Waveshare 2.7inch E-Ink display 264x176 px 
- Waveshare GSM/GPRS/GNSS/Bluetooth HAT (Prepaid SIM card Provider Netz O2)
- 2x 1 Kanal Relais 5V/230V
- Yeeco DC/DC Konverter 8-50V 12V/24V/36V/48V bis 5V3A / 15W Wasserdichter
- Selbst entworfenes Gehäuse aus PLA
- Kabel, Lötzinn, Heißkleber, Montageband usw.


### Scooter:
 - [Xiaomi M365](https://www.mi.com/global/mi-electric-scooter/)



