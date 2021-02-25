
print('hello, world')

def myAbs(x):
    print('abs')
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    
    if x >= 0:
        return x
    else:
        return -x


a1=(-b+math.sqrt(b*b-4*a*c))/(2*a)
a2=(-b-math.sqrt(b*b-4*a*c))/(2*a)
return a1, a2


s[0]要换成是s[:1]

s[-1]要换成s[-1:]
def trim(s):
if s[0] == ' ':
    return trim(s[1:])
elif s[-1] == ' ':
    return trim(s[:-1])
else:
    return s



def trim(s):
while s == None:
    return '测试失败'
while ' ' == s[:1]:
    s= s[1:]
while ' '== s[-1:]:
    s= s[:-1]
return s


当s = ' '时,字符串只有一个元素，索引值为0，调用函数在执行第一个if语句的时候，返回值取得是索引为1之后的元素，超出了s的索引范围
