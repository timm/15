#http://stackoverflow.com/questions/10943655/pairwaise-testing-combination-generator-in-python
from itertools import chain, combinations, product

def pairwiseGen(n,*sequences):
    unseen = set(chain.from_iterable(product(*i) for i in combinations(sequences, n)))
    for path in product(*sequences):
        common_pairs = set(combinations(path, n)) & unseen
        if common_pairs:
            yield path
            unseen.difference_update(common_pairs)

parameters = [ [ "Brand X", "Brand Y","Brand A","Brand B","Brand C","Brand D" ]
             , [ "98", "NT", "2000", "XP"]
             , [ "Internal", "Modem" ]
             , [ "Salaried", "Hourly", "Part-Time", "Contr." ]
             , [ 6, 10, 15, 30, 60 ]
             ]

parameters = [ [ "Brand X", "Brand Y","Brand A","Brand B","Brand C","Brand D" ]
             , [ "98", "NT", "2000", "XP"]
             , [ "Internal", "Modem","A","B","C","D","E","F","G","H","I","J","K","L","M" ]
             , [ "Salaried", "Hourly", "Part-Time", "Contr.","AA","BB","CC","DD","EE","FF","GG","HH","II" ]
             , [ 6, 10, 15, 30, 60, 70, 80, 90, 100, 110, 120, 130, 140 ]
             ]

print(len(list(pairwiseGen(3,*parameters))))
