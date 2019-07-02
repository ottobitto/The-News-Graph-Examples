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
    elif k > 0:
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
                                    if e[3]['color_{}'.format(c)] == "grey" or e[3]['id_component_{}'.format(c)] in unstables:
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
    insertNodeDAG(dag, 0, ine, 0, "9/8/2018 8:00:32")
    # 26
#     insertNodeDAG(dag, 26, ine, 0)
    # 1
#     ine.append([26, 1, 1, dag.node[26]])
    ine.append([0, 1, 1, dag.node[0]])
    insertNodeDAG(dag, 1, ine, 1, "9/8/2018 17:09:00")
    # 2
    ine.clear()
    ine.append([0, 2, -1, dag.node[0]])
    insertNodeDAG(dag, 2, ine, 1, "9/8/2018 18:42:00")
    # 3
    ine.clear()
    ine.append([0, 3, 0, dag.node[0]])
    ine.append([1, 3, 0, dag.node[1]])
    insertNodeDAG(dag, 3, ine, 2, "9/8/2018 19:29:00")
    # 4
    ine.clear()
    ine.append([0, 4, 1, dag.node[0]])
    ine.append([1, 4, 1, dag.node[1]])
    ine.append([2, 4, -1, dag.node[2]])
    ine.append([3, 4, 0, dag.node[3]])
    insertNodeDAG(dag, 4, ine, 4, "10/8/2018 6:00:00")
    # 5
    ine.clear()
    ine.append([0, 5, -1, dag.node[0]])
    ine.append([2, 5, 1, dag.node[2]])
    insertNodeDAG(dag, 5, ine, 2, "10/8/2018 10:47:10")
    # 6
    ine.clear()
    ine.append([0, 6, -1, dag.node[0]])
    ine.append([2, 6, 1, dag.node[2]])
    ine.append([3, 6, -1, dag.node[3]])
    insertNodeDAG(dag, 6, ine, 3, "10/8/2018 11:26:59")
    # 7
    ine.clear()
    ine.append([0, 7, 0, dag.node[0]])
    ine.append([2, 7, 0, dag.node[2]])
    ine.append([3, 7, 0, dag.node[3]])
    ine.append([4, 7, 0, dag.node[4]])
    ine.append([6, 7, 0, dag.node[6]])
    insertNodeDAG(dag, 7, ine, 5, "10/8/2018 11:27:00")
    # 8
    ine.clear()
    ine.append([7, 8, 0, dag.node[7]])
    insertNodeDAG(dag, 8, ine, 1, "10/8/2018 11:27:01")
    # 9
    ine.clear()
    ine.append([0, 9, -1, dag.node[0]])
    ine.append([2, 9, 1, dag.node[2]])
    insertNodeDAG(dag, 9, ine, 2, "10/8/2018 11:41:45")
    # 10
    ine.clear()
    ine.append([0, 10, -1, dag.node[0]])
    ine.append([1, 10, -1, dag.node[1]])
    insertNodeDAG(dag, 10, ine, 2, "10/8/2018 12:50:17")
    # 11
    ine.clear()
    ine.append([0, 11, 1, dag.node[0]])
    ine.append([1, 11, 0, dag.node[1]])
    ine.append([3, 11, 0, dag.node[3]])
    insertNodeDAG(dag, 11, ine, 3, "10/8/2018 14:44:00")
    # 12
    ine.clear()
    ine.append([0, 12, 0, dag.node[0]])
    ine.append([8, 12, 0, dag.node[8]])
    insertNodeDAG(dag, 12, ine, 2, "10/8/2018 14:49:00")
    # 13
    ine.clear()
    ine.append([2, 13, 0, dag.node[2]])
    insertNodeDAG(dag, 13, ine, 1, "10/8/2018 15:15:00")
    # 14
    ine.clear()
    ine.append([0, 14, -1, dag.node[0]])
    ine.append([1, 14, -1, dag.node[1]])
    ine.append([2, 14, 1, dag.node[2]])
    ine.append([5, 14, 1, dag.node[5]])
    ine.append([6, 14, 1, dag.node[6]])
    ine.append([9, 14, 1, dag.node[9]])
    ine.append([11, 14, -1, dag.node[11]])
    insertNodeDAG(dag, 14, ine, 7, "10/8/2018 15:25:02")
    # 15
    ine.clear()
    ine.append([0, 15, 0, dag.node[0]])
    ine.append([2, 15, 0, dag.node[2]])
    ine.append([3, 15, 0, dag.node[3]])
    ine.append([4, 15, 0, dag.node[4]])
    ine.append([6, 15, 0, dag.node[6]])
    insertNodeDAG(dag, 15, ine, 5, "10/8/2018 16:20:00")
    # 16
    ine.clear()
    ine.append([15, 16, 0, dag.node[15]])
    insertNodeDAG(dag, 16, ine, 1, "10/8/2018 16:21:00")
    # 17
    ine.clear()
    ine.append([2, 17, 0, dag.node[2]])
    ine.append([14, 17, 0, dag.node[14]])
    insertNodeDAG(dag, 17, ine, 2, "10/8/2018 16:51:56")
    # 18
    ine.clear()
    ine.append([0, 18, 0, dag.node[0]])
    insertNodeDAG(dag, 18, ine, 1, "10/8/2018 17:23:08")
    # 19
    ine.clear()
    ine.append([0, 19, -1, dag.node[0]])
    ine.append([2, 19, 1, dag.node[2]])
    ine.append([3, 19, -1, dag.node[3]])
    ine.append([6, 19, 1, dag.node[6]])
    ine.append([10, 19, 1, dag.node[10]])
    ine.append([18, 19, -1, dag.node[18]])
    insertNodeDAG(dag, 19, ine, 6, "10/8/2018 19:07:00")
    # 20
    ine.clear()
    ine.append([16, 20, 0, dag.node[16]])
    insertNodeDAG(dag, 20, ine, 1, "10/8/2018 20:00:00")
    # 21
    ine.clear()
    ine.append([0, 21, 0, dag.node[0]])
    insertNodeDAG(dag, 21, ine, 1, "11/8/2018 11:33:42")
    # 22
    ine.clear()
    ine.append([0, 22, 0, dag.node[0]])
    insertNodeDAG(dag, 22, ine, 1, "11/8/2018 15:51:11")
    # 23
    ine.clear()
    ine.append([2, 23, 0, dag.node[2]])
    ine.append([3, 23, 0, dag.node[3]])
    ine.append([4, 23, 0, dag.node[4]])
    ine.append([6, 23, 0, dag.node[6]])
    ine.append([7, 23, 0, dag.node[7]])
    ine.append([10, 23, 0, dag.node[10]])
    ine.append([12, 23, 0, dag.node[12]])
    ine.append([19, 23, 0, dag.node[19]])
    ine.append([21, 23, 0, dag.node[21]])
    ine.append([22, 23, 0, dag.node[22]])
    insertNodeDAG(dag, 23, ine, 10, "11/8/2018 15:51:12")
    # 24
    ine.clear()
    ine.append([23, 24, 0, dag.node[23]])
    insertNodeDAG(dag, 24, ine, 1, "17/9/2018 8:25:00")
    # 25
    ine.clear()
    ine.append([4, 25, 0, dag.node[4]])
    ine.append([7, 25, 0, dag.node[7]])
    ine.append([23, 25, 0, dag.node[23]])
    ine.append([24, 25, 0, dag.node[24]])
    insertNodeDAG(dag, 25, ine, 4, "17/9/2018 8:51:00")

    return dag


