# 1  这个是测试单源的效果，如果样本路径的效果本来就差，那我这多源分区效果再好也没用。


# 2  测试手法，看看样本路径行不行。


# 3 一些发现

3.1  单源覆盖也不行的啦，垃圾，综合也到了2。8多


# 1 试试单源收集比较好节点的方法。
# 2 验证手段，判断是否那些收集到50%消息的节点，感染点是否都在里面的。


#  4 文件作用

single_source.py  是为了检测单源定位行不行。 发现准确率本来就比较差啊
sample_way_togetbestNode.py   检测样本路径，能否帮我们拿到比较好的覆盖率集合。
结果发现，能拿到的节点太多了，简直了。都快达到整个感染图那么大了。




