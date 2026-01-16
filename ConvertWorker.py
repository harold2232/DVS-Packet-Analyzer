# ConvertWorker.py

from pathlib import Path

from PyQt5.QtCore import QThread, pyqtSignal

from hex_convert import extract_hex_bytes_from_text, bytes_to_bin_lines

class ConvertWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str, str)
    error = pyqtSignal(str)

    def __init__(self, in_path: str):
        super().__init__()
        self.in_path = in_path

    def run(self):
        try:
            in_file = Path(self.in_path)
            if not in_file.exists():
                self.error.emit("Input file not found.")
                return

            total_size = in_file.stat().st_size
            if total_size <= 0:
                self.error.emit("Input file is empty.")
                return

            collected = []
            with in_file.open("r", encoding="utf-8", errors="ignore") as f:
                while True:
                    line = f.readline()
                    if not line:
                        break

                    collected.extend(extract_hex_bytes_from_text(line))

                    pct = int((f.tell() / total_size) * 100)
                    self.progress.emit(max(0, min(100, pct)))

            if not collected:
                self.error.emit("No valid 2-digit HEX tokens found.")
                return

            bin_lines = bytes_to_bin_lines(collected, bits_per_line=32)
            bin_text = "\n".join(bin_lines)

            suggested_filename = in_file.with_suffix(".bin.txt").name
            self.progress.emit(100)
            self.finished.emit(suggested_filename, bin_text)

        except Exception as e:
            self.error.emit(f"Convert error: {e}")
