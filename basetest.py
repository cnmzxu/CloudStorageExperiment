import base

ES = base.EncSch(4)
c = ES.Enc(b"aaaa", b"asdfghjkl")
print(c)
p = ES.Dec(b"aaaa", c)
print(p)
p_ = ES.Dec(b"bbbb", c)
print(p_)