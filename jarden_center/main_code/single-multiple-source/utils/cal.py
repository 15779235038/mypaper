import math
def  calcuce(axisA,asisB):
    c1=2.0
    c2=1.0
    x=axisA[0]-asisB[0]
    y=axisA[1]-asisB[1]
    distance=math.sqrt((x ** 2) + (y ** 2))
    return c1*math.log(distance/c2)


import math
def  calcucedistance(axisA,asisB):
    c1=2.0
    c2=1.0
    x=axisA[0]-asisB[0]
    y=axisA[1]-asisB[1]
    distance=math.sqrt((x ** 2) + (y ** 2))
    return distance





 # 计算方位角函数
def azimuthAngle( list1,list2):
    angle = 0.0;
    dx = list2[0] - list1[0]
    dy = list2[1] - list1[1]
    if  list2[0] == list1[0]:
        angle = math.pi / 2.0
        if  list2[1] == list1[1] :
            angle = 0.0
        elif list2[1] < list1[1] :
            angle = 3.0 * math.pi / 2.0
    elif list2[0] > list1[0] and list2[1] > list1[1]:
        angle = math.atan(dx / dy)
    elif  list2[0] > list1[0] and  list2[1] < list1[1] :
        angle = math.pi / 2 + math.atan(-dy / dx)
    elif  list2[0] < list1[0] and list2[1] < list1[1] :
        angle = math.pi + math.atan(dx / dy)
    elif  list2[0] < list1[0] and list2[1] > list1[1] :
        angle = 3.0 * math.pi / 2.0 + math.atan(dy / -dx)
    return (angle * 180 / math.pi)




print (azimuthAngle([1,1],[2,2]))
angele=azimuthAngle([1,1],[2,2])

print (abs(math.cos(math.radians(angele)))*calcucedistance([1,1],[2,2]))

print (math.cos(math.radians(45)))