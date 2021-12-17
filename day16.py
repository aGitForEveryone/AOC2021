from aocd import submit, data

# print(data)


def to_binary(hex_input):
    bin_str = ''
    for hex_num in hex_input:
        bin_str += bin(int(hex_num, 16))[2:].zfill(4)
    return bin_str


def perform_op_code(type_id, values):
    if type_id == 0:
        return sum(values)
    elif type_id == 1:
        prod = 1
        for val in values:
            prod *= val
        return prod
    elif type_id == 2:
        return min(values)
    elif type_id == 3:
        return max(values)
    elif type_id == 5:
        if len(values) != 2:
            raise ValueError(f'Expected 2 values for operation with type id {type_id}, but got {len(values)} instead.')
        return 1 if values[0] > values[1] else 0
    elif type_id == 6:
        if len(values) != 2:
            raise ValueError(f'Expected 2 values for operation with type id {type_id}, but got {len(values)} instead.')
        return 1 if values[0] < values[1] else 0
    elif type_id == 7:
        if len(values) != 2:
            raise ValueError(f'Expected 2 values for operation with type id {type_id}, but got {len(values)} instead.')
        return 1 if values[0] == values[1] else 0


def analyze_package(package_string, version_sum, results):
    # print(package_string, version_sum, results)
    # while package_string.count('1'):
        # As long as there are ones in the package strings, we should continue reading
    version = int(package_string[:3], 2)
    type_id = int(package_string[3:6], 2)
    # print(f'Version {version}, type {type_id}, from bin string: {package_string[:6]}')
    version_sum += version
    if type_id == 4:  # the package contains a literal value
        stored_number = ''
        idx = 6
        while package_string[idx] == '1':
            stored_number += package_string[idx + 1:idx + 5]
            idx += 5

        # first digit of next group of 5 bits is now 0, so we need to add the final 4 bits
        stored_number += package_string[idx + 1:idx + 5]
        package_string = package_string[idx + 5:]
        results += [int(stored_number, 2)]
    else:  # the package represents an operator
        length_type_id = package_string[6]
        # print(f'Length type id: {length_type_id}')
        if length_type_id == '1':
            # next 11 bits indicate the number of subpackages
            num_of_packages = int(package_string[7:18], 2)
            # print(f'Number of packages: {num_of_packages}, from bin string {package_string[7:18]}')
            package_string = package_string[18:]
            values = []
            for _ in range(num_of_packages):
                package_string, version_sum, values = analyze_package(package_string, version_sum, values)
            # print(package_string, version_sum, values)
        else:  # == '0'
            # next 15 bits indicate the remaining length of the operator package
            sub_package_length = int(package_string[7:22], 2)
            # print(f'Sub package length: {sub_package_length}, from bin string {package_string[7:22]}')
            sub_package_string = package_string[22:22 + sub_package_length]
            # print(f'Sub package string {sub_package_string}')
            values = []
            while sub_package_string != '':
                sub_package_string, version_sum, values = analyze_package(sub_package_string, version_sum, values)
            package_string = package_string[22 + sub_package_length:]
        # print(f'Found package operator {type_id}, with length type id: {length_type_id} and values {values}')
        results += [perform_op_code(type_id, values)]
        # print(results)

    return package_string, version_sum, results


def solve(input, should_submit=False):
    print(f'\nStarting solving for hex string: {input}')
    package_string = to_binary(input)
    remaining_string, version_sum, results = analyze_package(package_string, 0, [])

    print(f'The remaining package string: {remaining_string}\n'
          f'The version sum             : {version_sum}\n'
          f'Literal values found        : {results}')
    if should_submit:
        submit(version_sum, part='a')
        submit(results[0], part='b')


example_1 = 'D2FE28'
example_2 = '38006F45291200'
example_3 = 'EE00D40C823060'
example_4 = '8A004A801A8002F478'
example_5 = '620080001611562C8802118E34'
example_6 = 'C0015000016115A2E0802F182340'
example_7 = 'A0016C880162017C3686B18A3D4780'

# print(to_binary(example_1))
# print(analyze_package(to_binary(example_1), 0, []))
# print(analyze_package(to_binary(example_2), 0, []))
# print(analyze_package(to_binary(example_3), 0, []))
# for example in [example_4, example_5, example_6, example_7]:
#     solve(example)

solve(data, True)
# solve('C200B40A82')
# solve('04005AC33890')
# solve('880086C3E88112')
# solve('CE00C43D881120')
# solve('D8005AC2A8F0')
# solve('F600BC2D8F')
# solve('9C005AC2F8F0')
# solve('9C0141080250320F1802104A08')
# assert '110100101111111000101000' == to_binary(example_1)