import networkx as nx
import matplotlib.pyplot as plt
import random
from scipy import stats
import math
from datetime import datetime


def date_difference(dt1, dt2):
    datetime1 = dt1.split(" ")
    datetime2 = dt2.split(" ")
    date1 = datetime1[0].split("/")
    date2 = datetime2[0].split("/")
    dt_1 = datetime.strptime('{}-{}-{} {}'.format(date1[2], date1[1], date1[0], datetime1[1]), '%Y-%m-%d %H:%M:%S')
    dt_2 = datetime.strptime('{}-{}-{} {}'.format(date2[2], date2[1], date2[0], datetime2[1]), '%Y-%m-%d %H:%M:%S')
    timedelta = dt_2 - dt_1
    print(timedelta)
    return timedelta.days * 24 * 3600 + timedelta.seconds


def dfs_color(g, s, d, cn, v_not, v_pos_0, v_neg_0, v_pos_1, v_neg_1, v_pos_2, v_neg_2):
    g.node[s]['visited'] = True
    d += 1
    for a in g[s]:
        if g[s][a]['visited'] is False:
            g[s][a]['visited'] = True
            for a_c in range(cn['n_components']):
                id_s = cn['id_component_{}'.format(a_c)]
                cl_s = cn['color_{}'.format(a_c)]
                #                 print("distance", d)
                if d == 1:
                    if cl_s == "grey/black":
                        cn['color_{}'.format(a_c)] = "black"
                        cl_s = "black"
                    elif cl_s == "grey/white":
                        cn['color_{}'.format(a_c)] = "white"
                        cl_s = "white"
                #                 print("source", s, cl_s, id_s)
                a_col = ""
                for a_cc in range(g.nodes[a]['n_components']):
                    if g.nodes[a]['id_component_{}'.format(a_cc)] is id_s:
                        a_col = g.nodes[a]['color_{}'.format(a_cc)]
                #                         print(a, a_col, g.nodes[a]['id_component_{}'.format(a_cc)], id_s)
                if a_col == "grey":
                    v_not[id_s].append((s, a))
                    #                     print("v_not append", s, a)
                    dfs_color(g, a, d, cn, v_not, v_pos_0, v_neg_0, v_pos_1, v_neg_1, v_pos_2, v_neg_2)
                elif a_col == cl_s or a_col == "grey/{}".format(cl_s):
                    if g[s][a]['weight'] == 0:
                        v_not[id_s].append((s, a))
                        #                         print("v_not append", s, a)
                        dfs_color(g, a, d, cn, v_not, v_pos_0, v_neg_0, v_pos_1, v_neg_1, v_pos_2, v_neg_2)
                    else:
                        v_pos_0[id_s].append((s, a))
                        v_pos_1[id_s].append(float(1 / (2 ** d)))
                        v_pos_2[id_s].append(float(1 / d))
                        #                         print("v_pos append", s, a)
                        dfs_color(g, a, d, cn, v_not, v_pos_0, v_neg_0, v_pos_1, v_neg_1, v_pos_2, v_neg_2)
                else:
                    if g[s][a]['weight'] == 0:
                        v_not[id_s].append((s, a))
                        #                         print("v_not append", s, a)
                        dfs_color(g, a, d, cn, v_not, v_pos_0, v_neg_0, v_pos_1, v_neg_1, v_pos_2, v_neg_2)
                    else:
                        v_neg_0[id_s].append((s, a))
                        v_neg_1[id_s].append(float(1 / (2 ** d)))
                        v_neg_2[id_s].append(float(1 / d))
                        #                         print("v_neg append", s, a)
                        dfs_color(g, a, d, cn, v_not, v_pos_0, v_neg_0, v_pos_1, v_neg_1, v_pos_2, v_neg_2)


def build_dag(g, n_edges, maxxx):
    for m in range(maxxx):
        if maxxx - m - n_edges > 0:
            for w in range(random.randint(0, n_edges)):
                r = random.randint(m + 1, maxxx)
                while g.has_edge(m, r):
                    print("has edge {0}-{1}".format(m, r))
                    r = random.randint(m + 1, maxxx)
                g.add_edge(m, r, weight=random.randint(-1, 1), visited=False)


def allEqualLabels(es):
    e = es[0]
    for x in range(1, len(es)):
        if es[x][2] != e[2]:
            return False
    return True


def allConfirmationSharingLabels(es):
    for x in range(len(es)):
        if es[x][2] == -1:
            return False
    return True


def allConfutationSharingLabels(es):
    for x in range(len(es)):
        if es[x][2] == 1:
            return False
    return True


def allConfutationLabels(es):
    for x in range(len(es)):
        if es[x][2] == 1 or es[x][2] == 0:
            return False
    return True


def allConfirmationLabels(es):
    for x in range(len(es)):
        if es[x][2] == -1 or es[x][2] == 0:
            return False
    return True


def allSharingLabels(es):
    for x in range(len(es)):
        if es[x][2] == -1 or es[x][2] == 1:
            return False
    return True


def isAdmissible(es, uns):
    src = []
    for e in es:
        for cmp in range(e[3]['n_components']):
            if e[3]['id_component_{}'.format(cmp)] not in src:
                src.append(e[3]['id_component_{}'.format(cmp)])
                B = []
                W = []
                Gr = []
                if e[3]['color_{}'.format(cmp)] == "grey":
                    Gr.append(e)
                elif e[3]['color_{}'.format(cmp)] == "white" or e[3]['color_{}'.format(cmp)] == "grey/white":
                    W.append(e)
                elif e[3]['color_{}'.format(cmp)] == "black" or e[3]['color_{}'.format(cmp)] == "grey/black":
                    B.append(e)
                for ee in es:
                    if ee != e:
                        for c in range(ee[3]['n_components']):
                            if ee[3]['id_component_{}'.format(c)] == e[3]['id_component_{}'.format(cmp)]:
                                if ee[3]['color_{}'.format(c)] == "grey":
                                    Gr.append(ee)
                                elif ee[3]['color_{}'.format(c)] == "white" or ee[3][
                                    'color_{}'.format(c)] == "grey/white":
                                    W.append(ee)
                                elif ee[3]['color_{}'.format(c)] == "black" or ee[3][
                                    'color_{}'.format(c)] == "grey/black":
                                    B.append(ee)
                #                 print(B)
                #                 print(W)
                #                 print(Gr)
                if len(Gr) > 0:
                    if (len(B) > 0 and not allSharingLabels(B)) or (len(W) > 0 and not allSharingLabels(W)) or not allSharingLabels(Gr):
                        return False
                else:
                    if len(B) > 0 and len(W) == 0:
                        if not allEqualLabels(B) and not allConfirmationSharingLabels(B):
                            return False
                    elif len(B) == 0 and len(W) > 0:
                        if not allEqualLabels(W) and not allConfirmationSharingLabels(W):
                            return False
                    else:
                        if (not allConfutationLabels(B) or not allConfirmationSharingLabels(W)) and (
                                not allConfutationLabels(W) or not allConfirmationSharingLabels(B)) and (
                                not allSharingLabels(B) or not allSharingLabels(W)):
                            return False
                if len(B) > 0 and len(W) > 0 and allSharingLabels(B) and allSharingLabels(W):
                    uns.append(e[3]['id_component_{}'.format(cmp)])
    return True


