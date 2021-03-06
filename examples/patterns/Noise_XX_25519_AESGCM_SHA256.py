"""
This following demonstrates a Noise_XX_25519_AESGCM_SHA256 handshake and initial transport messages.
"""
from noise.processing.impl.handshakestate import HandshakeState
from noise.processing.impl.symmetricstate import SymmetricState
from noise.processing.impl.cipherstate import CipherState
from noise.processing.handshakepatterns.interactive.XX import XXHandshakePattern
from noise.cipher.aesgcm import AESGCMCipher
from noise.dh.x25519.x25519 import X25519DH
from noise.hash.sha256 import SHA256Hash
import noise, logging


if __name__ == "__main__":
    noise.logger.setLevel(logging.DEBUG)
    # setup initiator and responder variables
    alice_s = X25519DH().generate_keypair()
    bob_s = X25519DH().generate_keypair()

    # prepare handshakestate objects for initiator and responder
    alice_handshakestate = HandshakeState(
        SymmetricState(
            CipherState(
                AESGCMCipher()
            ),
            SHA256Hash()
        ),
        X25519DH()
    )
    bob_handshakestate = HandshakeState(
        SymmetricState(
            CipherState(
                AESGCMCipher()
            ),
            SHA256Hash()
        ),
        X25519DH()
    )
    # initialize handshakestate objects
    alice_handshakestate.initialize(XXHandshakePattern(), True, b'', s=alice_s)
    bob_handshakestate.initialize(XXHandshakePattern(), False, b'', s=bob_s)

    # -> e
    message_buffer = bytearray()
    alice_handshakestate.write_message(b'', message_buffer)
    bob_handshakestate.read_message(bytes(message_buffer), bytearray())

    # <- e, ee, s, es
    message_buffer = bytearray()
    bob_handshakestate.write_message(b'', message_buffer)
    alice_handshakestate.read_message(bytes(message_buffer), bytearray())

    # -> s, se
    message_buffer = bytearray()
    alice_cipherstates = alice_handshakestate.write_message(b'', message_buffer)
    bob_cipherstates = bob_handshakestate.read_message(bytes(message_buffer), bytearray())

    # transport phase
    # alice to bob
    ciphertext = alice_cipherstates[0].encrypt_with_ad(b'', b'Hello')
    plaintext = bob_cipherstates[0].decrypt_with_ad(b'', ciphertext)
    assert plaintext == b'Hello'

    # bob to alice
    ciphertext = bob_cipherstates[1].encrypt_with_ad(b'', b'World')
    plaintext = alice_cipherstates[1].decrypt_with_ad(b'', ciphertext)
    assert plaintext == b'World'
