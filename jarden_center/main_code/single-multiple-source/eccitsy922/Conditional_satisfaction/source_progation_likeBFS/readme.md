#  1  验证谣言传播结构确实类似BFS。




## 1     猜想


问题是这个分区的假设是很难成立的。首先，每个源都以一定
的概率去传播，不一定会形成BFS树。 仅仅以BFS为主体去区分
未免不太好。如果我们能够提出更好的分区过程，必定是大大有利的。




## 2 实验


### 2.1     验证单源

实验在单源上，从一个源点的BFS的层数和次数上作图分析。分别以谣言为BFS树根节点以及传播源点来分析传播过程。


###  2.2  验证双源


## 3 反驳

### 3。1  真实不一定，有些点可能传播的特别快。有些点还在慢慢传播，虽然效果一样，但过程不一样。

###  3。2  可不可以有一个真实的动态图形式？