def insertNodeDAG(g, h, edges, k, dt):
    #     print(edges)
    if k == 0:
        g.add_node(h, visited=False, n_components=1, color_0="black", id_component_0=h, time=dt)
        print("Node {0} is inserted".format(h))
    elif k == 1:
        g.add_node(h, visited=False, n_components=0, time=dt)
        print("Node {0} is inserted".format(h))
        n_c = edges[0][3]['n_components']
        for cmp in range(n_c):
            cl = edges[0][3]['color_{}'.format(cmp)]
            if cl == "grey" and edges[0][2] != 0:
                print("Edge {}-{} is not inserted".format(edges[0][0], edges[0][1]))
            else:
                g.add_edge(edges[0][0], edges[0][1], weight=edges[0][2], visited=False)
                g.node[edges[0][1]]['id_component_{}'.format(cmp)] = edges[0][3]['id_component_{}'.format(cmp)]
                if cl == "grey":
                    g.node[edges[0][1]]['color_{}'.format(cmp)] = "grey"
                elif cl == "black" or cl == "grey/black":
                    if edges[0][2] == 0:
                        g.node[edges[0][1]]['color_{}'.format(cmp)] = "grey/black"
                    elif edges[0][2] == 1:
                        g.node[edges[0][1]]['color_{}'.format(cmp)] = "black"
                    else:
                        g.node[edges[0][1]]['color_{}'.format(cmp)] = "white"
                else:
                    if edges[0][2] == 0:
                        g.node[edges[0][1]]['color_{}'.format(cmp)] = "grey/white"
                    elif edges[0][2] == 1:
                        g.node[edges[0][1]]['color_{}'.format(cmp)] = "white"
                    else:
                        g.node[edges[0][1]]['color_{}'.format(cmp)] = "black"
                g.node[edges[0][1]]['n_components'] += 1
                print("node", edges[0][1], "color", g.node[edges[0][1]]['color_{}'.format(cmp)], "component",
                      g.node[edges[0][1]]['id_component_{}'.format(cmp)], "number", cmp)
    else:
        unstables = []
        if isAdmissible(edges, unstables):
            g.add_node(h, visited=False, n_components=0, time=dt)
            print("Node {0} is inserted".format(h))
            print("unstables", unstables)
            cmp = 0
            sources = []
            for e in edges:
                g.add_edge(e[0], e[1], weight=e[2], visited=False)
                for c in range(e[3]['n_components']):
                    if e[3]['id_component_{}'.format(c)] not in sources:
                        sources.append(e[3]['id_component_{}'.format(c)])
                        g.node[e[1]]['id_component_{}'.format(cmp)] = e[3]['id_component_{}'.format(c)]
                        if e[3]['color_{}'.format(c)] == "grey" or e[3]['id_component_{}'.format(c)] in unstables:
                            g.node[e[1]]['color_{}'.format(cmp)] = "grey"
                        elif e[3]['color_{}'.format(c)] == "black" or e[3]['color_{}'.format(c)] == "grey/black":
                            if e[2] == 0:
                                g.node[e[1]]['color_{}'.format(cmp)] = "grey/black"
                            elif e[2] == 1:
                                g.node[e[1]]['color_{}'.format(cmp)] = "black"
                            else:
                                g.node[e[1]]['color_{}'.format(cmp)] = "white"
                        else:
                            if e[2] == 0:
                                g.node[e[1]]['color_{}'.format(cmp)] = "grey/white"
                            elif e[2] == 1:
                                g.node[e[1]]['color_{}'.format(cmp)] = "white"
                            else:
                                g.node[e[1]]['color_{}'.format(cmp)] = "black"
                        print("node", e[1], "color", g.node[e[1]]['color_{}'.format(cmp)], "component",
                              g.node[e[1]]['id_component_{}'.format(cmp)], "number", cmp)
                        cmp += 1
                        g.node[e[1]]['n_components'] += 1
                        print("n_components", g.node[e[1]]['n_components'])
                    else:
                        for ic in range(cmp):
                            if g.node[e[1]]['id_component_{}'.format(ic)] == e[3]['id_component_{}'.format(c)]:
                                past_clr = g.node[e[1]]['color_{}'.format(ic)]
                                if past_clr != "white" and past_clr != "black":
                                    if e[3]['color_{}'.format(c)] == "grey" or e[3][
                                        'id_component_{}'.format(c)] in unstables:
                                        g.node[e[1]]['color_{}'.format(ic)] = "grey"
                                    elif past_clr == "grey/black" and e[2] != 0:
                                        g.node[e[1]]['color_{}'.format(ic)] = "black"
                                    elif past_clr == "grey/white" and e[2] != 0:
                                        g.node[e[1]]['color_{}'.format(ic)] = "white"
                                print("node", e[1], "color", g.node[e[1]]['color_{}'.format(ic)], "component",
                                      g.node[e[1]]['id_component_{}'.format(ic)], "number", ic, "n_components",
                                      g.node[e[1]]['n_components'])
        else:
            g.add_node(h, visited=False, n_components=1, color_0="black", id_component_0=h, time=dt)
            print("Insertion not admissible, Node {0} is inserted as source!".format(h))


def build_news_graph(g, lim):
    for head in range(lim):
        in_edges = []
        tails = []
        k = random.randint(0, head)
        if k < head and head - 1 > 0:
            for o in range(k):
                tail = random.randint(0, head - 1)
                lab = random.randint(-1, 1)
                while tail in tails:
                    print("has edge {0}-{1}".format(tail, head))
                    tail = random.randint(0, head - 1)
                tails.append(tail)
                in_edges.append([tail, head, lab, g.node[tail]])
            insertNodeDAG(g, head, in_edges, k)
        else:
            insertNodeDAG(g, head, in_edges, 0)


def count_swap(d1, d2, len):
    p = 0
    for z in range(len):
        for u in range(len):
            if d1[z][0] == d2[u][0]:
                pp = 0
                #                 print("{0} node is in position {1} and {2}".format(d1[z][0], z, u))
                for zz in range(len):
                    if zz != z:
                        for uu in range(len):
                            if uu != u:
                                if d1[zz][0] == d2[uu][0]:
                                    if (zz > z and uu < u) or (zz < z and uu > u):
                                        pp += 1
        #                 print(pp)
        p += pp
    #     print(p)
    return float(p / (len * (len - 1)))


def distances(d1, d2, len):
    res = {}
    avg = 0
    for z in range(len):
        res[z] = math.sqrt(abs(pow(d1[z][1], 2) - pow(d2[z][1], 2)))
        avg += res[z]
    #     print(float(avg/len))
    #     return res
    return float(avg / len)


def w_in(g, u, v):
    iv = len(g.in_edges(v))
    if iv == 0:
        return 1
    iu = 0
    for uu, vv in g.out_edges(u):
        iu += len(g.in_edges(vv))
    return float(iv / iu)


def w_out(g, u, v):
    ov = len(g.out_edges(v))
    if ov == 0:
        return 1
    ou = 0
    for uu, vv in g.out_edges(u):
        ou += len(g.out_edges(vv))
    return float(ov / ou)


def simplifiedPR(g, l, i, d):
    r = 0
    init = float((1 - d) / len(list(g.nodes)))
    if not g.node[i]['visited']:
        g.node[i]['visited'] = True
        #         print("simplifiedPR {}".format(i))
        for u, v in g.in_edges(i):
            simplifiedPR(g, l, u, d)
            win = w_in(g, u, v)
            wout = w_out(g, u, v)
            pu = float(l[u] * win * wout)
            #            pu = float(l[u] / len(g.out_edges(u)))
            r += pu
        l[i] = init + d * r


def PageRank(g, d):
    ns = list(g.nodes)
    init = float((1 - d) / len(ns))
    #    print(d, init)
    rl = dict((e, 0) for e in ns)
    for idx in ns:
        simplifiedPR(g, rl, idx, d)
    return rl


