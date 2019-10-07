def stringConvert(input_str):
    '''

    :param input_str: a string
    :return: keep 'a'~'z', 'A'~'Z', '0'~'9, convert others to '%' + ASCII
    '''
    output_str = []
    for each in input_str:
        mark = ord(each)
        if (mark == 38) or (mark >= 48 and mark <= 57) or (mark >= 65 and mark <= 90) or (mark >= 97 and mark <= 122):
            output_str.append(chr(mark))
        else:
            output_str.append('%' + str(mark))

    return ''.join(output_str)
