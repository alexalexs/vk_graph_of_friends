#!/usr/bin/env python
# coding: utf-8

import vk
import json
import time


def open_session(id_app, login, passwd):

    session = vk.AuthSession(id_app, login, passwd,
                             scope='notify,photos,friends,audio,video,notes,pages,docs,status,questions,offers,wall,groups,messages,notifications,stats,ads,offline')
    vk_api = vk.API(session)
    print(session)
    return vk_api


def get_list_id(w, id_):
    list_id = [i['id'] for i in w[id_]['items']]
    return list_id


def get_friends(vk_api, id_src, cycles_all=100, N_obs=200, N_mut=5):

    cn_ = 0

    a = {id_src: vk_api.friends.get(
        user_id=id_src, fields='first_name,last_name,sex', v=5.92)}
    list_id = get_list_id(a, id_src)
    for j in list_id[:N_obs]:
        cn_ += 1
        print('cycle_num:', cn_)
        if cn_ < cycles_all:
            print('Go throw:', j)
            try:
                time.sleep(1)
                if len(vk_api.friends.getMutual(source_uid=id_src, target_uid=j, target_uids=vk_api.friends.get(user_id=id_src, v=5.92)['items'], v=5.92)) > N_mut:
                    a[str(j)] = vk_api.friends.get(
                        user_id=j, fields='first_name,last_name,sex', v=5.92, count='10')
                    list_id.extend(get_list_id(a, str(j)))
                    print('Ok:', j, 'len list:', len(
                        list_id), 'len dict:', len(a))
                else:
                    print('too few mutual friends:', j)
            except vk.exceptions.VkAPIError:
                print('private permission for user:', j)

        else:
            break
    return a


def write_dict(a, Name):

    with open(Name+'_firends.json', 'w') as f:
        f.write(json.dumps(a))


def main():
    Name = '*************'
    id_src = '*************'
    id_app = '*************'
    login = '*************'
    passwd = '*************'
    vk_api = open_session(id_app, login, passwd)
    a = get_friends(vk_api, id_src)
    write_dict(a, Name)


if __name__ == '__main__':
    main()
