# Define.py
# Constants

UI_PATH = "DVSpacketanalyzer.ui"

TYPE_COLUMN = 1
TYPE_TIMESTAMP = 2
TYPE_FRAME_END = 3
TYPE_GROUP = 32

MAX_COLS = 960

APP_QSS = """
    QWidget {
        background-color: #FFFFFF;
        color: #222222;
        font-size: 12px;
    }

    QGroupBox {
        border: 1px solid #DADADA;
        border-radius: 6px;
        margin-top: 12px;
        font-weight: bold;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 6px;
        color: #444444;
    }

    QLineEdit {
        border: 1px solid #CCCCCC;
        border-radius: 4px;
        padding: 4px 6px;
        background-color: #FFFFFF;
    }

    QPushButton:hover {
        background-color: #F0F0F0;
    }

    QPushButton:pressed {
        background-color: #E0E0E0;
    }

    QPushButton:disabled {
        color: #9A9A9A;
        background-color: #F0F0F0;
        border: 2px solid #B5B5B5;
    }
                           
    QTextBrowser {
        border: 1px solid #DADADA;
        border-radius: 6px;
        background-color: #FAFAFA;
        font-family: Consolas, monospace;
        font-size: 11px;
    }

    QProgressBar {
        border: 1px solid #DADADA;
        border-radius: 5px;
        text-align: center;
    }

    QProgressBar::chunk {
        background-color: #3A7AFE;
        border-radius: 5px;
    }
    """