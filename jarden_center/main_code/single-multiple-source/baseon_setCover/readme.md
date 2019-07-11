## 1 
1  Source_number_accuracy   文件时没有加贪心就是肯定有源点的   
2  we_heuristic_algorithm.py  加了贪心版本的东西，贪心找点。构成找到的源点。  只对源点贪心
3  main.py  最初的版本，没有源点的选择定位。  
4 heuristic_algorithm_h.py  对h和源点都加了贪心。jaya算法

##  2  思路

1  随机选择a，b两点，相距最少为3.
2  对于传播社区其他点，选择离a，b两点较近的加入。这样构成了两个地方。使用jarden center 试试。这样可以处理我们的
不同时间传播，感染区域重合的问题。


3  