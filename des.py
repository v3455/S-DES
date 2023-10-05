import re

# 定义
P10 = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]  # P10置换
P8 = [5, 2, 6, 3, 7, 4, 9, 8]        # P8置换
Shift1 = [1, 2, 3, 4, 0]               # 循环左移1
Shift2 = [2, 3, 4, 0, 1]               # 循环左移2
IP = [1, 5, 2, 0, 3, 7, 4, 6]        # 初始置换
IP_INV = [3, 0, 2, 4, 6, 1, 7, 5]    # 最终逆置换
EP = [3, 0, 1, 2, 1, 2, 3, 0]        # 轮函数扩展置换
SW = [4, 5, 6, 7, 0, 1, 2, 3]        # SW置换
SBOX1 = [[1, 0, 3, 2],
         [3, 2, 1, 0],
         [0, 2, 1, 3],
         [3, 1, 0, 2]]
SBOX2 = [[0, 1, 2, 3],
         [2, 3, 1, 0],
         [3, 0, 1, 2],
         [2, 1, 0, 3]]
SPBOX = [1, 3, 2, 0]                  # SPBox置换盒


# 整数转换为n位二进制
def int_to_bin(key, n):
    return bin(int(key))[2:].rjust(n, '0')


# 二进制转换为整数
def bin_to_int(binary):
    return int(binary, 2)


# 按位异或
def xor(a, b):
    xor_result = ''
    for i, j in zip(a, b):
        if int(i) == int(j):
            xor_result += '0'
        else:
            xor_result += '1'
    return xor_result


# 将每个ASCII字符转换为对应的8位二进制字符，并添加到列表中
def ascii_to_bin_groups(ascii_string):
    binary_groups = []  # 用于存储8位二进制字符的列表
    for char in ascii_string:
        ascii_char = ord(char)
        binary_char = bin(ascii_char)[2:].rjust(8, '0')
        binary_groups.append(binary_char)
    return binary_groups


# 将二进制字符串转换为对应的ASCII字符
def bin_to_ascii(binary_string):
    ascii_string = ''
    for bin in binary_string:
        ascii_char = int(bin, 2)  # 将二进制字符转换为十进制值
        ascii_char = chr(ascii_char)
        ascii_string += ascii_char
    return ascii_string


# 判断输入的明/密文是否为二进制字符，若不是则转换为二进制
def is_bin_string(key):
    # 定义正则表达式模式，表示只包含0和1的字符串
    bin = r'^[01]+$'
    # 使用re.match()来匹配字符串
    match = re.match(bin, key)
    # 如果匹配成功，说明是二进制字符串，返回True；否则返回False
    if match:
        # print("输入的是二进制字符串")
        return True
    else:
        # print("输入的是ASCII字符串")
        return False


# 根据置换表进行置换
def p(key, p_table):
    result = ''
    for i in range(len(p_table)):
        result += key[p_table[i]]
    return result


# 循环左移n位
def left_shift(bits, n):
    return bits[n:] + bits[:n]


# 密钥扩展,生成8bits子密钥
def key_expansion(key):
    # key =to_bin(key, 10)
    p10_key = p(key, P10)
    # print("p10_key=",p10_key)
    left_key = p10_key[:5]
    right_key = p10_key[5:]
    subkey1 = left_shift(left_key, 1)+left_shift(right_key, 1)
    subkey1 = p(subkey1, P8)
    subkey2 = left_shift(left_key, 2)+left_shift(right_key, 2)
    subkey2 = p(subkey2, P8)
    # print('密钥扩展为:',subkey1,subkey2)
    return subkey1, subkey2


# S盒替代
def sbox_substitution(bits, sbox):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return bin(sbox[row][col])[2:].rjust(2, '0')


