#!/usr/bin/env python
# coding: utf-8

import csv
import json
import jgraph as ig
import plotly.offline as py
import plotly.graph_objs as go
import os
from IPython.display import display, HTML

def find_last(row, name):
    c = []
    for a in row[::-1]:
        if a['name'] == name:
            c.append(a['id'])
        else:
            c.append(None)
    return c


def check_nodes_for_repetition(data, r):
    ac_ = 0
    for c, i in enumerate(data['nodes']):
        if i['name'] == r:
            return c
        else:
            pass
    return None


def del_appendix_users(data):
    l_ = []
    n_del = [i for i in data if data.count(i) == 1]
    return n_del


def row_transform_add_node(row, c_dict, n_del=[None]):
    if c_dict == {}:
        c_ = 0
        # --------------nodes-----------------------------
        c_dict['nodes'] = [{'name': i, 'id': c_, 'group': 1, 'size': 6}
                           for c_, i in enumerate(row)]
        # --------------links-----------------------------
        c_dict['links'] = [{'source': 0, 'target': i, 'value': 1,
                            'source_name': row[0], 'target_name':row[i]} for i in range(1, len(row))]
    else:
        for i in row[1::]:
            # --------------nodes-----------------------------
            # is node exist?--------------------------
            c_node = check_nodes_for_repetition(c_dict, i)
            if c_node == None:
                # node does'n exist--------------------------
                # is't in deletion list?
                if i not in n_del:
                    c_ = len(c_dict['nodes'])
                    c_dict['nodes'].append(
                        {'name': i, 'id': c_, 'group': 1, 'size': 6})
                    c_ += 1
                else:
                    pass

            else:

                # node exists--------------------------
                c_dict['nodes'][c_node]['size'] += 2

    return c_dict


def row_transform_add_links(row, c_dict, n_del=[None]):
    if c_dict == {}:
        c_ = 0
        # --------------nodes-----------------------------
        c_dict['nodes'] = [{'name': i, 'id': c_, 'group': 1, 'size': 6}
                           for c_, i in enumerate(row)]
        # --------------links-----------------------------
        c_dict['links'] = [{'source': 0, 'target': i, 'value': 1,
                            'source_name': row[0], 'target_name':row[i]} for i in range(1, len(row))]
    else:
        for i in row[1::]:
            # --------------nodes-----------------------------
            # is node exist?--------------------------
            c_node = check_nodes_for_repetition(c_dict, i)
            if c_node == None:
                # node does'n exist--------------------------
                # is't in deletion list?
                if i not in n_del:
                    c_ = len(c_dict['nodes'])
                    c_dict['nodes'].append(
                        {'name': i, 'id': c_, 'group': 1, 'size': 6})
#                     #---------links----------------------------------
                    res = find_last(c_dict['nodes'], row[0])
                    for j in res:

                        if j != None:
                            c_dict['links'].append({'source':
                                                    j,
                                                    'target': c_, 'value': 1,
                                                    'source_name': c_dict['nodes'][j]['name'],
                                                    'target_name': c_dict['nodes'][c_]['name']})
                    c_ += 1
                else:
                    pass

            else:

                # node exists--------------------------
                # ---------links----------------------------------
                res = find_last(c_dict['nodes'], row[0])
                for j in res:

                    if j != None:
                        c_dict['links'].append({'source':
                                                j,
                                                'target': c_node, 'value': 1,
                                                'source_name': c_dict['nodes'][j]['name'],
                                                'target_name': c_dict['nodes'][c_node]['name']})

    return c_dict


def preprocessing_(row, fname):
    with open(fname, 'a') as f:
        t_ = row[0]+','+','.join([i+'_'+row[0].split('_')[0]
                                  for i in row[1::]])+'\n'
        f.write(t_)


def check_collisions_(c_dict):
    k = 1
    check = {}
    for i in c_dict['links'][::-1]:
        k += 1
        check[i['source_name']] = 'fail'
        for j in c_dict['links'][::-1]:
            if i['source_name'] == j['target_name']:
                check[i['source_name']] = 'ok'
        if (check[i['source_name']] == 'fail') or (i['source_name'] == c_dict['nodes'][0]['name']):
            print('gaps_warning:', i['source_name'])
    return check


