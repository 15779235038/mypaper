
import   networkx as nx


H = nx.Graph()
nx.add_path(H, [0, 1, 2, 3, 4, 5, 6])
# nx.add_path(H,[2,34,54,65])
#
# print(list(nx.bfs_tree(H,source=2,depth_limit=2).nodes))
# # [(0, 1), (1, 2)]
# # print(nx.eccentricity(H,0))
#
# # A = [1,2,3,4,5]
# # B = [1,2,3]
# # C = [1,2,3,4,5]
# #
# # print  (set(A) > set(B) )

#
#
#
# def diff(listA,listB):
#     #求交集的两种方式
#     retA = [i for i in listA if i in listB]
#     retB = list(set(listA).intersection(set(listB)))
#
#     print ("retA is: ",retA)
#     print ("retB is: ",retB)
#
#     #求并集
#     retC = list(set(listA).union(set(listB)))
#     print ("retC1 is: ",retC)
#
#     #求差集，在B中但不在A中
#     retD = list(set(listB).difference(set(listA)))
#     print ("retD is: ",retD)
#
#     retE = [i for i in listB if i not in listA]
#     print ("retE is: ",retE)
#
# def main():
#     listA = [1,2,3,4,5]
#     listB = [3,4,5,6,7]
#     diff(listA,listB)
#
# if __name__ == '__main__':
#     main()



import   networkx as nx


H = nx.Graph()
nx.add_path(H, [0, 1, 2, 3, 4, 5, 6])


# 在nodelist找出源点来。
times = 3
IDdict = {}
IDdict_dup={}
# 先赋予初始值。
for node in list(H .nodes):
    # subinfectG.node[node]['ID']=list(node)   #赋予的初始值为list
    IDdict[node] = [node]
    IDdict_dup[node]=[node]
allnodelist_keylist = []  # 包含所有接受全部节点id的键值对的key
for t in range(times):
    print('t为' + str(t) + '的时候-----------------------------------------------------------------------------')
    for node in H.nodes:  # 对每一个节点来说
        for heighbour in list(H.neighbors(node)):  # 对每一个节点的邻居来说
            retD = list(set(IDdict[heighbour]).difference(set(IDdict[node])))  # 如果邻居中有这个node没有的，那就加到这个node中去。
            if len(retD) != 0:  # 表示在B中，但不在A.是有的，那就求并集
                # 求并集,把并集放进我们的retC中。
                # print ('并集就是可使用'+str(retD))
                retC = list(set(IDdict[heighbour]).union(set(IDdict[node])))
                IDdict_dup[node]=list(set(IDdict_dup[node]+retC))

    for key, value in IDdict_dup.items():
     IDdict[key] = IDdict_dup[key]
    for key, value in IDdict.items():
        print (key,value)

    # 在每一个时间刻检查是否有节点满足获得所有的id了。

    flag = 0
    for key, value in IDdict.items():
        # d.iteritems: an iterator over the (key, value) items
        if sorted(IDdict[key]) == sorted(list(H.nodes)):
            print('在t为' + str(t) + '的时间的时候，我们有了接受全部node的ID的人')
            print('它的key为' + str(key))
            allnodelist_keylist.append(key)
            print('有了接受所有的节点了这样的节点了')
            flag = 1

    if flag == 1:
        break
# print (IDdict)
print(allnodelist_keylist)