import psycopg2
from datetime import datetime


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


def deleteNotMatchRoute(iti_tab, from_stop, to_stop):
    a_sup=[] 

    for tab in iti_tab: # Suppression 
        if(search_stop(iti_tab[tab], from_stop, to_stop)==False):
            a_sup.append(tab)

    for i in range(len(a_sup)):
            iti_tab.pop(a_sup[i])
    
    return iti_tab

def sort_trip(trips):
    return dict(sorted(trips.items(), key=lambda e: e[1][0][2]))




def getNetwork(from_stop, to_stop, route_type):
    # print(route_type)
    values = [] 
    if(from_stop != to_stop):
        conn = psycopg2.connect(database="", user="", host="", password="")
        cursor = conn.cursor()

        if(route_type == -1):
            cursor.execute(""f"SELECT S.name, N.trip_I, N.arr_time_ut, R.route_name, T.mode_name, S.latitude, S.longitude FROM network_bis N, station S, route R, travel_mode T WHERE R.route_type=T.route_type and  R.route_id=N.route_id and S.stop_id=N.from_stop and trip_I IN ( (SELECT distinct trip_I FROM network_bis N, station S WHERE S.stop_id=N.from_stop and S.name=$${from_stop}$$) INTERSECT (SELECT distinct trip_I FROM network_bis N1, station S1 WHERE S1.stop_id=N1.to_stop and S1.name=$${to_stop}$$)) ORDER BY trip_I, N.route_id, N.arr_time_ut""")
        else:
            cursor.execute(""f"SELECT S.name, N.trip_I, N.arr_time_ut, R.route_name, T.mode_name, S.latitude, S.longitude FROM network_bis N, station S, route R, travel_mode T WHERE R.route_type=T.route_type and R.route_type = $${route_type}$$ and R.route_id=N.route_id and S.stop_id=N.from_stop and trip_I IN ( (SELECT distinct trip_I FROM network_bis N, station S WHERE S.stop_id=N.from_stop and S.name=$${from_stop}$$) INTERSECT (SELECT distinct trip_I FROM network_bis N1, station S1 WHERE S1.stop_id=N1.to_stop and S1.name=$${to_stop}$$)) ORDER BY trip_I, N.route_id, N.arr_time_ut""")

        conn.commit()
        rows = cursor.fetchall()

        iti_tab = {}

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

        iti_tab = deleteNotMatchRoute(iti_tab, from_stop, to_stop)
        iti_tab = sort_trip(iti_tab)

        test_stop=False


        for tab in iti_tab: # tab = itineraire, trip_I 
            str_trip = ""
            i = 0
            for row in iti_tab[tab]:

                if(row[0] == from_stop):
                    str_trip =  str(row[1]) + ";" + str(row[4]) + " " + row[3] +  " : Depart à " + datetime.fromtimestamp(row[2]).strftime("%H:%M:%S") + " : " + row[0] + "*" + row[5] + "*" + row[6] + "*"   
                    test_stop = True

                # if(test_stop == True) :
                    # self.addItem(row[0] + " " + str(row[1]) + " " +  + " " + row[3] )

                if((row[0] == to_stop) & (test_stop == True)) :
                    str_trip += " - Arrivée : "  + row[0] + " à " + datetime.fromtimestamp(row[2]).strftime("%H:%M:%S") + "*" + row[5] + "*" + row[6] + "*" 
                    test_stop = False
                    


                if((row[0] == to_stop) &  (test_stop == False)) :
                    break
            i+=1
            if((str_trip != "") & (i<= 5)):    
                values.append(str_trip)

    if(len(values) == 0):
        values.append(" ;***No route available !**")   

    return values

def get_route(trip_id, from_stop, to_stop):
    str_trip=""
    if(from_stop != to_stop):
        conn = psycopg2.connect(database="", user="", host="", password="")
        cursor = conn.cursor()

        cursor.execute(""f"SELECT S.name, N.arr_time_ut, R.route_name, T.mode_name FROM network_bis N, station S, route R, travel_mode T WHERE R.route_type=T.route_type and  R.route_id=N.route_id and S.stop_id=N.from_stop and N.trip_I=$${trip_id}$$ ORDER BY N.arr_time_ut""")

        conn.commit()
        rows = cursor.fetchall()

        # tab = rows 


        test_stop=False

        # tab = itineraire, trip_I
        direction="Direction : " + rows[(len(rows)-1)][0]
        travel= str(rows[0][3] + " " + rows[0][2] + " ")# mode name et route name 
        str_trip= travel + ":" + direction + ";"

        for row in rows:
            if(row[0] == from_stop):
                test_stop = True

            if(test_stop == True) :
                str_trip += str(row[0]) + "   " + datetime.fromtimestamp(row[1]).strftime("%H:%M:%S") + ","
                

            if((row[0] == to_stop) & (test_stop == True)) :
                test_stop = False

            if((row[0] == to_stop) &  (test_stop == False)) :
                break
  

    return str_trip

def save_to_database(from_station, to_station, hist_name):
    count = 0
    if(from_station != to_station):
        conn = psycopg2.connect(database="", user="", host="", password="")
        cursor = conn.cursor()
        cursor.execute(""f" INSERT INTO registered VALUES ($${hist_name}$$ , $${from_station}$$ , $${to_station}$$ )""")

        conn.commit()
        count = cursor.rowcount
    
    return count


def VerifyRouteInDatabase(hist_name):
    count = 0
    conn = psycopg2.connect(database="", user="", host="", password="")
    cursor = conn.cursor()
    cursor.execute(""f"SELECT from_station, to_station FROM registered WHERE name = $${hist_name}$$ LIMIT 1""")

    conn.commit()
    rows = cursor.fetchall()
    return rows
def info_disturb():
    values = [] 
    conn = psycopg2.connect(database="", user="", host="", password="")
    cursor = conn.cursor()

    date_actuel = str(datetime.today()).split(" ")[0]
    date_actuel = date_actuel.split("-")



    cursor.execute(""f"SELECT mode_name, route_name, d_message, end_at FROM travel_mode T, route R, disturb D WHERE T.route_type = R.route_type and D.route_id = R.route_id""")
    conn.commit()
    rows = cursor.fetchall()

    for row in rows:
        
        date_end = str(row[3]).split("-")

        if((date_end[0] >= date_actuel[0]) & (date_end[1] >= date_actuel[1]) & (date_end[2] >= date_actuel[2])):
            values.append(row[0] + " "+row[1] + ": "+row[2])
    
    return values