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

# Декодирование Прюфера
def anticode_pruf(code):
    map_me = dict()
    all_number = len(code) + 2
    anticode = deque()
    for i in range(1, all_number+1):
        map_me[i] = list()
        if i not in code:
            anticode.append(i)
    code = deque(code)
    while len(code) > 0:
        v = code.popleft()
        v2 = anticode.popleft()
        map_me[v].append(v2)
        map_me[v2].append(v)
        if v not in code:
            anticode.appendleft(v)
            anticode = deque(sorted(anticode))
    v = anticode.popleft()
    v2 = anticode.popleft()
    map_me[v].append(v2)
    map_me[v2].append(v)
    # Сортировка не является обязательной!
    for i in map_me:
        map_me[i] = sorted(map_me[i])
    return map_me

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
map_me2 = anticode_pruf(code_pruf(map_me))
for i in map_me2:
    print(str(i), map_me2[i])

