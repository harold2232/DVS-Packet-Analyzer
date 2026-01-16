import re

def extract_hex_bytes_from_text(text: str):
    return re.findall(r'\b[0-9A-Fa-f]{2}\b', text)

def bytes_to_bin_lines(hex_bytes, bits_per_line=32):
    bit_str = "".join(f"{int(b, 16):08b}" for b in hex_bytes)

    lines = []
    for i in range(0, len(bit_str), bits_per_line):
        chunk = bit_str[i:i + bits_per_line]
        chunk_grouped = " ".join(chunk[j:j + 4] for j in range(0, len(chunk), 4))
        lines.append(chunk_grouped)
    return lines

def parse_bin_line_to_word(line: str):
    bits = line.strip().replace(" ", "")
    if not bits:
        return None
    if any(c not in "01" for c in bits):
        return None
    if len(bits) != 32:
        return None
    return int(bits, 2)