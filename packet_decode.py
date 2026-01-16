from Define import (
    TYPE_COLUMN,
    TYPE_TIMESTAMP,
    TYPE_FRAME_END,
    TYPE_GROUP,
)

def packet_type(word: int) -> int:
    return (word >> 26) & 0x3F

def decode_word_to_lines(word: int) -> list:
    t = packet_type(word)
    out = []

    if t == TYPE_COLUMN:
        frame = (word >> 11) & 0xFF
        col = word & 0x7FF
        out.append(f"Column packet : ( Frame number : {frame}, Column address : {col} )")
        return out

    if t == TYPE_GROUP:
        group = (word >> 18) & 0x7F
        off = (word >> 8) & 0xFF
        on = word & 0xFF
        out.append(f"Event group : ( Group address : {group} , OFF : {off} , ON : {on} )")
        return out

    if t == TYPE_FRAME_END:
        frame = (word >> 11) & 0xFF
        out.append(f"Frame end packet : ( Frame number : {frame} )")
        return out

    if t == TYPE_TIMESTAMP:
        is_sub = (word >> 23) & 0x1
        if is_sub == 0:
            ref = word & 0x3FFFFF
            out.append(f"RefTs : {ref}")
        else:
            sub = word & 0x3FF
            out.append(f"SubTs : {sub}")
        return out

    out.append(f"UNKNOWN(type={t}) : 0x{word:08X}")
    return out