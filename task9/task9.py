from collections import deque

##ans2 = []
# Нахождения кратчайших путей от заданной вершины до остальных
# вершин графа
def min_dist_nodes(map_me, point_start):
##    global ans2
    visit_v = set()
    dq = deque()
    dq.append([point_start, 0])
    ans = dict()
    
    for i in map_me:
        ans[i] = 1000000
    ans[point_start] = 0
    while len(dq) > 0:
        v = dq.popleft()
        visit_v.add(v[0])
        mn = [1000000, 1000000]
        for i in visit_v:
            for j in map_me[i]:
                if j[0] not in visit_v:
                    if mn[1] > j[1]:
                        mn = j
                    if ans[i] + j[1] < ans[j[0]]:
                        ans[j[0]] = ans[i] + j[1]
##                        ans2[i-1][j[0]-1] = j[0]
        if mn[0] != 1000000:
            dq.append(mn)
    return ans

# Создание матрицы кратчайших путей
def matrix_min_put(map_me):
##    global ans2
    # Матрица кратчайших(смежности) путей
    ans = []
##    # Матрица достижимости
##    ans2 = []
##    for i in map_me:
##        tmp2 = []
##        for j in map_me:
##            tmp2.append(j)
##        ans2.append(tmp2)
    for i in map_me:
        tmp = []
        t = min_dist_nodes(map_me, i)
        for j in map_me:
            tmp.append(t[j])
        ans.append(tmp)

    for i in ans:
        print(i)
    print()
        
    for q in map_me:
        for i in map_me[q]:
            for j in map_me[q]:
##                if i[1] + j[1] < ans[i[0]-1][j[0]-1]:
##                    ans2[i[0]-1][j[0]-1] = q
                ans[i[0]-1][j[0]-1] = min(ans[i[0]-1][j[0]-1], i[1] + j[1])
    return ans
    
  
# Список смежности с весом ребра
map_me = {
    1: [[2, 2], [5, 6], [6, 3]],
    2: [[1, 2], [3, 4], [6, 1], [7, 7]],
    3: [[2, 4], [4, 1], [7, 6], [8, 5]],
    4: [[3, 1], [8, 6]],
    5: [[1, 6], [6, 5]],
    6: [[1, 3], [2, 1], [5, 5], [7, 7]],
    7: [[2, 7], [3, 6], [6, 7], [8, 3]],
    8: [[3, 5], [4, 6], [7, 3]]
    }

### Список смежности с весом ребра
##map_me = {
##    1: [[2, 2], [3, 6], [4, 8], [7, 3]],
##    2: [[1, 2], [3, 9], [4, 3], [6, 4], [7, 9]],
##    3: [[1, 6], [2, 9], [4, 7]],
##    4: [[1, 8], [2, 3], [3, 7], [5, 5], [6, 5]],
##    5: [[4, 5], [7, 8], [8, 9]],
##    6: [[2, 4], [4, 5], [8, 6], [9, 4]],
##    7: [[1, 3], [2, 9], [5, 8]],
##    8: [[5, 9], [6, 6], [9, 1]],
##    9: [[6, 4], [8, 1]]
##    }

# Матрица кратчайших(смежности) путей
matr_s = matrix_min_put(map_me)

for i in matr_s:
    print(i)
            
            

