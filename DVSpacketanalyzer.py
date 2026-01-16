import sys
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from ConvertWorker import ConvertWorker
from AnalyzeWorker import AnalyzeWorker
from Define import UI_PATH, APP_QSS

form_class = uic.loadUiType(UI_PATH)[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon("app.ico"))

        self.setStyleSheet(APP_QSS)

        self.selected_hex_path = ""
        self.converted_text = ""
        self.suggested_filename = ""
        self.worker = None

        self.selected_bin_path = ""
        self.analysis_text = ""
        self.suggested_analyzed_name = ""
        self.analyze_worker = None

        self.Btn_selectHex.clicked.connect(self.Btn_selectHexFunction)
        self.Btn_Convert.clicked.connect(self.Btn_ConvertFunction)
        self.Btn_Download.clicked.connect(self.Btn_DownloadFunction)

        self.Btn_selectBin.clicked.connect(self.Btn_selectBinFunction)
        self.Btn_Analyze.clicked.connect(self.Btn_AnalyzeFunction)
        self.Btn_Download_analyzer.clicked.connect(self.Btn_Download_analyzerFunction)

        self.progressBar.setValue(0)
        self.lineEdit_result.setText("")
        self.Btn_Download.setEnabled(False)
        self.lineEdit_InputBin.setText("")
        self.lineEdit_result_analyzer.setText("")
        self.textBrowser_Analyzer.clear()
        self.Btn_Download_analyzer.setEnabled(False)

    def Btn_selectHexFunction(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select HEX File",
            "",
            "Hex Files (*.txt *.hex);;All Files (*.*)"
        )
        if not path:
            return

        self.selected_hex_path = path
        self.lineEdit_hex.setText(path)

        self.converted_text = ""
        self.suggested_filename = ""
        self.lineEdit_result.setText("")
        self.progressBar.setValue(0)
        self.Btn_Download.setEnabled(False)

    def Btn_ConvertFunction(self):
        if not self.selected_hex_path:
            QMessageBox.warning(self, "Notice", "Please select a HEX file first.")
            return

        self.progressBar.setValue(0)
        self.lineEdit_result.setText("Converting...")
        self.Btn_Download.setEnabled(False)

        self.worker = ConvertWorker(self.selected_hex_path)
        self.worker.progress.connect(self.progressBar.setValue)
        self.worker.finished.connect(self._on_convert_finished)
        self.worker.error.connect(self._on_convert_error)
        self.worker.start()

    def _on_convert_finished(self, suggested_filename: str, bin_text: str):
        self.suggested_filename = suggested_filename
        self.converted_text = bin_text

        self.lineEdit_result.setText(self.suggested_filename)
        QMessageBox.information(self, "Done", "Convert Complete!")

        self.Btn_Download.setEnabled(True)

    def _on_convert_error(self, msg: str):
        self.converted_text = ""
        self.suggested_filename = ""
        self.lineEdit_result.setText("")
        self.Btn_Download.setEnabled(False)
        QMessageBox.critical(self, "Error", msg)

    def Btn_DownloadFunction(self):
        if not self.converted_text:
            QMessageBox.warning(self, "Notice", "Run Convert first, then click Download.")
            return

        default_name = self.suggested_filename or "output.bin.txt"
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Converted File",
            default_name,
            "Text Files (*.txt);;All Files (*.*)"
        )
        if not save_path:
            return

        try:
            Path(save_path).write_text(self.converted_text, encoding="utf-8")
            QMessageBox.information(self, "Done", f"Saved:\n{save_path}")
            self.progressBar.setValue(0)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Save failed: {e}")

    def Btn_selectBinFunction(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select BIN File",
            "",
            "BIN Text Files (*.txt *.bin);;All Files (*.*)"
        )
        if not path:
            return

        self.selected_bin_path = path
        self.lineEdit_InputBin.setText(path)

        self.analysis_text = ""
        self.suggested_analyzed_name = ""
        self.lineEdit_result_analyzer.setText("")
        self.textBrowser_Analyzer.clear()
        self.progressBar.setValue(0)
        self.Btn_Download_analyzer.setEnabled(False)

    def Btn_AnalyzeFunction(self):
        if not self.selected_bin_path:
            QMessageBox.warning(self, "Notice", "Please select a BIN file first.")
            return

        self.progressBar.setValue(0)
        self.textBrowser_Analyzer.clear()
        self.lineEdit_result_analyzer.setText("Analyzing...")
        self.Btn_Download_analyzer.setEnabled(False)

        self.analyze_worker = AnalyzeWorker(self.selected_bin_path)
        self.analyze_worker.progress.connect(self.progressBar.setValue)
        self.analyze_worker.finished.connect(self._on_analyze_finished)
        self.analyze_worker.error.connect(self._on_analyze_error)
        self.analyze_worker.start()

    def _on_analyze_finished(self, suggested_filename: str, detail_text: str, summary_text: str):
        self.suggested_analyzed_name = suggested_filename
        self.analysis_text = detail_text

        self.lineEdit_result_analyzer.setText(self.suggested_analyzed_name)

        self.textBrowser_Analyzer.setPlainText(summary_text)
        QMessageBox.information(self, "Done", "Analyze Complete!")

        self.Btn_Download_analyzer.setEnabled(True)

    def _on_analyze_error(self, msg: str):
        self.analysis_text = ""
        self.suggested_analyzed_name = ""
        self.lineEdit_result_analyzer.setText("")
        self.Btn_Download_analyzer.setEnabled(False)
        QMessageBox.critical(self, "Error", msg)

    def Btn_Download_analyzerFunction(self):
        if not self.analysis_text:
            QMessageBox.warning(self, "Notice", "Run Analyze first, then click Download.")
            return

        default_name = self.suggested_analyzed_name or "analysis.txt"
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Analysis Result",
            default_name,
            "Text Files (*.txt);;All Files (*.*)"
        )
        if not save_path:
            return

        try:
            Path(save_path).write_text(self.analysis_text, encoding="utf-8")
            QMessageBox.information(self, "Done", f"Saved:\n{save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Saved failed: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