max = 26

G = new_news_graph_DAG()

GT = nx.DiGraph.reverse(G, copy=True)

print("number of nodes {0} ".format(G.number_of_nodes()))
print("number of edges {0} ".format(G.number_of_edges()))
print("DAG {0} ".format(nx.is_directed_acyclic_graph(G)))

tv = {}

sh = {}
un = {}
tw = {}
di = {}
pr = {}
wp = {}

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

    sh[i] = vtotnot
    un[i] = vtot0
    tw[i] = vtot1
    di[i] = vtot2

    print("NODE {}, color {}, vnot {}, v0node {}, v1node {}, v2node {} v3node {}".format(i, G.node[i], vtotnot, vtot0,
                                                                                         vtot1, vtot2, pr[i]))
    print(tv, vtotnot)
    ax0.plot(vtot0, vtotnot, 'ro')
    #     ax0.annotate(i, (vtot0, vtotnot))
    ax1.plot(vtot1, vtotnot, 'bo')
    ax2.plot(vtot2, vtotnot, 'go')


GprpT = nx.DiGraph.reverse(Gprp, copy=True)
GprnT = nx.DiGraph.reverse(Gprn, copy=True)


print("Sorted first")
sorted_un = sorted(un.items(), key=lambda kv: kv[1])
print(sorted_un)
print("Sorted second")
sorted_tw = sorted(tw.items(), key=lambda kv: kv[1])
print(sorted_tw)
print("Sorted third")
sorted_di = sorted(di.items(), key=lambda kv: kv[1])
print(sorted_di)
print("Sorted pagerank 1")
sorted_p1 = sorted(pr.items(), key=lambda kv: kv[1])
print(sorted_p1)
sorted_wp = sorted(wp.items(), key=lambda kv: kv[1])
print("Sorted w pagerank")
print(sorted_wp)