def new_news_graph_DAG():
    dag = nx.DiGraph()

    ine = []
    # 0
    insertNodeDAG(dag, 0, ine, 0, "30/7/2017 7:45:22")
    # 1
    ine.clear()
    ine.append([0, 1, 1, dag.node[0]])
    insertNodeDAG(dag, 1, ine, 1, "30/7/2017 10:09:12")
    # 2
    ine.clear()
    ine.append([0, 2, 0, dag.node[0]])
    insertNodeDAG(dag, 2, ine, 1, "30/7/2017 11:03:00")
    # 3
    ine.clear()
    ine.append([0, 3, 0, dag.node[0]])
    insertNodeDAG(dag, 3, ine, 1, "30/7/2017 11:56:55")
    # 4
    ine.clear()
    ine.append([0, 4, 0, dag.node[0]])
    insertNodeDAG(dag, 4, ine, 1, "30/7/2017 13:02:58")
    # 5
    ine.clear()
    ine.append([0, 5, 0, dag.node[0]])
    insertNodeDAG(dag, 5, ine, 1, "30/7/2017 15:44:00")
    # 6
    ine.clear()
    ine.append([0, 6, 0, dag.node[0]])
    insertNodeDAG(dag, 6, ine, 1, "30/7/2017 16:07:33")
    # 7
    ine.clear()
    ine.append([0, 7, 1, dag.node[0]])
    ine.append([1, 7, 1, dag.node[1]])
    insertNodeDAG(dag, 7, ine, 2, "30/7/2017 16:37:00")
    # 8
    ine.clear()
    ine.append([0, 8, 1, dag.node[0]])
    ine.append([1, 8, 1, dag.node[1]])
    ine.append([7, 8, 1, dag.node[7]])
    insertNodeDAG(dag, 8, ine, 3, "31/7/2017 14:26:00")
    # 9
    ine.clear()
    ine.append([0, 9, 1, dag.node[0]])
    ine.append([1, 9, 1, dag.node[1]])
    ine.append([7, 9, 1, dag.node[7]])
    ine.append([8, 9, 1, dag.node[8]])
    insertNodeDAG(dag, 9, ine, 4, "31/7/2017 15:37:10")
    # 10
    ine.clear()
    ine.append([0, 10, 1, dag.node[0]])
    ine.append([1, 10, 1, dag.node[1]])
    ine.append([7, 10, 1, dag.node[7]])
    ine.append([8, 10, 1, dag.node[8]])
    insertNodeDAG(dag, 10, ine, 4, "31/7/2017 16:26:00")
    # 11
    ine.clear()
    ine.append([3, 11, 0, dag.node[3]])
    ine.append([10, 11, 0, dag.node[10]])
    insertNodeDAG(dag, 11, ine, 2, "31/7/2017 16:28:58")
    # 12
    ine.clear()
    ine.append([6, 12, 0, dag.node[6]])
    insertNodeDAG(dag, 12, ine, 1, "31/7/2017 18:35:08")
    # 13
    ine.clear()
    ine.append([1, 13, 0, dag.node[1]])
    insertNodeDAG(dag, 13, ine, 1, "31/7/2017 18:40:46")
    # 14
    ine.clear()
    ine.append([3, 14, 0, dag.node[3]])
    ine.append([11, 14, 0, dag.node[11]])
    insertNodeDAG(dag, 14, ine, 2, "31/7/2017 19:45:41")
    # 15
    ine.clear()
    ine.append([13, 15, 0, dag.node[13]])
    insertNodeDAG(dag, 15, ine, 1, "31/7/2017 23:59:59")
    # 16
    ine.clear()
    ine.append([12, 16, 0, dag.node[12]])
    insertNodeDAG(dag, 16, ine, 1, "4/8/2017 20:56:15")
    # 17
    ine.clear()
    insertNodeDAG(dag, 17, ine, 0, "5/8/2017 18:25:13")
    # 18
    insertNodeDAG(dag, 18, ine, 0, "5/8/2017 20:11:00")
    # 19
    ine.clear()
    ine.append([16, 19, 0, dag.node[16]])
    ine.append([17, 19, 0, dag.node[17]])
    ine.append([18, 19, 0, dag.node[18]])
    insertNodeDAG(dag, 19, ine, 3, "6/8/2017 16:52:35")
    # 20
    ine.clear()
    insertNodeDAG(dag, 20, ine, 0, "2/11/2017 20:56:51")
    # 21
    insertNodeDAG(dag, 21, ine, 0, "4/11/2017 6:53:00")
    # 22
    ine.append([21, 22, 0, dag.node[21]])
    insertNodeDAG(dag, 22, ine, 1, "6/11/2017 7:31:36")
    # 23
    ine.clear()
    insertNodeDAG(dag, 23, ine, 0, "21/11/2017 7:55:00")
    # 24
    ine.append([23, 24, 1, dag.node[23]])
    insertNodeDAG(dag, 24, ine, 1, "21/11/2017 9:25:19")
    # 25
    ine.clear()
    ine.append([23, 25, 1, dag.node[23]])
    ine.append([24, 25, 1, dag.node[24]])
    insertNodeDAG(dag, 25, ine, 2, "21/11/2017 10:01:22")
    # 26
    ine.clear()
    ine.append([24, 26, 0, dag.node[24]])
    insertNodeDAG(dag, 26, ine, 1, "21/11/2017 10:15:00")
    # 27
    ine.clear()
    ine.append([23, 27, 1, dag.node[23]])
    ine.append([24, 27, 1, dag.node[24]])
    ine.append([25, 27, 1, dag.node[25]])
    insertNodeDAG(dag, 27, ine, 3, "21/11/2017 10:41:49")
    # 28
    ine.clear()
    ine.append([24, 28, 0, dag.node[24]])
    insertNodeDAG(dag, 28, ine, 1, "21/11/2017 10:43:00")
    # 29
    ine.clear()
    ine.append([23, 29, 1, dag.node[23]])
    ine.append([24, 29, 1, dag.node[24]])
    ine.append([25, 29, 1, dag.node[25]])
    ine.append([27, 29, 1, dag.node[27]])
    insertNodeDAG(dag, 29, ine, 4, "21/11/2017 11:24:16")
    # 30
    ine.clear()
    ine.append([29, 30, 0, dag.node[29]])
    insertNodeDAG(dag, 30, ine, 1, "21/11/2017 11:25:00")
    # 31
    ine.clear()
    ine.append([29, 31, 0, dag.node[29]])
    insertNodeDAG(dag, 31, ine, 1, "21/11/2017 11:25:01")
    # 32
    ine.clear()
    ine.append([24, 32, 0, dag.node[24]])
    insertNodeDAG(dag, 32, ine, 1, "21/11/2017 12:20:00")
    # 33
    ine.clear()
    ine.append([24, 33, 0, dag.node[24]])
    insertNodeDAG(dag, 33, ine, 1, "21/11/2017 13:02:19")
    # 34
    ine.clear()
    ine.append([24, 34, 0, dag.node[24]])
    ine.append([26, 34, 0, dag.node[26]])
    insertNodeDAG(dag, 34, ine, 2, "21/11/2017 13:28:35")
    # 35
    ine.clear()
    ine.append([23, 35, 1, dag.node[23]])
    ine.append([24, 35, 1, dag.node[24]])
    ine.append([25, 35, 1, dag.node[25]])
    ine.append([27, 35, 1, dag.node[27]])
    ine.append([29, 35, 1, dag.node[29]])
    insertNodeDAG(dag, 35, ine, 5, "21/11/2017 15:17:44")
    # 36
    ine.clear()
    ine.append([24, 36, 0, dag.node[24]])
    insertNodeDAG(dag, 36, ine, 1, "21/11/2017 16:21:00")
    # 37
    ine.clear()
    ine.append([23, 37, 1, dag.node[23]])
    ine.append([24, 37, 1, dag.node[24]])
    ine.append([25, 37, 1, dag.node[25]])
    ine.append([27, 37, 1, dag.node[27]])
    ine.append([29, 37, 1, dag.node[29]])
    ine.append([35, 37, 1, dag.node[35]])
    insertNodeDAG(dag, 37, ine, 6, "21/11/2017 16:22:00")
    # 38
    ine.clear()
    ine.append([23, 38, -1, dag.node[23]])
    ine.append([24, 38, -1, dag.node[24]])
    ine.append([25, 38, -1, dag.node[25]])
    ine.append([27, 38, -1, dag.node[27]])
    ine.append([29, 38, -1, dag.node[29]])
    ine.append([35, 38, -1, dag.node[35]])
    ine.append([37, 38, -1, dag.node[37]])
    insertNodeDAG(dag, 38, ine, 7, "21/11/2017 18:06:00")
    # 39
    ine.clear()
    ine.append([37, 39, 0, dag.node[37]])
    insertNodeDAG(dag, 39, ine, 1, "21/11/2017 18:30:00")
    # 40
    ine.clear()
    ine.append([23, 40, -1, dag.node[23]])
    ine.append([24, 40, -1, dag.node[24]])
    ine.append([25, 40, -1, dag.node[25]])
    ine.append([27, 40, -1, dag.node[27]])
    ine.append([29, 40, -1, dag.node[29]])
    ine.append([30, 40, -1, dag.node[30]])
    ine.append([31, 40, -1, dag.node[31]])
    ine.append([35, 40, -1, dag.node[35]])
    ine.append([37, 40, -1, dag.node[37]])
    ine.append([38, 40, 1, dag.node[38]])
    insertNodeDAG(dag, 40, ine, 10, "21/11/2017 18:52:06")
    # 41
    ine.clear()
    ine.append([24, 41, 0, dag.node[24]])
    ine.append([40, 41, 0, dag.node[40]])
    insertNodeDAG(dag, 41, ine, 2, "21/11/2017 19:37:22")
    # 42
    ine.clear()
    ine.append([24, 42, 0, dag.node[24]])
    ine.append([30, 42, 0, dag.node[30]])
    ine.append([31, 42, 0, dag.node[31]])
    ine.append([40, 42, 0, dag.node[40]])
    insertNodeDAG(dag, 42, ine, 4, "21/11/2017 20:11:10")
    # 43
    ine.clear()
    ine.append([24, 43, 0, dag.node[24]])
    ine.append([28, 43, 0, dag.node[28]])
    ine.append([40, 43, 0, dag.node[40]])
    insertNodeDAG(dag, 43, ine, 3, "21/11/2017 20:17:48")
    # 44
    ine.clear()
    ine.append([23, 44, 0, dag.node[23]])
    ine.append([24, 44, 0, dag.node[24]])
    ine.append([25, 44, 0, dag.node[25]])
    ine.append([27, 44, 0, dag.node[27]])
    ine.append([29, 44, 0, dag.node[29]])
    ine.append([35, 44, 0, dag.node[35]])
    ine.append([37, 44, 0, dag.node[37]])
    insertNodeDAG(dag, 44, ine, 7, "22/11/2017 7:05:00")
    # 45
    ine.clear()
    ine.append([24, 45, 0, dag.node[24]])
    ine.append([25, 45, 0, dag.node[25]])
    ine.append([27, 45, 0, dag.node[27]])
    ine.append([28, 45, 0, dag.node[28]])
    ine.append([29, 45, 0, dag.node[29]])
    ine.append([31, 45, 0, dag.node[31]])
    ine.append([36, 45, 0, dag.node[36]])
    ine.append([40, 45, 0, dag.node[40]])
    ine.append([44, 45, 0, dag.node[44]])
    insertNodeDAG(dag, 45, ine, 9, "22/11/2017 8:31:22")
    # 46
    ine.clear()
    ine.append([24, 46, 0, dag.node[24]])
    ine.append([25, 46, 0, dag.node[25]])
    ine.append([26, 46, 0, dag.node[26]])
    ine.append([27, 46, 0, dag.node[27]])
    ine.append([28, 46, 0, dag.node[28]])
    ine.append([29, 46, 0, dag.node[29]])
    ine.append([40, 46, 0, dag.node[40]])
    insertNodeDAG(dag, 46, ine, 7, "22/11/2017 9:21:56")
    # 47
    ine.clear()
    ine.append([24, 47, 0, dag.node[24]])
    ine.append([28, 47, 0, dag.node[28]])
    ine.append([40, 47, 0, dag.node[40]])
    insertNodeDAG(dag, 47, ine, 3, "22/11/2017 9:32:28")
    # 48
    ine.clear()
    ine.append([27, 48, -1, dag.node[27]])
    ine.append([38, 48, 1, dag.node[38]])
    ine.append([40, 48, 1, dag.node[40]])
    ine.append([44, 48, -1, dag.node[44]])
    insertNodeDAG(dag, 48, ine, 4, "22/11/2017 9:44:00")
    # 49
    ine.clear()
    ine.append([41, 49, 0, dag.node[41]])
    ine.append([44, 49, 0, dag.node[44]])
    ine.append([48, 49, 0, dag.node[48]])
    insertNodeDAG(dag, 49, ine, 3, "22/11/2017 10:13:20")
    # 50
    ine.clear()
    ine.append([24, 50, 0, dag.node[24]])
    ine.append([30, 50, 0, dag.node[30]])
    ine.append([31, 50, 0, dag.node[31]])
    ine.append([42, 50, 0, dag.node[42]])
    insertNodeDAG(dag, 50, ine, 4, "22/11/2017 11:00:32")
    # 51
    ine.clear()
    ine.append([20, 51, 0, dag.node[20]])
    ine.append([22, 51, 0, dag.node[22]])
    ine.append([24, 51, 0, dag.node[24]])
    ine.append([25, 51, 0, dag.node[25]])
    ine.append([28, 51, 0, dag.node[28]])
    ine.append([29, 51, 0, dag.node[29]])
    ine.append([30, 51, 0, dag.node[30]])
    ine.append([40, 51, 0, dag.node[40]])
    ine.append([44, 51, 0, dag.node[44]])
    insertNodeDAG(dag, 51, ine, 9, "22/11/2017 16:02:01")
    # 52
    ine.clear()
    ine.append([40, 52, 0, dag.node[40]])
    insertNodeDAG(dag, 52, ine, 1, "22/11/2017 17:02:41")
    # 53
    ine.clear()
    ine.append([27, 53, 0, dag.node[27]])
    insertNodeDAG(dag, 53, ine, 1, "22/11/2017 17:22:00")
    # 54
    ine.clear()
    ine.append([23, 54, -1, dag.node[23]])
    ine.append([24, 54, -1, dag.node[24]])
    ine.append([25, 54, -1, dag.node[25]])
    ine.append([27, 54, -1, dag.node[27]])
    ine.append([29, 54, -1, dag.node[29]])
    ine.append([35, 54, -1, dag.node[35]])
    ine.append([37, 54, -1, dag.node[37]])
    ine.append([38, 54, 1, dag.node[38]])
    ine.append([40, 54, 1, dag.node[40]])
    ine.append([44, 54, -1, dag.node[44]])
    ine.append([48, 54, 1, dag.node[48]])
    insertNodeDAG(dag, 54, ine, 11, "22/11/2017 17:58:53")
    # 55
    ine.clear()
    ine.append([27, 55, 0, dag.node[27]])
    ine.append([40, 55, 0, dag.node[40]])
    ine.append([41, 55, 0, dag.node[41]])
    ine.append([53, 55, 0, dag.node[53]])
    insertNodeDAG(dag, 55, ine, 4, "22/11/2017 18:20:49")
    # 56
    ine.clear()
    ine.append([46, 56, 0, dag.node[46]])
    insertNodeDAG(dag, 56, ine, 1, "22/11/2017 19:14:38")
    # 57
    ine.clear()
    ine.append([27, 57, 0, dag.node[27]])
    ine.append([53, 57, 0, dag.node[53]])
    insertNodeDAG(dag, 57, ine, 2, "22/11/2017 20:35:00")
    # 58
    ine.clear()
    ine.append([53, 58, 0, dag.node[53]])
    insertNodeDAG(dag, 58, ine, 1, "22/11/2017 21:37:29")
    # 59
    ine.clear()
    ine.append([40, 59, 0, dag.node[40]])
    ine.append([53, 59, 0, dag.node[53]])
    insertNodeDAG(dag, 59, ine, 2, "23/11/2017 8:50:00")
    # 60
    ine.clear()
    ine.append([53, 60, 0, dag.node[53]])
    insertNodeDAG(dag, 60, ine, 1, "23/11/2017 10:39:18")
    # 61
    ine.clear()
    ine.append([53, 61, 0, dag.node[53]])
    insertNodeDAG(dag, 61, ine, 1, "23/11/2017 15:33:00")
    # 62
    ine.clear()
    ine.append([16, 62, 0, dag.node[16]])
    ine.append([34, 62, 0, dag.node[34]])
    ine.append([38, 62, 0, dag.node[38]])
    ine.append([58, 62, 0, dag.node[58]])
    ine.append([61, 62, 0, dag.node[61]])
    insertNodeDAG(dag, 62, ine, 5, "23/11/2017 16:00:47")
    # 63
    ine.clear()
    insertNodeDAG(dag, 63, ine, 0, "29/11/2017 14:27:00")
    # 64
    ine.clear()
    ine.append([1, 64, 0, dag.node[1]])
    ine.append([63, 64, 1, dag.node[63]])
    insertNodeDAG(dag, 64, ine, 2, "29/11/2017 15:58:58")
    # 65
    ine.clear()
    ine.append([63, 65, 1, dag.node[63]])
    ine.append([64, 65, 1, dag.node[64]])
    insertNodeDAG(dag, 65, ine, 2, "29/11/2017 17:31:11")
    # 66
    ine.clear()
    ine.append([63, 66, 1, dag.node[63]])
    ine.append([64, 66, 1, dag.node[64]])
    ine.append([65, 66, 1, dag.node[65]])
    insertNodeDAG(dag, 66, ine, 3, "30/11/2017 20:21:00")

    return dag


