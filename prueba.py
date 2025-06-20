
people = ['Dr. Christopher Brooks', 'Dr. Kevyn Collins-Thompson', 'Dr. VG Vinod Vydiswaran', 'Dr. Daniel Romero']

def split_title_and_name(person):
    parts = person.split()
    title = parts[0]
    last_name = parts[-1]
    return f"{title} {last_name}"

result = list(map(split_title_and_name, people))
print(result)