for i in list(G.nodes):
    ax3.plot(wp[i], sh[i], 'ys')
    ax4.plot(pr[i], sh[i], 'ms')

un_sorted = []
tw_sorted = []
di_sorted = []
# p_sorted = []
p1_sorted = []
wp_sorted = []

for index in list(G.nodes):
    un_sorted.append(sorted_un[index][0])
    tw_sorted.append(sorted_tw[index][0])
    di_sorted.append(sorted_di[index][0])
    p1_sorted.append(sorted_p1[index][0])
    wp_sorted.append(sorted_wp[index][0])


print(un_sorted)
print(tw_sorted)
print(di_sorted)
print(p1_sorted)
print(wp_sorted)

# inversion coefficient
swap_f_s = count_swap(sorted_un, sorted_tw, max)
print("Inversion coefficient u t: {}".format(swap_f_s))
swap_f_t = count_swap(sorted_un, sorted_di, max)
print("Inversion coefficient u d: {}".format(swap_f_t))
swap_f_p1 = count_swap(sorted_un, sorted_p1, max)
print("Inversion coefficient u p1: {}".format(swap_f_p1))
swap_f_wp = count_swap(sorted_un, sorted_wp, max)
print("Inversion coefficient u wp: {}".format(swap_f_wp))
swap_s_t = count_swap(sorted_tw, sorted_di, max)
print("Inversion coefficient t d: {}".format(swap_s_t))
swap_s_p1 = count_swap(sorted_tw, sorted_p1, max)
print("Inversion coefficient t p1: {}".format(swap_s_p1))
swap_s_wp = count_swap(sorted_tw, sorted_wp, max)
print("Inversion coefficient t wp: {}".format(swap_s_wp))
swap_t_p1 = count_swap(sorted_di, sorted_p1, max)
print("Inversion coefficient d p1: {}".format(swap_t_p1))
swap_t_wp = count_swap(sorted_di, sorted_wp, max)
print("Inversion coefficient d wp: {}".format(swap_t_wp))
swap_p1_wp = count_swap(sorted_p1, sorted_wp, max)
print("Inversion coefficient p1 wp: {}".format(swap_p1_wp))

