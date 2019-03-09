import pandas as pd
from igraph import Graph as IGraph
#读取文件中边关系，然后成为一个成熟的图
def  txt_Csv(dir):
    sourceNode=[]
    tailNode=[]
    weight=[]
    with open(dir, 'r') as f:
        for line in f:
            line1=line.strip().split("\t")
            sourceNode.append(int(line1[0]))
            tailNode.append(int(line1[1]))
            weight.append(1)
    # 字典中的key值即为csv中列名
    dataframe = pd.DataFrame({'sourceID': sourceNode, 'tailID': tailNode,'weight':weight})
    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv("test.csv", index=False, sep=',')

    return 1




# 转化gml文件到csv
def gml2csv(gmlfile):
    '''
    This function is used to convert a gml file into csv format.
    The graph information included in the gml file will be stored in the csv
    file as edges with the format 'vertex1 vertex2\n'
    gmlfile: The name of the gml file. Path and postfix should be included.
    '''

    g = IGraph.Graph.Read_GML(gmlfile)
    newfile = open(filepath + shotname + '.csv', 'wb')
    writer = csv.writer(newfile, dialect = 'excel')
    for line in g.get_edgelist():
     writer.writerow(line)
    return



# txt_Csv('as_Second.txt')


gml2csv('karate.gml')