def build_fake_news_graph(g, m):
    g.add_nodes_from(range(m), visited=False, color="b")
    g.add_edge(0, 1, weight=1, visited=False)
    g.add_edge(0, 2, weight=0, visited=False)
    g.add_edge(0, 3, weight=0, visited=False)
    g.add_edge(0, 4, weight=0, visited=False)
    g.add_edge(0, 5, weight=0, visited=False)
    g.add_edge(0, 6, weight=0, visited=False)
    g.add_edge(0, 7, weight=1, visited=False)
    g.add_edge(1, 7, weight=1, visited=False)
    g.add_edge(0, 8, weight=1, visited=False)
    g.add_edge(1, 8, weight=1, visited=False)
    g.add_edge(7, 8, weight=1, visited=False)
    g.add_edge(0, 9, weight=1, visited=False)
    g.add_edge(1, 9, weight=1, visited=False)
    g.add_edge(7, 9, weight=1, visited=False)
    g.add_edge(8, 9, weight=1, visited=False)
    g.add_edge(0, 10, weight=1, visited=False)
    g.add_edge(1, 10, weight=1, visited=False)
    g.add_edge(7, 10, weight=1, visited=False)
    g.add_edge(8, 10, weight=1, visited=False)
    g.add_edge(3, 11, weight=0, visited=False)
    g.add_edge(10, 11, weight=0, visited=False)
    g.add_edge(6, 12, weight=0, visited=False)
    g.add_edge(1, 13, weight=0, visited=False)
    g.add_edge(3, 14, weight=0, visited=False)
    g.add_edge(11, 14, weight=0, visited=False)
    g.add_edge(13, 15, weight=0, visited=False)
    g.add_edge(12, 16, weight=0, visited=False)
    g.add_edge(16, 19, weight=0, visited=False)
    g.add_edge(17, 19, weight=0, visited=False)
    g.add_edge(18, 19, weight=0, visited=False)
    g.add_edge(21, 22, weight=0, visited=False)
    g.add_edge(23, 24, weight=1, visited=False)
    g.add_edge(23, 25, weight=1, visited=False)
    g.add_edge(24, 25, weight=1, visited=False)
    g.add_edge(24, 26, weight=0, visited=False)
    g.add_edge(23, 27, weight=1, visited=False)
    g.add_edge(24, 27, weight=1, visited=False)
    g.add_edge(25, 27, weight=1, visited=False)
    g.add_edge(24, 28, weight=0, visited=False)
    g.add_edge(23, 29, weight=1, visited=False)
    g.add_edge(24, 29, weight=1, visited=False)
    g.add_edge(25, 29, weight=1, visited=False)
    g.add_edge(27, 29, weight=1, visited=False)
    g.add_edge(29, 30, weight=0, visited=False)
    g.add_edge(29, 31, weight=0, visited=False)
    g.add_edge(24, 32, weight=0, visited=False)
    g.add_edge(24, 33, weight=0, visited=False)
    g.add_edge(24, 34, weight=0, visited=False)
    g.add_edge(26, 34, weight=0, visited=False)
    g.add_edge(23, 35, weight=1, visited=False)
    g.add_edge(24, 35, weight=1, visited=False)
    g.add_edge(25, 35, weight=1, visited=False)
    g.add_edge(27, 35, weight=1, visited=False)
    g.add_edge(29, 35, weight=1, visited=False)
    g.add_edge(24, 36, weight=0, visited=False)
    g.add_edge(23, 37, weight=1, visited=False)
    g.add_edge(24, 37, weight=1, visited=False)
    g.add_edge(25, 37, weight=1, visited=False)
    g.add_edge(27, 37, weight=1, visited=False)
    g.add_edge(29, 37, weight=1, visited=False)
    g.add_edge(35, 37, weight=1, visited=False)
    g.add_edge(23, 38, weight=-1, visited=False)
    g.add_edge(24, 38, weight=-1, visited=False)
    g.add_edge(25, 38, weight=-1, visited=False)
    g.add_edge(27, 38, weight=-1, visited=False)
    g.add_edge(29, 38, weight=-1, visited=False)
    g.add_edge(35, 38, weight=-1, visited=False)
    g.add_edge(37, 38, weight=-1, visited=False)
    g.add_edge(37, 39, weight=0, visited=False)
    g.add_edge(23, 40, weight=-1, visited=False)
    g.add_edge(24, 40, weight=-1, visited=False)
    g.add_edge(25, 40, weight=-1, visited=False)
    g.add_edge(27, 40, weight=-1, visited=False)
    g.add_edge(29, 40, weight=-1, visited=False)
    g.add_edge(30, 40, weight=-1, visited=False)
    g.add_edge(31, 40, weight=-1, visited=False)
    g.add_edge(35, 40, weight=-1, visited=False)
    g.add_edge(37, 40, weight=-1, visited=False)
    g.add_edge(38, 40, weight=1, visited=False)
    g.add_edge(24, 41, weight=0, visited=False)
    g.add_edge(40, 41, weight=0, visited=False)
    g.add_edge(24, 42, weight=0, visited=False)
    g.add_edge(30, 42, weight=0, visited=False)
    g.add_edge(31, 42, weight=0, visited=False)
    g.add_edge(40, 42, weight=0, visited=False)
    g.add_edge(24, 43, weight=0, visited=False)
    g.add_edge(28, 43, weight=0, visited=False)
    g.add_edge(40, 43, weight=0, visited=False)
    g.add_edge(23, 44, weight=0, visited=False)
    g.add_edge(24, 44, weight=0, visited=False)
    g.add_edge(25, 44, weight=0, visited=False)
    g.add_edge(27, 44, weight=0, visited=False)
    g.add_edge(29, 44, weight=0, visited=False)
    g.add_edge(35, 44, weight=0, visited=False)
    g.add_edge(37, 44, weight=0, visited=False)
    g.add_edge(24, 45, weight=0, visited=False)
    g.add_edge(25, 45, weight=0, visited=False)
    g.add_edge(27, 45, weight=0, visited=False)
    g.add_edge(28, 45, weight=0, visited=False)
    g.add_edge(29, 45, weight=0, visited=False)
    g.add_edge(31, 45, weight=0, visited=False)
    g.add_edge(36, 45, weight=0, visited=False)
    g.add_edge(40, 45, weight=0, visited=False)
    g.add_edge(44, 45, weight=0, visited=False)
    g.add_edge(24, 46, weight=0, visited=False)
    g.add_edge(25, 46, weight=0, visited=False)
    g.add_edge(26, 46, weight=0, visited=False)
    g.add_edge(27, 46, weight=0, visited=False)
    g.add_edge(28, 46, weight=0, visited=False)
    g.add_edge(29, 46, weight=0, visited=False)
    g.add_edge(40, 46, weight=0, visited=False)
    g.add_edge(24, 47, weight=0, visited=False)
    g.add_edge(28, 47, weight=0, visited=False)
    g.add_edge(40, 47, weight=0, visited=False)
    g.add_edge(27, 48, weight=-1, visited=False)
    g.add_edge(38, 48, weight=1, visited=False)
    g.add_edge(40, 48, weight=1, visited=False)
    g.add_edge(44, 48, weight=-1, visited=False)
    g.add_edge(41, 49, weight=0, visited=False)
    g.add_edge(44, 49, weight=0, visited=False)
    g.add_edge(48, 49, weight=0, visited=False)
    g.add_edge(24, 50, weight=0, visited=False)
    g.add_edge(30, 50, weight=0, visited=False)
    g.add_edge(31, 50, weight=0, visited=False)
    g.add_edge(42, 50, weight=0, visited=False)
    g.add_edge(20, 51, weight=0, visited=False)
    g.add_edge(22, 51, weight=0, visited=False)
    g.add_edge(24, 51, weight=0, visited=False)
    g.add_edge(25, 51, weight=0, visited=False)
    g.add_edge(28, 51, weight=0, visited=False)
    g.add_edge(29, 51, weight=0, visited=False)
    g.add_edge(30, 51, weight=0, visited=False)
    g.add_edge(40, 51, weight=0, visited=False)
    g.add_edge(44, 51, weight=0, visited=False)
    g.add_edge(40, 52, weight=0, visited=False)
    g.add_edge(27, 53, weight=0, visited=False)
    g.add_edge(23, 54, weight=-1, visited=False)
    g.add_edge(24, 54, weight=-1, visited=False)
    g.add_edge(25, 54, weight=-1, visited=False)
    g.add_edge(27, 54, weight=-1, visited=False)
    g.add_edge(29, 54, weight=-1, visited=False)
    g.add_edge(35, 54, weight=-1, visited=False)
    g.add_edge(37, 54, weight=-1, visited=False)
    g.add_edge(38, 54, weight=1, visited=False)
    g.add_edge(40, 54, weight=1, visited=False)
    g.add_edge(44, 54, weight=-1, visited=False)
    g.add_edge(48, 54, weight=1, visited=False)
    g.add_edge(27, 55, weight=0, visited=False)
    g.add_edge(40, 55, weight=0, visited=False)
    g.add_edge(41, 55, weight=0, visited=False)
    g.add_edge(53, 55, weight=0, visited=False)
    g.add_edge(46, 56, weight=0, visited=False)
    g.add_edge(27, 57, weight=0, visited=False)
    g.add_edge(53, 57, weight=0, visited=False)
    g.add_edge(53, 58, weight=0, visited=False)
    g.add_edge(40, 59, weight=0, visited=False)
    g.add_edge(53, 59, weight=0, visited=False)
    g.add_edge(53, 60, weight=0, visited=False)
    g.add_edge(53, 61, weight=0, visited=False)
    g.add_edge(16, 62, weight=0, visited=False)
    g.add_edge(34, 62, weight=0, visited=False)
    g.add_edge(38, 62, weight=0, visited=False)
    g.add_edge(58, 62, weight=0, visited=False)
    g.add_edge(61, 62, weight=0, visited=False)
    g.add_edge(1, 64, weight=0, visited=False)
    g.add_edge(63, 64, weight=1, visited=False)
    g.add_edge(63, 65, weight=1, visited=False)
    g.add_edge(64, 65, weight=1, visited=False)
    g.add_edge(63, 66, weight=1, visited=False)
    g.add_edge(64, 66, weight=1, visited=False)
    g.add_edge(65, 66, weight=1, visited=False)


