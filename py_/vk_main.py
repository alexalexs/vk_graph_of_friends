from vk_get_friends import *
from vk_plot_tree import *


def main():

    Name = '*************'
    id_src = '*************'
    id_app = '*************'
    login = '*************'
    passwd = '*************'
    vk_api = open_session(id_app, login, passwd)
    a = get_friends(vk_api, id_src)
    write_dict(a, Name)

    list_all_users, b_id_to_names, b_id_to_sex, n_del = some_init_procedures(
        Name)
    data = create_data_dict(Name, n_del)
    plot_(Name, data, b_id_to_names, b_id_to_sex)


if __name__ == '__main__':
    main()
