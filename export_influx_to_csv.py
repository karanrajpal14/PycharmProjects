import csv
from influxdb import InfluxDBClient

USER = 'root'
PASSWORD = 'root'
DB_NAME = 'sensordata'
HOST = 'localhost'
PORT = 8086

client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DB_NAME)

from_date = "2017-11-15 14:55:00"
to_date = "2017-11-15 14:55:05"
measurement = "home"
timezone = "Asia/Kolkata"
query = "select * from {0} where time > '{1}' AND time <= '{2}' tz('{3}')".format(measurement, from_date, to_date, timezone)
print(query)
result = client.query(query, epoch='ns')
exported_data = list(result.get_points())
header_list = list(exported_data[0].keys())
filename = "{0}_{1}_{2}".format(measurement, from_date, to_date)
print(filename)

with open("%s.csv" % filename, "w", newline='') as fp:
    writer = csv.writer(fp, dialect='excel')
    value_header = header_list[1]
    offset = sum(c.isalpha() for c in value_header)
    header_list[1:] = sorted(header_list[1:], key=lambda x: int(x[offset:]))
    writer.writerow(header_list)
    for line in exported_data:
        writer.writerow([line[kn] for kn in header_list])
