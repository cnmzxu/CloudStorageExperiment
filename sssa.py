import math
import random

import myerror
import translation

#2070 bits
PRIME1 = 112670236818672966462084349700290165356550375016925655364575996640577617897965098435948875592100066953832688448996119599700666698262273919269856852666432075410433025951703705205848224870757789325697033887299273663579207176475459083690834126398808269735152235954547562811538953075818917877314692531204767090875627381141377939140948640019182251221510629300918298062330264740103499925047316745310416424590584018399789081069785433067281125970339861510610269648600034007200610157667961575574586287958319242799890116326483448136646576001126690164760675657757728822136063559131947918389358404286379872283714170427234420085946330343
#1050 bits
PRIME2 = 7585358808511087815129894771036576423580204840699572218434791514925610705355836741544871565382844851692835024301121260127960156319421645848440957049808373883323734063203919445655150225035853759224972799016547420701950791101797030369207189272011763142251734642928713290690734486757817504046731438817416117426541577481
#535 bits
PRIME3 = 60161877336477840013993538172634380014092641908844646558968803515802693328585626031760680092315634311833585646797885751794848458398258714780442836257796364239969

def inverse(a, b):
    exp = b - 2
    w = a
    ans = 1
    while exp > 0:
        if exp & 1 == 1:
            ans = (ans * w) % b
        w = (w ** 2) % b
        exp = exp >> 1
    return ans


class sssa:
    def __init__(self, th, n, PRIME): #threshlod = th, bits length = n
        self.th = th
        self.P = PRIME
        self.n = n
        self.m = math.ceil(n / th)

    def __inverse__(self, a):
        return inverse(a, self.P)

    def share(self, secret):#secret: n bits
        if len(secret) != self.n:
            raise myerror.myerror("Byteslength_Not_Match")

        secret = secret[::-1]
        x = random.randint((1 << self.m) + 1, self.P - 1)
        ans = 0
        for i in range(self.th):
            ans = (ans * x + int(secret[(self.th - i - 1) * self.m :(self.th - i) * self.m][::-1].zfill(1),2)) % self.P
        return (x, ans)

    def recovery(self, shares):
        if (len(shares) != self.th):
            raise myerror.myerror("Error_With_Shares_Number")
        
        secret = 0
        for i in range(self.th):
            w = shares[i][1]
            xi = shares[i][0]
            for j in range(self.th):
                if (j == i):
                    continue
                xj = shares[j][0]
                if xj == xi:
                    raise myerror.myerror("Shares_Equal_Error")
                w = ((((xj - 2 ** self.m) * self.__inverse__(xj - xi)) % self.P) * w) % self.P
            secret = (secret + w) % self.P
        return bin(secret)[2:].zfill(self.n)

def test():
    ss = sssa(10, 2048, PRIME1)
    t = random.randint(0, 2 ** 2047 - 1)
    t = bin(t)[2:]#.zfill(2048)
    print(t)
    shs = [ss.share(t) for i in range(10)]
    r = ss.recovery(shs)
    print(r)
    print(len(t))
    print(len(r))
    print(r == t.zfill(2048))

#test()