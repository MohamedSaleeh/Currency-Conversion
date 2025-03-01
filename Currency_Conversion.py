from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
import requests

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(896, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # Label: Background
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-6, -5, 901, 910))
        self.label.setPixmap(QtGui.QPixmap("Background2.jpg"))
        self.label.setScaledContents(True)

        # Label: Enter Amount
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(340, 110, 201, 41))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255); font: italic 18pt \"Sitka\";")
        self.label_2.setText("Enter Amount")

        # Input: Amount
        self.spinBox_amount = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.spinBox_amount.setGeometry(QtCore.QRect(370, 160, 141, 28))
        self.spinBox_amount.setMaximum(1000000)

        # Label: From Currency
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(330, 210, 221, 41))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255); font: italic 18pt \"Sitka\";")
        self.label_3.setText("From Currency")

        # ComboBox: From
        self.comboBox_from = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_from.setGeometry(QtCore.QRect(390, 260, 86, 28))
        self.comboBox_from.addItems(["USD", "EUR", "TRY", "SYP"])

        # Label: To Currency
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(350, 300, 181, 41))
        self.label_4.setStyleSheet("color: rgb(255, 255, 255); font: italic 18pt \"Sitka\";")
        self.label_4.setText("To Currency")

        # ComboBox: To
        self.comboBox_to = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_to.setGeometry(QtCore.QRect(390, 350, 86, 28))
        self.comboBox_to.addItems(["USD", "EUR", "TRY", "SYP"])

        # Button: Convert
        self.button_convert = QtWidgets.QPushButton(self.centralwidget)
        self.button_convert.setGeometry(QtCore.QRect(330, 410, 221, 47))
        self.button_convert.setStyleSheet("font: bold 12pt; color: rgb(3, 0, 59);")
        self.button_convert.setText("Convert")
        self.button_convert.clicked.connect(self.convert_currency)

        # Label: Converted Amount
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(300, 480, 291, 41))
        self.label_5.setStyleSheet("color: rgb(255, 255, 255); font: italic 18pt \"Sitka\";")
        self.label_5.setText("Converted Amount: ")

        # Label: Result
        self.label_result = QtWidgets.QLabel(self.centralwidget)
        self.label_result.setGeometry(QtCore.QRect(360, 540, 291, 41))
        self.label_result.setStyleSheet("color: rgb(255, 255, 255); font: italic 18pt \"Sitka\";")
        self.label_result.setText("")

        # Section: Live Rates
        self.label_live_rates = QLabel(self.centralwidget)
        self.label_live_rates.setGeometry(QtCore.QRect(200, 600, 500, 300))
        self.label_live_rates.setStyleSheet("color: white; font: 14pt;")
        self.label_live_rates.setAlignment(QtCore.Qt.AlignCenter)
        self.label_live_rates.setText("Loading live rates...")

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowTitle("Currency Converter")

        self.update_live_rates()

    def fetch_rates(self):
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
            response.raise_for_status()
            return response.json()["rates"]
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Could not fetch rates: {e}")
            return None

    def convert_currency(self):
        rates = self.fetch_rates()
        if rates:
            try:
                amount = self.spinBox_amount.value()
                from_currency = self.comboBox_from.currentText()
                to_currency = self.comboBox_to.currentText()

                rate_from = rates.get(from_currency,1)
                rate_to = rates.get(to_currency, 1)
                converted_amount = amount * (rate_to / rate_from)
                self.label_result.setText(f"{converted_amount:.2f} {to_currency}")

            except Exception as e:
                QMessageBox.warning(None, "Conversion Error", f"An error occurred: {e}")

    def update_live_rates(self):
        rates = self.fetch_rates()
        if rates:
            try:
                rates_text = (
                    f"\nTRY: {rates['TRY']:.2f} ⇄ 1 USD\n\n"
                    f"EUR: {rates['EUR']:.2f} ⇄ 1 USD\n\n"
                    f"SYP: {rates['SYP']:.2f} ⇄ 1 USD\n\n"
                    f"TRY: {rates['TRY']/rates['EUR']:.2f} ⇄ 1 EUR\n\n"
                    f"SYP: {rates['SYP']/rates['TRY']:.2f} ⇄ 1 TRY"
                )
                self.label_live_rates.setText(rates_text)
            except KeyError:
                self.label_live_rates.setText("Error: Some rates are missing.")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
