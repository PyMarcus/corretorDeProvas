data = "[{'1': [0, 2]}, {'2': [1, 1]}]".split('}, {')
data1 = data[0].replace('{', '').replace('[', '').replace(']', '').replace('}', '').strip()
data2 = data[1].replace('{', '').replace('[', '').replace(']', '').replace('}', '').strip()
print(f"Questão {int(data1[1])}: {data1.split(':')[1][1]} acertos e {data1.split(':')[1][4].replace(',', '')} erros")
print(f"Questão {int(data2[1])}: {data2.split(':')[1][1]} acertos e {data2.split(':')[1][4].replace(',', '')} erros")

