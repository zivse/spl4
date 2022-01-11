from persistence import repo
from persistence import order
from persistence import hat
from persistence import supplier
import sys


def parser():
    # repo.create_tables()
    # parsing input file
    file = open(sys.argv[1], 'r')
    line = file.readline()
    num = line.split(",")
    hatsnum = int(num[0])
    suppliernum = int(num[1][:-1])

    for i in range(hatsnum):
        line = file.readline()
        info = line.split(",")
        id = int(info[0])
        topping = info[1]
        currentsupplier = int(info[2])
        quantity = int(info[3][:-1])
        repo.hats.insert(hat(id, topping, currentsupplier, quantity))

    for i in range(suppliernum):
        line = file.readline()
        info = line.split(",")
        id = int(info[0])
        if i == suppliernum-1:
            name = info[1]
        else:
            name = info[1][:-1]
        currentsupplier = supplier(id, name)
        repo.suppliers.insert(supplier(id, name))
    file.close()

    # parsing orders file
    file = open(sys.argv[2], 'r')
    filetowrite = open("output.txt", 'w')
    line = file.readline()
    idcounter = 1
    while(line != None):
        info = line.split(",")
        location = info[0]
        topping = info[1]
        if topping[-1] == "\n":
            topping = topping[:-1]
        hat_list = repo.hats.findall(topping)
        print(hat_list)
        if len(hat_list) == 0 or hat_list == None:
            continue
        min_supplier = hat_list[0][2]
        min_index = 0
        for i in range(1, len(hat_list)):
            if hat_list[i][2] < min_supplier:
                min_supplier = hat_list[i][2]
                min_index = i
        print(f"id of requested hat is {hat_list[min_index][0]}")
        repo.hats.orderhat(hat_list[min_index][0])
        repo.orders.insert(order(idcounter, location, topping))
        suppliername = repo.suppliers.find(min_supplier)
        filetowrite.write(topping+","+suppliername+","+location+"\n")
        line = file.readline()
        idcounter += 1
    file.close()
    filetowrite.close()