def check_repetition_name_surname(fname):
    a = []
    with open(fname, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            preprocessing_(row, fname_exp)
            a.append(row[0])
    d = {x: a.count(x) for x in a if a.count(x) > 1}
    print('problem_nodes', d)


def beacon(c_dict, tar_):
    c_dict['nodes'][0]['size'] = 10
    c_dict['nodes'][0]['group'] = 2
    for i in range(len(c_dict['nodes'])-1, 1, -1):
        c_dict['nodes'][i]['size'] = 6
        if c_dict['nodes'][i]['name'] == tar_:
            c_dict['nodes'][i]['group'] = 2
            c_dict['nodes'][i]['size'] = 10
            print(c_dict['nodes'][i]['group'])
            for j in c_dict['links'][::-1]:
                if j['target_name'] == tar_:
                    tar_ = j['source_name']
                    print(tar_)
                    break

    return c_dict


def some_init_procedures(Name):

    with open(Name+'_firends.json', 'r') as f:
        w = json.load(f)

    if os.path.isfile(Name+'_tree_friends.txt'):
        open(Name+'_tree_friends.txt', 'w').close()
    else:
        pass

    # Create real names for nodes
    c_ = 0
    Num_nodec_rescric = 100
    b_id_to_names = {list(w.keys())[0]: Name}
    b_id_to_sex = {list(w.keys())[0]: 2}

    list_all_users = []
    for k, v in w.items():
        a = []
        if c_ < Num_nodec_rescric:

            for i in v['items']:
                a.append(str(i['id']))
                list_all_users.append(str(i['id']))
                b_id_to_names.update(
                    {str(i['id']): i['first_name']+' '+i['last_name']})
                b_id_to_sex.update({str(i['id']): i['sex']})
            with open(Name+'_tree_friends.txt', 'a') as f:
                f.write(k+','+','.join(a)+'\n')
            c_ += 1
        else:
            pass

    n_del = del_appendix_users(list_all_users)
    print('число удаляемых пользователей:', len(n_del))

    return list_all_users, b_id_to_names, b_id_to_sex, n_del


def create_data_dict(Name, n_del):
    # second pass to delete spurious friends
    with open(Name+'_tree_friends.txt', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        c_dict = {}
        k_ = 0
        for row in spamreader:
            data = row_transform_add_node(row, c_dict, n_del=n_del)

    with open(Name+'_tree_friends.txt', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

        k_ = 0
        for row in spamreader:
            data = row_transform_add_links(row, data, n_del=n_del)

    data_chk = check_collisions_(data)
    print('\ndata_dict created')
    return data


def plot_(Name,data, b_id_to_names, b_id_to_sex):
    print('starting plot creating')
    N = len(data['nodes'])

    L = len(data['links'])
    Edges = [(data['links'][k]['source'], data['links'][k]['target'])
             for k in range(L)]

    display(HTML(ig.draw(Edges, directed=False)))

    labels = []
    group = []
    size_ = []
    for node in data['nodes']:
        labels.append(b_id_to_names[node['name']])
        group.append(b_id_to_sex[node['name']])
        size_.append(node['size'])

    layt = ig.generate(Edges)

    Xn = [layt['nodes'][k]['location'][0]
          for k in range(N)]  # x-coordinates of nodes
    Yn = [layt['nodes'][k]['location'][1] for k in range(N)]  # y-coordinates
    Zn = [layt['nodes'][k]['location'][2] for k in range(N)]  # z-coordinates
    Xe = []
    Ye = []
    Ze = []
    for e in Edges:
        Xe += [layt['nodes'][e[0]]['location'][0], layt['nodes']
                   [e[1]]['location'][0], None]  # x-coordinates of edge ends
        Ye += [layt['nodes'][e[0]]['location'][1],
               layt['nodes'][e[1]]['location'][1], None]
        Ze += [layt['nodes'][e[0]]['location'][2],
               layt['nodes'][e[1]]['location'][2], None]

    trace1 = go.Scatter3d(x=Xe,
                          y=Ye,
                          z=Ze,
                          mode='lines',
                          line=dict(color='rgb(125,125,125)', width=1),
                          hoverinfo='none'
                          )

    trace2 = go.Scatter3d(x=Xn,
                          y=Yn,
                          z=Zn,
                          mode='markers+text',
                          name='actors',
                          marker=dict(symbol='circle',
                                      size=size_,
                                      color=group,
                                      colorscale='Viridis',
                                      line=dict(
                                          color='rgb(50,50,50)', width=0.5)
                                      ),
                          text=labels,
                          hoverinfo='text'
                          )

    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )

    layout = go.Layout(
        title="Мои друзья",
        width=1000,
        height=1000,
        showlegend=False,
        scene=dict(
            xaxis=dict(axis),
            yaxis=dict(axis),
            zaxis=dict(axis),
        ),
        margin=dict(
            t=100
        ),
        hovermode='closest',

    )

    data = [trace1, trace2]
    fig = go.FigureWidget(data=data, layout=layout)

    py.plot(fig, filename=Name+'_Friends.html')


def main():
    Name = '*************'
    list_all_users, b_id_to_names, b_id_to_sex, n_del = some_init_procedures(
        Name)
    data = create_data_dict(Name, n_del)
    plot_(Name,data, b_id_to_names, b_id_to_sex)


if __name__ == '__main__':
    main()
