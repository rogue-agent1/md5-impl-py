"""MD5 — message digest from scratch."""
import struct, math

def md5(message):
    if isinstance(message, str): message = message.encode()
    def left_rotate(x, n): return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF
    s = [7,12,17,22]*4 + [5,9,14,20]*4 + [4,11,16,23]*4 + [6,10,15,21]*4
    K = [int(abs(math.sin(i+1)) * 2**32) & 0xFFFFFFFF for i in range(64)]
    a0,b0,c0,d0 = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476
    msg = bytearray(message)
    orig_len = len(msg) * 8
    msg.append(0x80)
    while len(msg) % 64 != 56: msg.append(0)
    msg += struct.pack('<Q', orig_len)
    for i in range(0, len(msg), 64):
        M = struct.unpack('<16I', msg[i:i+64])
        A, B, C, D = a0, b0, c0, d0
        for j in range(64):
            if j < 16: F = (B & C) | (~B & D); g = j
            elif j < 32: F = (D & B) | (~D & C); g = (5*j+1) % 16
            elif j < 48: F = B ^ C ^ D; g = (3*j+5) % 16
            else: F = C ^ (B | ~D); g = (7*j) % 16
            F = (F + A + K[j] + M[g]) & 0xFFFFFFFF
            A, D, C, B = D, C, B, (B + left_rotate(F, s[j])) & 0xFFFFFFFF
        a0 = (a0+A) & 0xFFFFFFFF; b0 = (b0+B) & 0xFFFFFFFF
        c0 = (c0+C) & 0xFFFFFFFF; d0 = (d0+D) & 0xFFFFFFFF
    return struct.pack('<4I', a0, b0, c0, d0).hex()

if __name__ == "__main__":
    import hashlib
    tests = ["", "hello", "The quick brown fox jumps over the lazy dog"]
    for t in tests:
        mine = md5(t)
        ref = hashlib.md5(t.encode()).hexdigest()
        match = "✅" if mine == ref else "❌"
        print(f"{match} md5({t[:30]!r}) = {mine}")
        assert mine == ref
    print("All tests passed!")
