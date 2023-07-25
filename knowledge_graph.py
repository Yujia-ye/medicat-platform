from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
import pandas as pd
import numpy as np

part = []  # 总的发病部位
each_part = []  # 各病的发病部位
department = []  # 总的就诊科室
each_department = []  # 各病的就诊科室
drag = []  # 总的疾病用药
each_drag = []  # 各病的疾病用药
test_self = []  # 总的疾病自测
each_test_self = []  # 各病的疾病自测
name = []  # 疾病名称
each_alias = []  # 各病的疾病别名
ill = pd.read_csv('ill_book_.csv')

for i in ill.index:
    a = []
    p = ill.iloc[i]['发病部位'][1:-1]
    p = p.split(',')
    for j in range(len(p)):
        p[j] = p[j].strip()[1:-1]
        if p[j] == '':
            p[j] = '其他'
        if p[j] not in part:
            part.append(p[j])
        for k in range(len(part)):
            if part[k] == p[j]:
                p[j] = k
                break
        a.append(p[j])
    each_part.append(a)

    '''
    print(ill.iloc[i]['疾病自测'])
    print(ill.iloc[i]['名称'])
    '''

# 就诊科室
for i in ill.index:
    a = []
    p = ill.iloc[i]['就诊科室'][1:-1]
    p = p.split(',')
    for j in range(len(p)):
        p[j] = p[j].strip()[1:-1]
        if p[j] == '':
            p[j] = '其他'
        if p[j] not in department:
            department.append(p[j])
        for k in range(len(department)):
            if department[k] == p[j]:
                p[j] = k
                break
        a.append(p[j])
    each_department.append(a)

# 疾病用药
for i in ill.index:
    a = []
    p = ill.iloc[i]['疾病用药'][1:-1]
    p = p.split(',')
    for j in range(len(p)):
        p[j] = p[j].strip()[1:-1]
        if p[j] == '暂无数据':
            p[j] = ''
        else:
            if p[j] not in drag:
                drag.append(p[j])
            for k in range(len(drag)):
                if drag[k] == p[j]:
                    p[j] = k
                    break
            a.append(p[j])
    each_drag.append(a)

# 疾病自测
for i in ill.index:
    a = []
    p = ill.iloc[i]['疾病自测'][1:-1]
    p = p.split(',')
    for j in range(len(p)):
        p[j] = p[j].strip()[1:-1]
        if p[j] == '暂无数据':
            p[j] = ''
        else:
            if p[j] not in test_self:
                test_self.append(p[j])
            for k in range(len(test_self)):
                if test_self[k] == p[j]:
                    p[j] = k
                    break
            a.append(p[j])
    each_test_self.append(a)

# 疾病名称与别名

for i in ill.index:
    a = []
    p = ill.iloc[i]['名称']
    p = p.split('(',1)
    name.append(p[0])
    if len(p)>1:
        p = p[1].split(',')
        p[-1] = p[-1][:-1]
        www = []
        num = []
        for j in range(len(p)):
            p[j] = p[j].strip()
            if '，' in p[j]:
                w = p[j].split('，')
                www.extend(w)
                num.append(j)
        p.extend(www)
        for nu in num:
            p.pop(nu)
        num.clear()
        for j in range(len(p)):
            if p[j] == '':
                num.append(j)
        for nu in num:
            p.pop(nu)
        each_alias.append(p)
    else:
        each_alias.append(a)

graph = Graph('http://localhost:7474', username='neo4j', password='007672')
graph.delete_all()
name_node = []
part_node = []
department_node = []
drag_node = []
test_self_node = []
alias_node = []
part_relation = []
department_relation = []
drag_relation = []
test_self_relation = []
alias_relation = []

for i in range(len(part)):
    node = Node('part', name=part[i])
    graph.create(node)
    part_node.append(node)
for i in range(len(department)):
    node = Node('department', name=department[i])
    graph.create(node)
    department_node.append(node)
for i in range(len(drag)):
    node = Node('drag', name=drag[i])
    graph.create(node)
    drag_node.append(node)
for i in range(len(test_self)):
    node = Node('test_self', name=test_self[i])
    graph.create(node)
    test_self_node.append(node)
for i in range(len(each_alias)):
    for j in range(len(each_alias[i])):
        node = Node('alias',name=each_alias[i][j])
        graph.create(node)
        alias_node.append(node)
alias_index = 0
for i in range(len(name)):
    node = Node('disease', name=name[i])
    # node['summary'] = ill['概述'][i]
    graph.create(node)
    name_node.append(node)
    for j in range(len(each_part[i])):
        r = Relationship(name_node[i], 'PART_IS', part_node[each_part[i][j]])
        graph.create(r)
        part_relation.append(r)
    for j in range(len(each_department[i])):
        r = Relationship(name_node[i], 'DEPARTMENT_IS', department_node[each_department[i][j]])
        graph.create(r)
        department_relation.append(r)
    for j in range(len(each_drag[i])):
        r = Relationship(name_node[i], 'DRAG_IS', drag_node[each_drag[i][j]])
        graph.create(r)
        drag_relation.append(r)
    for j in range(len(each_test_self[i])):
        r = Relationship(name_node[i], 'TEST_BY_SELF_IS', test_self_node[each_test_self[i][j]])
        graph.create(r)
        test_self_relation.append(r)
    for j in range(len(each_test_self[i])):
        r = Relationship(name_node[i], 'TEST_BY_SELF_IS', test_self_node[each_test_self[i][j]])
        graph.create(r)
        test_self_relation.append(r)
    for j in range(len(each_alias[i])):
        r = Relationship(name_node[i], 'ALIAS_IS', alias_node[alias_index])
        graph.create(r)
        alias_relation.append(r)
        alias_index += 1




