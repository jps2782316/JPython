#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'Michael Liao'

#第1行和第2行是标准注释，第1行注释可以让这个hello.py文件直接在Unix/Linux/Mac上运行，第2行注释表示.py文件本身使用标准UTF-8编码；
#第4行是一个字符串，表示模块的文档注释，任何模块代码的第一个字符串都被视为模块的文档注释；
#第6行使用__author__变量把作者写进去，这样当你公开源代码后别人就可以瞻仰你的大名；

#以上就是Python模块的标准文件模板，当然也可以全部删掉不写，但是，按标准办事肯定没错。


print('hello, world')

#s = ' hello'
#s = [' ', 'h', 'e', 'l', 'l', 'o']
#注意: 字符串 s[:1] 得到的是一个字符' '。列表[:1]得到的是一个列表 [' ']。注意区别。

def trim(s):
  if s[:1] == ' ':
  #递归的时候，记得一定要写return啊，不要只写最后一个return s。
  #靠，就说怎么一直测试失败，明明逻辑没问题。用变量存了打印出来才发现，为None。在这里卡了两三个小时。
    return trim(s[1:])
  elif s[-1:] == ' ':
    return trim(s[:-1])
  else:
    print('----', s, '----')
    return s
    
    
def trim2(s):
    if s[0] == ' ':
        return trim2(s[1:])
    elif s[-1] == ' ':
        return trim2(s[:-1])
    else:
        return s
        

def testTrim():
    # test:
    if trim('hello  ') != 'hello':
        print('测试失败1')
    elif trim('  hello') != 'hello':
        print('测试失败2')
    elif trim('  hello  ') != 'hello':
        print('测试失败3')
    elif trim('  hello  world  ') != 'hello  world':
        print('测试失败4')
    elif trim('') != '':
        print('测试失败5')
    elif trim('    ') != '':
        print('测试失败6')
    else:
        print('测试成功!')