# G = nx.DiGraph()
# G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
max = 67
# G.add_nodes_from(range(max), visited=False, color="w")
# build_dag(G, 6, max-1)

# build_fake_news_graph(G, max)
G = new_news_graph_DAG()

GT = nx.DiGraph.reverse(G, copy=True)
# PR = nx.pagerank(G)
# PRT= nx.pagerank(GT)
# A = nx.adjacency_matrix(G)
# AT = nx.adjacency_matrix(GT)
# print(PR)
# print(PRT)
# print(A.todense())
# print(AT.todense())
print("number of nodes {0} ".format(G.number_of_nodes()))
print("number of edges {0} ".format(G.number_of_edges()))
print("DAG {0} ".format(nx.is_directed_acyclic_graph(G)))
print("TREE {0} ".format(nx.is_tree(G)))
print("FOREST {0} ".format(nx.is_forest(G)))
print("ARBORESCENCE {0} ".format(nx.is_arborescence(G)))
print("BRANCHING {0} ".format(nx.is_branching(G)))

tv = {}

sh = {}
un = {}
tw = {}
di = {}
pr = {}
wp = {}
# e = 1
# ee = random.randint(e, e+5)
# while e < max:
#     e = build_dag_forest(G, e, ee, max)
#     print(e)
#     ee = random.randint(e, e+5)
#     e += 1

# for i in range(1, 6):
#    for j in range(random.randint(0, 6)):
#        G.add_edge(i, random.randint(i + 1, random.randint(i + 1, 6)), weight=random.randint(-1, 1))
# for i in range(11, 30):
#    for j in range(random.randint(0, 5)):
#        G.add_edge(i, random.randint(i+1, 50), weight=random.randint(-1, 1))
# for i in range(6, 18):
#     for j in range(random.randint(0, 3)):
#         G.add_edge(i, random.randint(i + 1, random.randint(i + 1, 50)), weight=random.randint(-1, 1))

