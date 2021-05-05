import yaml

one = ['msg_1', 'msg_2', 'msg_3']

two = {'A' : 'Welcome', 'B' : 'To', 'C' : 'Geeks'}

data_to_yaml = {'list1_€':one, 'list2_€':25, 'list3_€':two}

with open('data_write.yaml', 'w') as f_n:
    yaml.dump(data_to_yaml, f_n,  default_flow_style=False, allow_unicode = True)

with open('data_write.yaml') as f_n:
    print(f_n.read())
