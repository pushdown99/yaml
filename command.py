import yaml

dct = yaml.safe_load('''
name: John
age: 30
automobiles:
- brand: Honda
  type: Odyssey
  year: 2018
- brand: Toyota
  type: Sienna
  year: 2015
''')
assert dct['name'] == 'John'
assert dct['age'] == 30
assert len(dct["automobiles"]) == 2
assert dct["automobiles"][0]["brand"] == "Honda"
assert dct["automobiles"][1]["year"] == 2015


print(dct['name'])