plt.figure(max + 2)
ax0 = plt.subplot(511)
plt.ylabel('vnot')
ax1 = plt.subplot(512)
plt.ylabel('vnot')
ax2 = plt.subplot(513)
plt.ylabel('vnot')
ax3 = plt.subplot(514)
plt.ylabel('vnot')
ax4 = plt.subplot(515)
plt.ylabel('vnot')
# ax5 = plt.subplot(616)
# plt.ylabel('vnot')
plt.xlabel('vtot')

Gprp = nx.DiGraph()
Gprp.add_nodes_from(range(max), visited=False)
Gprn = nx.DiGraph()
Gprn.add_nodes_from(range(max), visited=False)
for i in list(G.nodes):
    vnot = {}
    vpos0 = {}
    vneg0 = {}
    vpos1 = {}
    vneg1 = {}
    vpos2 = {}
    vneg2 = {}
    Gp = {}
    Gn = {}
    nx.set_node_attributes(G, False, 'visited')
    nx.set_edge_attributes(G, False, 'visited')

    print(i, G.node[i])
    for comp in range(G.node[i]['n_components']):
        com = G.node[i]['id_component_{}'.format(comp)]
        Gp[com] = nx.DiGraph()
        Gp[com].add_nodes_from(range(max))
        Gn[com] = nx.DiGraph()
        Gn[com].add_nodes_from(range(max))
        vnot[com] = []
        vpos0[com] = []
        vneg0[com] = []
        vpos1[com] = []
        vneg1[com] = []
        vpos2[com] = []
        vneg2[com] = []

    dfs_color(G, i, 0, G.node[i].copy(), vnot, vpos0, vneg0, vpos1, vneg1, vpos2, vneg2)

    vtotnot = 0
    vtot0 = 0
    vtot1 = 0
    vtot2 = 0
    pr[i] = 0
    wp[i] = 0

    for comp in range(G.node[i]['n_components']):
        com = G.node[i]['id_component_{}'.format(comp)]
        vtotnot += len(vnot[com])
        vtot0 += len(vpos0[com]) - len(vneg0[com])
        vtot1 += sum(vpos1[com]) - sum(vneg1[com])
        vtot2 += sum(vpos2[com]) - sum(vneg2[com])
        tv[com] = sum(vpos2[com]) - sum(vneg2[com])
        Gp[com].add_edges_from(vpos0[com])
        Gprp.add_edges_from(vpos0[com])
        Gn[com].add_edges_from(vneg0[com])
        Gprn.add_edges_from(vneg0[com])
        GpT = nx.DiGraph.reverse(Gp[com], copy=True)
        GnT = nx.DiGraph.reverse(Gn[com], copy=True)
        nx.set_node_attributes(GpT, False, 'visited')
        nx.set_edge_attributes(GpT, False, 'visited')
        nx.set_node_attributes(GnT, False, 'visited')
        nx.set_edge_attributes(GnT, False, 'visited')
        prp = nx.pagerank(GpT)
        prn = nx.pagerank(GnT)
        pr[i] += prp[i] - prn[i]

        wpp = PageRank(GpT, 0.85)
        wpn = PageRank(GnT, 0.85)
        wp[i] += wpp[i] - wpn[i]

    #     Gp.add_edges_from(vpos0)
    #     Gprp.add_edges_from(vpos0)
    #     Gn.add_edges_from(vneg0)
    #     Gprn.add_edges_from(vneg0)
    #     GpT = nx.DiGraph.reverse(Gp, copy=True)
    #     GnT = nx.DiGraph.reverse(Gn, copy=True)
    #     plt.figure(i)
    #     plt.subplot(121)
    #     nx.draw_spring(GpT, with_labels=True)
    #     plt.subplot(122)
    #     nx.draw_spring(GnT, with_labels=True)
    #     nx.set_node_attributes(GpT, False, 'visited')
    #     nx.set_edge_attributes(GpT, False, 'visited')
    #     nx.set_node_attributes(GnT, False, 'visited')
    #     nx.set_edge_attributes(GnT, False, 'visited')

    #     prp = nx.pagerank(GpT)
    #     prn = nx.pagerank(GnT)
    #     pr[i] = prp[i] - prn[i]

    #     wpp = PageRank(GpT, 0.85)
    #     wpn = PageRank(GnT, 0.85)
    #     wp[i] = wpp[i] - wpn[i]

    '''
    vtotnot = len(vnot)

    vtot0 = len(vpos0) - len(vneg0)
    vtot1 = sum(vpos1) - sum(vneg1)
    vtot2 = sum(vpos2) - sum(vneg2)

    vt0_num = len(vpos0) - len(vneg0)
    vt0_den = len(vpos0) + len(vneg0)
    if vt0_num == 0 or vt0_den == 0:
        vtot0 = 0
    else:
        vtot0 = float(vt0_num / vt0_den)

    vt1_num = sum(vpos1) - sum(vneg1)
    vt1_den = sum(vpos1) + sum(vneg1)
    if vt1_num == 0 or vt1_den == 0:
        vtot1 = 0
    else:
        vtot1 = float(vt1_num / vt1_den)

    vt2_num = sum(vpos2) - sum(vneg2)
    vt2_den = sum(vpos2) + sum(vneg2)
    if vt2_num == 0 or vt2_den == 0:
        vtot2 = 0
    else:
        vtot2 = float(vt2_num / vt2_den)
    '''
    sh[i] = vtotnot
    un[i] = vtot0
    tw[i] = vtot1
    di[i] = vtot2
    '''
    print("vnot", vnot)
    print(len(vnot))
    print("vpos0", vpos0)
    print(len(vpos0))
    print("vneg0", vneg0)
    print(len(vneg0))
    print("vpos1", vpos1)
    print(len(vpos1))
    print("vneg1", vneg1)
    print(len(vneg1))
    print("vpos2", vpos2)
    print(len(vpos2))
    print("vneg2", vneg2)
    print(len(vneg2))
    '''
    #     sorp = sorted(prp.items(), key=lambda kv: kv[1])
    #     print("Positive pagerank {}".format(i))
    #     print(sorp)
    #     sorn = sorted(prn.items(), key=lambda kv: kv[1])
    #     print("Negative pagerank {}".format(i))
    #     print(sorn)
    #     sor = sorted(pr.items(), key=lambda kv: kv[1])
    #     print("Tot pagerank {}".format(i))
    #     print(sor)
    print("NODE {}, color {}, vnot {}, v0node {}, v1node {}, v2node {} v3node {}".format(i, G.node[i], vtotnot, vtot0,
                                                                                         vtot1, vtot2, pr[i]))
    print(tv, vtotnot)
    ax0.plot(vtot0, vtotnot, 'ro')
    #     ax0.annotate(i, (vtot0, vtotnot))
    ax1.plot(vtot1, vtotnot, 'bo')
    ax2.plot(vtot2, vtotnot, 'go')
#     ax3.plot(pr[i], vtotnot, 'ys')
#     ax4.plot(PR[i], vtotnot, 'ms')
#     ax5.plot(PRT[i], vtotnot, 'ks')
#     if i == 0:
#         con = ConnectionPatch(xyA=(vtot1, vtotnot), xyB=(vtot0, vtotnot), coordsA="data", coordsB="data", axesA=ax1,
#                               axesB=ax0, color="black")
#         ax1.add_artist(con)
# plt.axis([-3.5, 3.5, -1, 25])
# plt.show()


GprpT = nx.DiGraph.reverse(Gprp, copy=True)
GprnT = nx.DiGraph.reverse(Gprn, copy=True)
# plt.figure(0)
# nx.draw_spring(GprpT, with_labels=True)
# plt.figure(1)
# nx.draw_spring(GprnT, with_labels=True)

print("Sorted first")
sorted_un = sorted(un.items(), key=lambda kv: kv[1])
print(sorted_un)
print("Sorted second")
sorted_tw = sorted(tw.items(), key=lambda kv: kv[1])
print(sorted_tw)
print("Sorted third")
sorted_di = sorted(di.items(), key=lambda kv: kv[1])
print(sorted_di)
# print("Sorted pagerank 0")
# sorted_p = sorted(pr.items(), key=lambda kv: kv[1])
# print(sorted_p)
print("Sorted pagerank 1")
# prp = nx.pagerank(GprpT)
# prn = nx.pagerank(GprnT)
# pr1 = {key: prp[key] - prn.get(key, 0) for key in prp.keys()}
sorted_p1 = sorted(pr.items(), key=lambda kv: kv[1])
print(sorted_p1)

# wprp = PageRank(GprpT, 0.85)
# wprn = PageRank(GprnT, 0.85)
# wpr = {key: wprp[key] - wprn.get(key, 0) for key in wprp.keys()}
sorted_wp = sorted(wp.items(), key=lambda kv: kv[1])
print("Sorted w pagerank")
print(sorted_wp)

