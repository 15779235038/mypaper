#coding=utf-8
from numpy import *
#文件读取
def LoadAdjacentMatrixData(filename,vertices):
    Adjmartrix = [[0 for col in range(vertices)] for row in range(vertices)]
    file_object = open(filename, 'r')
    for x, line in enumerate(file_object):
        line=line.strip()
        t_list = line.split('\t')
        for y in range(len(t_list)):
            Adjmartrix[x][y] = int(t_list[y])
    #Adjmartrix = mat(Adjmartrix)
    return Adjmartrix
#获取队列
def Degree_Sorting(Adjmartrix,vertices):
    degree_s = [[i,0] for i in range(vertices)]
    neighbours = [[] for i in range(vertices)]
    sums = 0
    for i in range(vertices):
        for j in range(vertices):
            if Adjmartrix[i][j] == 1:
                degree_s[i][1] += 1
                sums += 1
                neighbours[i].append(j)
                #degree_s = sorted(degree_s, key=lambda x: x[1], reverse=True)
    return degree_s,neighbours,sums/2
#获取graph的所有邻居节点
def get_allneighbours(coms,neighbours):
    ne = []
    for each in coms:
        for eachne in neighbours[each]:
            if eachne not in ne and eachne not in coms:
                ne.append(eachne)
    return ne
#获取所有graph邻居加入后的F值列表
def get_allfitness(A,coms,neighbours,Func='F'):
    nel = get_allneighbours(coms,neighbours)
    #print 'coms',coms,'neigh',nel
    nelf = []
    if nel:
        if Func == 'Q':
            s,v = get_sumver(A,coms)
            fib = Modulartiy(A,coms,s,v)
        else:
            fib = get_Fitness(A, coms, neighbours)
        for eachne in nel:
            coms.add(eachne)
            if Func == 'Q':
                s,v = get_sumver(A,coms)
                fia = Modulartiy(A,coms,s,v)
            else:
                fia = get_Fitness(A, coms, neighbours)
            fi = fia - fib
            #print 'coms',coms,fi
            nelf.append(fi)
            coms.remove(eachne)
    return nel,nelf
#清洗graph内部F小于0的点（返回F值列表）
def get_infitness(A,coms,neighbours,Func='F'):
    if Func == 'Q':
        s,v = get_sumver(A,coms)
        fia = Modulartiy(A,coms,s,v)
    else:
        fia = get_Fitness(A, coms, neighbours)
    for each in coms:
        coms.remove(each)
        if Func == 'Q':
            s,v = get_sumver(A,coms)
            fib = Modulartiy(A,coms,s,v)
        else:
            fib = get_Fitness(A, coms, neighbours)
        fi = fia - fib
        coms.add(each)
        if fi < 0:
            return each
    return -1
#迭代过程
def Propagate(A,coms,neighbours,Func='F'):
    nel, nelf = get_allfitness(A,coms,neighbours)
    #stops when the nodes all have negative fitness
    if max(nelf) >= 0:
        t = nel[nelf.index(max(nelf))]
        coms.add(t)
        #print 'r',coms
        while(1):
            negative = get_infitness(A,coms,neighbours)
            if negative != -1:
                coms.remove(negative)
                return Propagate(A,coms,neighbours)
            else:
                return Propagate(A,coms,neighbours)
    else:
        return coms
#获取自然子图结构，重叠节点
def get_naturalcoms(A, neighbours,vertices,Func='F'):
    nodes = [i for i in range(vertices)]
    graph = {}
    gnums = 0
    while(1):
        a = nodes[random.randint(len(nodes))]
        graph[gnums] = {a}
        print ('before:','graphid',gnums,',seed',list(graph[gnums]))
        graph[gnums] = Propagate(A,graph[gnums],neighbours,Func)
        print ('after:',list(graph[gnums]))
        for node in graph[gnums]:
            if node in nodes:
                nodes.remove(node)
        if len(nodes) == 0:
            return graph
        gnums += 1
    return graph
#获取graph的边数和节点数
def get_sumver(A,coms):
    s = 0
    v = len(coms)
    for i in coms:
        for j in coms:
            if A[i][j] == 1:
                s += 1
    return s/2,v
#Q函数
def Modulartiy(A, coms, sums,vertices):
    Q = 0.0
    for eachc in coms:
        li = 0
        for eachp in coms[eachc]:
            for eachq in coms[eachc]:
                li += A[eachp][eachq]
        li /= 2
        di = 0
        for eachp in coms[eachc]:
            for eachq in range(vertices):
                di += A[eachp][eachq]
        Q = Q + (li - (di * di) /(sums*4))
    Q = Q / float(sums)
    return Q
#F函数
def get_Fitness(A, coms, neighbours, alpha=1):
    #获得内部度数
    kin = 0
    for eachp in coms:
        for eachq in coms:
            kin += A[eachp][eachq]
    #获得外部度数
    kout = 0
    #只算边数，没考虑连接的外部节点数
    for eachp in coms:
        for each in neighbours[eachp]:
            if each not in coms:
                kout += 1
    fitness = pow((kin + kout),alpha)
    fitness = kin / float(fitness)
    return fitness
#主函数
if __name__ == '__main__':
     #节点个数,V
    vertices = [34,115,105,62]
    txtlist = ['karate.txt','football.txt','books.txt','dolphins.txt']
    #vertices = [64,128,256,512]
    #txtlist = ['RN1.txt','RN2.txt','RN3.txt','RN4.txt']
    testv = [1,2,3,4,5]
    #testv = [i+1 for i in range(34)]
    for i in range(len(txtlist)):
        print (txtlist[i],vertices[i])
        A = LoadAdjacentMatrixData(txtlist[i],vertices[i])
        degree_s, neighbours, sums = Degree_Sorting(A, vertices[i])
        graph = get_naturalcoms(A,neighbours,vertices[i],Func='Q')
        #获得重叠节点
        prenode = {}
        for p in graph:
            for q in graph:
                if p != q:
                    if graph[p]&graph[q]:
                        prenode[str(p)+'_'+str(q)] = graph[p] & graph[q]
        #获得分区结果
        print ('子图结构',graph)
        coms = {}
        for eg in graph:
            coms[eg] = list(graph[eg])
        print ('Q=',Modulartiy(A,coms,sums,vertices[i]))
        print()
