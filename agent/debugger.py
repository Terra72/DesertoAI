from db.queries import Queries

q = Queries()
rows = q.select_all_events()

for row in rows:
    print(row)