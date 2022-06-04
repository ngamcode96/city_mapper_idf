import psycopg2
from datetime import datetime
import collections

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget

def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def search_stop(tab, from_stop , to_stop):
    tmp=0
    for row in tab:
        if from_stop==row[0] :
            tmp+=1
        if to_stop==row[0] :
            tmp+=1
    if tmp==2:
        return True
    return False



from_stop='MASSY PALAISEAU'
to_stop='PARIS NORD'

conn = psycopg2.connect(database="", user="", host="", password="")
cursor = conn.cursor()

cursor.execute(""f"SELECT S.name, N.trip_I, N.arr_time_ut, R.route_name FROM network_bis N, station S, route R WHERE  R.route_id=N.route_id and S.stop_id=N.from_stop and trip_I IN ( (SELECT distinct trip_I FROM network_bis N, station S WHERE S.stop_id=N.from_stop and S.name=$${from_stop}$$) INTERSECT (SELECT distinct trip_I FROM network_bis N1, station S1 WHERE S1.stop_id=N1.to_stop and S1.name=$${to_stop}$$)) ORDER BY trip_I, N.route_id, N.arr_time_ut""")
conn.commit()
rows = cursor.fetchall()

iti = 0
#print(iti)


iti_tab = {}

# tab ={} 
# tab[3]=3
# tab[10]=10

# for i in tab :
#     print(i)
#     print(len(tab))
# print(tab[10])
suiv=0
prec=0

for row in rows :
    heure_actuel = get_sec(datetime.today().strftime("%H:%M:%S"))
    heure_bdd = get_sec(datetime.fromtimestamp(row[2]).strftime("%H:%M:%S"))

    if(heure_actuel<= heure_bdd):
        suiv=row[1] # premier trip_I 
        if(suiv != prec):
            iti_tab[row[1]]  = []
        prec=suiv
        iti_tab[row[1]].append(row)
        

a_sup=[] 

for tab in iti_tab: # Suppression 
    if(search_stop(iti_tab[tab], from_stop, to_stop)==False):
        a_sup.append(tab)

for i in range(len(a_sup)):
        iti_tab.pop(a_sup[i])

#iti_tab = collections.OrderedDict(sorted(iti_tab.items()))
# { k: v for k, v in sorted(iti_tab.items(), key=lambda item: item[1]) } # Tri






class ListWidgetDemo(QListWidget):
    def sort_trip(trips):
        return dict(sorted(trips.items(), key=lambda e: e[1][0][2]))

    def get_values(self):

        test_stop=False

        # iti_tab = self.sort_trip(iti_tab)

        for tab in iti_tab: # tab = itineraire, trip_I 
            str = ""
            i = 0
            for row in iti_tab[tab]:
    
                if(row[0] == from_stop):
                    str = "RER " + row[3] +  " : Depart à " + datetime.fromtimestamp(row[2]).strftime("%H:%M:%S") + " : " + row[0] 
                    test_stop = True

                # if(test_stop == True) :
                    # self.addItem(row[0] + " " + str(row[1]) + " " +  + " " + row[3] )

                if((row[0] == to_stop) & (test_stop == True)) :
                    str += " - Arrivée : " + row[0] + " à " + datetime.fromtimestamp(row[2]).strftime("%H:%M:%S") 
                    test_stop = False
                    


                if((row[0] == to_stop) &  (test_stop == False)) :
                    break
            i+=1
            if((str != "") & (i<= 5)):    
                self.addItem(str)
            # iti_tab = sort_trip(iti_tab)

    def __init__(self):
        super().__init__()
        self.resize(800, 800)

        self.get_values()


if(__name__ == '__main__'):
    app = QApplication(sys.argv)
    
    demo = ListWidgetDemo()
    demo.show()

    sys.exit(app.exec_())