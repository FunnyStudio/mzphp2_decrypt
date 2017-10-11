import os
import re
import requests
import argparse

slash = "\\"


def str_list_in_str(str_list, _str):
    if not isinstance(str_list, list):
        raise TypeError
    for x in str_list:
        if x in _str:
            return True
    return False


def format_php_code(php_code):
    try:
        format_result = requests.post("http://tools.jb51.net/static/api/phpfmt/doformat.php",
                                      data={"phpcode": "<?php \r\n" + php_code}).text
    except:
        if args.o is not None:
            print('尝试使用 http://tools.jb51.net/static/api/phpfmt/doformat.php 格式化php代码失败，或许您需要手动格式化代码')
        format_result = "<?php \r\n" + php_code
    return format_result


def parse_code(file_name):
    file_content = open(file_name, 'rb').read()
    file_content = repr(file_content).replace(slash + 'n', '')[8:-1]  # convert bin to str and remove b"<?php "

    file_content = re.sub(r';(?:\\x[a-z0-9]{2})+;', ';', file_content)  # remove dirty php code

    global var_list
    global var_key

    def get_var_list(repl):
        global var_list
        global var_key
        var_key = slash + repl.group(1)
        var_list = repl.group(3).replace(slash * 2, slash).split(repl.group(2))
        return ''

    # get_var_list
    file_content = re.sub(
        r'\$(?:(?:GLOBALS)|(?:_SERVER))\[(\\x[a-z0-9]{2})+?\] = explode\(\s*["\'](.+?)["\']\s*,\s*["\'](.+?)["\']\s*\);',
        get_var_list,
        file_content
    )

    # remove var_list define

    file_content = re.sub(r"define\(\s*'" + var_key + r"'\s*,\s*'(?:\\x[a-z0-9]{2})+'\s*\);", "\r\n", file_content)

    # replace $GLOBALS{var_key}[hex_id] var
    file_content = re.sub(
        r"\$(?:(?:GLOBALS)|(?:_SERVER)){" + var_key + r"}[\[\{](.+?)[\]\}]",
        lambda x: repr(var_list[int(x.group(1), 16)]),
        file_content
    )

    global mnc
    global var_list_instance

    mnc = 0
    var_list_instance = []

    def rp_var(repl):
        global var_list_instance
        if repl.group(1) not in var_list_instance:
            var_list_instance.append(repl.group(1))
        return ''

    file_content = re.sub(r"(\$(?:\\x[a-z0-9]{2})+)=&\$(?:(?:GLOBALS)|(?:_SERVER)){" + var_key + r"};", rp_var,
                          file_content)

    var_list_instance.sort(key=lambda x: len(x), reverse=True)

    for instance in var_list_instance:
        file_content = re.sub(slash + repr(instance)[1:-1] + r"[\[\{](.+?)[\]\}]",
                              lambda x: repr(var_list[int(x.group(1), 16)]), file_content)

    mnc = 0
    var_list_instance = {}

    def fix_var(repl):
        global var_list_instance
        global mnc
        if repl.group(1) not in var_list_instance:
            var_list_instance[repl.group(1)] = "$_var_" + str(mnc)
            mnc += 1
        return var_list_instance[repl.group(1)]

    file_content = re.sub(r"(\$(?:\\x[a-z0-9]{2})+)", fix_var, file_content)

    file_content = re.sub(r'(0x[0-9a-z]+)', lambda x: str(int(x.group(1), 16)), file_content)

    # do final

    file_content = format_php_code(file_content)
    return file_content


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='mzphp decrypt tool')
    parser.add_argument('f', metavar="mzphp encrypt file", help='mzphp encrypt file')
    parser.add_argument('o', metavar="Output file", help='output file')
    args = parser.parse_args()
    if not os.path.isfile(args.f):
        raise FileNotFoundError
    result = parse_code(args.f)

    if args.o is not None:
        with open(args.o, 'wb') as of:
            of.write(result.encode('utf-8'))
    else:
        print(result)