# Kendall
kendall_u_t, p_value = stats.kendalltau(un_sorted, tw_sorted)
print("Kendall's tau u t {}, p_value {}".format(kendall_u_t, p_value))
kendall_u_d, p_value = stats.kendalltau(un_sorted, di_sorted)
print("Kendall's tau u d {}, p_value {}".format(kendall_u_d, p_value))
kendall_u_p1, p_value = stats.kendalltau(un_sorted, p1_sorted)
print("Kendall's tau u p1 {}, p_value {}".format(kendall_u_p1, p_value))
kendall_u_wp, p_value = stats.kendalltau(un_sorted, wp_sorted)
print("Kendall's tau u wp {}, p_value {}".format(kendall_u_wp, p_value))
kendall_t_d, p_value = stats.kendalltau(tw_sorted, di_sorted)
print("Kendall's tau t d {}, p_value {}".format(kendall_t_d, p_value))
kendall_t_p1, p_value = stats.kendalltau(tw_sorted, p1_sorted)
print("Kendall's tau t p1 {}, p_value {}".format(kendall_t_p1, p_value))
kendall_t_wp, p_value = stats.kendalltau(tw_sorted, wp_sorted)
print("Kendall's tau t wp {}, p_value {}".format(kendall_t_wp, p_value))
kendall_d_p1, p_value = stats.kendalltau(di_sorted, p1_sorted)
print("Kendall's tau d p1 {}, p_value {}".format(kendall_d_p1, p_value))
kendall_d_wp, p_value = stats.kendalltau(di_sorted, wp_sorted)
print("Kendall's tau d wp {}, p_value {}".format(kendall_d_wp, p_value))
kendall_p1_wp, p_value = stats.kendalltau(p1_sorted, wp_sorted)
print("Kendall's tau p1 wp {}, p_value {}".format(kendall_p1_wp, p_value))

# Spearman
spearman_u_t, p_value = stats.spearmanr(un_sorted, tw_sorted)
print("Spearman's rho u t {}, p_value {}".format(spearman_u_t, p_value))
spearman_u_d, p_value = stats.spearmanr(un_sorted, di_sorted)
print("Spearman's rho u d {}, p_value {}".format(spearman_u_d, p_value))
spearman_u_p1, p_value = stats.spearmanr(un_sorted, p1_sorted)
print("Spearman's rho u p1 {}, p_value {}".format(spearman_u_p1, p_value))
spearman_u_wp, p_value = stats.spearmanr(un_sorted, wp_sorted)
print("Spearman's rho u wp {}, p_value {}".format(spearman_u_wp, p_value))
spearman_t_d, p_value = stats.spearmanr(tw_sorted, di_sorted)
print("Spearman's rho t d {}, p_value {}".format(spearman_t_d, p_value))
spearman_t_p1, p_value = stats.spearmanr(tw_sorted, p1_sorted)
print("Spearman's rho t p1 {}, p_value {}".format(spearman_t_p1, p_value))
spearman_t_wp, p_value = stats.spearmanr(tw_sorted, wp_sorted)
print("Spearman's rho t wp {}, p_value {}".format(spearman_t_wp, p_value))
spearman_d_p1, p_value = stats.spearmanr(di_sorted, p1_sorted)
print("Spearman's rho d p1 {}, p_value {}".format(spearman_d_p1, p_value))
spearman_d_wp, p_value = stats.spearmanr(di_sorted, wp_sorted)
print("Spearman's rho d wp {}, p_value {}".format(spearman_d_wp, p_value))
spearman_p1_wp, p_value = stats.spearmanr(p1_sorted, wp_sorted)
print("Spearman's rho p1 wp {}, p_value {}".format(spearman_p1_wp, p_value))

# distances
print("Distances between u t")
print(distances(sorted_un, sorted_tw, max))
print("Distances between u d")
print(distances(sorted_un, sorted_di, max))
print("Distances between u p1")
print(distances(sorted_un, sorted_p1, max))
print("Distances between u wp")
print(distances(sorted_un, sorted_wp, max))
print("Distances between t d")
print(distances(sorted_tw, sorted_di, max))
print("Distances between t p1")
print(distances(sorted_tw, sorted_p1, max))
print("Distances between t wp")
print(distances(sorted_tw, sorted_wp, max))
print("Distances between d p1")
print(distances(sorted_di, sorted_p1, max))
print("Distances between d wp")
print(distances(sorted_di, sorted_wp, max))
print("Distances between p1 wp")
print(distances(sorted_p1, sorted_wp, max))


for y in range(G.number_of_nodes()-1):
    print(y, y + 1)
    diff = date_difference(G.node[y]['time'], G.node[y + 1]['time'])
    print(diff)
tot_time = date_difference(G.node[0]['time'], G.node[25]['time'])
print(tot_time)

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
