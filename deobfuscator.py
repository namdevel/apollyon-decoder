'''
Deobfuscate python code obfuscated by Apollyon (https://github.com/billythegoat356/Apollyon)
Author : namdevel (https://github.com/namdevel/)
'''

import codecs
import importlib
import os
import re
import sys

sys.dont_write_bytecode = True

strings = "abcdefghijklmnopqrstuvwxyz0123456789"
file_name = "src/_run.py"

def disX():
    generatePyc()
    dis = os.popen(f'disx {file_name[:-3]}.pyc && disx {file_name[:-3]}.pyc > disx.log')
    byte = re.search("4: '((.+?))'", dis.read()).group(1)
    dis.close()
    
    data = codecs.decode(byte, "unicode-escape").encode('latin1').decode('utf-8')
    deob = decrypt(data)
    os.unlink("src/_run.pyc")
    os.unlink("tmp.py")
    
    with open("file_deobfuscated.py", "w") as file:
        file.write(deob)
    # Show real code in terminal
    print(deob) 
    
def generatePyc():
    with open(file_name) as file:
        code = "disX=" + file.read()[4:]
        
    with open("tmp.py", "w") as file:
        file.write(code)
    
    from tmp import disX as codeObject

    l = importlib.machinery.SourceFileLoader('<py_compile>', file_name)
    sb = l.get_data(file_name)
    sh = importlib.util.source_hash(sb)
    bytecode = importlib._bootstrap_external._code_to_hash_pyc(codeObject, sh)

    with open(file_name[:-3] + ".pyc", "wb") as file:
        file.write(bytecode)
    
def decrypt(text: str, key: str = 49348):
    t = [chr(ord(t)-key) if t != "ζ" else "\n" for t in text]
    ts = "".join(t)
    r = ""
    for a in ts:
        if a in strings:
            i = strings.index(a)+1
            if i >= len(strings):
                i = 0
            a = strings[i]
        r += a
    return r

if __name__ == "__main__":
    disX()