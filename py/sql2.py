import psycopg2
from datetime import datetime

def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

conn = psycopg2.connect(database="", user="", host="", password="")
cursor = conn.cursor()

cursor.execute("""SELECT S.name, N.trip_I, N.arr_time_ut, R.route_name FROM network_bis N, station S, route R WHERE  R.route_id=N.route_id and S.stop_id=N.from_stop and trip_I IN ( (SELECT distinct trip_I FROM network_bis N, station S WHERE S.stop_id=N.from_stop and S.name='PARIS NORD') INTERSECT (SELECT distinct trip_I FROM network_bis N1, station S1 WHERE S1.stop_id=N1.to_stop and S1.name='ANTONY')) ORDER BY trip_I, N.route_id, N.arr_time_ut""")
conn.commit()
rows = cursor.fetchall()

iti = rows[0][1]
#print(iti)
test_stop=False
skip=False

# tab ={} 
# tab[3]=3
# tab[10]=10

# for i in tab :
#     print(i)
#     print(len(tab))
# print(tab[10])

for row in rows :
    heure_actuel = get_sec(datetime.today().strftime("%H:%M:%S"))
    heure_bdd = get_sec(datetime.fromtimestamp(row[2]).strftime("%H:%M:%S"))

    if(heure_actuel<= heure_bdd):
        if(iti != row[1]) :
            print("-------------------------------------------------------------------")
            iti = row[1]
            test_stop=False
            skip=False

        if((row[0] == 'ANTONY') & (test_stop == False)) :
            skip=True

        if(row[0] == 'PARIS NORD') :
            test_stop = True
        
        if((test_stop==True) & (skip==False)) :
            print(row[0] + " " + str(row[1]) + " " + datetime.fromtimestamp(row[2]).strftime("%H:%M:%S") + " " + row[3] )

        if(row[0] == 'ANTONY') :
            test_stop = False
    