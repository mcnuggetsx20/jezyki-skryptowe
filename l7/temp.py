import z2
import z4_5


gen1 = z4_5.make_generator(lambda n: 2*n)
res = z2.forall(lambda x: x < 15, gen1(5))
print(res)
