from collections import deque

# Код Прюфера возвращается в виде массива
# На вход подается список смежности
def code_pruf(map_me2):
    map_me = dict()
    for i in map_me2:
        map_me[i] = map_me2[i]
    ans = []
    dq = deque()
    for i in map_me:
        if len(map_me[i]) == 1:
            dq.append(i)
    dq = deque(sorted(dq))
    while len(dq) > 0:
        v = dq.popleft()
        if len(map_me[v]) == 0:
            break
        ans.append(map_me[v][0])
        tmp = []
        for i in map_me[map_me[v][0]]:
            if i != v:
                tmp.append(i)
        map_me[map_me[v][0]] = tmp
        if len(map_me[map_me[v][0]]) == 1:
            dq.append(map_me[v][0])
            dq = deque(sorted(dq))
    return ans[:len(ans)-1]

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

print(code_pruf(map_me))

