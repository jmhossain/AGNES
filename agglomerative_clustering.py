import math
import heapq

class Floot:
    def __init__(self, value):
        self.val = value
    def __eq__(self, other):
        return (math.isclose(self.val, other.val, rel_tol=1e-8))
    def __ne__(self, other):
        return not(self.__eq__(other))
    def __lt__(self, other):
        return (self.val < other.val and self.__ne__(other))
    def __gt__(self, other):
        return (self.val > other.val and self.__ne__(other))
    def __le__(self, other):
        return (self.__lt__(other) or self.__eq__(other))
    def __ge__(self, other):
        return (self.__gt__(other) or self.__eq__(other))
    
Nk = input().split()
N = int(Nk[0])
K = int(Nk[1])

data_list = []
for i in range(N):
    data_list.append([float(x) for x in input().split()])
    data_list[i].append(i)

dimensions = len(data_list[0])-1

min_heap = []
dissimilarity_matrix = {}
for i in range(N):
    for j in range(i+1, N):
        euclidean_distance = 0.0
        for k in range(dimensions):
            euclidean_distance += (data_list[i][k]-data_list[j][k])**2
        euclidean_distance = math.sqrt(euclidean_distance)
        min_heap.append((Floot(euclidean_distance), i, j, [[i], [j]]))
        dissimilarity_matrix[str(i)+' '+str(j)] = Floot(euclidean_distance)
        dissimilarity_matrix[str(j)+' '+str(i)] = Floot(euclidean_distance)

heapq.heapify(min_heap)

curr_clusters = {}
for i in range(N):
    curr_clusters[str(i)] = (i, [i])
    
old_clusters = []

while len(curr_clusters) > K:
    cluster_distance, min_cluster_id, max_cluster_id, cluster_pair = heapq.heappop(min_heap)
    torf = True
    for old_cluster in old_clusters:
        if old_cluster in cluster_pair:
            torf = False
            break
    if not torf:
        continue
    str1 = " ".join(str(e) for e in cluster_pair[0])
    str2 = " ".join(str(e) for e in cluster_pair[1])
    old_clusters.append(cluster_pair[0])
    old_clusters.append(cluster_pair[1])
    new_cluster_members = sum(cluster_pair, [])
    str3 = " ".join(str(e) for e in new_cluster_members)
    
    del curr_clusters[str1]
    del curr_clusters[str2]
    
    for key in curr_clusters.keys():
        dist1 = dissimilarity_matrix[key + " " + str1]
        dist2 = dissimilarity_matrix[key + " " + str2]
        min_id = min(min_cluster_id, curr_clusters[key][0])
        max_id = max(min_cluster_id, curr_clusters[key][0])
        if dist1 <= dist2:
            dissimilarity_matrix[key+ " " + str3] = dist1
            dissimilarity_matrix[str3+ " " + key] = dist1
        else:
            dissimilarity_matrix[key+ " " + str3] = dist2
            dissimilarity_matrix[str3+ " " + key] = dist2
        
        heapq.heappush(min_heap, (dissimilarity_matrix[key+ " " + str3], min_id, max_id, [new_cluster_members, curr_clusters[key][1]]))
        
    curr_clusters[str3] = (min_cluster_id, new_cluster_members)
    
for val in curr_clusters.values():
    for data in val[1]:
        data_list[data][dimensions]= val[0]
for data in data_list:
    print(data[dimensions])
