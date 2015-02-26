import random
from curve import curve
from convert import little_endian

class curve25519:
    def curve25519(self, n, q):
        """
        `n` is the private key. It is at least 2**254 and a multiple 
        of 8. It is the scalar which with we want to multiply.
        `q` is the x of point Q. The point Q is the point we want to
        multiply. `q` is an element of the field over `p`.
        Returns `s`, which is the x of `n` * `Q`
        """

        assert len(n) == 32
        assert len(q) == 32

        n = little_endian().from_string(n)
        assert n >= pow(2, 254)
        assert n % 8 == 0

        q = little_endian().from_string(q)

        curve25519 = curve(486662, pow(2, 255) - 19)
        (Q0, Q1) = curve25519.points(q)
        nQ = curve25519.multiply(Q0, n)
        assert nQ[0] == curve25519.multiply(Q1, n)[0]

        s = nQ[0]
        return little_endian().to_string(s)

    def create_secret_key_num(self):
        return pow(2, 254) + 8 * random.SystemRandom().randint(0, pow(2, 251) -1)

    def create_secret_key_str(self):
        return little_endian().to_string(self.create_secret_key_num())


if __name__ == "__main__":
    nine = "\x09" + 31 * "\0"

    c = curve25519()
    alices_secret = c.create_secret_key_str()
    alices_public = c.curve25519(alices_secret, nine)

    bobs_secret = c.create_secret_key_str()
    bobs_public = c.curve25519(bobs_secret, nine)

    alices_shared = c.curve25519(alices_secret, bobs_public)
    bobs_shared = c.curve25519(bobs_secret, alices_public)

    assert alices_shared == bobs_shared
