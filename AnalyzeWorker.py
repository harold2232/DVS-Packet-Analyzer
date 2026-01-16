# AnalyzeWorker.py
from pathlib import Path

from PyQt5.QtCore import QThread, pyqtSignal

from Define import (
    TYPE_COLUMN,
    TYPE_TIMESTAMP,
    TYPE_FRAME_END,
    MAX_COLS,
)

from hex_convert import parse_bin_line_to_word
from packet_decode import packet_type, decode_word_to_lines

class AnalyzeWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str, str, str)
    error = pyqtSignal(str)

    def __init__(self, in_bin_path: str):
        super().__init__()
        self.in_bin_path = in_bin_path

    def run(self):
        try:
            in_file = Path(self.in_bin_path)
            if not in_file.exists():
                self.error.emit("BIN file not found.")
                return

            total_size = in_file.stat().st_size
            if total_size <= 0:
                self.error.emit("BIN file is empty.")
                return

            detail_lines = []
            summary_lines = []

            current_ref = None
            current_sub = None

            current_frame = None
            current_cols_set = set()

            with in_file.open("r", encoding="utf-8", errors="ignore") as f:
                while True:
                    line = f.readline()
                    if not line:
                        break

                    word = parse_bin_line_to_word(line)
                    if word is None:
                        pass
                    else:
                        detail_lines.extend(decode_word_to_lines(word))

                        t = packet_type(word)

                        if t == TYPE_TIMESTAMP:
                            is_sub = (word >> 23) & 0x1
                            if is_sub == 0:
                                current_ref = word & 0x3FFFFF
                            else:
                                current_sub = word & 0x3FF

                        elif t == TYPE_COLUMN:
                            frame = (word >> 11) & 0xFF
                            col = word & 0x7FF

                            if col >= MAX_COLS:
                                pass
                            else :
                                if current_frame is None:
                                    current_frame = frame

                                if frame != current_frame:
                                    pass
                                else :
                                    current_cols_set.add(col)

                        elif t == TYPE_FRAME_END:
                            frame_end = (word >> 11) & 0xFF

                            if current_frame is None:
                                continue

                            if frame_end != current_frame:
                                continue

                            cnt = len(current_cols_set)

                            summary_lines.append(f"Frame {current_frame} : columns = {cnt}")
                            summary_lines.append(f"RefTs : {current_ref if current_ref is not None else 'N/A'}")
                            summary_lines.append(f"SubTs : {current_sub if current_sub is not None else 'N/A'}")

                            current_cols_set.clear()
                            current_frame = None

                    pct = int((f.tell() / total_size) * 100)
                    self.progress.emit(max(0, min(100, pct)))

            detail_text = "\n".join(detail_lines)
            summary_text = "\n".join(summary_lines)
            suggested = in_file.with_suffix(".analyzed.txt").name

            self.progress.emit(100)
            self.finished.emit(suggested, detail_text, summary_text)

        except Exception as e:
            self.error.emit(f"Analyze Error: {e}")
