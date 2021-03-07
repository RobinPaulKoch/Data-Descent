import numpy
import random

def recursive_root_finder(l, edge):
    #Define random starting point

    target_l = []
    for v1, v2 in l:
        target_l.append(v2)

    if edge[0] in target_l:
        predecessors_i = [i for i, e in enumerate(target_l) if e == edge[0]]
        for i in predecessors_i:
            return recursive_root_finder(l, l[i])
    else:
        root = edge[0]
        return root

def find_roots(links):
    roots = []
    for edge in links:
        r = recursive_root_finder(links, edge)
        if r not in roots:
            roots.append(r)

    return roots

def test_find_roots():
    # Define example
    links = [('dg_i_p_40ana_p1_input.new', 'BATCH.v_feat1'),
            ('dg_i_p_40ana_p1_input.new', 'BATCH.v_feat2'),
            ('BATCH.v_feat1', 'dg_i_p_40ana_p1.abt'),
            ('BATCH.v_feat2', 'BATCH.v_tmp'),
            ('BATCH.v_feat2', 'dg_i_p_40ana_p1.abt'),
            ('dg_i_p_40ana_p1.abt', 'dg_i_p_50pro_p1_50.signal'),
            ('BATCH.v_tmp', 'BATCH.v_feat2'),
            ('test_source', 'BATCH.v_feat1')]

    return find_roots(links)

if __name__ == '__main__':
    print(f'Running test function...')
    try:
        print(test_find_roots())
        print(f'Test run was succesful!')
    except:
        print(f'Test run was not succesful!')
