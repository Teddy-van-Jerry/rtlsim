import rtlsim
import numpy as np

Q_u_6_2 = rtlsim.Quantize(False, 6, 2)
print(Q_u_6_2.info(verbose=True))
a = np.array([1.23, -1.2, 34.1, 0, 3.26, 1, -2.34])
print(f'\noriginal array:  {a}')
print(f'as bits string:  {Q_u_6_2.asBits(a)}')
print(f'quantized array: {Q_u_6_2.q(a)}')
print(f'quantized wrap:  {rtlsim.quantize(a, False, 6, 2, overflow="saturate")}')