# F轮函数
def F(bits, subkey):
    # print(bits,"正在扩展..")
    ep_key = p(bits, EP)  # 扩展置换
    # print("ep_key=",ep_key)
    xor_key = xor(ep_key, subkey)
    # print("xor_key=",xor_key)
    xor_key_l = xor_key[:4]
    xor_key_r = xor_key[4:]
    sbox_key_l = sbox_substitution(xor_key_l, SBOX1)
    sbox_key_r = sbox_substitution(xor_key_r, SBOX2)
    sbox_key = sbox_key_l+sbox_key_r
    # print("sbox_key=",sbox_key)
    spbox_key = p(sbox_key, SPBOX)
    # print("轮转换结果为:",spbox_key)
    # result = xor(bits[:4], spbox_key) + bits[4:]
    return spbox_key


def fk(l, r, subkey):
    F_result = F(r, subkey)
    l = xor(l, F_result)
    fk_result = l + r
    # print("fk_result=",fk_result)
    return fk_result


# 加密
def C(plaintext, key):
    # print("明文:",plaintext,'\n密钥:',key)
    subkeys = key_expansion(key)          # 生成子密钥
    result = []  # 最后的加密结果
    if is_bin_string(plaintext):
        # 转换为数组，方便后续的循环
        plaintext_trans = [plaintext]
    else:
        plaintext_trans = ascii_to_bin_groups(plaintext)
    # print("转换后的明文为:",plaintext_trans)

    for i in range(len(plaintext_trans)):
        # print("----------------------------")
        # 判断输入字符串是否为二进制或者ASCII码，若为ASCII码需要进行分组加密
        ip_initial = p(plaintext_trans[i], IP)     # 初始置换
        # print('ip_initial=',ip_initial)
        fk1_result = fk(ip_initial[:4], ip_initial[4:], subkeys[0])
        sw_result = p(fk1_result, SW)
        # print("sw_result=",sw_result)
        fk2_result = fk(sw_result[:4], sw_result[4:], subkeys[1])
        ip_final = p(fk2_result, IP_INV)
        result.append(ip_final)
    # print("加密为:",result)

    # 若输入明文为ascii码，则返回也为ascii码
    result = result if is_bin_string(plaintext) else bin_to_ascii(result)
    # print("转换后的加密为:",result)
    
    return result
    

# 解密
def P(ciphertext, key):
    # print("密文:",ciphertext,'\n密钥:',key)
    subkeys = key_expansion(key)
    result = []  # 最后的解密结果
    if is_bin_string(ciphertext):
        ciphertext_trans = [ciphertext]
    else:
        ciphertext_trans = ascii_to_bin_groups(ciphertext)
    # print("转换后的密文为:",ciphertext_trans)

    for i in range(len(ciphertext_trans)):
        # print("----------------------------")
        ip_initial = p(ciphertext_trans[i], IP)
        # print('ip_initial=',ip_initial)
        fk2_result = fk(ip_initial[:4], ip_initial[4:], subkeys[1])
        sw_result = p(fk2_result, SW)
        # print("sw_result=",sw_result)
        fk1_result = fk(sw_result[:4], sw_result[4:], subkeys[0])
        ip_final = p(fk1_result, IP_INV)
        result.append(ip_final)
    # print("解密为:",result)
        
    result = result if is_bin_string(ciphertext) else bin_to_ascii(result)
    # print("转换后解密为:",result)
    # 若输入密文为ascii码，则返回也为ascii码
    return result


# 暴力破解
def brute_force_decrypt(plaintext, ciphertext):
    # 密钥初始为空列表
    key = []
    # 将输入密文转为list
    ciphertext = ciphertext.split('789')
    for i in range(0, 1024):
        kk = i
        kk = bin(kk)[2:].zfill(10)
        cipher = C(plaintext, kk)
        if cipher == ciphertext:
            key.append(i)
        else:
            continue
    # 返回密钥列表所有可能的密钥
    return key


if __name__ == '__main__':

    key = '1101001001'
    plaintext = 'hello'
    ciphertext = '¥[ÄÄ^'

    # C(plaintext,key)
    # P(ciphertext,key)
