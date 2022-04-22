from collections import deque


# Обход графа в ширину для проверки
def check_bfs(map_me, v, bfs_user):
    ans = []
    check_v = [0]*len(map_me)
    check_v[v-1] = 1
    dq = deque()
    dq.append(v)
    step = 1
    while len(dq) > 0:
        new_dq = deque()
        while len(dq) > 0:
            cell = dq.popleft()
            for i in map_me[cell]:
                if check_v[i-1] == 0:
                    new_dq.append(i)
            check_v[cell-1] = 1
            ans.append([step, cell])
        dq = new_dq
        step += 1
    for i in range(1, step):
        tmp_ans = []
        for j in range(len(ans)):
            if ans[j][0] == i:
                tmp_ans.append(ans[j][1])
        tmp_bfs = bfs_user[:len(tmp_ans)]
        if len(tmp_bfs) != len(tmp_ans):
            return False
        tmp_bfs = sorted(tmp_bfs)
        for i in range(len(tmp_bfs)):
            if tmp_bfs[i] != tmp_ans[i]:
                return False
        ans = ans[len(tmp_ans):]
        bfs_user = bfs_user[len(tmp_ans):]
    return True


# Список смежности 
map_me = {
    1: [2, 3],
    2: [1, 4, 5],
    3: [1, 6, 7],
    4: [2, 8],
    5: [2],
    6: [3],
    7: [3],
    8: [4]
    }

# Пример входных данных пользователя
# Первая вершина, с которой мы будем обходить граф в ширину
# Brat
bfs_user = [1, 2, 3, 4, 5, 6, 7, 8]

# Brat
bfs_user2 = [1, 3, 2, 5, 4, 7, 6, 8]

# Ne Brat
bfs_user3 = [1, 3, 2, 5, 4, 7, 6]

# Ne Brat
bfs_user4 = [1, 3, 5, 2, 4, 7, 6, 8]

print(check_bfs(map_me, bfs_user4[0], bfs_user4))
