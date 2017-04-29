from accessor import *

def to_bits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def to_comp_name(name):
    cn = "c"
    count = 0
    totals = [0]
    i = 0
    for n in to_bits(name):
        totals[count] += n
        if i % 10 == 0:
            count += 1
            totals.append(0)
        i += 1
    for t in totals:
        cn += str(t)

    return cn

def comp_input_header():
    w = get_world()
    computer = w.player.computer
    computer_location = w.player.computer_location
    owner = w.get_computer(computer).owner

    header = to_comp_name(computer)
    header += ":"
    path = w.player.computer_location
    if len(path) > 0:
        path = path[-1]
    else:
        path = "~"
    header += str(path) + " "
    header += owner + "$"
    header += " "

    return header

def arr_to_path(arr):
    path = ""
    for e in arr:
        path += "/" + str(e)
    return path

def path_to_arr(path):
    arr = []
    for e in path.split("/"):
        arr.append(e)
    return arr