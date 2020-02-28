from pymongo import MongoClient
#client=MongoClient()
client=MongoClient("mongodb+srv://daniel:mongo-daniel@daniel-cluster-nezxu.mongodb.net/test?retryWrites=true&w=majority")

db= client.trias
triprequests=db.triprequests

xml=open("out-Kassel-Berlin.xml","r")
read=xml.read()

def cleaner(string):
    loop=string
    loop=loop.replace("<","@-")
    loop=loop.replace(">","@")
    loop=loop.replace("\n","@")
    loop=loop.split("@")
    loop=[x for x in loop if x]
    return(loop)


def udo(list):
    dic={}
    for i in range(len(list)):
        a=list[i]
        if a[0] == "-":
            continue
        else:
            att=list[i-1]
            att=att[1:]
            att=att.split(" ")
            att=att[0]
            arg=list[i]
            dic.update({att:arg})
    return(dic)


def convert(string):
    sven={}
    header_start=0
    header_end=string.find("TripLeg")
    header=string[:header_end]
    header=cleaner(header)
    header=udo(header)
    sven.update(header)

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


fuck=convert(read)
print(fuck)
print(type(fuck))
print(fuck)
triprequests.insert(fuck)

xml.close()
