"""
This following demonstrates a Noise_NNpsk0+psk2_25519_ChaChaPoly_BLAKE2s handshake and initial transport messages.
"""
from noise.processing.impl.handshakestate import HandshakeState
from noise.processing.impl.symmetricstate import SymmetricState
from noise.processing.impl.cipherstate import CipherState
from noise.processing.handshakepatterns.interactive.NN import NNHandshakePattern
from noise.processing.modifiers.psk import PSKPatternModifier
from noise.cipher.chachapoly import ChaChaPolyCipher
from noise.dh.x25519.x25519 import X25519DH
from noise.hash.blake2s import Blake2sHash
import noise, logging
import os

if __name__ == "__main__":
    noise.logger.setLevel(logging.DEBUG)
    # setup initiator and responder variables
    alice_s = X25519DH().generate_keypair()
    bob_s = X25519DH().generate_keypair()
    psks = (
        os.urandom(32),
        os.urandom(32)
    )

    # prepare handshakestate objects for initiator and responder
    alice_handshakestate = HandshakeState(
        SymmetricState(
            CipherState(
                ChaChaPolyCipher()
            ),
            Blake2sHash()
        ),
        X25519DH()
    )
    bob_handshakestate = HandshakeState(
        SymmetricState(
            CipherState(
                ChaChaPolyCipher()
            ),
            Blake2sHash()
        ),
        X25519DH()
    )
    # modify NNHandshakePattern
    nn_psk0_pattern = PSKPatternModifier(0).modify(NNHandshakePattern())
    nn_psk0_psk2_pattern = PSKPatternModifier(2).modify(nn_psk0_pattern)
    # initialize handshakestate objects
    alice_handshakestate.initialize(nn_psk0_psk2_pattern, True, b'prologue', s=alice_s, psks=psks)
    bob_handshakestate.initialize(nn_psk0_psk2_pattern, False, b'prologue', s=bob_s, psks=psks)

    # -> psk, e
    message_buffer = bytearray()
    alice_handshakestate.write_message(b'', message_buffer)
    bob_handshakestate.read_message(bytes(message_buffer), bytearray())

    # <- e, ee, psk
    message_buffer = bytearray()
    alice_cipherstates = bob_handshakestate.write_message(b'', message_buffer)
    bob_cipherstates = alice_handshakestate.read_message(bytes(message_buffer), bytearray())

    # transport phase
    # alice to bob
    ciphertext = alice_cipherstates[0].encrypt_with_ad(b'', b'Hello')
    plaintext = bob_cipherstates[0].decrypt_with_ad(b'', ciphertext)
    assert plaintext == b'Hello'

    # bob to alice
    ciphertext = bob_cipherstates[1].encrypt_with_ad(b'', b'World')
    plaintext = alice_cipherstates[1].decrypt_with_ad(b'', ciphertext)
    assert plaintext == b'World'
