from db.queries import Queries

q = Queries()
rows = q.select_all_events()

print("\n--- EVENTS IN DB ---\n")

for row in rows:
    print(row)