for i in list(G.nodes):
    ax3.plot(wp[i], sh[i], 'ys')
    ax4.plot(pr[i], sh[i], 'ms')

# print("Sorted PR")
# sorted_pr = sorted(PR.items(), key=lambda kv: kv[1])
# print(sorted_pr)
# print("Sorted PRT")
# sorted_prt = sorted(PRT.items(), key=lambda kv: kv[1])
# print(sorted_prt)
'''
wikipv = wikipedia_pagerank(nx.to_numpy_matrix(Gprp))
wikip = {}
wikinv = wikipedia_pagerank(nx.to_numpy_matrix(Gprn))
wikin = {}

for wi in range(len(wikipv)):
    wikip[wi] = wikipv.item(wi)
    wikin[wi] = wikinv.item(wi)

print("Sorted prp")
sorted_prp = sorted(prp.items(), key=lambda kv: kv[1])
print(sorted_prp)
print("Sorted my prp")
sorted_my_prp = sorted(PageRank(GprpT, 0.85).items(), key=lambda kv: kv[1])
print(sorted_my_prp)
print("Sorted wiki prp")
sorted_wiki_prp = sorted(wikip.items(), key=lambda kv: kv[1])
print(sorted_wiki_prp)
print("Sorted prn")
sorted_prn = sorted(prn.items(), key=lambda kv: kv[1])
print(sorted_prn)
print("Sorted my prn")
sorted_my_prn = sorted(PageRank(GprnT, 0.85).items(), key=lambda kv: kv[1])
print(sorted_my_prn)
print("Sorted wiki prn")
sorted_wiki_prn = sorted(wikin.items(), key=lambda kv: kv[1])
print(sorted_wiki_prn)
'''
un_sorted = []
tw_sorted = []
di_sorted = []
# p_sorted = []
p1_sorted = []
wp_sorted = []

'''
prp_sorted = []
myprp_sorted = []
wikiprp_sorted = []
prn_sorted = []
myprn_sorted = []
wikiprn_sorted = []
'''

for index in list(G.nodes):
    un_sorted.append(sorted_un[index][0])
    tw_sorted.append(sorted_tw[index][0])
    di_sorted.append(sorted_di[index][0])
    #     p_sorted.append(sorted_p[index][0])
    p1_sorted.append(sorted_p1[index][0])
    wp_sorted.append(sorted_wp[index][0])
    '''
    prp_sorted.append(sorted_prp[index][0])
    myprp_sorted.append(sorted_my_prp[index][0])
    wikiprp_sorted.append(sorted_wiki_prp[index][0])
    prn_sorted.append(sorted_prn[index][0])
    myprn_sorted.append(sorted_my_prn[index][0])
    wikiprn_sorted.append(sorted_wiki_prn[index][0])
    '''

print(un_sorted)
print(tw_sorted)
print(di_sorted)
# print(p_sorted)
print(p1_sorted)
print(wp_sorted)
'''
print(prp_sorted)
print(myprp_sorted)
print(wikiprp_sorted)
print(prn_sorted)
print(myprn_sorted)
print(wikiprn_sorted)
'''
# inversion coefficient
swap_f_s = count_swap(sorted_un, sorted_tw, max)
print("Inversion coefficient u t: {}".format(swap_f_s))
swap_f_t = count_swap(sorted_un, sorted_di, max)
print("Inversion coefficient u d: {}".format(swap_f_t))
# swap_f_p0 = count_swap(sorted_un, sorted_p, max)
# print("Inversion coefficient u p: {}".format(swap_f_p0))
swap_f_p1 = count_swap(sorted_un, sorted_p1, max)
print("Inversion coefficient u p1: {}".format(swap_f_p1))
swap_f_wp = count_swap(sorted_un, sorted_wp, max)
print("Inversion coefficient u wp: {}".format(swap_f_wp))
swap_s_t = count_swap(sorted_tw, sorted_di, max)
print("Inversion coefficient t d: {}".format(swap_s_t))
# swap_s_p0 = count_swap(sorted_tw, sorted_p, max)
# print("Inversion coefficient t p: {}".format(swap_s_p0))
swap_s_p1 = count_swap(sorted_tw, sorted_p1, max)
print("Inversion coefficient t p1: {}".format(swap_s_p1))
swap_s_wp = count_swap(sorted_tw, sorted_wp, max)
print("Inversion coefficient t wp: {}".format(swap_s_wp))
# swap_t_p0 = count_swap(sorted_di, sorted_p, max)
# print("Inversion coefficient d p: {}".format(swap_t_p0))
swap_t_p1 = count_swap(sorted_di, sorted_p1, max)
print("Inversion coefficient d p1: {}".format(swap_t_p1))
swap_t_wp = count_swap(sorted_di, sorted_wp, max)
print("Inversion coefficient d wp: {}".format(swap_t_wp))
# swap_p0_p1 = count_swap(sorted_p, sorted_p1, max)
# print("Inversion coefficient p p1: {}".format(swap_p0_p1))
# swap_p0_wp = count_swap(sorted_p, sorted_wp, max)
# print("Inversion coefficient p wp: {}".format(swap_p0_wp))
swap_p1_wp = count_swap(sorted_p1, sorted_wp, max)
print("Inversion coefficient p1 wp: {}".format(swap_p1_wp))

'''
swap_prp_myprp = count_swap(sorted_prp, sorted_my_prp, max)
print("Inversion coefficient prp myprp: {}".format(swap_prp_myprp))
swap_prp_wikiprp = count_swap(sorted_prp, sorted_wiki_prp, max)
print("Inversion coefficient prp wikiprp: {}".format(swap_prp_wikiprp))
swap_myprp_wikiprp = count_swap(sorted_my_prp, sorted_wiki_prp, max)
print("Inversion coefficient myprp wikiprp: {}".format(swap_myprp_wikiprp))
swap_prn_myprn = count_swap(sorted_prn, sorted_my_prn, max)
print("Inversion coefficient prn myprn: {}".format(swap_prn_myprn))
swap_prn_wikiprn = count_swap(sorted_prn, sorted_wiki_prn, max)
print("Inversion coefficient prn wikiprn: {}".format(swap_prn_wikiprn))
swap_myprn_wikiprn = count_swap(sorted_my_prn, sorted_wiki_prn, max)
print("Inversion coefficient myprn wikiprn: {}".format(swap_myprn_wikiprn))
'''
# Kendall
kendall_u_t, p_value = stats.kendalltau(un_sorted, tw_sorted)
print("Kendall's tau u t {}, p_value {}".format(kendall_u_t, p_value))
kendall_u_d, p_value = stats.kendalltau(un_sorted, di_sorted)
print("Kendall's tau u d {}, p_value {}".format(kendall_u_d, p_value))
# kendall_u_p, p_value = stats.kendalltau(un_sorted, p_sorted)
# print("Kendall's tau u p {}, p_value {}".format(kendall_u_p, p_value))
kendall_u_p1, p_value = stats.kendalltau(un_sorted, p1_sorted)
print("Kendall's tau u p1 {}, p_value {}".format(kendall_u_p1, p_value))
kendall_u_wp, p_value = stats.kendalltau(un_sorted, wp_sorted)
print("Kendall's tau u wp {}, p_value {}".format(kendall_u_wp, p_value))
kendall_t_d, p_value = stats.kendalltau(tw_sorted, di_sorted)
print("Kendall's tau t d {}, p_value {}".format(kendall_t_d, p_value))
# kendall_t_p, p_value = stats.kendalltau(tw_sorted, p_sorted)
# print("Kendall's tau t p {}, p_value {}".format(kendall_t_p, p_value))
kendall_t_p1, p_value = stats.kendalltau(tw_sorted, p1_sorted)
print("Kendall's tau t p1 {}, p_value {}".format(kendall_t_p1, p_value))
kendall_t_wp, p_value = stats.kendalltau(tw_sorted, wp_sorted)
print("Kendall's tau t wp {}, p_value {}".format(kendall_t_wp, p_value))
# kendall_d_p, p_value = stats.kendalltau(di_sorted, p_sorted)
# print("Kendall's tau d p {}, p_value {}".format(kendall_d_p, p_value))
kendall_d_p1, p_value = stats.kendalltau(di_sorted, p1_sorted)
print("Kendall's tau d p1 {}, p_value {}".format(kendall_d_p1, p_value))
kendall_d_wp, p_value = stats.kendalltau(di_sorted, wp_sorted)
print("Kendall's tau d wp {}, p_value {}".format(kendall_d_wp, p_value))
# kendall_p_p1, p_value = stats.kendalltau(p_sorted, p1_sorted)
# print("Kendall's tau p p1 {}, p_value {}".format(kendall_p_p1, p_value))
# kendall_p_wp, p_value = stats.kendalltau(p_sorted, wp_sorted)
# print("Kendall's tau p wp {}, p_value {}".format(kendall_p_wp, p_value))
kendall_p1_wp, p_value = stats.kendalltau(p1_sorted, wp_sorted)
print("Kendall's tau p1 wp {}, p_value {}".format(kendall_p1_wp, p_value))
'''
kendall_prp_myprp, p_value = stats.kendalltau(prp_sorted, myprp_sorted)
print("Kendall's tau prp myprp {}, p_value {}".format(kendall_prp_myprp, p_value))
kendall_prp_wikiprp, p_value = stats.kendalltau(prp_sorted, wikiprp_sorted)
print("Kendall's tau prp wikiprp {}, p_value {}".format(kendall_prp_wikiprp, p_value))
kendall_myprp_wikiprp, p_value = stats.kendalltau(myprp_sorted, wikiprp_sorted)
print("Kendall's tau myprp wikiprp {}, p_value {}".format(kendall_myprp_wikiprp, p_value))
kendall_prn_myprn, p_value = stats.kendalltau(prn_sorted, myprn_sorted)
print("Kendall's tau prn myprn {}, p_value {}".format(kendall_prn_myprn, p_value))
kendall_prn_wikiprn, p_value = stats.kendalltau(prn_sorted, wikiprn_sorted)
print("Kendall's tau prn wikiprn {}, p_value {}".format(kendall_prn_wikiprn, p_value))
kendall_myprn_wikiprn, p_value = stats.kendalltau(myprn_sorted, wikiprn_sorted)
print("Kendall's tau myprn wikiprn {}, p_value {}".format(kendall_myprn_wikiprn, p_value))
'''
# Spearman

