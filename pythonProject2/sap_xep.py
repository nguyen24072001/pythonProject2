switch_pos = [(370, 182, 36), (212, 182, 36), (372, 302, 38), (206, 304, 36)]
a = 290
b = 242
center = (a, b)

print(switch_pos)
print(center)

item1 = []
for i in range(4):
    item = tuple(switch_pos[i][:2])
    item1.append(item)

for i in range(4):
    # print(item1[i])
    if item1[i][0] > center[0] and item1[i][1] > center[1]:
        print("LED 1")
        print(item1[i][0], item1[i][1])
    elif item1[i][0] < center[0] and item1[i][1] > center[1]:
        print("LED 2")
        print(item1[i][0], item1[i][1])
    elif item1[i][0] > center[0] and item1[i][1] < center[1]:
        print("LED 3")
        print(item1[i][0], item1[i][1])
    elif item1[i][0] < center[0] and item1[i][1] < center[1]:
        print("LED 4")
        print(item1[i][0], item1[i][1])




