def read_literal_value(data, version):
    is_last_group = False
    group_number = 1
    packet_end = None
    while not is_last_group:
        start_index = 5 * group_number
        group = data[start_index+1:(start_index+6)]
        group_number += 1
        if int(group[:1]) == 0 or len(group) < 5:
            is_last_group = True
            packet_end = start_index+6
    return [version, packet_end]


def read_transmission(data):
    version = bin_to_num(data[:3])
    packet_id = bin_to_num(data[3:6])
    if packet_id == 4:
        return read_literal_value(data, version)
    else:
        length_type_id = int(data[6:7])
        last_index = 0
        if length_type_id == 0:
            subpacket_length = bin_to_num(data[7:22])
            is_packet_end = False
            last_index = 22
            last_subpacket_index = 22 + subpacket_length
            while not is_packet_end:
                packet_version, packet_end = read_transmission(data[last_index:last_subpacket_index])
                version += packet_version
                last_index += packet_end
                if last_index == last_subpacket_index:
                    is_packet_end = True
        else:
            subpacket_count = bin_to_num(data[7:18])
            seen = 0
            last_index = 18
            while seen < subpacket_count:
                packet_version, packet_end = read_transmission(data[last_index:])
                version += packet_version
                last_index += packet_end
                seen += 1
        return [version, last_index]


def bin_to_num(n):
    return int(n, 2)


def parse_output(filename):
    binary = None
    with open(filename) as fp:
        line = fp.readline()
        while line:
            end_length = len(line) * 4
            binary = bin(int(line, 16))[2:].zfill(end_length)
            line = fp.readline()
    return binary


def main():
    file = parse_output('input.txt')
    version, last_index = read_transmission(file)
    print('Part 1: ', version)


if __name__ == "__main__":
    main()
