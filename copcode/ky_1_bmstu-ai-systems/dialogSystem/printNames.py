from preprocessing import preprocessing


with open("../docs/data2.csv") as f:
    data = f.read()

items = data.split("\n")[1:]
names = ""
for item in items:
    names += f"{preprocessing(item.split(";")[0])}|"

names = names[:-1].replace(" '", "\\'").replace(" & ", "&")
print(names)
