import googlemaps
import xlsxwriter
import os

#   Ordner erstellen (Linux exclusive)
os.system("mkdir xml")

#   Googlemaps API Authentifizierung
apikeyfile=open("apikey.txt","r")
apikey=apikeyfile.read()
gmaps=googlemaps.Client(key=apikey)

#   Funktion die den Dateinamen entgegennimmt und einen darauf angepassten wget befehlt schreibt und ausführt (Linux exclusive)
def wget(name):
    a="""wget --post-file=./xml/""" + name + """.xml --header="Content-Type: text/xml" -O ./xml/out-""" + name + ".xml https://efa-bw.de/trias"""
    os.system(a)
    return

#   Nimmt einen Ortnamen entgegen, macht eine API abfrage und gibt Ort, Lat- und Longkoordinate zurück
def maps(ort):
    url=str(gmaps.geocode(ort))
    anfang=url.find("location")+19
    ende=url[anfang:].find(",")+anfang
    lat=url[anfang:ende]
    anfang=anfang+len(lat)+9
    ende=url[anfang:].find("}")+anfang
    long=url[anfang:ende]
    return([ort,lat,long])

#   Die Funktion, die aus Anfangs und Endkoordinaten die XML Datei schreibt für die TRIAS API
def xml(name,slat,slong,zlat,zlong):
    name="./xml/" + name + ".xml"
    file = open(name, "w")
    file.write("""<?xml version="1.0" encoding="UTF-8"?>""" + "\n")
    file.write("""<Trias version="1.1" xmlns="http://www.vdv.de/trias" xmlns:siri="http://www.siri.org.uk/siri" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.vdv.de/trias file:///C:/development/HEAD/extras/TRIAS/TRIAS_1.1/Trias.xsd">""" + "\n")
    file.write(" <ServiceRequest>" + "\n")
    file.write("   <siri:RequestTimestamp>2016-08-11T11:00:00</siri:RequestTimestamp>" + "\n")
    file.write("   <siri:RequestorRef>test</siri:RequestorRef>" + "\n")
    file.write("   <RequestPayload>" + "\n")
    file.write("    <TripRequest>" + "\n")
    file.write("     <Origin>" + "\n")
    file.write("      <LocationRef>" + "\n")
    file.write("       <GeoPosition>" + "\n")
    file.write("        <Longitude>" + slong + "</Longitude>" + "\n")
    file.write("        <Latitude>" + slat + "</Latitude>" + "\n")
    file.write("       </GeoPosition>" + "\n")
    file.write("      </LocationRef>" + "\n")
    file.write("     </Origin>" + "\n")
    file.write("     <Destination>" + "\n")
    file.write("      <LocationRef>" + "\n")
    file.write("       <GeoPosition>" + "\n")
    file.write("        <Longitude>" + zlong + "</Longitude>" + "\n")
    file.write("        <Latitude>" + zlat + "</Latitude>" + "\n")
    file.write("       </GeoPosition>" + "\n")
    file.write("      </LocationRef>" + "\n")
    file.write("     </Destination>" + "\n")
    file.write("    </TripRequest>" + "\n")
    file.write("   </RequestPayload>" + "\n")
    file.write(" </ServiceRequest>" + "\n")
    file.write("</Trias>" + "\n")
    file.close()
    return

#   überbleibsel aus der Zeit wo ich die Ergebnisse in eine .xlsx geschrieben habe
def kordsout(alle):
    kordsbook = xlsxwriter.Workbook("lat-long-out.xlsx")
    sheetk= kordsbook.add_worksheet()
    sheetk.write("A1" , "Stadt")
    sheetk.write("B1" , "Lat")
    sheetk.write("C1" , "Long")
    zeile=2
    for eine in alle:
        x="A" + str(zeile)
        y=eine[0]
        sheetk.write(x,y)

        x="B" + str(zeile)
        y=eine[1]
        sheetk.write(x,y)

        x="C" + str(zeile)
        y=eine[2]
        sheetk.write(x, y)

        zeile += 1
    kordsbook.close()
    print("Fertig!")
    os.system("start out.xlsx")
    return

#   Verteilerfunktion für Routenauskunft
def routsout(start,ziel):
    name=start[0] + "-" + ziel[0]
    slat=start[1]
    slong=start[2]
    zlat=ziel[1]
    zlong=ziel[2]
    xml(name,slat,slong,zlat,zlong)
    wget(name)
    return

#   altes Zeug für Koordinaten ausgabe in Excel Datei
def kords(infos):
    sammeln=[]
    for i in infos:
        info=maps(i)
        sammeln.append(info)
    kordsout(sammeln)
    return

#   Funktion, die alle Routen nacheinander bearbeitet 
def routs(routen):
    for route in routen:
        route=route.split("-")
        start=route[0]
        ziel=route[1]
        start=maps(start)
        ziel=maps(ziel)
        routsout(start,ziel)
    return

#   Eingabezeugs für Koordinatenabfrage
def kordsgui():
    print("Bitte gib die gewünschten Städte mit einem Komma getrennt ein:")
    citys=str(input("--> "))
    citys=citys.split(",")
    kords(citys)
    return

#   Eingabe von Routen
def routsgui():
    print("Bitte gib die Routen wie folge ein: Start-Ziel,Start-Ziel,Start-Ziel ")
    routen=input("--> ")
    routen=routen.split(",")
    routs(routen)
    return

#   Infos & Eingabe von gewünschter Funktion und Werten
print("Möchtest du Orte in Koordinaten umrechnen (1) oder eine Route berechnen (2) ?")

z=False
while z == False:
    eingabe=int(input("--> "))

    if eingabe == 1:
        kordsgui()
        z=True

    elif eingabe == 2:
        routsgui()
        z=True
