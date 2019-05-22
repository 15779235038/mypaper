def  Process(dir):
        with open(dir, 'r') as f:
            for line in f:
                line1 = line.split()
                G.add_edge(int(line1[0]), int(line1[1]))