from pymongo import MongoClient
#   Datenbankverbingun & Auswahl DB / Collection
#client=MongoClient() für localhost Verbindung
client=MongoClient("mongodb+srv://daniel:mongo-daniel@daniel-cluster-nezxu.mongodb.net/test?retryWrites=true&w=majority")
db= client.trias
triprequests=db.triprequests

#   Einlesen der entsprechenden XML
xml=open("./xml/out-Kassel-Mainz.xml","r")
read=xml.read()

#   Nimmt string mit XML Code entgegen und wandelt ihn in eine saubere Liste um
def cleaner(string):
    loop=string
    loop=loop.replace("<","@-")
    loop=loop.replace(">","@")
    loop=loop.replace("\n","@")
    loop=loop.split("@")
    loop=[x for x in loop if x]
    return(loop)

#   wandelt eine Liste aus Argumenten und Werten in entsprechende Dictionary Einträge um
def udo(list):
    dic={}
    for i in range(len(list)):
        a=list[i]
        if a[0] == "-":
            continue
#   Da oben "loop=loop.replace("<","@-")" im cleaner steht wird durch das if jedes "/Attribut" und "Attribut" rausgefiltert
        else:
            #   Folglich sind hier nur die Werte. welche dann als Attribut einfach den Eintrag vor sich in der Liste eintragen
            att=list[i-1]
            att=att[1:]
            att=att.split(" ")
            att=att[0]
            arg=list[i]
            dic.update({att:arg})
    return(dic)

#   nimmt XML String entgegen und ruft die anderen Funktionen auf 
def convert(string):
    sven={}
    #   Filtert den XML Dateianfang mit XML Argumenten raus
    header_end=string.find("TripLeg")
    header=string[:header_end]
    header=cleaner(header)
    header=udo(header)
    sven.update(header)

    #   Eine While Schleife die die ganzen Triplegs rausfiltert und in Unterdictionarys schreibt
    run=0
    while run < len(string):
        search=string[run:]
        beg=search.find("<TripLeg>")
        end=search.find("</TripLeg>")+10


        if beg == -1:
            return(sven)
        elif end == -1:
            return(sven)
        else:
            trip=search[beg:end]
            trip=cleaner(trip)
            trip=udo(trip)
            legid=trip["LegId"]
            obj={legid:trip}
            ##output="{" + obj + ":" + str(trip) + "}"
            sven.update(obj)
            run += end
    return(sven)

#   Eigentlicher Funktionsaufruf
sven=convert(read)
print(sven)
print(type(sven))

#   Schreiben in die DB
triprequests.insert_one(sven)

xml.close()
