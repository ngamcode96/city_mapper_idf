

SELECT trip_I FROM network_bis
WHERE from_stop IN (SELECT stop_id FROM station WHERE name = 'MASSY PALAISEAU')
GROUP BY trip_I

INTERSECT

SELECT S1.name, N1.trip_I, N1.dep_time_ut, N1.arr_time_ut, N1.route_id FROM network_bis N1, station S1  WHERE N1.from_stop = S1.stop_id and (N1.route_id, N1.trip_I) IN  ((SELECT  N.route_id, N.trip_I FROM network_bis N, station S WHERE from_stop = S.stop_id and S.name = 'MASSY PALAISEAU') INTERSECT ( SELECT DISTINCT N.route_id, N.trip_I FROM network_bis N, station S WHERE to_stop = S.stop_id and S.name = 'PARIS NORD'))