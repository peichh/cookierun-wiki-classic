import struct
import zlib
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

V2_KEY = bytes.fromhex(
    "e8911c7a40bc1f6059a1d910538543bc"
    "5df44840cc684d5f1493a3f6daf0fe1e"
)
V2_IV_MUL = bytes.fromhex("2a790622e6fef51e5cca503eca4d5c40")

def fastlz_decompress(data, maxout):
    ip = 0
    out = bytearray()
    if not data: return bytes()
    level = (data[0] >> 5) + 1
    ctrl = data[ip] & 31
    ip += 1
    while ip < len(data):
        if ctrl < 32:
            length = ctrl + 1
            out += data[ip : ip + length]
            ip += length
        else:
            length = (ctrl >> 5) - 1
            ref = len(out) - ((ctrl & 0x1F) << 8) - 1
            if length == 6:
                while True:
                    code = data[ip]
                    ip += 1
                    length += code
                    if level != 2 or code != 255:
                        break
            code = data[ip]
            ip += 1
            ref -= code
            length += 3
            if level == 2 and code == 255 and (ctrl & 0x1F) == 31:
                distance = (data[ip] << 8) + data[ip + 1]
                ip += 2
                ref = len(out) - distance - 8191 - 1
            if ref < 0: break
            for _ in range(length):
                out.append(out[ref])
                ref += 1
        if ip >= len(data): break
        ctrl = data[ip]
        ip += 1
    return bytes(out)

def decrypt_crm2(path):
    b = Path(path).read_bytes()
    if len(b) < 0x45: return None
    
    checksum = struct.unpack_from("<I", b, 8)[0]
    out_size = struct.unpack_from("<I", b, 12)[0]
    checksum_bytes = checksum.to_bytes(4, "little")
    
    suffix_len = b[0x44]
    payload_len = len(b) - 0x45
    enc = b[0x45:] + b[0x35 : 0x35 + suffix_len]
    
    if len(enc) % 16 != 0:
        print(f"Encrypted block size {len(enc)} not multiple of 16")
        return None

    iv = bytes((checksum_bytes[0] * x) & 0xFF for x in V2_IV_MUL)
    
    # Try different AES modes from djbf_v2_probe
    for mode_name, mode in [("cbc", modes.CBC(iv)), ("cfb", modes.CFB(iv)), ("ctr", modes.CTR(iv))]:
        dec = Cipher(algorithms.AES(V2_KEY), mode).decryptor()
        decrypted = dec.update(enc) + dec.finalize()
        compressed = decrypted[:payload_len]
        
        try:
            plain = fastlz_decompress(compressed, out_size)
            if len(plain) > 0:
                # Check for printable or expected markers
                printable = sum(32 <= c < 127 for c in plain[:100])
                if printable > 50 or b"{" in plain or b"[" in plain:
                    print(f"Hit with {mode_name}!")
                    return plain
        except:
            continue
    return None

path = "/Users/peach/Documents/cookierun file/extracted/apk/base/assets/kakaoBC_BalanceData/MapData_BR_001.crm2"
result = decrypt_crm2(path)
if result:
    print(f"Decrypted Size: {len(result)}")
    print("Preview (ASCII):", ''.join(chr(b) if 32 <= b <= 126 else '.' for b in result[:200]))
    # Save for inspection
    with open("MapData_BR_001_decrypted.bin", "wb") as f:
        f.write(result)
else:
    print("Decryption failed.")