spearman_u_t, p_value = stats.spearmanr(un_sorted, tw_sorted)
print("Spearman's rho u t {}, p_value {}".format(spearman_u_t, p_value))
spearman_u_d, p_value = stats.spearmanr(un_sorted, di_sorted)
print("Spearman's rho u d {}, p_value {}".format(spearman_u_d, p_value))
# spearman_u_p, p_value = stats.spearmanr(un_sorted, p_sorted)
# print("Spearman's rho u p {}, p_value {}".format(spearman_u_p, p_value))
spearman_u_p1, p_value = stats.spearmanr(un_sorted, p1_sorted)
print("Spearman's rho u p1 {}, p_value {}".format(spearman_u_p1, p_value))
spearman_u_wp, p_value = stats.spearmanr(un_sorted, wp_sorted)
print("Spearman's rho u wp {}, p_value {}".format(spearman_u_wp, p_value))
spearman_t_d, p_value = stats.spearmanr(tw_sorted, di_sorted)
print("Spearman's rho t d {}, p_value {}".format(spearman_t_d, p_value))
# spearman_t_p, p_value = stats.spearmanr(tw_sorted, p_sorted)
# print("Spearman's rho t p {}, p_value {}".format(spearman_t_p, p_value))
spearman_t_p1, p_value = stats.spearmanr(tw_sorted, p1_sorted)
print("Spearman's rho t p1 {}, p_value {}".format(spearman_t_p1, p_value))
spearman_t_wp, p_value = stats.spearmanr(tw_sorted, wp_sorted)
print("Spearman's rho t wp {}, p_value {}".format(spearman_t_wp, p_value))
# spearman_d_p, p_value = stats.spearmanr(di_sorted, p_sorted)
# print("Spearman's rho d p {}, p_value {}".format(spearman_d_p, p_value))
spearman_d_p1, p_value = stats.spearmanr(di_sorted, p1_sorted)
print("Spearman's rho d p1 {}, p_value {}".format(spearman_d_p1, p_value))
spearman_d_wp, p_value = stats.spearmanr(di_sorted, wp_sorted)
print("Spearman's rho d wp {}, p_value {}".format(spearman_d_wp, p_value))
# spearman_p_p1, p_value = stats.spearmanr(p_sorted, p1_sorted)
# print("Spearman's rho p p1 {}, p_value {}".format(spearman_p_p1, p_value))
# spearman_p_wp, p_value = stats.spearmanr(p_sorted, wp_sorted)
# print("Spearman's rho p wp {}, p_value {}".format(spearman_p_wp, p_value))
spearman_p1_wp, p_value = stats.spearmanr(p1_sorted, wp_sorted)
print("Spearman's rho p1 wp {}, p_value {}".format(spearman_p1_wp, p_value))
'''
spearman_prp_myprp, p_value = stats.spearmanr(prp_sorted, myprp_sorted)
print("Spearman's rho prp myprp {}, p_value {}".format(spearman_prp_myprp, p_value))
spearman_prp_wikiprp, p_value = stats.spearmanr(prp_sorted, wikiprp_sorted)
print("Spearman's rho prp wikiprp {}, p_value {}".format(spearman_prp_wikiprp, p_value))
spearman_myprp_wikiprp, p_value = stats.spearmanr(myprp_sorted, wikiprp_sorted)
print("Spearman's rho myprp wikiprp {}, p_value {}".format(spearman_myprp_wikiprp, p_value))
spearman_prn_myprn, p_value = stats.spearmanr(prn_sorted, myprn_sorted)
print("Spearman's rho prn myprn {}, p_value {}".format(spearman_prn_myprn, p_value))
spearman_prn_wikiprn, p_value = stats.spearmanr(prn_sorted, wikiprn_sorted)
print("Spearman's rho prn wikiprn {}, p_value {}".format(spearman_prn_wikiprn, p_value))
spearman_myprn_wikiprn, p_value = stats.spearmanr(myprn_sorted, wikiprn_sorted)
print("Spearman's rho myprn wikiprn {}, p_value {}".format(spearman_myprn_wikiprn, p_value))
'''
# distances
print("Distances between u t")
print(distances(sorted_un, sorted_tw, max))
print("Distances between u d")
print(distances(sorted_un, sorted_di, max))
# print("Distances between u p")
# print(distances(sorted_un, sorted_p, max))
print("Distances between u p1")
print(distances(sorted_un, sorted_p1, max))
print("Distances between u wp")
print(distances(sorted_un, sorted_wp, max))
print("Distances between t d")
print(distances(sorted_tw, sorted_di, max))
# print("Distances between t p")
# print(distances(sorted_tw, sorted_p, max))
print("Distances between t p1")
print(distances(sorted_tw, sorted_p1, max))
print("Distances between t wp")
print(distances(sorted_tw, sorted_wp, max))
# print("Distances between d p")
# print(distances(sorted_di, sorted_p, max))
print("Distances between d p1")
print(distances(sorted_di, sorted_p1, max))
print("Distances between d wp")
print(distances(sorted_di, sorted_wp, max))
# print("Distances between p p1")
# print(distances(sorted_p, sorted_p1, max))
# print("Distances between p wp")
# print(distances(sorted_p, sorted_wp, max))
print("Distances between p1 wp")
print(distances(sorted_p1, sorted_wp, max))

for y in range(G.number_of_nodes() - 1):
    print(y, y + 1)
    diff = date_difference(G.node[y]['time'], G.node[y + 1]['time'])
    print(diff)
print(date_difference(G.node[0]['time'], G.node[66]['time']))

e_pos = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 1]
e_neg = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == -1]
e_not = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 0]
plt.figure(max)
pos = nx.spring_layout(G)  # positions for all nodes

nx.draw_networkx_nodes(G, pos, node_size=100, node_color='y')  # nodes

nx.draw_networkx_edges(G, pos, edgelist=e_pos, width=1, alpha=0.5, edge_color='g', style='dashed')  # pos edges
nx.draw_networkx_edges(G, pos, edgelist=e_neg, width=1, alpha=0.5, edge_color='r', style='dashed')  # neg edges
nx.draw_networkx_edges(G, pos, edgelist=e_not, width=1, alpha=0.5, style='dashed')  # not edges

nx.draw_networkx_labels(G, pos, font_size=5, font_family='sans-serif', font_color='black')

# G.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (5, 6), (5, 7), (5, 8), (0, 9), (2, 11)])
# nx.draw_shell(G, with_labels=True, font_weight='bold', node_color='#A0CBE2', edge_color='b')
# nx.draw_spring(G, with_labels=True, font_weight='bold')

e1_pos = [(u, v) for (u, v, d) in GT.edges(data=True) if d['weight'] == 1]
e1_neg = [(u, v) for (u, v, d) in GT.edges(data=True) if d['weight'] == -1]
e1_not = [(u, v) for (u, v, d) in GT.edges(data=True) if d['weight'] == 0]
plt.figure(max + 1)
pos1 = nx.spring_layout(GT)  # positions for all nodes

nx.draw_networkx_nodes(GT, pos1, node_size=100, node_color='y')  # nodes

nx.draw_networkx_edges(GT, pos1, edgelist=e1_pos, width=1, alpha=0.5, edge_color='g', style='dashed')  # pos edges
nx.draw_networkx_edges(GT, pos1, edgelist=e1_neg, width=1, alpha=0.5, edge_color='r', style='dashed')  # neg edges
nx.draw_networkx_edges(GT, pos1, edgelist=e1_not, width=1, alpha=0.5, style='dashed')  # not edges

nx.draw_networkx_labels(GT, pos1, font_size=5, font_family='sans-serif', font_color='black')

plt.show()
