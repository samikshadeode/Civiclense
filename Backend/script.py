import sqlite3
conn = sqlite3.connect('civiclens.db')
c = conn.cursor()
for row in c.execute("SELECT report_id, lat, lon FROM reports ORDER BY report_id DESC LIMIT 1"):
    print(row)
conn.close()