def convert_float(joint_pos_string):
    joint_pos = [0] * 6
    joint_pos_string_list = joint_pos_string.split(', ')
    for i in range(6):
        joint_pos[i] = float(joint_pos_string_list[i])
    return joint_pos
