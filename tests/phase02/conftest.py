import importlib.util
import sys
import types
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MAIN_MODULE_PATH = PROJECT_ROOT / "main.pyw"


class DummySignal:
    def __init__(self, *_args, **_kwargs):
        self._callbacks = []

    def connect(self, callback):
        self._callbacks.append(callback)

    def emit(self, *args, **kwargs):
        for callback in list(self._callbacks):
            callback(*args, **kwargs)


def _stub_windows_modules():
    if "winshell" not in sys.modules:
        sys.modules["winshell"] = types.SimpleNamespace(
            startup=lambda common=False: str(PROJECT_ROOT),
            CreateShortcut=lambda **_kwargs: None,
        )

    if "win32com" not in sys.modules:
        win32com = types.ModuleType("win32com")
        client = types.ModuleType("win32com.client")
        client.Dispatch = lambda *_args, **_kwargs: None
        win32com.client = client
        sys.modules["win32com"] = win32com
        sys.modules["win32com.client"] = client


def _stub_qt_modules():
    qtgui = types.ModuleType("PySide6.QtGui")
    qtwidgets = types.ModuleType("PySide6.QtWidgets")
    qtcore = types.ModuleType("PySide6.QtCore")

    class QObject:
        pass

    class QRunnable:
        def __init__(self, *args, **kwargs):
            pass

    class QApplication:
        def __init__(self, *_args, **_kwargs):
            pass

        @staticmethod
        def instance():
            return None

    class QMainWindow:
        def __init__(self, *_args, **_kwargs):
            pass

        def close(self):
            pass

    class QDialog:
        def __init__(self, *_args, **_kwargs):
            pass

        def exec(self):
            pass

    class QSystemTrayIcon:
        def __init__(self, *_args, **_kwargs):
            self.messages = []

        def setIcon(self, *_args, **_kwargs):
            pass

        def setVisible(self, *_args, **_kwargs):
            pass

        def setToolTip(self, *_args, **_kwargs):
            pass

        def setContextMenu(self, *_args, **_kwargs):
            pass

        def showMessage(self, title, message):
            self.messages.append((title, message))

    class QMenu:
        def addAction(self, *_args, **_kwargs):
            pass

    class QAction:
        def __init__(self, *_args, **_kwargs):
            self.triggered = DummySignal()

    class QStyle:
        pass

    class QMessageBox:
        @staticmethod
        def critical(*_args, **_kwargs):
            return None

    class QIcon:
        def __init__(self, *_args, **_kwargs):
            pass

    class QThreadPool:
        def start(self, *_args, **_kwargs):
            pass

    class QTimer:
        def __init__(self):
            self.timeout = DummySignal()

        def setInterval(self, *_args, **_kwargs):
            pass

        def start(self):
            pass

        def stop(self):
            pass

    def Slot(*_args, **_kwargs):
        def decorator(func):
            return func

        return decorator

    qtgui.QIcon = QIcon
    qtgui.QAction = QAction
    qtwidgets.QApplication = QApplication
    qtwidgets.QMainWindow = QMainWindow
    qtwidgets.QDialog = QDialog
    qtwidgets.QSystemTrayIcon = QSystemTrayIcon
    qtwidgets.QMenu = QMenu
    qtwidgets.QStyle = QStyle
    qtwidgets.QMessageBox = QMessageBox
    qtcore.QRunnable = QRunnable
    qtcore.Signal = DummySignal
    qtcore.QObject = QObject
    qtcore.QThreadPool = QThreadPool
    qtcore.Slot = Slot
    qtcore.QTimer = QTimer

    pyside6 = types.ModuleType("PySide6")
    pyside6.QtGui = qtgui
    pyside6.QtWidgets = qtwidgets
    pyside6.QtCore = qtcore

    sys.modules["PySide6"] = pyside6
    sys.modules["PySide6.QtGui"] = qtgui
    sys.modules["PySide6.QtWidgets"] = qtwidgets
    sys.modules["PySide6.QtCore"] = qtcore


def _stub_project_modules():
    mainwindow = types.ModuleType("mainwindow")
    unilogindialog = types.ModuleType("unilogindialog")
    setupmanager = types.ModuleType("setupmanager")
    outlookmanager = types.ModuleType("outlookmanager")
    aula = types.ModuleType("aula")
    calendar_comparer = types.ModuleType("calendar_comparer")

    class Ui_MainWindow:
        def setupUi(self, *_args, **_kwargs):
            pass

    class Ui_UniloginDialog:
        def setupUi(self, *_args, **_kwargs):
            pass

    class SetupManager:
        def create_outlook_categories(self):
            pass

        def hide_on_startup(self):
            return False

        def get_aula_username(self):
            return ""

        def get_aula_password(self):
            return ""

        def update_unilogin(self, **_kwargs):
            pass

        def set_hide_on_startup(self, *_args, **_kwargs):
            pass

    class OutlookManager:
        def send_a_aula_creation_or_update_error_mail(self, *_args, **_kwargs):
            pass

    class AulaCalendar:
        pass

    class AulaConnection:
        pass

    class AulaEvent:
        pass

    class CalendarComparer:
        def __init__(self, *_args, **_kwargs):
            pass

    mainwindow.Ui_MainWindow = Ui_MainWindow
    unilogindialog.Ui_UniloginDialog = Ui_UniloginDialog
    setupmanager.SetupManager = SetupManager
    outlookmanager.OutlookManager = OutlookManager
    aula.AulaCalendar = AulaCalendar
    aula.AulaConnection = AulaConnection
    aula.AulaEvent = AulaEvent
    calendar_comparer.CalendarComparer = CalendarComparer

    sys.modules["mainwindow"] = mainwindow
    sys.modules["unilogindialog"] = unilogindialog
    sys.modules["setupmanager"] = setupmanager
    sys.modules["outlookmanager"] = outlookmanager
    sys.modules["aula"] = aula
    sys.modules["calendar_comparer"] = calendar_comparer


def _stub_git_module():
    git = types.ModuleType("git")

    class Repo:
        def __init__(self, *_args, **_kwargs):
            self.head = types.SimpleNamespace(
                commit=types.SimpleNamespace(committed_date=0),
            )

    git.Repo = Repo
    sys.modules["git"] = git


@pytest.fixture(scope="session")
def qapp():
    return None


@pytest.fixture(scope="session")
def main_module():
    _stub_windows_modules()
    _stub_qt_modules()
    _stub_project_modules()
    _stub_git_module()
    spec = importlib.util.spec_from_file_location("phase02_main", MAIN_MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def tray_spy():
    class TraySpy:
        def __init__(self):
            self.messages = []

        def showMessage(self, title, message):
            self.messages.append((title, message))

    return TraySpy()
