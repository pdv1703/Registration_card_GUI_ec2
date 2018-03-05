# -*- coding: utf-8 -*-
import sys
import mysql.connector
from mysql.connector import errorcode
import os
import datetime
from PyQt5.QtCore import Qt, QDateTime, QDate, QDir
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication,
    QPushButton, QMainWindow, QApplication, QScrollArea, QTableWidget,
    QTableWidgetItem, QSplitter, QHBoxLayout, QTabWidget, QSizePolicy,
    QComboBox, QDateEdit, QInputDialog, QErrorMessage, QMessageBox,
    QDateTimeEdit, QCheckBox)


# db_user = 'Pregnant_Admin'
# db_user_pass = 'a1w2PregAdmin'
# db_host= 'localhost'
# db_database_name='pregnant_application'

db_user = 'Pregnant_Admin'
db_user_pass = 'a1w2PregAdmin'
db_host= 'pregnant-db.co3fhen34njr.eu-central-1.rds.amazonaws.com'
db_database_name='pregnant_application'

class BigTextRedactor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.BigDataText = QTextEdit()
        self.CloseBigDataTextButton = QPushButton('Ok')

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.BigDataText, 0, 0, 2, 2)
        grid.addWidget(self.CloseBigDataTextButton, 2, 1)
        self.setLayout(grid)

        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('Редактор великих даних')
        self.show()


class Authorization(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.CloseTextFromTableButton = QPushButton('Ok')

        self.PasswordTitle = QLabel()
        self.PasswordTitle.setText('Введіть пароль:')
        self.PasswordLine = QLineEdit()
        self.PasswordLine.setText('q1w2e3r4')
        self.PasswordLine.setEchoMode(2)

        self.LoginTitle = QLabel()
        self.LoginTitle.setText('Логін:')
        self.LoginLine = QLineEdit()
        self.LoginLine.setText('Savka')

        self.AuthorizationButton = QPushButton('Ok')
        self.ExitButton = QPushButton('Exit')

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.LoginTitle, 0, 0, 1, 2)
        self.grid.addWidget(self.LoginLine, 1, 0, 1, 2)
        self.grid.addWidget(self.PasswordTitle, 2, 0, 1, 2)
        self.grid.addWidget(self.PasswordLine, 3, 0, 1, 2)
        self.grid.addWidget(self.AuthorizationButton, 4, 0)
        self.grid.addWidget(self.ExitButton, 4, 1)

        self.setLayout(self.grid)

        self.setGeometry(300, 300, 450, 100)
        self.setWindowTitle("Необхідно виконати авторизацію у програмі!")
        self.show()

        self.ExitButton.clicked.connect(QCoreApplication.instance().quit)


class PrimaryWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def SetPrivileges(self, *privileges):
        self.privileges = privileges
        return privileges

    def initUI(self):
        # self.Window('App_admin', 'Дмитро Горавський')
        self.d = Authorization()
        self.d.AuthorizationButton.clicked.connect(self.ParsCredential)

    def ParsCredential(self):
        self.Login = self.d.LoginLine.text()
        self.Login = self.Login.strip()

        self.Password = self.d.PasswordLine.text()
        self.Password = self.Password.strip()
        self.exception = "no exception"
        try:
            cnx = mysql.connector.connect(
                user=db_user,
                password=db_user_pass,
                host=db_host,
                database=db_database_name)

        except mysql.connector.DatabaseError as e:
            self.Info_mesage(str(e))
            self.exception = "error"

        if self.exception == 'no exception':
            cursor = cnx.cursor()
            query = ("SELECT s.Role from authorization s where s.Login=" + "'"
                     + self.Login + "' and s.Password='" + self.Password + "'")
            cursor.execute(query)
            mass = []
            for row in cursor:
                mass.append("""{:s}""".format(*row))

            if mass != []:
                if mass[0] == 'Administrator':
                    cursor = cnx.cursor()
                    query = ("SELECT s.pib from authorization s where s.Login="
                             + "'" + self.Login + "' and s.Password='" +
                             self.Password + "'")
                    cursor.execute(query)
                    pibmass = []
                    for row in cursor:
                        pibmass.append("""{:s}""".format(*row))

                    self.Window('App_admin', str(pibmass[0]))
                    self.d.close()

                elif mass[0] == 'User':
                    self.Window('App_user', 'Дмитро Горавський')
                    self.d.close()

            else:
                self.Error_mesage('Некоректний логін чи пароль!')
            cursor.close()
            cnx.close()
        else:
            self.Error_mesage(
                "Помилка у доступі до БД для можливості перевірки даних авторизації.\nЗверніться до адміністратора.\n\n"
                + str(self.exception))

    def Error_mesage(self, message):
        QMessageBox.information(self, "Помилка!", message)

    def Info_mesage(self, message):
        QMessageBox.information(self, "Інформація", message)

    def ConnectToPregnantBD(self):
        try:
            cnx = mysql.connector.connect(
                user=db_user,
                password=db_user_pass,
                host=db_host,
                database=db_database_name)
            return cnx
        except mysql.connector.DatabaseError as e:
            return 'Error in connection'

    def Window(self, privileges, WhoCangeParam):

        self.bottomLeftTabWidget = QTabWidget()

        # 1-st tab
        self.tab1 = QWidget()
        # 1 - паспортні дані
        # Подпункт ПІБ
        self.PIBLabel = QLabel(' I) Паспортні дані.')
        self.PIBLabel.setFixedHeight(20)
        self.PIBLabel.setStyleSheet(
            """QLabel{font-size:8pt; font-weight:600; color:#aa0000;}""")
        # self.PIBLabel.setTextFormat(Qt.RichText)

        self.OneLabel = QLabel('    1)')
        self.OneLabel.setFixedWidth(30)

        self.FirstNameLabel = QLabel("Ім'я:")
        self.FirstNameLabel.setFixedHeight(15)
        self.FirstNameLineEdit = QLineEdit()
        self.FirstNameLineEdit.setFixedHeight(30)
        self.splitter1 = QSplitter(Qt.Vertical)
        self.splitter1.addWidget(self.FirstNameLabel)
        self.splitter1.addWidget(self.FirstNameLineEdit)

        self.LastNameLabel = QLabel('Прізвище:')
        self.LastNameLabel.setFixedHeight(15)
        self.LastNameLineEdit = QLineEdit()
        self.splitter2 = QSplitter(Qt.Vertical)
        self.splitter2.addWidget(self.LastNameLabel)
        self.splitter2.addWidget(self.LastNameLineEdit)

        self.FatherNameLabel = QLabel('Побатькові:')
        self.FatherNameLabel.setFixedHeight(15)
        self.FatherNameLineEdit = QLineEdit()
        self.splitter3 = QSplitter(Qt.Vertical)
        self.splitter3.addWidget(self.FatherNameLabel)
        self.splitter3.addWidget(self.FatherNameLineEdit)

        self.splitter4 = QSplitter(Qt.Horizontal)
        self.splitter4.addWidget(self.splitter1)
        self.splitter4.addWidget(self.splitter2)
        self.splitter4.addWidget(self.splitter3)

        self.splitter5 = QSplitter(Qt.Horizontal)
        self.splitter5.addWidget(self.OneLabel)
        self.splitter5.addWidget(self.splitter4)

        self.splitter6 = QSplitter(Qt.Vertical)
        self.splitter6.addWidget(self.PIBLabel)
        self.splitter6.addWidget(self.splitter5)
        ###### Подпункт 2, 3, 4
        self.HistoryNumberLabel = QLabel(
            '    2)    № Історії вагітності/пологів:')
        self.HistoryNumberLabel.setFixedHeight(30)
        self.HistoryNumberLabel.setFixedWidth(180)

        self.HistoryNumberLineEdit = QLineEdit()
        self.HistoryNumberLineEdit.setFixedWidth(100)

        self.AgeLabel = QLabel('   3) Вік:')
        self.AgeLabel.setFixedHeight(30)
        self.AgeLabel.setFixedWidth(40)
        self.AgeLineEdit = QLineEdit()
        self.AgeLineEdit.setFixedWidth(100)
        self.AgeLineEdit.setInputMask("D00")

        self.AddressLabel = QLabel('   4) Адреса:')
        self.AddressLabel.setFixedHeight(30)
        self.AddressLabel.setFixedWidth(65)
        self.AddressLineEdit = QLineEdit()
        # self.AddressLineEdit.setMaximumWidth(500)

        self.splitter7 = QSplitter(Qt.Horizontal)
        self.splitter7.addWidget(self.HistoryNumberLabel)
        self.splitter7.addWidget(self.HistoryNumberLineEdit)
        self.splitter7.addWidget(self.AgeLabel)
        self.splitter7.addWidget(self.AgeLineEdit)
        self.splitter7.addWidget(self.AddressLabel)
        self.splitter7.addWidget(self.AddressLineEdit)

        ###Подпункт 5 Професійна діяльність:
        self.ProffesionalLabel = QLabel('    5)    Професійна діяльність:')
        self.ProffesionalLabel.setFixedHeight(30)
        self.ProffesionalLabel.setFixedWidth(180)

        self.ProffesionalDontWorkCheckBox = QCheckBox('Не працює')
        self.ProffesionalDontWorkCheckBox.stateChanged.connect(
            self.ProffesionalDontWork)

        self.ProffesionalStadyCheckBox = QCheckBox('Навчається')
        self.ProffesionalStadyCheckBox.stateChanged.connect(
            self.ProffesionalStady)

        self.ProffesionalWhiteCollarWorkerCheckBox = QCheckBox('Службовець')
        self.ProffesionalWhiteCollarWorkerCheckBox.stateChanged.connect(
            self.ProffesionalWhiteCollar)

        self.ProffesionalEmployeeCheckBox = QCheckBox('Робітник')
        self.ProffesionalEmployeeCheckBox.stateChanged.connect(
            self.ProffesionalEmployee)

        self.splitter8 = QSplitter(Qt.Horizontal)
        self.splitter8.addWidget(self.ProffesionalLabel)
        self.splitter8.addWidget(self.ProffesionalDontWorkCheckBox)
        self.splitter8.addWidget(self.ProffesionalStadyCheckBox)
        self.splitter8.addWidget(self.ProffesionalWhiteCollarWorkerCheckBox)
        self.splitter8.addWidget(self.ProffesionalEmployeeCheckBox)

        # Подпункт 6 - Інвалідність
        self.DisabilityLabel = QLabel('    6)   Інвалідність:')
        self.DisabilityLabel.setFixedHeight(30)
        self.DisabilityLabel.setFixedWidth(180)

        self.DisabilityNoneCheckBox = QCheckBox('Немає')
        self.DisabilityNoneCheckBox.setChecked(1)
        self.DisabilityNoneCheckBox.stateChanged.connect(
            self.DisabilityNoneFunc)

        self.DisabilityILevelCheckBox = QCheckBox('I група')
        self.DisabilityILevelCheckBox.setEnabled(0)
        self.DisabilityILevelCheckBox.stateChanged.connect(
            self.DisabilityILevelFunc)

        self.DisabilityIILevelCheckBox = QCheckBox('II група')
        self.DisabilityIILevelCheckBox.setEnabled(0)
        self.DisabilityIILevelCheckBox.stateChanged.connect(
            self.DisabilityIILevelFunc)

        self.DisabilityIIILevelCheckBox = QCheckBox('III група')
        self.DisabilityIIILevelCheckBox.setEnabled(0)
        self.DisabilityIIILevelCheckBox.stateChanged.connect(
            self.DisabilityIIILevelFunc)

        self.splitter9 = QSplitter(Qt.Horizontal)
        self.splitter9.addWidget(self.DisabilityLabel)
        self.splitter9.addWidget(self.DisabilityNoneCheckBox)
        self.splitter9.addWidget(self.DisabilityILevelCheckBox)
        self.splitter9.addWidget(self.DisabilityIILevelCheckBox)
        self.splitter9.addWidget(self.DisabilityIIILevelCheckBox)

        # Пункт 2 - Наявність постійних факторів ризику ТЕУ
        self.RiskFactorsPunktLabel = QLabel(
            '\n II) Наявність постійних факторів ризику ТЕУ.')
        self.RiskFactorsPunktLabel.setFixedHeight(30)
        self.RiskFactorsPunktLabel.setStyleSheet(
            """QLabel{font-size:8pt; font-weight:600; color:#aa0000;}""")

        # 1.	Рецидиви тромбоемболії в минулому
        self.ReceduvyTromboemboliiLabel = QLabel(
            '    1. Рецедиви тромбоемболіі в минулому:')
        self.ReceduvyTromboemboliiLabel.setFixedHeight(15)
        self.ReceduvyTromboemboliiLabel.setFixedWidth(400)

        self.ReceduvyTromboemboliiYesCheckBox = QCheckBox('Так')
        self.ReceduvyTromboemboliiYesCheckBox.setFixedWidth(100)
        self.ReceduvyTromboemboliiYesCheckBox.setEnabled(0)
        self.ReceduvyTromboemboliiYesCheckBox.stateChanged.connect(
            self.ReceduvyTromboemboliiYesFunc)

        self.ReceduvyTromboemboliiNoCheckBox = QCheckBox('Ні')
        self.ReceduvyTromboemboliiNoCheckBox.setChecked(1)
        self.ReceduvyTromboemboliiNoCheckBox.stateChanged.connect(
            self.ReceduvyTromboemboliiNoFunc)

        self.splitter10 = QSplitter(Qt.Horizontal)
        self.splitter10.addWidget(self.ReceduvyTromboemboliiLabel)
        self.splitter10.addWidget(self.ReceduvyTromboemboliiYesCheckBox)
        self.splitter10.addWidget(self.ReceduvyTromboemboliiNoCheckBox)

        # 2.	Тромбоемболії, неспровоковані або пов'язані з прийомом естрогенів
        self.TromboemboliiAndEstrogensLabel = QLabel(
            "    2. Тромбоемболії, неспровоковані або пов'язані з прийомом естрогенів:"
        )
        self.TromboemboliiAndEstrogensLabel.setFixedHeight(15)
        self.TromboemboliiAndEstrogensLabel.setFixedWidth(400)

        self.TromboemboliiAndEstrogensYesCheckBox = QCheckBox('Так')
        self.TromboemboliiAndEstrogensYesCheckBox.setFixedWidth(100)
        self.TromboemboliiAndEstrogensYesCheckBox.setEnabled(0)
        self.TromboemboliiAndEstrogensYesCheckBox.stateChanged.connect(
            self.TromboemboliiAndEstrogensYesFunc)

        self.TromboemboliiAndEstrogensNoCheckBox = QCheckBox('Ні')
        self.TromboemboliiAndEstrogensNoCheckBox.setChecked(1)
        self.TromboemboliiAndEstrogensNoCheckBox.stateChanged.connect(
            self.TromboemboliiAndEstrogensNoFunc)

        self.splitter11 = QSplitter(Qt.Horizontal)
        self.splitter11.addWidget(self.TromboemboliiAndEstrogensLabel)
        self.splitter11.addWidget(self.TromboemboliiAndEstrogensYesCheckBox)
        self.splitter11.addWidget(self.TromboemboliiAndEstrogensNoCheckBox)

        # 3.	тромбоемболія спровокована
        self.TromboemboliaSprovokovanaLabel = QLabel(
            "    3. Тромбоемболія спровокована:")
        self.TromboemboliaSprovokovanaLabel.setFixedHeight(15)
        self.TromboemboliaSprovokovanaLabel.setFixedWidth(400)

        self.TromboemboliaSprovokovanaYesCheckBox = QCheckBox('Так')
        self.TromboemboliaSprovokovanaYesCheckBox.setFixedWidth(100)
        self.TromboemboliaSprovokovanaYesCheckBox.setEnabled(0)
        self.TromboemboliaSprovokovanaYesCheckBox.stateChanged.connect(
            self.TromboemboliaSprovokovanaYesFunc)

        self.TromboemboliaSprovokovanaNoCheckBox = QCheckBox('Ні')
        self.TromboemboliaSprovokovanaNoCheckBox.setChecked(1)
        self.TromboemboliaSprovokovanaNoCheckBox.stateChanged.connect(
            self.TromboemboliaSprovokovanaNoFunc)

        self.splitter13 = QSplitter(Qt.Horizontal)
        self.splitter13.addWidget(self.TromboemboliaSprovokovanaLabel)
        self.splitter13.addWidget(self.TromboemboliaSprovokovanaYesCheckBox)
        self.splitter13.addWidget(self.TromboemboliaSprovokovanaNoCheckBox)

        # 4.	Сімейний анамнез тромбоемболії
        self.SimeinuiAnamnezTromboemboliiLabel = QLabel(
            "    4. Сімейний анамнез тромбоемболії:")
        self.SimeinuiAnamnezTromboemboliiLabel.setFixedHeight(15)
        self.SimeinuiAnamnezTromboemboliiLabel.setFixedWidth(400)

        self.SimeinuiAnamnezTromboemboliiYesCheckBox = QCheckBox('Так')
        self.SimeinuiAnamnezTromboemboliiYesCheckBox.setFixedWidth(100)
        self.SimeinuiAnamnezTromboemboliiYesCheckBox.setEnabled(0)
        self.SimeinuiAnamnezTromboemboliiYesCheckBox.stateChanged.connect(
            self.SimeinuiAnamnezTromboemboliiYesFunc)

        self.SimeinuiAnamnezTromboemboliiNoCheckBox = QCheckBox('Ні')
        self.SimeinuiAnamnezTromboemboliiNoCheckBox.setChecked(1)
        self.SimeinuiAnamnezTromboemboliiNoCheckBox.stateChanged.connect(
            self.SimeinuiAnamnezTromboemboliiNoFunc)

        self.splitter14 = QSplitter(Qt.Horizontal)
        self.splitter14.addWidget(self.SimeinuiAnamnezTromboemboliiLabel)
        self.splitter14.addWidget(self.SimeinuiAnamnezTromboemboliiYesCheckBox)
        self.splitter14.addWidget(self.SimeinuiAnamnezTromboemboliiNoCheckBox)

        # 5.	встановлена тромбофілія

        self.VstanovlennaTrombofiliaLabel = QLabel(
            '    5. Встановлена тромбофілія:')
        self.VstanovlennaTrombofiliaLabel.setFixedHeight(15)
        self.VstanovlennaTrombofiliaLabel.setFixedWidth(400)

        self.VstanovlennaTrombofiliaYesCheckBox = QCheckBox('Так')
        self.VstanovlennaTrombofiliaYesCheckBox.setFixedWidth(100)
        self.VstanovlennaTrombofiliaYesCheckBox.setEnabled(0)
        self.VstanovlennaTrombofiliaYesCheckBox.stateChanged.connect(
            self.VstanovlennaTrombofiliaYesFunc)

        self.VstanovlennaTrombofiliaNoCheckBox = QCheckBox('Ні')
        self.VstanovlennaTrombofiliaNoCheckBox.setChecked(1)
        self.VstanovlennaTrombofiliaNoCheckBox.stateChanged.connect(
            self.VstanovlennaTrombofiliaNoFunc)

        self.splitter15 = QSplitter(Qt.Horizontal)
        self.splitter15.addWidget(self.VstanovlennaTrombofiliaLabel)
        self.splitter15.addWidget(self.VstanovlennaTrombofiliaYesCheckBox)
        self.splitter15.addWidget(self.VstanovlennaTrombofiliaNoCheckBox)

        # 6.	Супутні захворювання 				а) так б) ні 	(обрати)

        self.SypytniZahvoryvannaLabel = QLabel('    6. Супутні захворювання:')
        self.SypytniZahvoryvannaLabel.setFixedHeight(15)
        self.SypytniZahvoryvannaLabel.setFixedWidth(400)

        self.SypytniZahvoryvannaYesCheckBox = QCheckBox('Так')
        self.SypytniZahvoryvannaYesCheckBox.setFixedWidth(100)
        self.SypytniZahvoryvannaYesCheckBox.setEnabled(0)
        self.SypytniZahvoryvannaYesCheckBox.stateChanged.connect(
            self.SypytniZahvoryvannaYesFunc)

        self.SypytniZahvoryvannaNoCheckBox = QCheckBox('Ні')
        self.SypytniZahvoryvannaNoCheckBox.setChecked(1)
        self.SypytniZahvoryvannaNoCheckBox.stateChanged.connect(
            self.SypytniZahvoryvannaNoFunc)

        # •    серцево - судинні,
        self.SypytniSercevoSydunniCheckBox = QCheckBox('Серцево-судинні')
        self.SypytniSercevoSydunniCheckBox.setFixedHeight(15)
        self.SypytniSercevoSydunniCheckBox.hide()

        # •    бронхо - легеневі,
        self.SypytniBronhoLegeneviCheckBox = QCheckBox('Бронхо-легеневі')
        self.SypytniBronhoLegeneviCheckBox.setFixedHeight(15)
        self.SypytniBronhoLegeneviCheckBox.hide()

        # •    СЧВ,
        self.SypytniSCHVCheckBox = QCheckBox('СЧВ')
        self.SypytniSCHVCheckBox.setFixedHeight(15)
        self.SypytniSCHVCheckBox.hide()

        # •    рак,
        self.SypytniRAKCheckBox = QCheckBox('Рак')
        self.SypytniRAKCheckBox.setFixedHeight(15)
        self.SypytniRAKCheckBox.hide()

        # •    нефротичний синдром
        self.SypytniNefrotuchnuiSundromCheckBox = QCheckBox(
            'Нефротичний синдром')
        self.SypytniNefrotuchnuiSundromCheckBox.setFixedHeight(15)
        self.SypytniNefrotuchnuiSundromCheckBox.hide()

        # •    серповидно - клітинна анемія
        self.SypytniSerpovudnoKlitynnaAnemiaCheckBox = QCheckBox(
            'Серповидно-клітинна анемія')
        self.SypytniSerpovudnoKlitynnaAnemiaCheckBox.setFixedHeight(15)
        self.SypytniSerpovudnoKlitynnaAnemiaCheckBox.hide()

        # •    внутрішньовенне введення медикаментів
        self.SypytniVnytrishnoVenneVvedennaMedukamentivCheckBox = QCheckBox(
            'Внутрішньовенне введення медикаментів')
        self.SypytniVnytrishnoVenneVvedennaMedukamentivCheckBox.setFixedHeight(
            15)
        self.SypytniVnytrishnoVenneVvedennaMedukamentivCheckBox.hide()

        # •    інші(уточнити)
        self.SypytniOtherCheckBox = QCheckBox('Інше:')
        self.SypytniOtherCheckBox.setFixedHeight(15)
        self.SypytniOtherCheckBox.setFixedWidth(50)
        self.SypytniOtherLineEdit = QLineEdit()
        self.SypytniOtherLineEdit.setMinimumWidth(200)
        self.SypytniOtherCheckBox.stateChanged.connect(
            self.SypytniOtherCheckBoxFunc)

        self.SypytniOtherLineSplitter = QSplitter(Qt.Horizontal)
        self.SypytniOtherLineSplitter.addWidget(self.SypytniOtherCheckBox)
        self.SypytniOtherLineSplitter.addWidget(self.SypytniOtherLineEdit)
        self.SypytniOtherLineEdit.hide()
        self.SypytniOtherCheckBox.hide()

        self.splitter16 = QSplitter(Qt.Horizontal)
        self.splitter16.addWidget(self.SypytniZahvoryvannaLabel)
        self.splitter16.addWidget(self.SypytniZahvoryvannaYesCheckBox)
        self.splitter16.addWidget(self.SypytniZahvoryvannaNoCheckBox)

        # 7.  Вік > 35 років

        self.OldMore35Label = QLabel('    7. Вік > 35 років:')
        self.OldMore35Label.setFixedHeight(15)
        self.OldMore35Label.setFixedWidth(400)
        self.OldMore35Label.show()

        self.OldMore35YesCheckBox = QCheckBox('Так')
        self.OldMore35YesCheckBox.setFixedWidth(100)
        self.OldMore35YesCheckBox.setEnabled(0)
        self.OldMore35YesCheckBox.show()
        self.OldMore35YesCheckBox.stateChanged.connect(self.OldMore35YesFunc)

        self.OldMore35NoCheckBox = QCheckBox('Ні')
        self.OldMore35NoCheckBox.setChecked(1)
        self.OldMore35NoCheckBox.show()
        self.OldMore35NoCheckBox.stateChanged.connect(self.OldMore35NoFunc)

        self.splitter18 = QSplitter(Qt.Horizontal)
        self.splitter18.addWidget(self.OldMore35Label)
        self.splitter18.addWidget(self.OldMore35YesCheckBox)
        self.splitter18.addWidget(self.OldMore35NoCheckBox)

        # 8.	Ожиріння (ІМТ> 30)
        self.OgirinnaLabel = QLabel('    8. Ожиріння:')
        self.OgirinnaLabel.setFixedHeight(15)
        self.OgirinnaLabel.setFixedWidth(400)
        self.OgirinnaLabel.show()

        self.OgirinnaYesCheckBox = QCheckBox('Так')
        self.OgirinnaYesCheckBox.setFixedWidth(100)
        self.OgirinnaYesCheckBox.setEnabled(0)
        self.OgirinnaYesCheckBox.show()
        self.OgirinnaYesCheckBox.stateChanged.connect(self.OgirinnaYesFunc)

        self.OgirinnaNoCheckBox = QCheckBox('Ні')
        self.OgirinnaNoCheckBox.setChecked(1)
        self.OgirinnaNoCheckBox.show()
        self.OgirinnaNoCheckBox.stateChanged.connect(self.OgirinnaNoFunc)

        self.splitter19 = QSplitter(Qt.Horizontal)
        self.splitter19.addWidget(self.OgirinnaLabel)
        self.splitter19.addWidget(self.OgirinnaYesCheckBox)
        self.splitter19.addWidget(self.OgirinnaNoCheckBox)

        # 9.	Вагітність  ≥3
        self.VagitnistMore3Label = QLabel('    9. Вагітність ≥ 3:')
        self.VagitnistMore3Label.setFixedHeight(15)
        self.VagitnistMore3Label.setFixedWidth(400)
        self.VagitnistMore3Label.show()

        self.VagitnistMore3YesCheckBox = QCheckBox('Так')
        self.VagitnistMore3YesCheckBox.setFixedWidth(100)
        self.VagitnistMore3YesCheckBox.setEnabled(0)
        self.VagitnistMore3YesCheckBox.show()
        self.VagitnistMore3YesCheckBox.stateChanged.connect(
            self.VagitnistMore3YesFunc)

        self.VagitnistMore3NoCheckBox = QCheckBox('Ні')
        self.VagitnistMore3NoCheckBox.setChecked(1)
        self.VagitnistMore3NoCheckBox.show()
        self.VagitnistMore3NoCheckBox.stateChanged.connect(
            self.VagitnistMore3NoFunc)

        self.splitter20 = QSplitter(Qt.Horizontal)
        self.splitter20.addWidget(self.VagitnistMore3Label)
        self.splitter20.addWidget(self.VagitnistMore3YesCheckBox)
        self.splitter20.addWidget(self.VagitnistMore3NoCheckBox)

        # 10.	Куріння
        self.KyrinnaLabel = QLabel('    10. Куріння:')
        self.KyrinnaLabel.setFixedHeight(15)
        self.KyrinnaLabel.setFixedWidth(400)
        self.KyrinnaLabel.show()

        self.KyrinnaYesCheckBox = QCheckBox('Так')
        self.KyrinnaYesCheckBox.setFixedWidth(100)
        self.KyrinnaYesCheckBox.setEnabled(0)
        self.KyrinnaYesCheckBox.show()
        self.KyrinnaYesCheckBox.stateChanged.connect(self.KyrinnaYesFunc)

        self.KyrinnaNoCheckBox = QCheckBox('Ні')
        self.KyrinnaNoCheckBox.setChecked(1)
        self.KyrinnaNoCheckBox.show()
        self.KyrinnaNoCheckBox.stateChanged.connect(self.KyrinnaNoFunc)

        self.splitter21 = QSplitter(Qt.Horizontal)
        self.splitter21.addWidget(self.KyrinnaLabel)
        self.splitter21.addWidget(self.KyrinnaYesCheckBox)
        self.splitter21.addWidget(self.KyrinnaNoCheckBox)

        # 11.	Великі варикозні вени
        self.VelykiVarikozniVenuLabel = QLabel(
            '    11. Великі варикозні вени:')
        self.VelykiVarikozniVenuLabel.setFixedHeight(15)
        self.VelykiVarikozniVenuLabel.setFixedWidth(400)
        self.VelykiVarikozniVenuLabel.show()

        self.VelykiVarikozniVenuYesCheckBox = QCheckBox('Так')
        self.VelykiVarikozniVenuYesCheckBox.setFixedWidth(100)
        self.VelykiVarikozniVenuYesCheckBox.setEnabled(0)
        self.VelykiVarikozniVenuYesCheckBox.show()
        self.VelykiVarikozniVenuYesCheckBox.stateChanged.connect(
            self.VelykiVarikozniVenuYesFunc)

        self.VelykiVarikozniVenuNoCheckBox = QCheckBox('Ні')
        self.VelykiVarikozniVenuNoCheckBox.setChecked(1)
        self.VelykiVarikozniVenuNoCheckBox.show()
        self.VelykiVarikozniVenuNoCheckBox.stateChanged.connect(
            self.VelykiVarikozniVenuNoFunc)

        self.splitter22 = QSplitter(Qt.Horizontal)
        self.splitter22.addWidget(self.VelykiVarikozniVenuLabel)
        self.splitter22.addWidget(self.VelykiVarikozniVenuYesCheckBox)
        self.splitter22.addWidget(self.VelykiVarikozniVenuNoCheckBox)

        # Финальный сплиттер Наявність постійних факторів ризику ТЕУ
        self.splitter12 = QSplitter(Qt.Vertical)
        self.splitter12.addWidget(self.RiskFactorsPunktLabel)
        self.splitter12.addWidget(self.splitter10)
        self.splitter12.addWidget(self.splitter11)
        self.splitter12.addWidget(self.splitter13)
        self.splitter12.addWidget(self.splitter14)
        self.splitter12.addWidget(self.splitter15)
        self.splitter12.addWidget(self.splitter16)
        self.splitter12.addWidget(self.splitter18)
        self.splitter12.addWidget(self.splitter19)
        self.splitter12.addWidget(self.splitter20)
        self.splitter12.addWidget(self.splitter21)
        self.splitter12.addWidget(self.splitter22)
        # ІІІ. Проведення профілактики/терапії ТЕУ до вагітності: а) так б)ні

        self.ProvedennaProfTEYdpVagitnostiLabel = QLabel(
            ' III. Проведення профілактики/терапії ТЕУ до вагітності:')
        self.ProvedennaProfTEYdpVagitnostiLabel.setFixedWidth(400)
        self.ProvedennaProfTEYdpVagitnostiLabel.setStyleSheet(
            """QLabel{font-size:8pt; font-weight:600; color:#aa0000;}""")

        self.ProvedennaProfTEYdpVagitnostiLabelYesCheckBox = QCheckBox('Так')
        self.ProvedennaProfTEYdpVagitnostiLabelYesCheckBox.setFixedWidth(100)
        self.ProvedennaProfTEYdpVagitnostiLabelYesCheckBox.setEnabled(0)
        self.ProvedennaProfTEYdpVagitnostiLabelYesCheckBox.show()
        self.ProvedennaProfTEYdpVagitnostiLabelYesCheckBox.stateChanged.connect(
            self.ProvedennaProfTEYdpVagitnostiLabelYesFunc)

        self.ProvedennaProfTEYdpVagitnostiLabelNoCheckBox = QCheckBox('Ні')
        self.ProvedennaProfTEYdpVagitnostiLabelNoCheckBox.setChecked(1)
        self.ProvedennaProfTEYdpVagitnostiLabelNoCheckBox.show()
        self.ProvedennaProfTEYdpVagitnostiLabelNoCheckBox.stateChanged.connect(
            self.ProvedennaProfTEYdpVagitnostiLabelNoFunc)

        self.splitter23 = QSplitter(Qt.Horizontal)
        self.splitter23.addWidget(self.ProvedennaProfTEYdpVagitnostiLabel)
        self.splitter23.addWidget(
            self.ProvedennaProfTEYdpVagitnostiLabelYesCheckBox)
        self.splitter23.addWidget(
            self.ProvedennaProfTEYdpVagitnostiLabelNoCheckBox)

        # 1)	Еластична компресія
        self.ElastychnaKompresiaLabel = QLabel('    1. Еластична компресія:')
        self.ElastychnaKompresiaLabel.setFixedHeight(15)
        self.ElastychnaKompresiaLabel.setFixedWidth(400)
        self.ElastychnaKompresiaLabel.setEnabled(0)

        self.ElastychnaKompresiaYesCheckBox = QCheckBox('Так')
        self.ElastychnaKompresiaYesCheckBox.setFixedWidth(100)
        self.ElastychnaKompresiaYesCheckBox.setEnabled(0)
        self.ElastychnaKompresiaYesCheckBox.stateChanged.connect(
            self.ElastychnaKompresiaYesFunc)

        self.ElastychnaKompresiaNoCheckBox = QCheckBox('Ні')
        self.ElastychnaKompresiaNoCheckBox.setChecked(1)
        self.ElastychnaKompresiaNoCheckBox.show()
        self.ElastychnaKompresiaNoCheckBox.setFixedWidth(40)
        self.ElastychnaKompresiaNoCheckBox.stateChanged.connect(
            self.ElastychnaKompresiaNoFunc)
        self.ElastychnaKompresiaNoCheckBox.setEnabled(0)

        self.ElastychnaKompresiaLevelLabel = QLabel('Клас:')
        self.ElastychnaKompresiaLevelLabel.setFixedWidth(40)
        self.ElastychnaKompresiaLevelLabel.hide()
        self.ElastychnaKompresiaLevelLabel.setEnabled(0)

        self.ElastychnaKompresiaLevelLineEdit = QLineEdit()
        self.ElastychnaKompresiaLevelLineEdit.hide()
        self.ElastychnaKompresiaLevelLineEdit.setEnabled(0)

        self.splitter24 = QSplitter(Qt.Horizontal)
        self.splitter24.addWidget(self.ElastychnaKompresiaLabel)
        self.splitter24.addWidget(self.ElastychnaKompresiaYesCheckBox)
        self.splitter24.addWidget(self.ElastychnaKompresiaNoCheckBox)
        self.splitter24.addWidget(self.ElastychnaKompresiaLevelLabel)
        self.splitter24.addWidget(self.ElastychnaKompresiaLevelLineEdit)

        # 2)	Медикаментозна профілактика 	а) так б)ні

        self.MedukamentoznaProfilaktukaLabel = QLabel(
            '    2. Медикаментозна профілактика:')
        self.MedukamentoznaProfilaktukaLabel.setFixedHeight(15)
        self.MedukamentoznaProfilaktukaLabel.setFixedWidth(400)
        self.MedukamentoznaProfilaktukaLabel.setEnabled(0)

        self.MedukamentoznaProfilaktukaYesCheckBox = QCheckBox('Так')
        self.MedukamentoznaProfilaktukaYesCheckBox.setFixedWidth(100)
        self.MedukamentoznaProfilaktukaYesCheckBox.setEnabled(0)
        self.MedukamentoznaProfilaktukaYesCheckBox.stateChanged.connect(
            self.MedukamentoznaProfilaktukaYesFunc)

        self.MedukamentoznaProfilaktukaNoCheckBox = QCheckBox('Ні')
        self.MedukamentoznaProfilaktukaNoCheckBox.setChecked(1)
        self.MedukamentoznaProfilaktukaNoCheckBox.setEnabled(0)
        self.MedukamentoznaProfilaktukaNoCheckBox.setFixedWidth(40)
        self.MedukamentoznaProfilaktukaNoCheckBox.stateChanged.connect(
            self.MedukamentoznaProfilaktukaNoFunc)

        self.MedukamentoznaProfilaktukaNazvaPreperatyLabel = QLabel(
            '2.1 Назва препарату:')
        self.MedukamentoznaProfilaktukaNazvaPreperatyLabel.setFixedWidth(40)
        self.MedukamentoznaProfilaktukaNazvaPreperatyLabel.hide()
        self.MedukamentoznaProfilaktukaNazvaPreperatyLabel.setEnabled(0)

        self.MedukamentoznaProfilaktukaNazvaPreperatyLineEdit = QLineEdit()
        self.MedukamentoznaProfilaktukaNazvaPreperatyLineEdit.hide()

        self.MedukamentoznaProfilaktukaRegymPrujomyLabel = QLabel(
            '2.2 Режим прийому:')
        self.MedukamentoznaProfilaktukaRegymPrujomyLabel.setFixedWidth(40)
        self.MedukamentoznaProfilaktukaRegymPrujomyLabel.hide()

        self.MedukamentoznaProfilaktukaRegymPrujomyLineEdit = QLineEdit()
        self.MedukamentoznaProfilaktukaRegymPrujomyLineEdit.hide()

        self.SplitterMedukamentoznaProfilaktuka = QSplitter(Qt.Horizontal)
        self.SplitterMedukamentoznaProfilaktuka.addWidget(
            self.MedukamentoznaProfilaktukaLabel)
        self.SplitterMedukamentoznaProfilaktuka.addWidget(
            self.MedukamentoznaProfilaktukaYesCheckBox)
        self.SplitterMedukamentoznaProfilaktuka.addWidget(
            self.MedukamentoznaProfilaktukaNoCheckBox)
        self.SplitterMedukamentoznaProfilaktuka.addWidget(
            self.MedukamentoznaProfilaktukaNazvaPreperatyLabel)
        self.SplitterMedukamentoznaProfilaktuka.addWidget(
            self.MedukamentoznaProfilaktukaNazvaPreperatyLineEdit)
        self.SplitterMedukamentoznaProfilaktuka.addWidget(
            self.MedukamentoznaProfilaktukaRegymPrujomyLabel)
        self.SplitterMedukamentoznaProfilaktuka.addWidget(
            self.MedukamentoznaProfilaktukaRegymPrujomyLineEdit)

        # 3)	Хірургічне лікування :		          а) так б)ні
        self.HiryrgichneLikyvannaLabel = QLabel('    3. Хірургічне лікування:')
        self.HiryrgichneLikyvannaLabel.setFixedHeight(15)
        self.HiryrgichneLikyvannaLabel.setFixedWidth(400)
        self.HiryrgichneLikyvannaLabel.setEnabled(0)

        self.HiryrgichneLikyvannaYesCheckBox = QCheckBox('Так')
        self.HiryrgichneLikyvannaYesCheckBox.setFixedWidth(100)
        self.HiryrgichneLikyvannaYesCheckBox.setEnabled(0)
        self.HiryrgichneLikyvannaYesCheckBox.stateChanged.connect(
            self.HiryrgichneLikyvannaYesFunc)

        self.HiryrgichneLikyvannaNoCheckBox = QCheckBox('Ні')
        self.HiryrgichneLikyvannaNoCheckBox.setChecked(1)
        self.HiryrgichneLikyvannaNoCheckBox.show()
        self.HiryrgichneLikyvannaNoCheckBox.setFixedWidth(40)
        self.HiryrgichneLikyvannaNoCheckBox.setEnabled(0)
        self.HiryrgichneLikyvannaNoCheckBox.stateChanged.connect(
            self.HiryrgichneLikyvannaNoFunc)

        self.HiryrgichneLikyvannaNazvaOpericiiLabel = QLabel(
            'Назва операції та рік:')
        self.HiryrgichneLikyvannaNazvaOpericiiLabel.setFixedWidth(40)
        self.HiryrgichneLikyvannaNazvaOpericiiLabel.hide()
        self.HiryrgichneLikyvannaNazvaOpericiiLabel.setEnabled(0)

        self.HiryrgichneLikyvannaNazvaOpericiiLineEdit = QLineEdit()
        self.HiryrgichneLikyvannaNazvaOpericiiLineEdit.hide()

        self.HiryrgichneLikyvannaSplitter = QSplitter(Qt.Horizontal)
        self.HiryrgichneLikyvannaSplitter.addWidget(
            self.HiryrgichneLikyvannaLabel)
        self.HiryrgichneLikyvannaSplitter.addWidget(
            self.HiryrgichneLikyvannaYesCheckBox)
        self.HiryrgichneLikyvannaSplitter.addWidget(
            self.HiryrgichneLikyvannaNoCheckBox)
        self.HiryrgichneLikyvannaSplitter.addWidget(
            self.HiryrgichneLikyvannaNazvaOpericiiLabel)
        self.HiryrgichneLikyvannaSplitter.addWidget(
            self.HiryrgichneLikyvannaNazvaOpericiiLineEdit)

        # 4)	Тривалість проведеної профілактики _____________________

        self.TryvalistProvedennoiProfilaktykyLabel = QLabel(
            '    4. Тривалість проведеної профілактики:')
        self.TryvalistProvedennoiProfilaktykyLabel.setFixedWidth(400)
        self.TryvalistProvedennoiProfilaktykyLabel.setFixedHeight(15)
        self.TryvalistProvedennoiProfilaktykyLabel.setEnabled(0)
        self.TryvalistProvedennoiProfilaktykyLineEdit = QLineEdit()
        self.TryvalistProvedennoiProfilaktykyLineEdit.setEnabled(0)
        self.TryvalistProvedennoiProfilaktykyLineEdit.setMinimumWidth(200)

        self.TryvalistProvedennoiProfilaktykySplitter = QSplitter(
            Qt.Horizontal)
        self.TryvalistProvedennoiProfilaktykySplitter.addWidget(
            self.TryvalistProvedennoiProfilaktykyLabel)
        self.TryvalistProvedennoiProfilaktykySplitter.addWidget(
            self.TryvalistProvedennoiProfilaktykyLineEdit)

        # 5)	Наявність ускладнень від проведеної профілактики: а) так б)ні Ускладення:_______________________________________________

        self.YskladneenaVidProfilaktykuLabel = QLabel(
            '    5. Наявність ускладнень від проведеної профілактики:')
        self.YskladneenaVidProfilaktykuLabel.setFixedHeight(15)
        self.YskladneenaVidProfilaktykuLabel.setFixedWidth(400)
        self.YskladneenaVidProfilaktykuLabel.setEnabled(0)

        self.YskladneenaVidProfilaktykuYesCheckBox = QCheckBox('Так')
        self.YskladneenaVidProfilaktykuYesCheckBox.setFixedWidth(100)
        self.YskladneenaVidProfilaktykuYesCheckBox.setEnabled(0)
        self.YskladneenaVidProfilaktykuYesCheckBox.stateChanged.connect(
            self.YskladneenaVidProfilaktykuYesFunc)

        self.YskladneenaVidProfilaktykuNoCheckBox = QCheckBox('Ні')
        self.YskladneenaVidProfilaktykuNoCheckBox.setChecked(1)
        self.YskladneenaVidProfilaktykuNoCheckBox.show()
        self.YskladneenaVidProfilaktykuNoCheckBox.setFixedWidth(40)
        self.YskladneenaVidProfilaktykuNoCheckBox.setEnabled(0)
        self.YskladneenaVidProfilaktykuNoCheckBox.stateChanged.connect(
            self.YskladneenaVidProfilaktykuNoFunc)

        self.YskladneenaVidProfilaktykuNajavnistLabel = QLabel('Ускладення:')
        self.YskladneenaVidProfilaktykuNajavnistLabel.setFixedWidth(40)
        self.YskladneenaVidProfilaktykuNajavnistLabel.hide()

        self.YskladneenaVidProfilaktykuNajavnistLineEdit = QLineEdit()
        self.YskladneenaVidProfilaktykuNajavnistLineEdit.hide()

        self.YskladneenaVidProfilaktykuSplitter = QSplitter(Qt.Horizontal)
        self.YskladneenaVidProfilaktykuSplitter.addWidget(
            self.YskladneenaVidProfilaktykuLabel)
        self.YskladneenaVidProfilaktykuSplitter.addWidget(
            self.YskladneenaVidProfilaktykuYesCheckBox)
        self.YskladneenaVidProfilaktykuSplitter.addWidget(
            self.YskladneenaVidProfilaktykuNoCheckBox)
        self.YskladneenaVidProfilaktykuSplitter.addWidget(
            self.YskladneenaVidProfilaktykuNajavnistLabel)
        self.YskladneenaVidProfilaktykuSplitter.addWidget(
            self.YskladneenaVidProfilaktykuNajavnistLineEdit)

        # финальный сплиттер пункта III    Проведення профілактики/терапії ТЕУ до вагітності
        self.PynctIIISplitter = QSplitter(Qt.Vertical)
        self.PynctIIISplitter.addWidget(self.splitter23)
        self.PynctIIISplitter.addWidget(self.splitter24)
        self.PynctIIISplitter.addWidget(
            self.SplitterMedukamentoznaProfilaktuka)
        self.PynctIIISplitter.addWidget(self.HiryrgichneLikyvannaSplitter)
        self.PynctIIISplitter.addWidget(
            self.TryvalistProvedennoiProfilaktykySplitter)
        self.PynctIIISplitter.addWidget(
            self.YskladneenaVidProfilaktykuSplitter)

        # ІV. Акушерський анамнез.

        self.AkysherskiiAnamnezLabel = QLabel('\n IV) Акушерський анамнез.')
        self.AkysherskiiAnamnezLabel.setFixedHeight(30)
        self.AkysherskiiAnamnezLabel.setStyleSheet(
            """QLabel{font-size:8pt; font-weight:600; color:#aa0000;}""")

        # 1)	Дана вагітність: а) природна  б) індукована  в) ЕКЗ.
        self.DanaVagitnistLabel = QLabel('    1. Дана вагітність:')
        self.DanaVagitnistLabel.setFixedHeight(15)
        self.DanaVagitnistLabel.setFixedWidth(400)

        self.DanaVagitnisPryrodnaCheckBox = QCheckBox('Природна')
        self.DanaVagitnisPryrodnaCheckBox.setChecked(1)
        self.DanaVagitnisPryrodnaCheckBox.stateChanged.connect(
            self.DanaVagitnisPryrodnaFunc)

        self.DanaVagitnisIndykovanaCheckBox = QCheckBox('Індукована')
        self.DanaVagitnisIndykovanaCheckBox.setEnabled(0)
        self.DanaVagitnisIndykovanaCheckBox.stateChanged.connect(
            self.DanaVagitnisIndykovanaFunc)

        self.DanaVagitnisEKZCheckBox = QCheckBox('ЕКЗ')
        self.DanaVagitnisEKZCheckBox.setEnabled(0)
        self.DanaVagitnisEKZCheckBox.stateChanged.connect(
            self.DanaVagitnisEKZFunc)

        self.DanaVagitnistSplitter = QSplitter(Qt.Horizontal)
        self.DanaVagitnistSplitter.addWidget(self.DanaVagitnistLabel)
        self.DanaVagitnistSplitter.addWidget(self.DanaVagitnisPryrodnaCheckBox)
        self.DanaVagitnistSplitter.addWidget(
            self.DanaVagitnisIndykovanaCheckBox)
        self.DanaVagitnistSplitter.addWidget(self.DanaVagitnisEKZCheckBox)

        # 2)	Дана вагітність за рахунком
        self.DanaVagitnistZaRahynkomLabel = QLabel(
            '    2. Дана вагітність за рахунком:')
        self.DanaVagitnistZaRahynkomLabel.setFixedHeight(15)
        self.DanaVagitnistZaRahynkomLabel.setFixedWidth(400)

        self.DanaVagitnistZaRahynkomLineEdit = QLineEdit()
        self.DanaVagitnistZaRahynkomLineEdit.setFixedWidth(30)
        self.DanaVagitnistZaRahynkomLineEdit.setInputMask('D0')

        self.DanaVagitnistZaRahynkomSplitter = QSplitter(Qt.Horizontal)
        self.DanaVagitnistZaRahynkomSplitter.addWidget(
            self.DanaVagitnistZaRahynkomLabel)
        self.DanaVagitnistZaRahynkomSplitter.addWidget(
            self.DanaVagitnistZaRahynkomLineEdit)

        # 3)	Дані пологи за рахунком 		_____
        self.DaniPologuZaRahynkomLabel = QLabel(
            '    3. Дані пологи за рахунком:')
        self.DaniPologuZaRahynkomLabel.setFixedHeight(15)
        self.DaniPologuZaRahynkomLabel.setFixedWidth(400)

        self.DaniPologuZaRahynkomLineEdit = QLineEdit()
        self.DaniPologuZaRahynkomLineEdit.setFixedWidth(30)
        self.DaniPologuZaRahynkomLineEdit.setInputMask('D0')

        self.DaniPologuZaRahynkomSplitter = QSplitter(Qt.Horizontal)
        self.DaniPologuZaRahynkomSplitter.addWidget(
            self.DaniPologuZaRahynkomLabel)
        self.DaniPologuZaRahynkomSplitter.addWidget(
            self.DaniPologuZaRahynkomLineEdit)
        # 4)	Попередні вагітності завершились
        # а) пологами  б) аборт самовільний _____ в) аборт штучний _____

        self.PoperedniPologuZavershulusLabel = QLabel(
            '    4. Попередні вагітності завершились:')
        self.PoperedniPologuZavershulusLabel.setFixedHeight(15)
        self.PoperedniPologuZavershulusLabel.setFixedWidth(400)

        self.PoperedniPologuZavershulusPologamuCheckBox = QCheckBox('Пологами')
        self.PoperedniPologuZavershulusPologamuCheckBox.setChecked(1)
        self.PoperedniPologuZavershulusPologamuCheckBox.stateChanged.connect(
            self.PoperedniPologuZavershulusPologamuFunc)

        self.PoperedniPologuZavershulusAbortomSamovilnumCheckBox = QCheckBox(
            'Аборт самовільний')
        self.PoperedniPologuZavershulusAbortomSamovilnumCheckBox.setEnabled(0)
        self.PoperedniPologuZavershulusAbortomSamovilnumCheckBox.stateChanged.connect(
            self.PoperedniPologuZavershulusAbortomSamovilnumFunc)

        self.PoperedniPologuZavershulusAbortomShtychnumCheckBox = QCheckBox(
            'Аборт штучний')
        self.PoperedniPologuZavershulusAbortomShtychnumCheckBox.setEnabled(0)
        self.PoperedniPologuZavershulusAbortomShtychnumCheckBox.stateChanged.connect(
            self.PoperedniPologuZavershulusAbortomShtychnumFunc)

        self.PoperednihPologivNeByloP4CheckBox = QCheckBox('Не було')
        self.PoperednihPologivNeByloP4CheckBox.setEnabled(0)
        self.PoperednihPologivNeByloP4CheckBox.stateChanged.connect(
            self.PoperednihPologivNeByloP4Func)

        self.PoperedniPologuZavershulusSplitter = QSplitter(Qt.Horizontal)
        self.PoperedniPologuZavershulusSplitter.addWidget(
            self.PoperedniPologuZavershulusLabel)
        self.PoperedniPologuZavershulusSplitter.addWidget(
            self.PoperedniPologuZavershulusPologamuCheckBox)
        self.PoperedniPologuZavershulusSplitter.addWidget(
            self.PoperednihPologivNeByloP4CheckBox)
        self.PoperedniPologuZavershulusSplitter.addWidget(
            self.PoperedniPologuZavershulusAbortomSamovilnumCheckBox)
        self.PoperedniPologuZavershulusSplitter.addWidget(
            self.PoperedniPologuZavershulusAbortomShtychnumCheckBox)

        # 5)	Попередні пологи а) фізіологічні б) патологічні в)ускладені
        self.PoperedniPologuLabel = QLabel('    5. Попередні пологи:')
        self.PoperedniPologuLabel.setFixedHeight(15)
        self.PoperedniPologuLabel.setFixedWidth(400)

        self.PoperedniPologuFiziologichniCheckBox = QCheckBox('Фізіологічні')
        self.PoperedniPologuFiziologichniCheckBox.setChecked(1)
        self.PoperedniPologuFiziologichniCheckBox.setFixedWidth(100)
        self.PoperedniPologuFiziologichniCheckBox.stateChanged.connect(
            self.PoperedniPologuFiziologichniFunc)

        self.PoperednihPologivNeByloP5CheckBox = QCheckBox('Не було')
        self.PoperednihPologivNeByloP5CheckBox.setEnabled(0)
        self.PoperednihPologivNeByloP5CheckBox.stateChanged.connect(
            self.PoperednihPologivNeByloP5Func)

        self.PoperedniPologuPatologichniCheckBox = QCheckBox('Патологічні')
        self.PoperedniPologuPatologichniCheckBox.setEnabled(0)
        self.PoperedniPologuPatologichniCheckBox.show()
        self.PoperedniPologuPatologichniCheckBox.setFixedWidth(90)
        self.PoperedniPologuPatologichniCheckBox.stateChanged.connect(
            self.PoperedniPologuPatologichniFunc)

        self.PoperedniPologuYskladneniCheckBox = QCheckBox('Ускладені')
        self.PoperedniPologuYskladneniCheckBox.setEnabled(0)
        self.PoperedniPologuYskladneniCheckBox.show()
        self.PoperedniPologuYskladneniCheckBox.setFixedWidth(70)
        self.PoperedniPologuYskladneniCheckBox.stateChanged.connect(
            self.PoperedniPologuYskladneniFunc)

        self.PoperedniPologuYskladneniLineEdit = QLineEdit()
        self.PoperedniPologuYskladneniLineEdit.setMinimumWidth(150)
        self.PoperedniPologuYskladneniLineEdit.hide()

        self.PoperedniPologuSplitter = QSplitter(Qt.Horizontal)
        self.PoperedniPologuSplitter.addWidget(self.PoperedniPologuLabel)
        self.PoperedniPologuSplitter.addWidget(
            self.PoperedniPologuFiziologichniCheckBox)
        self.PoperedniPologuSplitter.addWidget(
            self.PoperednihPologivNeByloP5CheckBox)
        self.PoperedniPologuSplitter.addWidget(
            self.PoperedniPologuPatologichniCheckBox)
        self.PoperedniPologuSplitter.addWidget(
            self.PoperedniPologuYskladneniCheckBox)
        self.PoperedniPologuSplitter.addWidget(
            self.PoperedniPologuYskladneniLineEdit)

        # 6)	Наявність живих дітей а) так б) ні
        self.NayavnistGuvyhDiteyLabel = QLabel('    6. Наявність живих дітей:')
        self.NayavnistGuvyhDiteyLabel.setFixedHeight(15)
        self.NayavnistGuvyhDiteyLabel.setFixedWidth(400)
        self.NayavnistGuvyhDiteyLabel.show()

        self.NayavnistGuvyhDiteyYesCheckBox = QCheckBox('Так')
        self.NayavnistGuvyhDiteyYesCheckBox.setFixedWidth(100)
        self.NayavnistGuvyhDiteyYesCheckBox.setEnabled(0)
        self.NayavnistGuvyhDiteyYesCheckBox.show()
        self.NayavnistGuvyhDiteyYesCheckBox.stateChanged.connect(
            self.NayavnistGuvyhDiteyYesFunc)

        self.NayavnistGuvyhDiteyNoCheckBox = QCheckBox('Ні')
        self.NayavnistGuvyhDiteyNoCheckBox.setChecked(1)
        self.NayavnistGuvyhDiteyNoCheckBox.show()
        self.NayavnistGuvyhDiteyNoCheckBox.stateChanged.connect(
            self.NayavnistGuvyhDiteyNoFunc)

        self.NayavnistGuvyhDiteySplitter = QSplitter(Qt.Horizontal)
        self.NayavnistGuvyhDiteySplitter.addWidget(
            self.NayavnistGuvyhDiteyLabel)
        self.NayavnistGuvyhDiteySplitter.addWidget(
            self.NayavnistGuvyhDiteyYesCheckBox)
        self.NayavnistGuvyhDiteySplitter.addWidget(
            self.NayavnistGuvyhDiteyNoCheckBox)

        # финальный сплиттер пункта IV    Акушерський анамнез.

        self.PynkIVSplitter = QSplitter(Qt.Vertical)
        self.PynkIVSplitter.addWidget(self.AkysherskiiAnamnezLabel)
        self.PynkIVSplitter.addWidget(self.DanaVagitnistSplitter)
        self.PynkIVSplitter.addWidget(self.DanaVagitnistZaRahynkomSplitter)
        self.PynkIVSplitter.addWidget(self.DaniPologuZaRahynkomSplitter)
        self.PynkIVSplitter.addWidget(self.PoperedniPologuZavershulusSplitter)
        self.PynkIVSplitter.addWidget(self.PoperedniPologuSplitter)
        self.PynkIVSplitter.addWidget(self.NayavnistGuvyhDiteySplitter)

        # V. Перебіг даної вагітності.
        self.PereBigDanoiVagitnostiLabel = QLabel(
            '\n  V) Перебіг даної вагітності.')
        self.PereBigDanoiVagitnostiLabel.setFixedHeight(30)
        self.PereBigDanoiVagitnostiLabel.setStyleSheet(
            """QLabel{font-size:8pt; font-weight:600; color:#aa0000;}""")

        # 1) Вагітність: а) одноплідна;  б) багатоплідна
        self.VagitnistLabel = QLabel('    1. Вагітність:')
        self.VagitnistLabel.setFixedHeight(15)
        self.VagitnistLabel.setFixedWidth(400)

        self.VagitnistOdnoplidnaCheckBox = QCheckBox('Одноплідна')
        self.VagitnistOdnoplidnaCheckBox.setFixedWidth(100)
        self.VagitnistOdnoplidnaCheckBox.setChecked(1)
        self.VagitnistOdnoplidnaCheckBox.stateChanged.connect(
            self.VagitnistOdnoplidnaFunc)

        self.VagitnistBagatodnoplidnaCheckBox = QCheckBox('Багатоплідна')
        self.VagitnistBagatodnoplidnaCheckBox.setEnabled(0)
        self.VagitnistBagatodnoplidnaCheckBox.stateChanged.connect(
            self.VagitnistBagatoplidnaFunc)

        self.VagitnistSplitter = QSplitter(Qt.Horizontal)
        self.VagitnistSplitter.addWidget(self.VagitnistLabel)
        self.VagitnistSplitter.addWidget(self.VagitnistOdnoplidnaCheckBox)
        self.VagitnistSplitter.addWidget(self.VagitnistBagatodnoplidnaCheckBox)

        # 2) На обліку в жіночій консультації з ______тиж
        self.NaOblikyVGinochiiKonsyltaciiLabel = QLabel(
            '    2. На обліку в жіночій консультації з:')
        self.NaOblikyVGinochiiKonsyltaciiLabel.setFixedHeight(15)
        self.NaOblikyVGinochiiKonsyltaciiLabel.setFixedWidth(400)
        # self.NaOblikyVGinochiiKonsyltaciiLabel.show()

        self.NaOblikyVGinochiiKonsyltaciiLineEdit = QLineEdit()
        self.NaOblikyVGinochiiKonsyltaciiLineEdit.setInputMask('D0')
        self.NaOblikyVGinochiiKonsyltaciiLineEdit.setFixedWidth(20)

        self.NaOblikyVGinochiiKonsyltaciiLabel2 = QLabel('тижнів')
        self.NaOblikyVGinochiiKonsyltaciiLabel2.setFixedHeight(15)

        self.NaOblikyVGinochiiKonsyltaciiSplitter = QSplitter(Qt.Horizontal)
        self.NaOblikyVGinochiiKonsyltaciiSplitter.addWidget(
            self.NaOblikyVGinochiiKonsyltaciiLabel)
        self.NaOblikyVGinochiiKonsyltaciiSplitter.addWidget(
            self.NaOblikyVGinochiiKonsyltaciiLineEdit)
        self.NaOblikyVGinochiiKonsyltaciiSplitter.addWidget(
            self.NaOblikyVGinochiiKonsyltaciiLabel2)

        # ) Загроза переривання вагітності: а) ні  б) в терміні вагітності ____.
        self.ZagrozaPereruvannaVagitnostiLabel = QLabel(
            '    3. Загроза переривання вагітності:')
        self.ZagrozaPereruvannaVagitnostiLabel.setFixedHeight(15)
        self.ZagrozaPereruvannaVagitnostiLabel.setFixedWidth(400)

        self.ZagrozaPereruvannaVagitnostiNoCheckBox = QCheckBox('Ні')
        self.ZagrozaPereruvannaVagitnostiNoCheckBox.setChecked(1)
        self.ZagrozaPereruvannaVagitnostiNoCheckBox.show()
        self.ZagrozaPereruvannaVagitnostiNoCheckBox.setFixedWidth(40)
        self.ZagrozaPereruvannaVagitnostiNoCheckBox.stateChanged.connect(
            self.ZagrozaPereruvannaVagitnostiNoFunc)

        self.ZagrozaPereruvannaVagitnostiYesCheckBox = QCheckBox('Так')
        self.ZagrozaPereruvannaVagitnostiYesCheckBox.setFixedWidth(100)
        self.ZagrozaPereruvannaVagitnostiYesCheckBox.setEnabled(0)
        self.ZagrozaPereruvannaVagitnostiYesCheckBox.stateChanged.connect(
            self.ZagrozaPereruvannaVagitnostiYesFunc)

        self.ZagrozaPereruvannaVagitnostiYTerminiLabel = QLabel(
            'В терміні вагітності:')
        self.ZagrozaPereruvannaVagitnostiYTerminiLabel.setFixedWidth(40)
        self.ZagrozaPereruvannaVagitnostiYTerminiLabel.hide()

        self.ZagrozaPereruvannaVagitnostiYTerminiLineEdit = QLineEdit()
        self.ZagrozaPereruvannaVagitnostiYTerminiLineEdit.hide()
        self.ZagrozaPereruvannaVagitnostiYTerminiLineEdit.setInputMask('D0')

        self.ZagrozaPereruvannaVagitnostiSplitter = QSplitter(Qt.Horizontal)
        self.ZagrozaPereruvannaVagitnostiSplitter.addWidget(
            self.ZagrozaPereruvannaVagitnostiLabel)
        self.ZagrozaPereruvannaVagitnostiSplitter.addWidget(
            self.ZagrozaPereruvannaVagitnostiNoCheckBox)
        self.ZagrozaPereruvannaVagitnostiSplitter.addWidget(
            self.ZagrozaPereruvannaVagitnostiYesCheckBox)
        self.ZagrozaPereruvannaVagitnostiSplitter.addWidget(
            self.ZagrozaPereruvannaVagitnostiYTerminiLabel)
        self.ZagrozaPereruvannaVagitnostiSplitter.addWidget(
            self.ZagrozaPereruvannaVagitnostiYTerminiLineEdit)

        # ) Загроза передчасних пологів:    а) ні  б) в терміні вагітності  ____.
        self.ZagrozaPeredchasnuhPologivLabel = QLabel(
            '    4. Загроза передчасних пологів:')
        self.ZagrozaPeredchasnuhPologivLabel.setFixedHeight(15)
        self.ZagrozaPeredchasnuhPologivLabel.setFixedWidth(400)

        self.ZagrozaPeredchasnuhPologivNoCheckBox = QCheckBox('Ні')
        self.ZagrozaPeredchasnuhPologivNoCheckBox.setChecked(1)
        self.ZagrozaPeredchasnuhPologivNoCheckBox.show()
        self.ZagrozaPeredchasnuhPologivNoCheckBox.setFixedWidth(40)
        self.ZagrozaPeredchasnuhPologivNoCheckBox.stateChanged.connect(
            self.ZagrozaPeredchasnuhPologivNoFunc)

        self.ZagrozaPeredchasnuhPologivYesCheckBox = QCheckBox('Так')
        self.ZagrozaPeredchasnuhPologivYesCheckBox.setFixedWidth(100)
        self.ZagrozaPeredchasnuhPologivYesCheckBox.setEnabled(0)
        self.ZagrozaPeredchasnuhPologivYesCheckBox.stateChanged.connect(
            self.ZagrozaPeredchasnuhPologivYesFunc)

        self.ZagrozaPeredchasnuhPologivTerminiLabel = QLabel(
            'В терміні вагітності:')
        self.ZagrozaPeredchasnuhPologivTerminiLabel.setFixedWidth(40)
        self.ZagrozaPeredchasnuhPologivTerminiLabel.hide()

        self.ZagrozaPeredchasnuhPologivYTerminiLineEdit = QLineEdit()
        self.ZagrozaPeredchasnuhPologivYTerminiLineEdit.hide()
        self.ZagrozaPeredchasnuhPologivYTerminiLineEdit.setInputMask('D0')

        self.ZagrozaPeredchasnuhPologivSplitter = QSplitter(Qt.Horizontal)
        self.ZagrozaPeredchasnuhPologivSplitter.addWidget(
            self.ZagrozaPeredchasnuhPologivLabel)
        self.ZagrozaPeredchasnuhPologivSplitter.addWidget(
            self.ZagrozaPeredchasnuhPologivNoCheckBox)
        self.ZagrozaPeredchasnuhPologivSplitter.addWidget(
            self.ZagrozaPeredchasnuhPologivYesCheckBox)
        self.ZagrozaPeredchasnuhPologivSplitter.addWidget(
            self.ZagrozaPeredchasnuhPologivTerminiLabel)
        self.ZagrozaPeredchasnuhPologivSplitter.addWidget(
            self.ZagrozaPeredchasnuhPologivYTerminiLineEdit)

        # 4.1 а відшарування хоріона; б) кровомазання в) ІЦН
        self.ZagrozaPereruvannaVagitnostiP41Label = QLabel('       4.1.')
        self.ZagrozaPereruvannaVagitnostiP41Label.setEnabled(0)

        self.ZagrozaPereruvannaVagitnostiVidsharyvannaHorionaCheckBox = QCheckBox(
            'Відшарування хоріона')
        self.ZagrozaPereruvannaVagitnostiVidsharyvannaHorionaCheckBox.setEnabled(
            0)

        self.ZagrozaPereruvannaVagitnostiKrovomazannaCheckBox = QCheckBox(
            'Кровомазання')
        self.ZagrozaPereruvannaVagitnostiKrovomazannaCheckBox.setEnabled(0)

        self.ZagrozaPereruvannaVagitnostiICNCheckBox = QCheckBox('ІЦН')
        self.ZagrozaPereruvannaVagitnostiICNCheckBox.setEnabled(0)

        self.ZagrozaPereruvannaVagitnostiP41Splitter = QSplitter(Qt.Horizontal)
        self.ZagrozaPereruvannaVagitnostiP41Splitter.addWidget(
            self.ZagrozaPereruvannaVagitnostiP41Label)
        self.ZagrozaPereruvannaVagitnostiP41Splitter.addWidget(
            self.ZagrozaPereruvannaVagitnostiVidsharyvannaHorionaCheckBox)
        self.ZagrozaPereruvannaVagitnostiP41Splitter.addWidget(
            self.ZagrozaPereruvannaVagitnostiKrovomazannaCheckBox)
        self.ZagrozaPereruvannaVagitnostiP41Splitter.addWidget(
            self.ZagrozaPereruvannaVagitnostiICNCheckBox)

        # 5) Гестоз І половини вагітності: а) так  б) ні.
        self.GestozIPolovunuVagitnostiLabel = QLabel(
            '    5. Гестоз І половини вагітності:')
        self.GestozIPolovunuVagitnostiLabel.setFixedHeight(15)
        self.GestozIPolovunuVagitnostiLabel.setFixedWidth(400)
        self.GestozIPolovunuVagitnostiLabel.show()

        self.GestozIPolovunuVagitnostiYesCheckBox = QCheckBox('Так')
        self.GestozIPolovunuVagitnostiYesCheckBox.setFixedWidth(100)
        self.GestozIPolovunuVagitnostiYesCheckBox.setEnabled(0)
        self.GestozIPolovunuVagitnostiYesCheckBox.show()
        self.GestozIPolovunuVagitnostiYesCheckBox.stateChanged.connect(
            self.GestozIPolovunuVagitnostiYesFunc)

        self.GestozIPolovunuVagitnostiNoCheckBox = QCheckBox('Ні')
        self.GestozIPolovunuVagitnostiNoCheckBox.setFixedWidth(100)
        self.GestozIPolovunuVagitnostiNoCheckBox.setChecked(1)
        self.GestozIPolovunuVagitnostiNoCheckBox.show()
        self.GestozIPolovunuVagitnostiNoCheckBox.stateChanged.connect(
            self.GestozIPolovunuVagitnostiNoFunc)

        self.GestozIPolovunuVagitnostiSplitter = QSplitter(Qt.Horizontal)
        self.GestozIPolovunuVagitnostiSplitter.addWidget(
            self.GestozIPolovunuVagitnostiLabel)
        self.GestozIPolovunuVagitnostiSplitter.addWidget(
            self.GestozIPolovunuVagitnostiNoCheckBox)
        self.GestozIPolovunuVagitnostiSplitter.addWidget(
            self.GestozIPolovunuVagitnostiYesCheckBox)

        # 6) Інші причини зневоднення: а) так  б) ні; в)____________________
        self.InshiPruchynyZnevodnennaLabel = QLabel(
            '    6. Інші причини зневоднення:')
        self.InshiPruchynyZnevodnennaLabel.setFixedHeight(15)
        self.InshiPruchynyZnevodnennaLabel.setFixedWidth(400)

        self.InshiPruchynyZnevodnennaNoCheckBox = QCheckBox('Ні')
        self.InshiPruchynyZnevodnennaNoCheckBox.setChecked(1)
        self.InshiPruchynyZnevodnennaNoCheckBox.show()
        self.InshiPruchynyZnevodnennaNoCheckBox.setFixedWidth(40)
        self.InshiPruchynyZnevodnennaNoCheckBox.stateChanged.connect(
            self.InshiPruchynyZnevodnennaNoFunc)

        self.InshiPruchynyZnevodnennaYesCheckBox = QCheckBox('Так')
        self.InshiPruchynyZnevodnennaYesCheckBox.setFixedWidth(50)
        self.InshiPruchynyZnevodnennaYesCheckBox.setEnabled(0)
        self.InshiPruchynyZnevodnennaYesCheckBox.stateChanged.connect(
            self.InshiPruchynyZnevodnennaYesFunc)

        self.InshiPruchynyZnevodnennaVarVCheckBox = QCheckBox('Інше:')
        self.InshiPruchynyZnevodnennaVarVCheckBox.setFixedWidth(50)
        self.InshiPruchynyZnevodnennaVarVCheckBox.setChecked(0)
        self.InshiPruchynyZnevodnennaVarVCheckBox.setEnabled(0)
        self.InshiPruchynyZnevodnennaVarVCheckBox.stateChanged.connect(
            self.InshiPruchynyZnevodnennaVarVFunc)

        self.InshiPruchynyZnevodnennaVarVLineEdit = QLineEdit()
        self.InshiPruchynyZnevodnennaVarVLineEdit.hide()
        self.InshiPruchynyZnevodnennaVarVLineEdit.setMinimumWidth(200)

        self.InshiPruchynyZnevodnennaSplitter = QSplitter(Qt.Horizontal)
        self.InshiPruchynyZnevodnennaSplitter.addWidget(
            self.InshiPruchynyZnevodnennaLabel)
        self.InshiPruchynyZnevodnennaSplitter.addWidget(
            self.InshiPruchynyZnevodnennaNoCheckBox)
        self.InshiPruchynyZnevodnennaSplitter.addWidget(
            self.InshiPruchynyZnevodnennaYesCheckBox)
        self.InshiPruchynyZnevodnennaSplitter.addWidget(
            self.InshiPruchynyZnevodnennaVarVCheckBox)
        self.InshiPruchynyZnevodnennaSplitter.addWidget(
            self.InshiPruchynyZnevodnennaVarVLineEdit)

        # 7) Гестоз II половини вагітності  а) ні, б) прееклампсія легкого ст   в)середнього ст, г) важкого ст
        self.GestozIIPolovunuVagitnostiLabel = QLabel(
            '    7. Гестоз II половини вагітності:')
        self.GestozIIPolovunuVagitnostiLabel.setFixedHeight(15)
        self.GestozIIPolovunuVagitnostiLabel.setFixedWidth(400)

        self.GestozIIPolovunuVagitnostiNoCheckBox = QCheckBox('Ні')
        self.GestozIIPolovunuVagitnostiNoCheckBox.setChecked(1)
        self.GestozIIPolovunuVagitnostiNoCheckBox.setFixedWidth(40)
        self.GestozIIPolovunuVagitnostiNoCheckBox.show()
        self.GestozIIPolovunuVagitnostiNoCheckBox.stateChanged.connect(
            self.GestozIIPolovunuVagitnostiNoFunc)

        self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox = QCheckBox(
            'Прееклампсія легкого ступеня')
        # self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.setFixedWidth(50)
        self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.setChecked(
            0)
        self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.setEnabled(
            0)
        self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.stateChanged.connect(
            self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStFunc)

        self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox = QCheckBox(
            'Середнього ступеня')
        # self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.setFixedWidth(50)
        self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.setChecked(
            0)
        self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.setEnabled(
            0)
        self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.stateChanged.connect(
            self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStFunc)

        self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox = QCheckBox(
            'Важкого ступеня')
        # self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.setFixedWidth(50)
        self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.setChecked(
            0)
        self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.setEnabled(
            0)
        self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.stateChanged.connect(
            self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStFunc)

        self.GestozIIPolovunuVagitnostiSplitter = QSplitter(Qt.Horizontal)
        self.GestozIIPolovunuVagitnostiSplitter.addWidget(
            self.GestozIIPolovunuVagitnostiLabel)
        self.GestozIIPolovunuVagitnostiSplitter.addWidget(
            self.GestozIIPolovunuVagitnostiNoCheckBox)
        self.GestozIIPolovunuVagitnostiSplitter.addWidget(
            self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox)
        self.GestozIIPolovunuVagitnostiSplitter.addWidget(
            self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox)
        self.GestozIIPolovunuVagitnostiSplitter.addWidget(
            self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox)

        # 8) Гестоз ІІ половини вагітності діагностовано в терміні________.
        self.GestozIIPolovunuDiagnostovanoVTerminiLabel = QLabel(
            '    8. Гестоз II половини вагітності діагностовано в терміні:')
        self.GestozIIPolovunuDiagnostovanoVTerminiLabel.setFixedHeight(15)
        self.GestozIIPolovunuDiagnostovanoVTerminiLabel.setFixedWidth(400)
        self.GestozIIPolovunuDiagnostovanoVTerminiLabel.setEnabled(0)

        self.GestozIIPolovunuDiagnostovanoVTerminiLineEdit = QLineEdit()
        self.GestozIIPolovunuDiagnostovanoVTerminiLineEdit.setEnabled(0)
        self.GestozIIPolovunuDiagnostovanoVTerminiLineEdit.setInputMask('D0')
        self.GestozIIPolovunuDiagnostovanoVTerminiLineEdit.setFixedWidth(40)

        self.GestozIIPolovunuDiagnostovanoVTerminiSplitter = QSplitter(
            Qt.Horizontal)
        self.GestozIIPolovunuDiagnostovanoVTerminiSplitter.addWidget(
            self.GestozIIPolovunuDiagnostovanoVTerminiLabel)
        self.GestozIIPolovunuDiagnostovanoVTerminiSplitter.addWidget(
            self.GestozIIPolovunuDiagnostovanoVTerminiLineEdit)

        # 9) Винекнення ТЕУ а) так  б) ні.
        self.VunuknennaTEYLabel = QLabel('    9. Винекнення ТЕУ:')
        self.VunuknennaTEYLabel.setFixedHeight(15)
        self.VunuknennaTEYLabel.setFixedWidth(400)
        self.VunuknennaTEYLabel.show()

        self.VunuknennaTEYYesCheckBox = QCheckBox('Так')

        self.VunuknennaTEYYesCheckBox.setEnabled(0)
        self.VunuknennaTEYYesCheckBox.show()
        self.VunuknennaTEYYesCheckBox.stateChanged.connect(
            self.VunuknennaTEYYesFunc)

        self.VunuknennaTEYNoCheckBox = QCheckBox('Ні')
        self.VunuknennaTEYNoCheckBox.setChecked(1)
        self.VunuknennaTEYNoCheckBox.setFixedWidth(100)
        self.VunuknennaTEYNoCheckBox.stateChanged.connect(
            self.VunuknennaTEYNoFunc)

        self.VunuknennaTEYSplitter = QSplitter(Qt.Horizontal)
        self.VunuknennaTEYSplitter.addWidget(self.VunuknennaTEYLabel)
        self.VunuknennaTEYSplitter.addWidget(self.VunuknennaTEYNoCheckBox)
        self.VunuknennaTEYSplitter.addWidget(self.VunuknennaTEYYesCheckBox)
        # 9.1. Вид ТЕУ______________________________________________
        self.VudTEYLabel = QLabel('    9.1. Вид ТЕУ:')
        self.VudTEYLabel.setFixedHeight(15)
        self.VudTEYLabel.setFixedWidth(400)
        self.VudTEYLabel.show()
        self.VudTEYLabel.setEnabled(0)

        self.VudTEYLineEdit = QLineEdit()
        self.VudTEYLineEdit.setEnabled(0)

        self.VudTEYSplitter = QSplitter(Qt.Horizontal)
        self.VudTEYSplitter.addWidget(self.VudTEYLabel)
        self.VudTEYSplitter.addWidget(self.VudTEYLineEdit)

        # 9.2. термін вагітності __________тиж
        self.TEYTerminVagitnostiLabel = QLabel(
            '    9.2. Термін вагітності (тижнів):')
        self.TEYTerminVagitnostiLabel.setFixedHeight(15)
        self.TEYTerminVagitnostiLabel.setFixedWidth(400)
        self.TEYTerminVagitnostiLabel.show()
        self.TEYTerminVagitnostiLabel.setEnabled(0)

        self.TEYTerminVagitnostiLineEdit = QLineEdit()
        self.TEYTerminVagitnostiLineEdit.setEnabled(0)
        self.TEYTerminVagitnostiLineEdit.setFixedWidth(40)
        self.TEYTerminVagitnostiLineEdit.setInputMask('D0')

        self.TEYTerminVagitnostiplitter = QSplitter(Qt.Horizontal)
        self.TEYTerminVagitnostiplitter.addWidget(
            self.TEYTerminVagitnostiLabel)
        self.TEYTerminVagitnostiplitter.addWidget(
            self.TEYTerminVagitnostiLineEdit)

        # 10) Багатоводдя: а) ні  б) помірне в) виражене
        self.BagatovoddaLabel = QLabel('    10. Багатоводдя:')
        self.BagatovoddaLabel.setFixedHeight(15)
        self.BagatovoddaLabel.setFixedWidth(400)
        self.BagatovoddaLabel.show()

        self.BagatovoddaNoCheckBox = QCheckBox('Ні')
        self.BagatovoddaNoCheckBox.setChecked(1)
        self.BagatovoddaNoCheckBox.stateChanged.connect(self.BagatovoddaNoFunc)

        self.BagatovoddaPomirneCheckBox = QCheckBox('Помірне')
        self.BagatovoddaPomirneCheckBox.setFixedWidth(100)
        self.BagatovoddaPomirneCheckBox.setEnabled(0)
        self.BagatovoddaPomirneCheckBox.stateChanged.connect(
            self.BagatovoddaPomirneFunc)

        self.BagatovoddaVurageneCheckBox = QCheckBox('Виражене')
        self.BagatovoddaVurageneCheckBox.setEnabled(0)
        self.BagatovoddaVurageneCheckBox.stateChanged.connect(
            self.BagatovoddaVurageneFunc)

        self.BagatovoddaSplitter = QSplitter(Qt.Horizontal)
        self.BagatovoddaSplitter.addWidget(self.BagatovoddaLabel)
        self.BagatovoddaSplitter.addWidget(self.BagatovoddaNoCheckBox)
        self.BagatovoddaSplitter.addWidget(self.BagatovoddaPomirneCheckBox)
        self.BagatovoddaSplitter.addWidget(self.BagatovoddaVurageneCheckBox)

        # 10.1Багатоводдя діагностовано з терміну вагітності ____________.
        self.BagatovoddaDiagnostovanoVTerminVagitnostiLabel = QLabel(
            '    10.1. Багатоводдя діагностовано з терміну вагітності (тижнів):'
        )
        self.BagatovoddaDiagnostovanoVTerminVagitnostiLabel.setFixedHeight(15)
        self.BagatovoddaDiagnostovanoVTerminVagitnostiLabel.setFixedWidth(400)
        self.BagatovoddaDiagnostovanoVTerminVagitnostiLabel.show()
        self.BagatovoddaDiagnostovanoVTerminVagitnostiLabel.setEnabled(0)

        self.BagatovoddaDiagnostovanoVTerminVagitnostiLineEdit = QLineEdit()
        self.BagatovoddaDiagnostovanoVTerminVagitnostiLineEdit.setEnabled(0)
        self.BagatovoddaDiagnostovanoVTerminVagitnostiLineEdit.setFixedWidth(
            40)
        self.BagatovoddaDiagnostovanoVTerminVagitnostiLineEdit.setInputMask(
            'D0')

        self.BagatovoddaDiagnostovanoVTerminVagitnostiSplitter = QSplitter(
            Qt.Horizontal)
        self.BagatovoddaDiagnostovanoVTerminVagitnostiSplitter.addWidget(
            self.BagatovoddaDiagnostovanoVTerminVagitnostiLabel)
        self.BagatovoddaDiagnostovanoVTerminVagitnostiSplitter.addWidget(
            self.BagatovoddaDiagnostovanoVTerminVagitnostiLineEdit)

        # 11) Маловоддя: а) ні  б) помірне  в) виражене
        self.MaloVoddaLabel = QLabel('    11. Маловоддя:')
        self.MaloVoddaLabel.setFixedHeight(15)
        self.MaloVoddaLabel.setFixedWidth(400)
        self.MaloVoddaLabel.show()

        self.MaloVoddaNoCheckBox = QCheckBox('Ні')
        self.MaloVoddaNoCheckBox.setChecked(1)
        self.MaloVoddaNoCheckBox.stateChanged.connect(self.MaloVoddaNoFunc)

        self.MaloVoddaPomirneCheckBox = QCheckBox('Помірне')
        self.MaloVoddaPomirneCheckBox.setFixedWidth(100)
        self.MaloVoddaPomirneCheckBox.setEnabled(0)
        self.MaloVoddaPomirneCheckBox.stateChanged.connect(
            self.MaloVoddaPomirneFunc)

        self.MaloVoddaVurageneCheckBox = QCheckBox('Виражене')
        self.MaloVoddaVurageneCheckBox.setEnabled(0)
        self.MaloVoddaVurageneCheckBox.stateChanged.connect(
            self.MaloVoddaVurageneFunc)

        self.MaloVoddaSplitter = QSplitter(Qt.Horizontal)
        self.MaloVoddaSplitter.addWidget(self.MaloVoddaLabel)
        self.MaloVoddaSplitter.addWidget(self.MaloVoddaNoCheckBox)
        self.MaloVoddaSplitter.addWidget(self.MaloVoddaPomirneCheckBox)
        self.MaloVoddaSplitter.addWidget(self.MaloVoddaVurageneCheckBox)

        # 11.1 Маловоддя діагностовано з терміну вагітності ____________.
        self.MaloVoddaDiagnostovanoVTerminVagitnostiLabel = QLabel(
            '    11.1. Маловоддя діагностовано з терміну вагітності (тижнів):')
        self.MaloVoddaDiagnostovanoVTerminVagitnostiLabel.setFixedHeight(15)
        self.MaloVoddaDiagnostovanoVTerminVagitnostiLabel.setFixedWidth(400)
        self.MaloVoddaDiagnostovanoVTerminVagitnostiLabel.show()
        self.MaloVoddaDiagnostovanoVTerminVagitnostiLabel.setEnabled(0)

        self.MaloVoddaDiagnostovanoVTerminVagitnostiLineEdit = QLineEdit()
        self.MaloVoddaDiagnostovanoVTerminVagitnostiLineEdit.setEnabled(0)
        self.MaloVoddaDiagnostovanoVTerminVagitnostiLineEdit.setFixedWidth(40)
        self.MaloVoddaDiagnostovanoVTerminVagitnostiLineEdit.setInputMask('D0')

        self.MaloVoddaDiagnostovanoVTerminVagitnostiSplitter = QSplitter(
            Qt.Horizontal)
        self.MaloVoddaDiagnostovanoVTerminVagitnostiSplitter.addWidget(
            self.MaloVoddaDiagnostovanoVTerminVagitnostiLabel)
        self.MaloVoddaDiagnostovanoVTerminVagitnostiSplitter.addWidget(
            self.MaloVoddaDiagnostovanoVTerminVagitnostiLineEdit)

        # 12) Дистрес плода (за доплерометрією): а) ні; б) в ст. компенсації; в) в ст. субкомпенсації;
        # г) в ст. декомпенсації
        self.DustressPlodaLabel = QLabel(
            '    12. Дистрес плода (за доплерометрією):')
        self.DustressPlodaLabel.setFixedHeight(15)
        self.DustressPlodaLabel.setFixedWidth(400)
        self.DustressPlodaLabel.show()

        self.DustressPlodaNoCheckBox = QCheckBox('Ні')
        self.DustressPlodaNoCheckBox.setChecked(1)
        self.DustressPlodaNoCheckBox.stateChanged.connect(
            self.DustressPlodaNoFunc)

        self.DustressPlodaVKompensaciiCheckBox = QCheckBox(
            'В стадіі компенсації')
        self.DustressPlodaVKompensaciiCheckBox.setEnabled(0)
        self.DustressPlodaVKompensaciiCheckBox.stateChanged.connect(
            self.DustressPlodaVKompensaciiFunc)

        self.DustressPlodaVSubKompensaciiCheckBox = QCheckBox(
            'В стадіі субкомпенсації')
        self.DustressPlodaVSubKompensaciiCheckBox.setEnabled(0)
        self.DustressPlodaVSubKompensaciiCheckBox.stateChanged.connect(
            self.DustressPlodaVSubKompensaciiFunc)

        self.DustressPlodaVDekompensaciiCheckBox = QCheckBox(
            'В стадіі декомпенсації')
        self.DustressPlodaVDekompensaciiCheckBox.setEnabled(0)
        self.DustressPlodaVDekompensaciiCheckBox.stateChanged.connect(
            self.DustressPlodaVDekompensaciiFunc)

        self.DustressPlodaSplitter = QSplitter(Qt.Horizontal)
        self.DustressPlodaSplitter.addWidget(self.DustressPlodaLabel)
        self.DustressPlodaSplitter.addWidget(self.DustressPlodaNoCheckBox)
        self.DustressPlodaSplitter.addWidget(
            self.DustressPlodaVKompensaciiCheckBox)
        self.DustressPlodaSplitter.addWidget(
            self.DustressPlodaVSubKompensaciiCheckBox)
        self.DustressPlodaSplitter.addWidget(
            self.DustressPlodaVDekompensaciiCheckBox)

        # 13) Затримка росту плода: 		в терміні _______тиж
        # а) ні  б) симетрична форма в) асиметрична форма
        self.ZatrumkaRozvutkyPlodaLabel = QLabel(
            '    13. Затримка росту плода:')
        self.ZatrumkaRozvutkyPlodaLabel.setFixedHeight(15)
        self.ZatrumkaRozvutkyPlodaLabel.setFixedWidth(400)
        self.ZatrumkaRozvutkyPlodaLabel.show()

        self.ZatrumkaRozvutkyPlodaNoCheckBox = QCheckBox('Ні')
        self.ZatrumkaRozvutkyPlodaNoCheckBox.setChecked(1)
        self.ZatrumkaRozvutkyPlodaNoCheckBox.stateChanged.connect(
            self.ZatrumkaRozvutkyPlodaNoFunc)

        self.ZatrumkaRozvutkyPlodaSumetrychnaFormaCheckBox = QCheckBox(
            'Симетрична форма')
        self.ZatrumkaRozvutkyPlodaSumetrychnaFormaCheckBox.setEnabled(0)
        self.ZatrumkaRozvutkyPlodaSumetrychnaFormaCheckBox.stateChanged.connect(
            self.ZatrumkaRozvutkyPlodaSumetrychnaFormaFunc)

        self.ZatrumkaRozvutkyPlodaAsumetruchnaFormaCheckBox = QCheckBox(
            'Асиметрична форма')
        self.ZatrumkaRozvutkyPlodaAsumetruchnaFormaCheckBox.setEnabled(0)
        self.ZatrumkaRozvutkyPlodaAsumetruchnaFormaCheckBox.stateChanged.connect(
            self.ZatrumkaRozvutkyPlodaAsumetruchnaFormaFunc)

        self.ZatrumkaRozvutkyPlodaVTerminiLabel = QLabel('В терміні (тижнів):')
        self.ZatrumkaRozvutkyPlodaVTerminiLabel.setEnabled(0)
        self.ZatrumkaRozvutkyPlodaVTerminiLabel.hide()

        self.ZatrumkaRozvutkyPlodaVTerminiLineEdit = QLineEdit()
        self.ZatrumkaRozvutkyPlodaVTerminiLineEdit.setEnabled(0)
        self.ZatrumkaRozvutkyPlodaVTerminiLineEdit.setInputMask('D0')
        self.ZatrumkaRozvutkyPlodaVTerminiLineEdit.hide()

        self.ZatrumkaRozvutkyPlodaSplitter = QSplitter(Qt.Horizontal)
        self.ZatrumkaRozvutkyPlodaSplitter.addWidget(
            self.ZatrumkaRozvutkyPlodaLabel)
        self.ZatrumkaRozvutkyPlodaSplitter.addWidget(
            self.ZatrumkaRozvutkyPlodaNoCheckBox)
        self.ZatrumkaRozvutkyPlodaSplitter.addWidget(
            self.ZatrumkaRozvutkyPlodaSumetrychnaFormaCheckBox)
        self.ZatrumkaRozvutkyPlodaSplitter.addWidget(
            self.ZatrumkaRozvutkyPlodaAsumetruchnaFormaCheckBox)
        self.ZatrumkaRozvutkyPlodaSplitter.addWidget(
            self.ZatrumkaRozvutkyPlodaVTerminiLabel)
        self.ZatrumkaRozvutkyPlodaSplitter.addWidget(
            self.ZatrumkaRozvutkyPlodaVTerminiLineEdit)

        # 14) Наявність системної інфекції : 		а) так; б) ні
        self.NajavnistSustemnoiInfekciiLabel = QLabel(
            '    14. Наявність системної інфекції:')
        self.NajavnistSustemnoiInfekciiLabel.setFixedHeight(15)
        self.NajavnistSustemnoiInfekciiLabel.setFixedWidth(400)

        self.NajavnistSustemnoiInfekciiNoCheckBox = QCheckBox('Ні')
        self.NajavnistSustemnoiInfekciiNoCheckBox.setChecked(1)
        self.NajavnistSustemnoiInfekciiNoCheckBox.setFixedWidth(100)
        self.NajavnistSustemnoiInfekciiNoCheckBox.stateChanged.connect(
            self.NajavnistSustemnoiInfekciiNoFunc)

        self.NajavnistSustemnoiInfekciiYesCheckBox = QCheckBox('Так')
        self.NajavnistSustemnoiInfekciiYesCheckBox.setEnabled(0)
        self.NajavnistSustemnoiInfekciiYesCheckBox.stateChanged.connect(
            self.NajavnistSustemnoiInfekciiYesFunc)

        self.NajavnistSustemnoiInfekciiSplitter = QSplitter(Qt.Horizontal)
        self.NajavnistSustemnoiInfekciiSplitter.addWidget(
            self.NajavnistSustemnoiInfekciiLabel)
        self.NajavnistSustemnoiInfekciiSplitter.addWidget(
            self.NajavnistSustemnoiInfekciiNoCheckBox)
        self.NajavnistSustemnoiInfekciiSplitter.addWidget(
            self.NajavnistSustemnoiInfekciiYesCheckBox)

        # 15) Патологія плаценти 			а) ні б) гіпоплазія в) гіперплазія
        self.PatologiaPlacentuLabel = QLabel('    15. Патологія плаценти:')
        self.PatologiaPlacentuLabel.setFixedHeight(15)
        self.PatologiaPlacentuLabel.setFixedWidth(400)
        self.PatologiaPlacentuLabel.show()

        self.PatologiaPlacentuNoCheckBox = QCheckBox('Ні')
        self.PatologiaPlacentuNoCheckBox.setChecked(1)
        self.PatologiaPlacentuNoCheckBox.setFixedWidth(100)
        self.PatologiaPlacentuNoCheckBox.stateChanged.connect(
            self.PatologiaPlacentuNoFunc)

        self.PatologiaPlacentuGipoplaziaCheckBox = QCheckBox('Гіпоплазія')
        self.PatologiaPlacentuGipoplaziaCheckBox.setEnabled(0)
        self.PatologiaPlacentuGipoplaziaCheckBox.stateChanged.connect(
            self.PatologiaPlacentuGipoplaziaFunc)

        self.PatologiaPlacentuGiperplaziaCheckBox = QCheckBox('Гіперплазія')
        self.PatologiaPlacentuGiperplaziaCheckBox.setEnabled(0)
        self.PatologiaPlacentuGiperplaziaCheckBox.setFixedWidth(100)
        self.PatologiaPlacentuGiperplaziaCheckBox.stateChanged.connect(
            self.PatologiaPlacentuGiperplaziaFunc)

        self.PatologiaPlacentuSplitter = QSplitter(Qt.Horizontal)
        self.PatologiaPlacentuSplitter.addWidget(self.PatologiaPlacentuLabel)
        self.PatologiaPlacentuSplitter.addWidget(
            self.PatologiaPlacentuNoCheckBox)
        self.PatologiaPlacentuSplitter.addWidget(
            self.PatologiaPlacentuGipoplaziaCheckBox)
        self.PatologiaPlacentuSplitter.addWidget(
            self.PatologiaPlacentuGiperplaziaCheckBox)

        # 15.1. Паталогія  локалізації плаценти:        а) ні;
        # б) низька плацентація;  в) крайове передлежання г) повне передлежання
        self.PatologiaLocalizaciiPlacentuLabel = QLabel(
            '       15.1. Паталогія  локалізації плаценти:')
        self.PatologiaLocalizaciiPlacentuLabel.setFixedHeight(15)
        self.PatologiaLocalizaciiPlacentuLabel.setFixedWidth(400)
        self.PatologiaLocalizaciiPlacentuLabel.show()

        self.PatologiaLocalizaciiPlacentuNoCheckBox = QCheckBox('Ні')
        self.PatologiaLocalizaciiPlacentuNoCheckBox.setChecked(1)
        self.PatologiaLocalizaciiPlacentuNoCheckBox.stateChanged.connect(
            self.PatologiaLocalizaciiPlacentuNoFunc)

        self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaCheckBox = QCheckBox(
            'Низька плацентація')
        self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaCheckBox.setEnabled(0)
        self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaCheckBox.stateChanged.connect(
            self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaFunc)

        self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaCheckBox = QCheckBox(
            'Крайове передлежання')
        self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaCheckBox.setEnabled(
            0)
        self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaCheckBox.stateChanged.connect(
            self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaFunc)

        self.PatologiaLocalizaciiPlacentuPovnePeredlegannaCheckBox = QCheckBox(
            'Повне передлежання')
        self.PatologiaLocalizaciiPlacentuPovnePeredlegannaCheckBox.setEnabled(
            0)
        self.PatologiaLocalizaciiPlacentuPovnePeredlegannaCheckBox.stateChanged.connect(
            self.PatologiaLocalizaciiPlacentuPovnePeredlegannaFunc)

        self.PatologiaLocalizaciiPlacentuSplitter = QSplitter(Qt.Horizontal)
        self.PatologiaLocalizaciiPlacentuSplitter.addWidget(
            self.PatologiaLocalizaciiPlacentuLabel)
        self.PatologiaLocalizaciiPlacentuSplitter.addWidget(
            self.PatologiaLocalizaciiPlacentuNoCheckBox)
        self.PatologiaLocalizaciiPlacentuSplitter.addWidget(
            self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaCheckBox)
        self.PatologiaLocalizaciiPlacentuSplitter.addWidget(
            self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaCheckBox)
        self.PatologiaLocalizaciiPlacentuSplitter.addWidget(
            self.PatologiaLocalizaciiPlacentuPovnePeredlegannaCheckBox)

        # 16) Передчасне відшарування плаценти 	а) ні б) так
        self.PeredchasneVadsharyvannaPlacentuLabel = QLabel(
            '    16. Передчасне відшарування плаценти:')
        self.PeredchasneVadsharyvannaPlacentuLabel.setFixedHeight(15)
        self.PeredchasneVadsharyvannaPlacentuLabel.setFixedWidth(400)

        self.PeredchasneVadsharyvannaPlacentuNoCheckBox = QCheckBox('Ні')
        self.PeredchasneVadsharyvannaPlacentuNoCheckBox.setChecked(1)
        self.PeredchasneVadsharyvannaPlacentuNoCheckBox.setFixedWidth(100)
        self.PeredchasneVadsharyvannaPlacentuNoCheckBox.stateChanged.connect(
            self.PeredchasneVadsharyvannaPlacentuNoFunc)

        self.PeredchasneVadsharyvannaPlacentuYesCheckBox = QCheckBox('Так')
        self.PeredchasneVadsharyvannaPlacentuYesCheckBox.setEnabled(0)
        self.PeredchasneVadsharyvannaPlacentuYesCheckBox.stateChanged.connect(
            self.PeredchasneVadsharyvannaPlacentuYesFunc)

        self.PeredchasneVadsharyvannaPlacentuSplitter = QSplitter(
            Qt.Horizontal)
        self.PeredchasneVadsharyvannaPlacentuSplitter.addWidget(
            self.PeredchasneVadsharyvannaPlacentuLabel)
        self.PeredchasneVadsharyvannaPlacentuSplitter.addWidget(
            self.PeredchasneVadsharyvannaPlacentuNoCheckBox)
        self.PeredchasneVadsharyvannaPlacentuSplitter.addWidget(
            self.PeredchasneVadsharyvannaPlacentuYesCheckBox)

        # 17) Хірургічні втручання під час вагітності: а) так; б) ні
        self.HiryrgichniVtyrchannaPidChasVagitnostiLabel = QLabel(
            '    17. Хірургічні втручання під час вагітності:')
        self.HiryrgichniVtyrchannaPidChasVagitnostiLabel.setFixedHeight(15)
        self.HiryrgichniVtyrchannaPidChasVagitnostiLabel.setFixedWidth(400)

        self.HiryrgichniVtyrchannaPidChasVagitnostiNoCheckBox = QCheckBox('Ні')
        self.HiryrgichniVtyrchannaPidChasVagitnostiNoCheckBox.setChecked(1)
        self.HiryrgichniVtyrchannaPidChasVagitnostiNoCheckBox.setFixedWidth(
            100)
        self.HiryrgichniVtyrchannaPidChasVagitnostiNoCheckBox.stateChanged.connect(
            self.HiryrgichniVtyrchannaPidChasVagitnostiNoFunc)

        self.HiryrgichniVtyrchannaPidChasVagitnostiYesCheckBox = QCheckBox(
            'Так')
        self.HiryrgichniVtyrchannaPidChasVagitnostiYesCheckBox.setEnabled(0)
        self.HiryrgichniVtyrchannaPidChasVagitnostiYesCheckBox.stateChanged.connect(
            self.HiryrgichniVtyrchannaPidChasVagitnostiYesFunc)

        self.HiryrgichniVtyrchannaPidChasVagitnostiSplitter = QSplitter(
            Qt.Horizontal)
        self.HiryrgichniVtyrchannaPidChasVagitnostiSplitter.addWidget(
            self.HiryrgichniVtyrchannaPidChasVagitnostiLabel)
        self.HiryrgichniVtyrchannaPidChasVagitnostiSplitter.addWidget(
            self.HiryrgichniVtyrchannaPidChasVagitnostiNoCheckBox)
        self.HiryrgichniVtyrchannaPidChasVagitnostiSplitter.addWidget(
            self.HiryrgichniVtyrchannaPidChasVagitnostiYesCheckBox)

        # 18) Тривала іммобілізація: а) так; б) ні
        self.TruvalaImmobilizaciaLabel = QLabel(
            '    17. Тривала іммобілізація:')
        self.TruvalaImmobilizaciaLabel.setFixedHeight(15)
        self.TruvalaImmobilizaciaLabel.setFixedWidth(400)

        self.TruvalaImmobilizaciaNoCheckBox = QCheckBox('Ні')
        self.TruvalaImmobilizaciaNoCheckBox.setChecked(1)
        self.TruvalaImmobilizaciaNoCheckBox.setFixedWidth(100)
        self.TruvalaImmobilizaciaNoCheckBox.stateChanged.connect(
            self.TruvalaImmobilizaciaNoFunc)

        self.TruvalaImmobilizaciaYesCheckBox = QCheckBox('Так')
        self.TruvalaImmobilizaciaYesCheckBox.setEnabled(0)
        self.TruvalaImmobilizaciaYesCheckBox.stateChanged.connect(
            self.TruvalaImmobilizaciaYesFunc)

        self.TruvalaImmobilizaciaSplitter = QSplitter(Qt.Horizontal)
        self.TruvalaImmobilizaciaSplitter.addWidget(
            self.TruvalaImmobilizaciaLabel)
        self.TruvalaImmobilizaciaSplitter.addWidget(
            self.TruvalaImmobilizaciaNoCheckBox)
        self.TruvalaImmobilizaciaSplitter.addWidget(
            self.TruvalaImmobilizaciaYesCheckBox)

        # 19) Завершення даної вагітності
        # а) переривання за медичними показаннями в терміні_______.
        # б) самовільний викидень в терміні_______.
        # в) пологи в терміні_______.
        self.ZavershennaDannoiVagitnostiLabel = QLabel(
            '    19. Завершення даної вагітності:')
        self.ZavershennaDannoiVagitnostiLabel.setFixedHeight(15)
        self.ZavershennaDannoiVagitnostiLabel.setFixedWidth(400)

        self.ZavershennaDannoiVagitnostiPologuVTerminiCheckBox = QCheckBox(
            'пологи в терміні')
        self.ZavershennaDannoiVagitnostiPologuVTerminiCheckBox.setChecked(1)
        self.ZavershennaDannoiVagitnostiPologuVTerminiCheckBox.setFixedWidth(
            100)
        self.ZavershennaDannoiVagitnostiPologuVTerminiCheckBox.stateChanged.connect(
            self.ZavershennaDannoiVagitnostiPologuVTerminiFunc)

        self.ZavershennaDannoiVagitnostiPologuVTerminiLineEdit = QLineEdit()
        self.ZavershennaDannoiVagitnostiPologuVTerminiLineEdit.setFixedWidth(
            100)

        self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokCheckBox = QCheckBox(
            'Переривання за медичними показаннями в терміні')
        self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokCheckBox.setEnabled(
            0)
        self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokCheckBox.stateChanged.connect(
            self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokFunc)

        self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokLineEdit = QLineEdit(
        )
        self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokLineEdit.setFixedWidth(
            100)
        self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokLineEdit.setEnabled(
            0)

        self.ZavershennaDannoiVagitnostiSamovilnuiVukudenCheckBox = QCheckBox(
            'Самовільний викидень в терміні')
        self.ZavershennaDannoiVagitnostiSamovilnuiVukudenCheckBox.setEnabled(0)
        self.ZavershennaDannoiVagitnostiSamovilnuiVukudenCheckBox.stateChanged.connect(
            self.ZavershennaDannoiVagitnostiSamovilnuiVukudenFunc)

        # ZavershennaDannoiVagitnostiPologuVTerminiFunc ZavershennaDannoiVagitnostiPereryvannaZaMedPokFunc
        # ZavershennaDannoiVagitnostiSamovilnuiVukudenFunc

        self.ZavershennaDannoiVagitnostiSamovilnuiVukudenLineEdit = QLineEdit()
        self.ZavershennaDannoiVagitnostiSamovilnuiVukudenLineEdit.setFixedWidth(
            100)
        self.ZavershennaDannoiVagitnostiSamovilnuiVukudenLineEdit.setEnabled(0)

        self.ZavershennaDannoiVagitnostiVertikal1Splitter = QSplitter(
            Qt.Vertical)
        self.ZavershennaDannoiVagitnostiVertikal1Splitter.addWidget(
            self.ZavershennaDannoiVagitnostiPologuVTerminiCheckBox)
        self.ZavershennaDannoiVagitnostiVertikal1Splitter.addWidget(
            self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokCheckBox)
        self.ZavershennaDannoiVagitnostiVertikal1Splitter.addWidget(
            self.ZavershennaDannoiVagitnostiSamovilnuiVukudenCheckBox)

        self.ZavershennaDannoiVagitnostiVertikal2Splitter = QSplitter(
            Qt.Vertical)
        self.ZavershennaDannoiVagitnostiVertikal2Splitter.addWidget(
            self.ZavershennaDannoiVagitnostiPologuVTerminiLineEdit)
        self.ZavershennaDannoiVagitnostiVertikal2Splitter.addWidget(
            self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokLineEdit)
        self.ZavershennaDannoiVagitnostiVertikal2Splitter.addWidget(
            self.ZavershennaDannoiVagitnostiSamovilnuiVukudenLineEdit)

        self.ZavershennaDannoiVagitnostiHorizontalSplitter = QSplitter(
            Qt.Horizontal)
        self.ZavershennaDannoiVagitnostiHorizontalSplitter.addWidget(
            self.ZavershennaDannoiVagitnostiLabel)
        self.ZavershennaDannoiVagitnostiHorizontalSplitter.addWidget(
            self.ZavershennaDannoiVagitnostiVertikal1Splitter)
        self.ZavershennaDannoiVagitnostiHorizontalSplitter.addWidget(
            self.ZavershennaDannoiVagitnostiVertikal2Splitter)

        # финальный сплиттер пункта V. Перебіг даної вагітності.
        self.PynkVSplitter = QSplitter(Qt.Vertical)
        self.PynkVSplitter.addWidget(self.PereBigDanoiVagitnostiLabel)
        self.PynkVSplitter.addWidget(self.VagitnistSplitter)
        self.PynkVSplitter.addWidget(self.NaOblikyVGinochiiKonsyltaciiSplitter)
        self.PynkVSplitter.addWidget(self.ZagrozaPereruvannaVagitnostiSplitter)
        self.PynkVSplitter.addWidget(self.ZagrozaPeredchasnuhPologivSplitter)
        self.PynkVSplitter.addWidget(
            self.ZagrozaPereruvannaVagitnostiP41Splitter)
        self.PynkVSplitter.addWidget(self.GestozIPolovunuVagitnostiSplitter)
        self.PynkVSplitter.addWidget(self.InshiPruchynyZnevodnennaSplitter)
        self.PynkVSplitter.addWidget(self.GestozIIPolovunuVagitnostiSplitter)
        self.PynkVSplitter.addWidget(
            self.GestozIIPolovunuDiagnostovanoVTerminiSplitter)
        self.PynkVSplitter.addWidget(self.VunuknennaTEYSplitter)
        self.PynkVSplitter.addWidget(self.VudTEYSplitter)
        self.PynkVSplitter.addWidget(self.TEYTerminVagitnostiplitter)
        self.PynkVSplitter.addWidget(self.BagatovoddaSplitter)
        self.PynkVSplitter.addWidget(
            self.BagatovoddaDiagnostovanoVTerminVagitnostiSplitter)
        self.PynkVSplitter.addWidget(self.MaloVoddaSplitter)
        self.PynkVSplitter.addWidget(
            self.MaloVoddaDiagnostovanoVTerminVagitnostiSplitter)
        self.PynkVSplitter.addWidget(self.DustressPlodaSplitter)
        self.PynkVSplitter.addWidget(self.ZatrumkaRozvutkyPlodaSplitter)
        self.PynkVSplitter.addWidget(self.NajavnistSustemnoiInfekciiSplitter)
        self.PynkVSplitter.addWidget(self.PatologiaPlacentuSplitter)
        self.PynkVSplitter.addWidget(self.PatologiaLocalizaciiPlacentuSplitter)
        self.PynkVSplitter.addWidget(
            self.PeredchasneVadsharyvannaPlacentuSplitter)
        self.PynkVSplitter.addWidget(
            self.HiryrgichniVtyrchannaPidChasVagitnostiSplitter)
        self.PynkVSplitter.addWidget(self.TruvalaImmobilizaciaSplitter)
        # self.PynkVSplitter.addWidget(self.ZavershennaDannoiVagitnostiLabel)
        self.PynkVSplitter.addWidget(
            self.ZavershennaDannoiVagitnostiHorizontalSplitter)

        # VІ Проведення профілактики/терапії ТЕУ під час вагітності: а) так б)ні

        self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiLabel = QLabel(
            '  VІ) Проведення профілактики/терапії ТЕУ під час вагітності:')
        self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiLabel.setFixedHeight(
            30)
        self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiLabel.setFixedWidth(
            400)
        self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiLabel.setStyleSheet(
            """QLabel{font-size:8pt; font-weight:600; color:#aa0000;}""")

        self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiYesCheckBox = QCheckBox(
            'Так')
        self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiYesCheckBox.setEnabled(
            0)
        self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiYesCheckBox.stateChanged.connect(
            self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiYesFunc)

        self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiNoCheckBox = QCheckBox(
            'Ні')
        self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiNoCheckBox.setChecked(
            1)
        self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiNoCheckBox.setFixedWidth(
            100)
        self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiNoCheckBox.stateChanged.connect(
            self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiNoFunc)

        self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiSplitter = QSplitter(
            Qt.Horizontal)
        self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiSplitter.addWidget(
            self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiLabel)
        self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiSplitter.addWidget(
            self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiNoCheckBox)
        self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiSplitter.addWidget(
            self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiYesCheckBox)

        # Покази до проведення профілактики ______
        self.PokazuDlaProvedennaProfilaktukyLabel = QLabel(
            '    Покази до проведення профілактики:')
        self.PokazuDlaProvedennaProfilaktukyLabel.setFixedHeight(15)
        self.PokazuDlaProvedennaProfilaktukyLabel.setFixedWidth(400)
        self.PokazuDlaProvedennaProfilaktukyLabel.setEnabled(0)
        self.PokazuDlaProvedennaProfilaktukyLabel.show()

        self.PokazuDlaProvedennaProfilaktukyLineEdit = QLineEdit()
        self.PokazuDlaProvedennaProfilaktukyLineEdit.setEnabled(0)
        self.PokazuDlaProvedennaProfilaktukyLineEdit.show()

        self.PokazuDlaProvedennaProfilaktukySplitter = QSplitter(Qt.Horizontal)
        self.PokazuDlaProvedennaProfilaktukySplitter.addWidget(
            self.PokazuDlaProvedennaProfilaktukyLabel)
        self.PokazuDlaProvedennaProfilaktukySplitter.addWidget(
            self.PokazuDlaProvedennaProfilaktukyLineEdit)

        # 1)	Еластична компресія:			 а) так б) ні;	в) клас ______
        self.ElastychnaKompresiaPynktVILabel = QLabel(
            '    1. Еластична компресія:')
        self.ElastychnaKompresiaPynktVILabel.setFixedHeight(15)
        self.ElastychnaKompresiaPynktVILabel.setFixedWidth(400)
        self.ElastychnaKompresiaPynktVILabel.setEnabled(0)

        self.ElastychnaKompresiaPynktVIYesCheckBox = QCheckBox('Так')
        self.ElastychnaKompresiaPynktVIYesCheckBox.setFixedWidth(40)
        self.ElastychnaKompresiaPynktVIYesCheckBox.setEnabled(0)
        self.ElastychnaKompresiaPynktVIYesCheckBox.stateChanged.connect(
            self.ElastychnaKompresiaPynktVIYesFunc)

        self.ElastychnaKompresiaPynktVINoCheckBox = QCheckBox('Ні')
        self.ElastychnaKompresiaPynktVINoCheckBox.setChecked(1)
        self.ElastychnaKompresiaPynktVINoCheckBox.show()
        self.ElastychnaKompresiaPynktVINoCheckBox.setFixedWidth(40)
        self.ElastychnaKompresiaPynktVINoCheckBox.setEnabled(0)
        self.ElastychnaKompresiaPynktVINoCheckBox.stateChanged.connect(
            self.ElastychnaKompresiaPynktVINoFunc)

        self.ElastychnaKompresiaPynktVILevelLabel = QLabel('Клас:')
        self.ElastychnaKompresiaPynktVILevelLabel.setFixedWidth(30)
        self.ElastychnaKompresiaPynktVILevelLabel.hide()

        self.ElastychnaKompresiaPynktVILevelLineEdit = QLineEdit()
        # self.ElastychnaKompresiaPynktVILevelLineEdit.setFixedHeight(20)
        self.ElastychnaKompresiaPynktVILevelLineEdit.setFixedWidth(30)
        self.ElastychnaKompresiaPynktVILevelLineEdit.hide()

        self.ElastychnaKompresiaPynktVISplitter = QSplitter(Qt.Horizontal)
        self.ElastychnaKompresiaPynktVISplitter.addWidget(
            self.ElastychnaKompresiaPynktVILabel)
        self.ElastychnaKompresiaPynktVISplitter.addWidget(
            self.ElastychnaKompresiaPynktVINoCheckBox)
        self.ElastychnaKompresiaPynktVISplitter.addWidget(
            self.ElastychnaKompresiaPynktVIYesCheckBox)
        self.ElastychnaKompresiaPynktVISplitter.addWidget(
            self.ElastychnaKompresiaPynktVILevelLabel)
        self.ElastychnaKompresiaPynktVISplitter.addWidget(
            self.ElastychnaKompresiaPynktVILevelLineEdit)

        # 2)	Медикаментозна профілактика 	а) так б)ні

        self.MedukamentoznaProfilaktukaPynktVILabel = QLabel(
            '    2. Медикаментозна профілактика:')
        self.MedukamentoznaProfilaktukaPynktVILabel.setFixedHeight(15)
        self.MedukamentoznaProfilaktukaPynktVILabel.setFixedWidth(400)
        self.MedukamentoznaProfilaktukaPynktVILabel.setEnabled(0)
        # self.MedukamentoznaProfilaktukaPynktVILabel.setEnabled(0)

        self.MedukamentoznaProfilaktukaPynktVIYesCheckBox = QCheckBox('Так')
        self.MedukamentoznaProfilaktukaPynktVIYesCheckBox.setFixedWidth(40)
        self.MedukamentoznaProfilaktukaPynktVIYesCheckBox.setEnabled(0)
        self.MedukamentoznaProfilaktukaPynktVIYesCheckBox.setEnabled(0)
        self.MedukamentoznaProfilaktukaPynktVIYesCheckBox.stateChanged.connect(
            self.MedukamentoznaProfilaktukaPynktVIYesFunc)

        self.MedukamentoznaProfilaktukaPynktVINoCheckBox = QCheckBox('Ні')
        self.MedukamentoznaProfilaktukaPynktVINoCheckBox.setChecked(1)
        self.MedukamentoznaProfilaktukaPynktVINoCheckBox.setFixedWidth(40)
        self.MedukamentoznaProfilaktukaPynktVINoCheckBox.setEnabled(0)
        self.MedukamentoznaProfilaktukaPynktVINoCheckBox.stateChanged.connect(
            self.MedukamentoznaProfilaktukaPynktVINoFunc)

        self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLabel = QLabel(
            '2.1 Назва препарату:')
        self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLabel.setFixedWidth(
            110)
        self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLabel.hide()

        self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLineEdit = QLineEdit(
        )
        self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLineEdit.setMinimumWidth(
            100)
        self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLineEdit.hide()

        self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLabel = QLabel(
            '2.2 Режим прийому:')
        self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLabel.setFixedWidth(
            100)
        self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLabel.hide()

        self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLineEdit = QLineEdit(
        )
        self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLineEdit.setMinimumWidth(
            100)
        self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLineEdit.hide()

        self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLabel = QLabel(
            '2.3 Термін коли призначено:')
        self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLabel.setFixedWidth(
            145)
        self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLabel.hide()

        self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLineEdit = QLineEdit(
        )
        self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLineEdit.setMinimumWidth(
            100)
        self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLineEdit.hide(
        )

        self.MedukamentoznaProfilaktukaPynktVISplitter = QSplitter(
            Qt.Horizontal)
        self.MedukamentoznaProfilaktukaPynktVISplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktVILabel)
        self.MedukamentoznaProfilaktukaPynktVISplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktVINoCheckBox)
        self.MedukamentoznaProfilaktukaPynktVISplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktVIYesCheckBox)
        self.MedukamentoznaProfilaktukaPynktVISplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLabel)
        self.MedukamentoznaProfilaktukaPynktVISplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLineEdit)
        self.MedukamentoznaProfilaktukaPynktVISplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLabel)
        self.MedukamentoznaProfilaktukaPynktVISplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLineEdit)
        self.MedukamentoznaProfilaktukaPynktVISplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLabel)
        self.MedukamentoznaProfilaktukaPynktVISplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLineEdit
        )

        # 3)	Хірургічне лікування :		          а) так б)ні Назва операції та дата _
        self.HiryrgichneLikyvannaPynktVILabel = QLabel(
            '    3. Хірургічне лікування:')
        self.HiryrgichneLikyvannaPynktVILabel.setFixedHeight(15)
        self.HiryrgichneLikyvannaPynktVILabel.setFixedWidth(400)
        self.HiryrgichneLikyvannaPynktVILabel.setEnabled(0)

        self.HiryrgichneLikyvannaPynktVIYesCheckBox = QCheckBox('Так')
        self.HiryrgichneLikyvannaPynktVIYesCheckBox.setFixedWidth(40)
        self.HiryrgichneLikyvannaPynktVIYesCheckBox.setEnabled(0)
        self.HiryrgichneLikyvannaPynktVIYesCheckBox.stateChanged.connect(
            self.HiryrgichneLikyvannaPynktVIYesFunc)

        self.HiryrgichneLikyvannaPynktVINoCheckBox = QCheckBox('Ні')
        self.HiryrgichneLikyvannaPynktVINoCheckBox.setChecked(1)
        self.HiryrgichneLikyvannaPynktVINoCheckBox.show()
        self.HiryrgichneLikyvannaPynktVINoCheckBox.setFixedWidth(40)
        self.HiryrgichneLikyvannaPynktVINoCheckBox.setEnabled(0)
        self.HiryrgichneLikyvannaPynktVINoCheckBox.stateChanged.connect(
            self.HiryrgichneLikyvannaPynktVINoFunc)

        self.HiryrgichneLikyvannaNazvaOpericiiPynktVILabel = QLabel(
            'Назва операції та дата:')
        self.HiryrgichneLikyvannaNazvaOpericiiPynktVILabel.setFixedWidth(150)
        self.HiryrgichneLikyvannaNazvaOpericiiPynktVILabel.hide()

        self.HiryrgichneLikyvannaNazvaOpericiiPynktVILineEdit = QLineEdit()
        self.HiryrgichneLikyvannaNazvaOpericiiPynktVILineEdit.setMinimumWidth(
            150)
        self.HiryrgichneLikyvannaNazvaOpericiiPynktVILineEdit.hide()

        self.HiryrgichneLikyvannaPynktVISplitter = QSplitter(Qt.Horizontal)
        self.HiryrgichneLikyvannaPynktVISplitter.addWidget(
            self.HiryrgichneLikyvannaPynktVILabel)
        self.HiryrgichneLikyvannaPynktVISplitter.addWidget(
            self.HiryrgichneLikyvannaPynktVINoCheckBox)
        self.HiryrgichneLikyvannaPynktVISplitter.addWidget(
            self.HiryrgichneLikyvannaPynktVIYesCheckBox)
        self.HiryrgichneLikyvannaPynktVISplitter.addWidget(
            self.HiryrgichneLikyvannaNazvaOpericiiPynktVILabel)
        self.HiryrgichneLikyvannaPynktVISplitter.addWidget(
            self.HiryrgichneLikyvannaNazvaOpericiiPynktVILineEdit)

        # 4)	Тривалість проведеної профілактики _____________________

        self.TryvalistProvedennoiProfilaktykyPynktVILabel = QLabel(
            '    4. Тривалість проведеної профілактики:')
        self.TryvalistProvedennoiProfilaktykyPynktVILabel.setFixedWidth(400)
        self.TryvalistProvedennoiProfilaktykyPynktVILabel.setFixedHeight(15)
        self.TryvalistProvedennoiProfilaktykyPynktVILabel.setEnabled(0)

        self.TryvalistProvedennoiProfilaktykyPynktVILineEdit = QLineEdit()
        # self.TryvalistProvedennoiProfilaktykyLineEdit.setFixedHeight(15)
        self.TryvalistProvedennoiProfilaktykyPynktVILineEdit.setMinimumWidth(
            200)
        self.TryvalistProvedennoiProfilaktykyPynktVILineEdit.setMaximumWidth(
            300)
        self.TryvalistProvedennoiProfilaktykyPynktVILineEdit.setEnabled(0)

        self.TryvalistProvedennoiProfilaktykyPynktVISplitter = QSplitter(
            Qt.Horizontal)
        self.TryvalistProvedennoiProfilaktykyPynktVISplitter.addWidget(
            self.TryvalistProvedennoiProfilaktykyPynktVILabel)
        self.TryvalistProvedennoiProfilaktykyPynktVISplitter.addWidget(
            self.TryvalistProvedennoiProfilaktykyPynktVILineEdit)

        # 5)	Наявність ускладнень від проведеної профілактики: а) так б)ні Ускладення:_______________________________________________

        self.YskladneenaVidProfilaktykuPynktVILabel = QLabel(
            '    5. Наявність ускладнень від проведеної профілактики:')
        self.YskladneenaVidProfilaktykuPynktVILabel.setFixedHeight(15)
        self.YskladneenaVidProfilaktykuPynktVILabel.setFixedWidth(400)
        self.YskladneenaVidProfilaktykuPynktVILabel.setEnabled(0)

        self.YskladneenaVidProfilaktykuPynktVIYesCheckBox = QCheckBox('Так')
        self.YskladneenaVidProfilaktykuPynktVIYesCheckBox.setFixedWidth(40)
        self.YskladneenaVidProfilaktykuPynktVIYesCheckBox.setEnabled(0)
        self.YskladneenaVidProfilaktykuPynktVIYesCheckBox.stateChanged.connect(
            self.YskladneenaVidProfilaktykuPynktVIYesFunc)

        self.YskladneenaVidProfilaktykuPynktVINoCheckBox = QCheckBox('Ні')
        self.YskladneenaVidProfilaktykuPynktVINoCheckBox.setChecked(1)
        self.YskladneenaVidProfilaktykuPynktVINoCheckBox.show()
        self.YskladneenaVidProfilaktykuPynktVINoCheckBox.setFixedWidth(40)
        self.YskladneenaVidProfilaktykuPynktVINoCheckBox.setEnabled(0)
        self.YskladneenaVidProfilaktykuPynktVINoCheckBox.stateChanged.connect(
            self.YskladneenaVidProfilaktykuPynktVINoFunc)

        self.YskladneenaVidProfilaktykuNajavnistPynktVILabel = QLabel(
            'Ускладення:')
        self.YskladneenaVidProfilaktykuNajavnistPynktVILabel.setFixedWidth(70)
        self.YskladneenaVidProfilaktykuNajavnistPynktVILabel.hide()

        self.YskladneenaVidProfilaktykuNajavnistPynktVILineEdit = QLineEdit()
        self.YskladneenaVidProfilaktykuNajavnistPynktVILineEdit.setMinimumWidth(
            200)
        self.YskladneenaVidProfilaktykuNajavnistPynktVILineEdit.hide()

        self.YskladneenaVidProfilaktykuPynktVISplitter = QSplitter(
            Qt.Horizontal)
        self.YskladneenaVidProfilaktykuPynktVISplitter.addWidget(
            self.YskladneenaVidProfilaktykuPynktVILabel)
        self.YskladneenaVidProfilaktykuPynktVISplitter.addWidget(
            self.YskladneenaVidProfilaktykuPynktVINoCheckBox)
        self.YskladneenaVidProfilaktykuPynktVISplitter.addWidget(
            self.YskladneenaVidProfilaktykuPynktVIYesCheckBox)
        self.YskladneenaVidProfilaktykuPynktVISplitter.addWidget(
            self.YskladneenaVidProfilaktykuNajavnistPynktVILabel)
        self.YskladneenaVidProfilaktykuPynktVISplitter.addWidget(
            self.YskladneenaVidProfilaktykuNajavnistPynktVILineEdit)

        # 6)	Терапію відмінено за _______________год до пологів.
        self.TerapiyVidminenoZaGodDoPologivPynktVILabel = QLabel(
            '    6. Терапію відмінено за:')
        self.TerapiyVidminenoZaGodDoPologivPynktVILabel.setFixedHeight(15)
        self.TerapiyVidminenoZaGodDoPologivPynktVILabel.setFixedWidth(400)
        self.TerapiyVidminenoZaGodDoPologivPynktVILabel.setEnabled(0)

        self.TerapiyVidminenoZaGodDoPologivPynktVILineEdit = QLineEdit()
        self.TerapiyVidminenoZaGodDoPologivPynktVILineEdit.setFixedWidth(30)
        self.TerapiyVidminenoZaGodDoPologivPynktVILineEdit.setInputMask('D0')
        self.TerapiyVidminenoZaGodDoPologivPynktVILineEdit.setEnabled(0)

        self.TerapiyVidminenoZaGodDoPologivPynktVILabel2 = QLabel(
            'годин до пологів')
        self.TerapiyVidminenoZaGodDoPologivPynktVILabel2.setFixedHeight(15)
        self.TerapiyVidminenoZaGodDoPologivPynktVILabel2.setEnabled(0)

        self.TerapiyVidminenoZaGodDoPologivPynktVISplitter = QSplitter(
            Qt.Horizontal)
        self.TerapiyVidminenoZaGodDoPologivPynktVISplitter.addWidget(
            self.TerapiyVidminenoZaGodDoPologivPynktVILabel)
        self.TerapiyVidminenoZaGodDoPologivPynktVISplitter.addWidget(
            self.TerapiyVidminenoZaGodDoPologivPynktVILineEdit)
        self.TerapiyVidminenoZaGodDoPologivPynktVISplitter.addWidget(
            self.TerapiyVidminenoZaGodDoPologivPynktVILabel2)

        # Финальный срдыттер пункта VІ Проведення профілактики/терапії ТЕУ під час вагітності

        self.PynktVISplitter = QSplitter(Qt.Vertical)
        self.PynktVISplitter.addWidget(
            self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiSplitter)
        self.PynktVISplitter.addWidget(
            self.PokazuDlaProvedennaProfilaktukySplitter)
        self.PynktVISplitter.addWidget(self.ElastychnaKompresiaPynktVISplitter)
        self.PynktVISplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktVISplitter)
        self.PynktVISplitter.addWidget(
            self.HiryrgichneLikyvannaPynktVISplitter)
        self.PynktVISplitter.addWidget(
            self.TryvalistProvedennoiProfilaktykyPynktVISplitter)
        self.PynktVISplitter.addWidget(
            self.YskladneenaVidProfilaktykuPynktVISplitter)
        self.PynktVISplitter.addWidget(
            self.TerapiyVidminenoZaGodDoPologivPynktVISplitter)

        # VII. Перебіг даних пологів.

        self.PerebigDannuhPologivLabel = QLabel(
            '  VІI) Перебіг даних пологів.')
        self.PerebigDannuhPologivLabel.setFixedHeight(30)
        self.PerebigDannuhPologivLabel.setFixedWidth(400)
        self.PerebigDannuhPologivLabel.setStyleSheet(
            """QLabel{font-size:8pt; font-weight:600; color:#aa0000;}""")

        # 1)	Пологи вагінальні а) ні, б) спонтанні, в) індуковані
        self.PologuVaginalniILabel = QLabel('    1. Пологи вагінальні:')
        self.PologuVaginalniILabel.setFixedHeight(15)
        self.PologuVaginalniILabel.setFixedWidth(400)

        self.PologuVaginalniNoCheckBox = QCheckBox('Ні')
        self.PologuVaginalniNoCheckBox.setChecked(1)
        self.PologuVaginalniNoCheckBox.setFixedWidth(40)
        self.PologuVaginalniNoCheckBox.stateChanged.connect(
            self.PologuVaginalniNoFunc)

        self.PologuVaginalniSpomtanniCheckBox = QCheckBox('Спонтанні')
        self.PologuVaginalniSpomtanniCheckBox.setEnabled(0)
        self.PologuVaginalniSpomtanniCheckBox.stateChanged.connect(
            self.PologuVaginalniSpomtanniFunc)

        self.PologuVaginalniIndykovaniCheckBox = QCheckBox('Індуковані')
        self.PologuVaginalniIndykovaniCheckBox.setEnabled(0)
        self.PologuVaginalniIndykovaniCheckBox.stateChanged.connect(
            self.PologuVaginalniIndykovaniFunc)

        # PologuVaginalniNoFunc PologuVaginalniSpomtanniFunc PologuVaginalniIndykovaniFunc

        self.PologuVaginalniSplitter = QSplitter(Qt.Horizontal)
        self.PologuVaginalniSplitter.addWidget(self.PologuVaginalniILabel)
        self.PologuVaginalniSplitter.addWidget(self.PologuVaginalniNoCheckBox)
        self.PologuVaginalniSplitter.addWidget(
            self.PologuVaginalniSpomtanniCheckBox)
        self.PologuVaginalniSplitter.addWidget(
            self.PologuVaginalniIndykovaniCheckBox)

        # 2)	Пологи абдомінальні а) ні, б) плановий КР, в) ургентний КР
        self.PologuAbdominalniLabel = QLabel('    2. Пологи абдомінальні:')
        self.PologuAbdominalniLabel.setFixedHeight(15)
        self.PologuAbdominalniLabel.setFixedWidth(400)

        self.PologuAbdominalniNoCheckBox = QCheckBox('Ні')
        self.PologuAbdominalniNoCheckBox.setChecked(1)
        self.PologuAbdominalniNoCheckBox.setFixedWidth(40)
        self.PologuAbdominalniNoCheckBox.stateChanged.connect(
            self.PologuAbdominalniNoFunc)

        self.PologuAbdominalniPlanovuiKRCheckBox = QCheckBox('Плановий КР')
        self.PologuAbdominalniPlanovuiKRCheckBox.setEnabled(0)
        self.PologuAbdominalniPlanovuiKRCheckBox.stateChanged.connect(
            self.PologuAbdominalniPlanovuiKRFunc)

        self.PologuAbdominalniYrgentbuiKRCheckBox = QCheckBox('Ургентний КР')
        self.PologuAbdominalniYrgentbuiKRCheckBox.setEnabled(0)
        self.PologuAbdominalniYrgentbuiKRCheckBox.stateChanged.connect(
            self.PologuAbdominalniYrgentbuiKRCFunc)

        self.PologuAbdominalniSplitter = QSplitter(Qt.Horizontal)
        self.PologuAbdominalniSplitter.addWidget(self.PologuAbdominalniLabel)
        self.PologuAbdominalniSplitter.addWidget(
            self.PologuAbdominalniNoCheckBox)
        self.PologuAbdominalniSplitter.addWidget(
            self.PologuAbdominalniPlanovuiKRCheckBox)
        self.PologuAbdominalniSplitter.addWidget(
            self.PologuAbdominalniYrgentbuiKRCheckBox)

        # 3)	Показання до абдомінального розродження
        self.PokazannaDlaAbdominalnogoRozrodjennaLabel = QLabel(
            '    3. Показання до абдомінального розродження:')
        self.PokazannaDlaAbdominalnogoRozrodjennaLabel.setFixedWidth(400)
        self.PokazannaDlaAbdominalnogoRozrodjennaLabel.setFixedHeight(15)

        self.PokazannaDlaAbdominalnogoRozrodjennaLineEdit = QLineEdit()

        self.PokazannaDlaAbdominalnogoRozrodjennaSplitter = QSplitter(
            Qt.Horizontal)
        self.PokazannaDlaAbdominalnogoRozrodjennaSplitter.addWidget(
            self.PokazannaDlaAbdominalnogoRozrodjennaLabel)
        self.PokazannaDlaAbdominalnogoRozrodjennaSplitter.addWidget(
            self.PokazannaDlaAbdominalnogoRozrodjennaLineEdit)

        # 4)	Порушення пологової діяльності а) ні, б) стрімкі пологи, в) дискоординація, г) слабкість
        self.PoryshennaPologovoiDialnostiLabel = QLabel(
            '    4. Порушення пологової діяльності:')
        self.PoryshennaPologovoiDialnostiLabel.setFixedHeight(15)
        self.PoryshennaPologovoiDialnostiLabel.setFixedWidth(400)

        self.PoryshennaPologovoiDialnostiNoCheckBox = QCheckBox('Ні')
        self.PoryshennaPologovoiDialnostiNoCheckBox.setChecked(1)
        self.PoryshennaPologovoiDialnostiNoCheckBox.setFixedWidth(40)
        self.PoryshennaPologovoiDialnostiNoCheckBox.stateChanged.connect(
            self.PoryshennaPologovoiDialnostiNoFunc)

        self.PoryshennaPologovoiDialnostiStrimkiPologuCheckBox = QCheckBox(
            'Стрімкі пологи')
        self.PoryshennaPologovoiDialnostiStrimkiPologuCheckBox.setEnabled(0)
        self.PoryshennaPologovoiDialnostiStrimkiPologuCheckBox.stateChanged.connect(
            self.PoryshennaPologovoiDialnostiStrimkiPologuFunc)

        self.PoryshennaPologovoiDialnostiDuskoordunaciaCheckBox = QCheckBox(
            'Дискоординація')
        self.PoryshennaPologovoiDialnostiDuskoordunaciaCheckBox.setEnabled(0)
        self.PoryshennaPologovoiDialnostiDuskoordunaciaCheckBox.stateChanged.connect(
            self.PoryshennaPologovoiDialnostiDuskoordunaciaFunc)

        self.PoryshennaPologovoiDialnostiSlabkistCheckBox = QCheckBox(
            'Слабкість')
        self.PoryshennaPologovoiDialnostiSlabkistCheckBox.setEnabled(0)
        self.PoryshennaPologovoiDialnostiSlabkistCheckBox.stateChanged.connect(
            self.PoryshennaPologovoiDialnostiSlabkistFunc)

        self.PoryshennaPologovoiDialnostiSplitter = QSplitter(Qt.Horizontal)
        self.PoryshennaPologovoiDialnostiSplitter.addWidget(
            self.PoryshennaPologovoiDialnostiLabel)
        self.PoryshennaPologovoiDialnostiSplitter.addWidget(
            self.PoryshennaPologovoiDialnostiNoCheckBox)
        self.PoryshennaPologovoiDialnostiSplitter.addWidget(
            self.PoryshennaPologovoiDialnostiStrimkiPologuCheckBox)
        self.PoryshennaPologovoiDialnostiSplitter.addWidget(
            self.PoryshennaPologovoiDialnostiDuskoordunaciaCheckBox)
        self.PoryshennaPologovoiDialnostiSplitter.addWidget(
            self.PoryshennaPologovoiDialnostiSlabkistCheckBox)

        # 5)	Корекція аномалій пологової діяльності а) ні, б) бета-міметики, в) окситоцин, г) ензапрост, д) окситоцин з ензапростом.

        self.KorekciaAnomaliiPologovoiDialnostiLabel = QLabel(
            '    5. Корекція аномалій пологової діяльності:')
        self.KorekciaAnomaliiPologovoiDialnostiLabel.setFixedHeight(15)
        self.KorekciaAnomaliiPologovoiDialnostiLabel.setFixedWidth(400)

        self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox = QCheckBox('Ні')
        self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.setChecked(1)
        self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.setFixedWidth(40)
        self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.stateChanged.connect(
            self.KorekciaAnomaliiPologovoiDialnostiNoFunc)

        self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox = QCheckBox(
            'Бета-міметики')
        self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox.setEnabled(
            0)
        self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox.stateChanged.connect(
            self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuFunc)

        self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox = QCheckBox(
            'Окситоцин')
        self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox.setEnabled(0)
        self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox.stateChanged.connect(
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunFunc)

        self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox = QCheckBox(
            'Ензапрост')
        self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox.setEnabled(0)
        self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox.stateChanged.connect(
            self.KorekciaAnomaliiPologovoiDialnostiEnzaprostFunc)

        self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox = QCheckBox(
            'Окситоцин з ензапростом')
        self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox.setEnabled(
            0)
        self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox.stateChanged.connect(
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomFunc)

        self.KorekciaAnomaliiPologovoiDialnostiSplitter = QSplitter(
            Qt.Horizontal)
        self.KorekciaAnomaliiPologovoiDialnostiSplitter.addWidget(
            self.KorekciaAnomaliiPologovoiDialnostiLabel)
        self.KorekciaAnomaliiPologovoiDialnostiSplitter.addWidget(
            self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox)
        self.KorekciaAnomaliiPologovoiDialnostiSplitter.addWidget(
            self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox)
        self.KorekciaAnomaliiPologovoiDialnostiSplitter.addWidget(
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox)
        self.KorekciaAnomaliiPologovoiDialnostiSplitter.addWidget(
            self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox)
        self.KorekciaAnomaliiPologovoiDialnostiSplitter.addWidget(
            self.
            KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox)

        # 6)	Вилив навколоплодових вод а) своєчасний, б) ранній, в) передчасний
        self.VuluvNavkoloplodovuhVodLabel = QLabel(
            '    6. Вилив навколоплодових вод:')
        self.VuluvNavkoloplodovuhVodLabel.setFixedHeight(15)
        self.VuluvNavkoloplodovuhVodLabel.setFixedWidth(400)

        self.VuluvNavkoloplodovuhVodSvoechasnuiCheckBox = QCheckBox(
            'Своєчасний')
        self.VuluvNavkoloplodovuhVodSvoechasnuiCheckBox.setChecked(1)
        self.VuluvNavkoloplodovuhVodSvoechasnuiCheckBox.stateChanged.connect(
            self.VuluvNavkoloplodovuhVodSvoechasnuiFunc)

        self.VuluvNavkoloplodovuhVodRaniiCheckBox = QCheckBox('Ранній')
        self.VuluvNavkoloplodovuhVodRaniiCheckBox.setEnabled(0)
        self.VuluvNavkoloplodovuhVodRaniiCheckBox.stateChanged.connect(
            self.VuluvNavkoloplodovuhVodRaniiFunc)

        self.VuluvNavkoloplodovuhVodPeredchasnuiCheckBox = QCheckBox(
            'Передчасний')
        self.VuluvNavkoloplodovuhVodPeredchasnuiCheckBox.setEnabled(0)
        self.VuluvNavkoloplodovuhVodPeredchasnuiCheckBox.stateChanged.connect(
            self.VuluvNavkoloplodovuhVodPeredchasnuiFunc)

        self.VuluvNavkoloplodovuhVodSplitter = QSplitter(Qt.Horizontal)
        self.VuluvNavkoloplodovuhVodSplitter.addWidget(
            self.VuluvNavkoloplodovuhVodLabel)
        self.VuluvNavkoloplodovuhVodSplitter.addWidget(
            self.VuluvNavkoloplodovuhVodSvoechasnuiCheckBox)
        self.VuluvNavkoloplodovuhVodSplitter.addWidget(
            self.VuluvNavkoloplodovuhVodRaniiCheckBox)
        self.VuluvNavkoloplodovuhVodSplitter.addWidget(
            self.VuluvNavkoloplodovuhVodPeredchasnuiCheckBox)

        # 7)	Дистрес плода в пологах а) ні, б) в І періоді, в) в ІІ періоді
        self.DustressPlodaVPologahLabel = QLabel(
            '    7. Дистрес плода в пологах:')
        self.DustressPlodaVPologahLabel.setFixedHeight(15)
        self.DustressPlodaVPologahLabel.setFixedWidth(400)

        self.DustressPlodaVPologahNoCheckBox = QCheckBox('Ні')
        self.DustressPlodaVPologahNoCheckBox.setChecked(1)
        self.DustressPlodaVPologahNoCheckBox.stateChanged.connect(
            self.DustressPlodaVPologahNoFunc)

        self.DustressPlodaVPologahVIPeriodiCheckBox = QCheckBox('В І періоді')
        self.DustressPlodaVPologahVIPeriodiCheckBox.setEnabled(0)
        self.DustressPlodaVPologahVIPeriodiCheckBox.stateChanged.connect(
            self.DustressPlodaVPologahVIPeriodiFunc)

        self.DustressPlodaVPologahVIIPeriodiCheckBox = QCheckBox(
            'В ІІ періоді')
        self.DustressPlodaVPologahVIIPeriodiCheckBox.setEnabled(0)
        self.DustressPlodaVPologahVIIPeriodiCheckBox.stateChanged.connect(
            self.DustressPlodaVPologahVIIPeriodiFunc)

        self.DustressPlodaVPologahSplitter = QSplitter(Qt.Horizontal)
        self.DustressPlodaVPologahSplitter.addWidget(
            self.DustressPlodaVPologahLabel)
        self.DustressPlodaVPologahSplitter.addWidget(
            self.DustressPlodaVPologahNoCheckBox)
        self.DustressPlodaVPologahSplitter.addWidget(
            self.DustressPlodaVPologahVIPeriodiCheckBox)
        self.DustressPlodaVPologahSplitter.addWidget(
            self.DustressPlodaVPologahVIIPeriodiCheckBox)

        #  8)    Гіпотонічна кровотеча    а) ні, б) в ІІІ  періоді, в) в  ранньому  післяпологовому  періоді, г) в пізньому  післяпологовому періоді.
        self.GipotonichnaKrovotechaLabel = QLabel(
            '    8. Гіпотонічна кровотеча:')
        self.GipotonichnaKrovotechaLabel.setFixedHeight(15)
        self.GipotonichnaKrovotechaLabel.setFixedWidth(400)

        self.GipotonichnaKrovotechaNoCheckBox = QCheckBox('Ні')
        self.GipotonichnaKrovotechaNoCheckBox.setChecked(1)
        self.GipotonichnaKrovotechaNoCheckBox.stateChanged.connect(
            self.GipotonichnaKrovotechaNoFunc)

        self.GipotonichnaKrovotechaVIIIPeriodiCheckBox = QCheckBox(
            'В ІII періоді')
        self.GipotonichnaKrovotechaVIIIPeriodiCheckBox.setEnabled(0)
        self.GipotonichnaKrovotechaVIIIPeriodiCheckBox.stateChanged.connect(
            self.GipotonichnaKrovotechaVIIIPeriodiFunc)

        self.GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiCheckBox = QCheckBox(
            'В ранньому післяпологовому періоді')
        self.GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiCheckBox.setEnabled(
            0)
        self.GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiCheckBox.stateChanged.connect(
            self.GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiFunc)

        self.GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiCheckBox = QCheckBox(
            'В пізньому післяпологовому періоді')
        self.GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiCheckBox.setEnabled(
            0)
        self.GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiCheckBox.stateChanged.connect(
            self.GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiFunc)

        self.GipotonichnaKrovotechaSplitter = QSplitter(Qt.Horizontal)
        self.GipotonichnaKrovotechaSplitter.addWidget(
            self.GipotonichnaKrovotechaLabel)
        self.GipotonichnaKrovotechaSplitter.addWidget(
            self.GipotonichnaKrovotechaNoCheckBox)
        self.GipotonichnaKrovotechaSplitter.addWidget(
            self.GipotonichnaKrovotechaVIIIPeriodiCheckBox)
        self.GipotonichnaKrovotechaSplitter.addWidget(
            self.GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiCheckBox)
        self.GipotonichnaKrovotechaSplitter.addWidget(
            self.GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiCheckBox)

        # 9)	Аномалії прикріплення плаценти а) ні, б) adherens, в) acreta, г) percreta.
        self.AnomaliiPrukriplennaPlacentuLabel = QLabel(
            '    9. Аномалії прикріплення плаценти:')
        self.AnomaliiPrukriplennaPlacentuLabel.setFixedHeight(15)
        self.AnomaliiPrukriplennaPlacentuLabel.setFixedWidth(400)

        self.AnomaliiPrukriplennaPlacentuNoCheckBox = QCheckBox('Ні')
        self.AnomaliiPrukriplennaPlacentuNoCheckBox.setChecked(1)
        self.AnomaliiPrukriplennaPlacentuNoCheckBox.stateChanged.connect(
            self.AnomaliiPrukriplennaPlacentuNoFunc)

        self.AnomaliiPrukriplennaPlacentuAdherensCheckBox = QCheckBox(
            'adherens')
        self.AnomaliiPrukriplennaPlacentuAdherensCheckBox.setEnabled(0)
        self.AnomaliiPrukriplennaPlacentuAdherensCheckBox.stateChanged.connect(
            self.AnomaliiPrukriplennaPlacentuAdherensFunc)

        self.AnomaliiPrukriplennaPlacentuAcretaCheckBox = QCheckBox('acreta')
        self.AnomaliiPrukriplennaPlacentuAcretaCheckBox.setEnabled(0)
        self.AnomaliiPrukriplennaPlacentuAcretaCheckBox.stateChanged.connect(
            self.AnomaliiPrukriplennaPlacentuAcretaFunc)

        self.AnomaliiPrukriplennaPlacentuPercretaCheckBox = QCheckBox(
            'percreta')
        self.AnomaliiPrukriplennaPlacentuPercretaCheckBox.setEnabled(0)
        self.AnomaliiPrukriplennaPlacentuPercretaCheckBox.stateChanged.connect(
            self.AnomaliiPrukriplennaPlacentuPercretaFunc)

        self.AnomaliiPrukriplennaPlacentuSplitter = QSplitter(Qt.Horizontal)
        self.AnomaliiPrukriplennaPlacentuSplitter.addWidget(
            self.AnomaliiPrukriplennaPlacentuLabel)
        self.AnomaliiPrukriplennaPlacentuSplitter.addWidget(
            self.AnomaliiPrukriplennaPlacentuNoCheckBox)
        self.AnomaliiPrukriplennaPlacentuSplitter.addWidget(
            self.AnomaliiPrukriplennaPlacentuAdherensCheckBox)
        self.AnomaliiPrukriplennaPlacentuSplitter.addWidget(
            self.AnomaliiPrukriplennaPlacentuAcretaCheckBox)
        self.AnomaliiPrukriplennaPlacentuSplitter.addWidget(
            self.AnomaliiPrukriplennaPlacentuPercretaCheckBox)

        #    10) Дефект посліду: а) ні  б) так
        self.DefektPoslidyLabel = QLabel('    10. Дефект посліду:')
        self.DefektPoslidyLabel.setFixedHeight(15)
        self.DefektPoslidyLabel.setFixedWidth(400)

        self.DefektPoslidyNoCheckBox = QCheckBox('Ні')
        self.DefektPoslidyNoCheckBox.setChecked(1)
        self.DefektPoslidyNoCheckBox.setFixedWidth(40)
        self.DefektPoslidyNoCheckBox.stateChanged.connect(
            self.DefektPoslidyNoFunc)

        self.DefektPoslidyYesCheckBox = QCheckBox('Так')
        self.DefektPoslidyYesCheckBox.setEnabled(0)
        self.DefektPoslidyYesCheckBox.stateChanged.connect(
            self.DefektPoslidyYesFunc)

        self.DefektPoslidySplitter = QSplitter(Qt.Horizontal)
        self.DefektPoslidySplitter.addWidget(self.DefektPoslidyLabel)
        self.DefektPoslidySplitter.addWidget(self.DefektPoslidyNoCheckBox)
        self.DefektPoslidySplitter.addWidget(self.DefektPoslidyYesCheckBox)

        #    11) Дефект оболонок: а) ні  б) так
        self.DefektObolonokLabel = QLabel('    11. Дефект оболонок:')
        self.DefektObolonokLabel.setFixedHeight(15)
        self.DefektObolonokLabel.setFixedWidth(400)

        self.DefektObolonokNoCheckBox = QCheckBox('Ні')
        self.DefektObolonokNoCheckBox.setChecked(1)
        self.DefektObolonokNoCheckBox.setFixedWidth(40)
        self.DefektObolonokNoCheckBox.stateChanged.connect(
            self.DefektObolonokNoFunc)

        self.DefektObolonokYesCheckBox = QCheckBox('Так')
        self.DefektObolonokYesCheckBox.setEnabled(0)
        self.DefektObolonokYesCheckBox.stateChanged.connect(
            self.DefektObolonokYesFunc)

        self.DefektObolonokSplitter = QSplitter(Qt.Horizontal)
        self.DefektObolonokSplitter.addWidget(self.DefektObolonokLabel)
        self.DefektObolonokSplitter.addWidget(self.DefektObolonokNoCheckBox)
        self.DefektObolonokSplitter.addWidget(self.DefektObolonokYesCheckBox)

        #    12) Аномалії прикріплення пуповини: а) ні, б) оболонкове
        self.AnomaliiPrukriplennaPypovunuLabel = QLabel(
            '    12. Аномалії прикріплення пуповини:')
        self.AnomaliiPrukriplennaPypovunuLabel.setFixedHeight(15)
        self.AnomaliiPrukriplennaPypovunuLabel.setFixedWidth(400)

        self.AnomaliiPrukriplennaPypovunuNoCheckBox = QCheckBox('Ні')
        self.AnomaliiPrukriplennaPypovunuNoCheckBox.setChecked(1)
        self.AnomaliiPrukriplennaPypovunuNoCheckBox.setFixedWidth(40)
        self.AnomaliiPrukriplennaPypovunuNoCheckBox.stateChanged.connect(
            self.AnomaliiPrukriplennaPypovunuNoFunc)

        self.AnomaliiPrukriplennaPypovunuObolonkoveCheckBox = QCheckBox(
            'Oболонкове')
        self.AnomaliiPrukriplennaPypovunuObolonkoveCheckBox.setEnabled(0)
        self.AnomaliiPrukriplennaPypovunuObolonkoveCheckBox.stateChanged.connect(
            self.AnomaliiPrukriplennaPypovunuObolonkoveFunc)

        self.AnomaliiPrukriplennaPypovunuSplitter = QSplitter(Qt.Horizontal)
        self.AnomaliiPrukriplennaPypovunuSplitter.addWidget(
            self.AnomaliiPrukriplennaPypovunuLabel)
        self.AnomaliiPrukriplennaPypovunuSplitter.addWidget(
            self.AnomaliiPrukriplennaPypovunuNoCheckBox)
        self.AnomaliiPrukriplennaPypovunuSplitter.addWidget(
            self.AnomaliiPrukriplennaPypovunuObolonkoveCheckBox)

        # 13) Оперативна допомога: а) ні б) ручна ревізія стінок порожнини матки в) інструментальна ревізія стінок порожнини матки г) ручне відокремлення плаценти та видалення посліду
        self.OperatuvnaDopomogaLabel = QLabel('    13. Оперативна допомога:')
        self.OperatuvnaDopomogaLabel.setFixedHeight(15)
        # self.OperatuvnaDopomogaLabel.setFixedWidth(400)

        self.OperatuvnaDopomogaNoCheckBox = QCheckBox('Ні')
        self.OperatuvnaDopomogaNoCheckBox.setChecked(1)
        self.OperatuvnaDopomogaNoCheckBox.setFixedWidth(40)
        self.OperatuvnaDopomogaNoCheckBox.stateChanged.connect(
            self.OperatuvnaDopomogaNoFunc)

        self.OperatuvnaDopomogaRychnaReviziaCheckBox = QCheckBox(
            'Ручна ревізія стінок порожнини матки')
        self.OperatuvnaDopomogaRychnaReviziaCheckBox.setEnabled(0)
        # self.OperatuvnaDopomogaRychnaReviziaCheckBox.stateChanged.connect(self.OperatuvnaDopomogaRychnaReviziaFunc)

        self.OperatuvnaDopomogaInstrymentalnaReviziaCheckBox = QCheckBox(
            'Інструментальна ревізія стінок порожнини матки')
        self.OperatuvnaDopomogaInstrymentalnaReviziaCheckBox.setEnabled(0)
        # self.OperatuvnaDopomogaInstrymentalnaReviziaCheckBox.stateChanged.connect(self.OperatuvnaDopomogaInstrymentalnaReviziaFunc)

        self.OperatuvnaDopomogaRychneVidokremlennaCheckBox = QCheckBox(
            'Ручне відокремлення плаценти та видалення посліду')
        self.OperatuvnaDopomogaRychneVidokremlennaCheckBox.setEnabled(0)
        # self.OperatuvnaDopomogaRychneVidokremlennaCheckBox.stateChanged.connect(self.OperatuvnaDopomogaRychneVidokremlennaFunc)

        self.OperatuvnaDopomogaSplitter = QSplitter(Qt.Horizontal)
        self.OperatuvnaDopomogaSplitter.addWidget(self.OperatuvnaDopomogaLabel)
        self.OperatuvnaDopomogaSplitter.addWidget(
            self.OperatuvnaDopomogaNoCheckBox)
        self.OperatuvnaDopomogaSplitter.addWidget(
            self.OperatuvnaDopomogaRychnaReviziaCheckBox)
        self.OperatuvnaDopomogaSplitter.addWidget(
            self.OperatuvnaDopomogaInstrymentalnaReviziaCheckBox)
        self.OperatuvnaDopomogaSplitter.addWidget(
            self.OperatuvnaDopomogaRychneVidokremlennaCheckBox)

        # 14) Розриви пологових шляхів: а) ні  б) промежини    в) піхви  г) шийки матки
        self.RozruvuPologovuhShlahivLabel = QLabel(
            '    14. Розриви пологових шляхів:')
        self.RozruvuPologovuhShlahivLabel.setFixedHeight(15)
        self.RozruvuPologovuhShlahivLabel.setFixedWidth(400)

        self.RozruvuPologovuhShlahivNoCheckBox = QCheckBox('Ні')
        self.RozruvuPologovuhShlahivNoCheckBox.setChecked(1)
        self.RozruvuPologovuhShlahivNoCheckBox.setFixedWidth(40)
        self.RozruvuPologovuhShlahivNoCheckBox.stateChanged.connect(
            self.RozruvuPologovuhShlahivNoFunc)

        self.RozruvuPologovuhShlahivPromejunuCheckBox = QCheckBox('Промежини')
        self.RozruvuPologovuhShlahivPromejunuCheckBox.setEnabled(0)
        self.RozruvuPologovuhShlahivPromejunuCheckBox.setFixedWidth(100)

        self.RozruvuPologovuhShlahivPihvuCheckBox = QCheckBox('Піхви')
        self.RozruvuPologovuhShlahivPihvuCheckBox.setFixedWidth(80)
        self.RozruvuPologovuhShlahivPihvuCheckBox.setEnabled(0)

        self.RozruvuPologovuhShlahivShuikiMatkuCheckBox = QCheckBox(
            'Шийки матки')
        self.RozruvuPologovuhShlahivShuikiMatkuCheckBox.setEnabled(0)

        self.StypinRozruvyPologovuhShlahivLabel = QLabel('Ступінь:')
        self.StypinRozruvyPologovuhShlahivLabel.hide()
        self.StypinRozruvyPologovuhShlahivLabel.setFixedWidth(45)

        self.StypinRozruvyPologovuhShlahivLineEdit = QLineEdit()
        self.StypinRozruvyPologovuhShlahivLineEdit.hide()

        self.RozruvuPologovuhShlahivSplitter = QSplitter(Qt.Horizontal)
        self.RozruvuPologovuhShlahivSplitter.addWidget(
            self.RozruvuPologovuhShlahivLabel)
        self.RozruvuPologovuhShlahivSplitter.addWidget(
            self.RozruvuPologovuhShlahivNoCheckBox)
        self.RozruvuPologovuhShlahivSplitter.addWidget(
            self.RozruvuPologovuhShlahivPromejunuCheckBox)
        self.RozruvuPologovuhShlahivSplitter.addWidget(
            self.RozruvuPologovuhShlahivPihvuCheckBox)
        self.RozruvuPologovuhShlahivSplitter.addWidget(
            self.RozruvuPologovuhShlahivShuikiMatkuCheckBox)
        self.RozruvuPologovuhShlahivSplitter.addWidget(
            self.StypinRozruvyPologovuhShlahivLabel)
        self.RozruvuPologovuhShlahivSplitter.addWidget(
            self.StypinRozruvyPologovuhShlahivLineEdit)

        # 15) Епізіо- або перінеотомія: а) так  б) ні
        self.EpizoAboPerineotomiaLabel = QLabel(
            '    15. Епізіо- або перінеотомія:')
        self.EpizoAboPerineotomiaLabel.setFixedHeight(15)
        self.EpizoAboPerineotomiaLabel.setFixedWidth(400)

        self.EpizoAboPerineotomiaNoCheckBox = QCheckBox('Ні')
        self.EpizoAboPerineotomiaNoCheckBox.setChecked(1)
        self.EpizoAboPerineotomiaNoCheckBox.setFixedWidth(40)
        self.EpizoAboPerineotomiaNoCheckBox.stateChanged.connect(
            self.EpizoAboPerineotomiaNoFunc)

        self.EpizoAboPerineotomiaYesCheckBox = QCheckBox('Так')
        self.EpizoAboPerineotomiaYesCheckBox.setEnabled(0)
        self.EpizoAboPerineotomiaYesCheckBox.stateChanged.connect(
            self.EpizoAboPerineotomiaYesFunc)

        self.EpizoAboPerineotomiaSplitter = QSplitter(Qt.Horizontal)
        self.EpizoAboPerineotomiaSplitter.addWidget(
            self.EpizoAboPerineotomiaLabel)
        self.EpizoAboPerineotomiaSplitter.addWidget(
            self.EpizoAboPerineotomiaNoCheckBox)
        self.EpizoAboPerineotomiaSplitter.addWidget(
            self.EpizoAboPerineotomiaYesCheckBox)

        # 16) Крововтрата в пологах __________
        self.KrovovtrataVPologahLabel = QLabel(
            '    16. Крововтрата в пологах:')
        self.KrovovtrataVPologahLabel.setFixedHeight(15)
        self.KrovovtrataVPologahLabel.setFixedWidth(400)

        self.KrovovtrataVPologahLineEdit = QLineEdit()
        self.KrovovtrataVPologahLineEdit.setMaximumWidth(200)

        self.KrovovtrataVPologahSplitter = QSplitter(Qt.Horizontal)
        self.KrovovtrataVPologahSplitter.addWidget(
            self.KrovovtrataVPologahLabel)
        self.KrovovtrataVPologahSplitter.addWidget(
            self.KrovovtrataVPologahLineEdit)

        # 17)Тривалість пологів загальна:  ____год. ____хв.
        self.TruvalistPologivZagalnaLabel = QLabel(
            '    17. Тривалість пологів загальна:')
        self.TruvalistPologivZagalnaLabel.setFixedHeight(15)
        self.TruvalistPologivZagalnaLabel.setFixedWidth(400)

        self.TruvalistPologivZagalnaGodunLineEdit = QLineEdit()
        self.TruvalistPologivZagalnaGodunLineEdit.setFixedWidth(40)
        self.TruvalistPologivZagalnaGodunLineEdit.setInputMask("D0")

        self.TruvalistPologivZagalnaGodunLabel = QLabel('год.')
        self.TruvalistPologivZagalnaGodunLabel.setFixedWidth(30)

        self.TruvalistPologivZagalnaHvulunLineEdit = QLineEdit()
        self.TruvalistPologivZagalnaHvulunLineEdit.setFixedWidth(40)
        self.TruvalistPologivZagalnaHvulunLineEdit.setInputMask("D0")

        self.TruvalistPologivZagalnaHvulunLabel = QLabel('хв.')

        self.TruvalistPologivZagalnaSplitter = QSplitter(Qt.Horizontal)
        self.TruvalistPologivZagalnaSplitter.addWidget(
            self.TruvalistPologivZagalnaLabel)
        self.TruvalistPologivZagalnaSplitter.addWidget(
            self.TruvalistPologivZagalnaGodunLineEdit)
        self.TruvalistPologivZagalnaSplitter.addWidget(
            self.TruvalistPologivZagalnaGodunLabel)
        self.TruvalistPologivZagalnaSplitter.addWidget(
            self.TruvalistPologivZagalnaHvulunLineEdit)
        self.TruvalistPologivZagalnaSplitter.addWidget(
            self.TruvalistPologivZagalnaHvulunLabel)

        #      - Ι період: 	____год. ____хв.
        self.TruvalistPologiIPeriodLabel = QLabel('      - Ι період:')
        self.TruvalistPologiIPeriodLabel.setFixedHeight(15)
        self.TruvalistPologiIPeriodLabel.setFixedWidth(400)
        self.TruvalistPologiIPeriodLabel.setAlignment(Qt.AlignRight
                                                      | Qt.AlignVCenter)

        self.TruvalistPologivIPeriodLineEdit = QLineEdit()
        self.TruvalistPologivIPeriodLineEdit.setFixedWidth(40)
        self.TruvalistPologivIPeriodLineEdit.setInputMask("D0")

        self.TruvalistPologivIPeriodGodunLabel = QLabel('год.')
        self.TruvalistPologivIPeriodGodunLabel.setFixedWidth(30)

        self.TruvalistPologivIPeriodHvulunLineEdit = QLineEdit()
        self.TruvalistPologivIPeriodHvulunLineEdit.setFixedWidth(40)
        self.TruvalistPologivIPeriodHvulunLineEdit.setInputMask("D0")

        self.TruvalistPologivIPeriodHvulunLabel = QLabel('хв.')

        self.TruvalistPologivIPeriodSplitter = QSplitter(Qt.Horizontal)
        self.TruvalistPologivIPeriodSplitter.addWidget(
            self.TruvalistPologiIPeriodLabel)
        self.TruvalistPologivIPeriodSplitter.addWidget(
            self.TruvalistPologivIPeriodLineEdit)
        self.TruvalistPologivIPeriodSplitter.addWidget(
            self.TruvalistPologivIPeriodGodunLabel)
        self.TruvalistPologivIPeriodSplitter.addWidget(
            self.TruvalistPologivIPeriodHvulunLineEdit)
        self.TruvalistPologivIPeriodSplitter.addWidget(
            self.TruvalistPologivIPeriodHvulunLabel)

        #     - ΙΙ період:       ____год. ____хв.
        self.TruvalistPologiIIPeriodLabel = QLabel('      - ΙI період:')
        self.TruvalistPologiIIPeriodLabel.setFixedHeight(15)
        self.TruvalistPologiIIPeriodLabel.setFixedWidth(400)
        self.TruvalistPologiIIPeriodLabel.setAlignment(Qt.AlignRight
                                                       | Qt.AlignVCenter)

        self.TruvalistPologivIIPeriodLineEdit = QLineEdit()
        self.TruvalistPologivIIPeriodLineEdit.setFixedWidth(40)
        self.TruvalistPologivIIPeriodLineEdit.setInputMask("D0")

        self.TruvalistPologivIIPeriodGodunLabel = QLabel('год.')
        self.TruvalistPologivIIPeriodGodunLabel.setFixedWidth(30)

        self.TruvalistPologivIIPeriodHvulunLineEdit = QLineEdit()
        self.TruvalistPologivIIPeriodHvulunLineEdit.setFixedWidth(40)
        self.TruvalistPologivIIPeriodHvulunLineEdit.setInputMask("D0")

        self.TruvalistPologivIIPeriodHvulunLabel = QLabel('хв.')

        self.TruvalistPologivIIPeriodSplitter = QSplitter(Qt.Horizontal)
        self.TruvalistPologivIIPeriodSplitter.addWidget(
            self.TruvalistPologiIIPeriodLabel)
        self.TruvalistPologivIIPeriodSplitter.addWidget(
            self.TruvalistPologivIIPeriodLineEdit)
        self.TruvalistPologivIIPeriodSplitter.addWidget(
            self.TruvalistPologivIIPeriodGodunLabel)
        self.TruvalistPologivIIPeriodSplitter.addWidget(
            self.TruvalistPologivIIPeriodHvulunLineEdit)
        self.TruvalistPologivIIPeriodSplitter.addWidget(
            self.TruvalistPologivIIPeriodHvulunLabel)

        #     - ΙΙΙ період:      ____год. ____хв.
        self.TruvalistPologiIIIPeriodLabel = QLabel('      - ΙII період:')
        self.TruvalistPologiIIIPeriodLabel.setFixedHeight(15)
        self.TruvalistPologiIIIPeriodLabel.setFixedWidth(400)
        self.TruvalistPologiIIIPeriodLabel.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter)

        self.TruvalistPologivIIIPeriodLineEdit = QLineEdit()
        self.TruvalistPologivIIIPeriodLineEdit.setFixedWidth(40)
        self.TruvalistPologivIIIPeriodLineEdit.setInputMask("D0")

        self.TruvalistPologivIIIPeriodGodunLabel = QLabel('год.')
        self.TruvalistPologivIIIPeriodGodunLabel.setFixedWidth(30)

        self.TruvalistPologivIIIPeriodHvulunLineEdit = QLineEdit()
        self.TruvalistPologivIIIPeriodHvulunLineEdit.setFixedWidth(40)
        self.TruvalistPologivIIIPeriodHvulunLineEdit.setInputMask("D0")

        self.TruvalistPologivIIIPeriodHvulunLabel = QLabel('хв.')

        self.TruvalistPologivIIIPeriodSplitter = QSplitter(Qt.Horizontal)
        self.TruvalistPologivIIIPeriodSplitter.addWidget(
            self.TruvalistPologiIIIPeriodLabel)
        self.TruvalistPologivIIIPeriodSplitter.addWidget(
            self.TruvalistPologivIIIPeriodLineEdit)
        self.TruvalistPologivIIIPeriodSplitter.addWidget(
            self.TruvalistPologivIIIPeriodGodunLabel)
        self.TruvalistPologivIIIPeriodSplitter.addWidget(
            self.TruvalistPologivIIIPeriodHvulunLineEdit)
        self.TruvalistPologivIIIPeriodSplitter.addWidget(
            self.TruvalistPologivIIIPeriodHvulunLabel)

        # Финальный сплиттер пункта VII. Перебіг даних пологів.
        self.PerebigDannuhPologivSplitter = QSplitter(Qt.Vertical)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.PerebigDannuhPologivLabel)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.PologuVaginalniSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.PologuAbdominalniSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.PokazannaDlaAbdominalnogoRozrodjennaSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.PoryshennaPologovoiDialnostiSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.KorekciaAnomaliiPologovoiDialnostiSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.VuluvNavkoloplodovuhVodSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.DustressPlodaVPologahSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.GipotonichnaKrovotechaSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.AnomaliiPrukriplennaPlacentuSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(self.DefektPoslidySplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.DefektObolonokSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.AnomaliiPrukriplennaPypovunuSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.OperatuvnaDopomogaSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.RozruvuPologovuhShlahivSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.EpizoAboPerineotomiaSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.KrovovtrataVPologahSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.TruvalistPologivZagalnaSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.TruvalistPologivIPeriodSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.TruvalistPologivIIPeriodSplitter)
        self.PerebigDannuhPologivSplitter.addWidget(
            self.TruvalistPologivIIIPeriodSplitter)

        # VIII. Стан новонародженого та перебіг раннього неонатального періоду.
        self.StanNovonarodgennogoTaNeoPeriodLabel = QLabel(
            '  VIII) Стан новонародженого та перебіг раннього неонатального періоду.'
        )
        self.StanNovonarodgennogoTaNeoPeriodLabel.setFixedHeight(30)
        self.StanNovonarodgennogoTaNeoPeriodLabel.setStyleSheet(
            """QLabel{font-size:8pt; font-weight:600; color:#aa0000;}""")

        # 1)	Народився а) живий, б) мертвий
        self.NaroduvsaLabel = QLabel('    1. Народився:')
        self.NaroduvsaLabel.setFixedHeight(15)
        self.NaroduvsaLabel.setFixedWidth(400)

        self.NaroduvsaGuvuiCheckBox = QCheckBox('Живий')
        self.NaroduvsaGuvuiCheckBox.setChecked(1)
        self.NaroduvsaGuvuiCheckBox.setFixedWidth(100)
        self.NaroduvsaGuvuiCheckBox.stateChanged.connect(
            self.NaroduvsaGuvuiFunc)

        self.NaroduvsaMertvuiCheckBox = QCheckBox('Мертвий')
        self.NaroduvsaMertvuiCheckBox.setEnabled(0)
        self.NaroduvsaMertvuiCheckBox.stateChanged.connect(
            self.NaroduvsaMertvuiFunc)

        self.NaroduvsaSplitter = QSplitter(Qt.Horizontal)
        self.NaroduvsaSplitter.addWidget(self.NaroduvsaLabel)
        self.NaroduvsaSplitter.addWidget(self.NaroduvsaGuvuiCheckBox)
        self.NaroduvsaSplitter.addWidget(self.NaroduvsaMertvuiCheckBox)

        # 2)	Причина мертвонародження а) антенатальна, б) інтранатальна
        self.PruchunaMertvonarodgennaLabel = QLabel(
            '    2. Причина мертвонародження:')
        self.PruchunaMertvonarodgennaLabel.setFixedHeight(15)
        self.PruchunaMertvonarodgennaLabel.setFixedWidth(400)
        self.PruchunaMertvonarodgennaLabel.setEnabled(0)

        self.PruchunaMertvonarodgennaAntenatalnaCheckBox = QCheckBox(
            'Антенатальна')
        self.PruchunaMertvonarodgennaAntenatalnaCheckBox.setEnabled(0)
        self.PruchunaMertvonarodgennaAntenatalnaCheckBox.setFixedWidth(100)
        self.PruchunaMertvonarodgennaAntenatalnaCheckBox.stateChanged.connect(
            self.PruchunaMertvonarodgennaAntenatalnaFunc)

        self.PruchunaMertvonarodgennaInternatalnaCheckBox = QCheckBox(
            'Інтранатальна')
        self.PruchunaMertvonarodgennaInternatalnaCheckBox.setEnabled(0)
        self.PruchunaMertvonarodgennaInternatalnaCheckBox.stateChanged.connect(
            self.PruchunaMertvonarodgennaInternatalnaFunc)

        self.PruchunaMertvonarodgennaSplitter = QSplitter(Qt.Horizontal)
        self.PruchunaMertvonarodgennaSplitter.addWidget(
            self.PruchunaMertvonarodgennaLabel)
        self.PruchunaMertvonarodgennaSplitter.addWidget(
            self.PruchunaMertvonarodgennaAntenatalnaCheckBox)
        self.PruchunaMertvonarodgennaSplitter.addWidget(
            self.PruchunaMertvonarodgennaInternatalnaCheckBox)

        # 3)	Зрілість новонародженого:
        # а) доношений; б)недоношений; в) переношений
        self.ZrilistNovonarodgennogoLabel = QLabel(
            '    3. Зрілість новонародженого:')
        self.ZrilistNovonarodgennogoLabel.setFixedHeight(15)
        self.ZrilistNovonarodgennogoLabel.setFixedWidth(400)

        self.ZrilistNovonarodgennogoDonoshenuiCheckBox = QCheckBox('Доношений')
        self.ZrilistNovonarodgennogoDonoshenuiCheckBox.setFixedWidth(100)
        self.ZrilistNovonarodgennogoDonoshenuiCheckBox.setChecked(1)
        self.ZrilistNovonarodgennogoDonoshenuiCheckBox.stateChanged.connect(
            self.ZrilistNovonarodgennogoDonoshenuiFunc)

        self.ZrilistNovonarodgennogoNedonoshenuiCheckBox = QCheckBox(
            'Недоношений')
        self.ZrilistNovonarodgennogoNedonoshenuiCheckBox.setEnabled(0)
        self.ZrilistNovonarodgennogoNedonoshenuiCheckBox.stateChanged.connect(
            self.ZrilistNovonarodgennogoNedonoshenuiFunc)

        self.ZrilistNovonarodgennogoPerenoshenuiCheckBox = QCheckBox(
            'Переношений')
        self.ZrilistNovonarodgennogoPerenoshenuiCheckBox.setEnabled(0)
        self.ZrilistNovonarodgennogoPerenoshenuiCheckBox.stateChanged.connect(
            self.ZrilistNovonarodgennogoPerenoshenuiFunc)

        self.ZrilistNovonarodgennogoSplitter = QSplitter(Qt.Horizontal)
        self.ZrilistNovonarodgennogoSplitter.addWidget(
            self.ZrilistNovonarodgennogoLabel)
        self.ZrilistNovonarodgennogoSplitter.addWidget(
            self.ZrilistNovonarodgennogoDonoshenuiCheckBox)
        self.ZrilistNovonarodgennogoSplitter.addWidget(
            self.ZrilistNovonarodgennogoNedonoshenuiCheckBox)
        self.ZrilistNovonarodgennogoSplitter.addWidget(
            self.ZrilistNovonarodgennogoPerenoshenuiCheckBox)

        # ) маса_________ зріст_________ Коефіцієнт ____
        self.MasaNovonarodgenogoLabel = QLabel('    4. Маса:')
        self.MasaNovonarodgenogoLabel.setFixedWidth(50)
        self.MasaNovonarodgenogoLineEdit = QLineEdit()
        self.MasaNovonarodgenogoLineEdit.setFixedWidth(100)

        self.ZristNovonarodgenogoLabel = QLabel('Зріст:')
        self.ZristNovonarodgenogoLabel.setFixedWidth(50)
        self.ZristNovonarodgenogoLabel.setAlignment(Qt.AlignRight
                                                    | Qt.AlignVCenter)
        self.ZristNovonarodgenogoLineEdit = QLineEdit()
        self.ZristNovonarodgenogoLineEdit.setFixedWidth(100)

        self.KoeficientNovonarodgenogoLabel = QLabel('Коефіцієнт:')
        self.KoeficientNovonarodgenogoLabel.setFixedWidth(80)
        self.KoeficientNovonarodgenogoLabel.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter)
        self.KoeficientNovonarodgenogoLineEdit = QLineEdit()
        self.KoeficientNovonarodgenogoLineEdit.setFixedWidth(100)

        self.MasaZristKoeficientSplitter = QSplitter(Qt.Horizontal)
        self.MasaZristKoeficientSplitter.addWidget(
            self.MasaNovonarodgenogoLabel)
        self.MasaZristKoeficientSplitter.addWidget(
            self.MasaNovonarodgenogoLineEdit)
        self.MasaZristKoeficientSplitter.addWidget(
            self.ZristNovonarodgenogoLabel)
        self.MasaZristKoeficientSplitter.addWidget(
            self.ZristNovonarodgenogoLineEdit)
        self.MasaZristKoeficientSplitter.addWidget(
            self.KoeficientNovonarodgenogoLabel)
        self.MasaZristKoeficientSplitter.addWidget(
            self.KoeficientNovonarodgenogoLineEdit)

        # 4.1. Гіпотрофія плода:  а) ні  б) так
        self.GipotrofiaPlodaLabel = QLabel('       4.1. Гіпотрофія плода:')
        self.GipotrofiaPlodaLabel.setFixedHeight(15)
        self.GipotrofiaPlodaLabel.setFixedWidth(400)

        self.GipotrofiaPlodaNoCheckBox = QCheckBox('Ні')
        self.GipotrofiaPlodaNoCheckBox.setChecked(1)
        self.GipotrofiaPlodaNoCheckBox.setFixedWidth(100)
        self.GipotrofiaPlodaNoCheckBox.stateChanged.connect(
            self.GipotrofiaPlodaNoFunc)

        self.GipotrofiaPlodaYesCheckBox = QCheckBox('Так')
        self.GipotrofiaPlodaYesCheckBox.setEnabled(0)
        self.GipotrofiaPlodaYesCheckBox.stateChanged.connect(
            self.GipotrofiaPlodaYesFunc)

        self.GipotrofiaPlodaSplitter = QSplitter(Qt.Horizontal)
        self.GipotrofiaPlodaSplitter.addWidget(self.GipotrofiaPlodaLabel)
        self.GipotrofiaPlodaSplitter.addWidget(self.GipotrofiaPlodaNoCheckBox)
        self.GipotrofiaPlodaSplitter.addWidget(self.GipotrofiaPlodaYesCheckBox)

        # 5) оцінка за шкалою Апгар: а) на 1 хв.______  б) на 5 хв.______
        self.OcinkaZaShkaloyApgarLabel = QLabel(
            '    5. Oцінка за шкалою Апгар::')
        self.OcinkaZaShkaloyApgarLabel.setFixedWidth(400)

        self.OcinkaZaShkaloyApgarNaPerHvLabel = QLabel('а) на 1 хв.:')
        self.OcinkaZaShkaloyApgarNaPerHvLabel.setFixedWidth(60)
        self.OcinkaZaShkaloyApgarNaPerHvLabel.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter)
        self.OcinkaZaShkaloyApgarNaPerHvLineEdit = QLineEdit()
        self.OcinkaZaShkaloyApgarNaPerHvLineEdit.setFixedWidth(20)
        self.OcinkaZaShkaloyApgarNaPerHvLineEdit.setInputMask("D0")

        self.OcinkaZaShkaloyApgarNa5HvLabel = QLabel('б) на 5 хв.:')
        self.OcinkaZaShkaloyApgarNa5HvLabel.setFixedWidth(70)
        self.OcinkaZaShkaloyApgarNa5HvLabel.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter)
        self.OcinkaZaShkaloyApgarNa5HvLineEdit = QLineEdit()
        self.OcinkaZaShkaloyApgarNa5HvLineEdit.setFixedWidth(20)
        self.OcinkaZaShkaloyApgarNa5HvLineEdit.setInputMask("D0")

        self.OcinkaZaShkaloyApgarSplitter = QSplitter(Qt.Horizontal)
        self.OcinkaZaShkaloyApgarSplitter.addWidget(
            self.OcinkaZaShkaloyApgarLabel)
        self.OcinkaZaShkaloyApgarSplitter.addWidget(
            self.OcinkaZaShkaloyApgarNaPerHvLabel)
        self.OcinkaZaShkaloyApgarSplitter.addWidget(
            self.OcinkaZaShkaloyApgarNaPerHvLineEdit)
        self.OcinkaZaShkaloyApgarSplitter.addWidget(
            self.OcinkaZaShkaloyApgarNa5HvLabel)
        self.OcinkaZaShkaloyApgarSplitter.addWidget(
            self.OcinkaZaShkaloyApgarNa5HvLineEdit)

        # 6) новонароджений з вадами розвиту: а) ні  б) так  в) які саме
        self.NovonarodjenuiZVadamuRozvutkyLabel = QLabel(
            '    6. Новонароджений з вадами розвиту:')
        self.NovonarodjenuiZVadamuRozvutkyLabel.setFixedHeight(15)
        self.NovonarodjenuiZVadamuRozvutkyLabel.setFixedWidth(400)

        self.NovonarodjenuiZVadamuRozvutkyNoCheckBox = QCheckBox('Ні')
        self.NovonarodjenuiZVadamuRozvutkyNoCheckBox.setChecked(1)
        self.NovonarodjenuiZVadamuRozvutkyNoCheckBox.setFixedWidth(100)
        self.NovonarodjenuiZVadamuRozvutkyNoCheckBox.stateChanged.connect(
            self.NovonarodjenuiZVadamuRozvutkyNoFunc)

        self.NovonarodjenuiZVadamuRozvutkyYesCheckBox = QCheckBox('Так')
        self.NovonarodjenuiZVadamuRozvutkyYesCheckBox.setEnabled(0)
        self.NovonarodjenuiZVadamuRozvutkyYesCheckBox.stateChanged.connect(
            self.NovonarodjenuiZVadamuRozvutkyYesFunc)

        self.NovonarodjenuiZVadamuRozvutkyJakiSameLabel = QLabel('Які саме:')
        self.NovonarodjenuiZVadamuRozvutkyJakiSameLabel.hide()
        self.NovonarodjenuiZVadamuRozvutkyJakiSameLineEdit = QLineEdit()
        self.NovonarodjenuiZVadamuRozvutkyJakiSameLineEdit.setMinimumWidth(300)
        self.NovonarodjenuiZVadamuRozvutkyJakiSameLineEdit.hide()

        self.NovonarodjenuiZVadamuRozvutkySplitter = QSplitter(Qt.Horizontal)
        self.NovonarodjenuiZVadamuRozvutkySplitter.addWidget(
            self.NovonarodjenuiZVadamuRozvutkyLabel)
        self.NovonarodjenuiZVadamuRozvutkySplitter.addWidget(
            self.NovonarodjenuiZVadamuRozvutkyNoCheckBox)
        self.NovonarodjenuiZVadamuRozvutkySplitter.addWidget(
            self.NovonarodjenuiZVadamuRozvutkyYesCheckBox)
        self.NovonarodjenuiZVadamuRozvutkySplitter.addWidget(
            self.NovonarodjenuiZVadamuRozvutkyJakiSameLabel)
        self.NovonarodjenuiZVadamuRozvutkySplitter.addWidget(
            self.NovonarodjenuiZVadamuRozvutkyJakiSameLineEdit)

        # 7) пологова травма: а) ні  б) так  в) яка саме ____________________
        self.PologovaTravmaLabel = QLabel('    7. Пологова травма:')
        self.PologovaTravmaLabel.setFixedHeight(15)
        self.PologovaTravmaLabel.setFixedWidth(400)

        self.PologovaTravmaNoCheckBox = QCheckBox('Ні')
        self.PologovaTravmaNoCheckBox.setChecked(1)
        self.PologovaTravmaNoCheckBox.setFixedWidth(100)
        self.PologovaTravmaNoCheckBox.stateChanged.connect(
            self.PologovaTravmaNoFunc)

        self.PologovaTravmaYesCheckBox = QCheckBox('Так')
        self.PologovaTravmaYesCheckBox.setEnabled(0)
        self.PologovaTravmaYesCheckBox.stateChanged.connect(
            self.PologovaTravmaYesFunc)

        self.PologovaTravmaJakaSameLabel = QLabel('Яка саме:')
        self.PologovaTravmaJakaSameLabel.hide()
        self.PologovaTravmaJakaSameLineEdit = QLineEdit()
        self.PologovaTravmaJakaSameLineEdit.setMinimumWidth(300)
        self.PologovaTravmaJakaSameLineEdit.hide()

        self.PologovaTravmaSplitter = QSplitter(Qt.Horizontal)
        self.PologovaTravmaSplitter.addWidget(self.PologovaTravmaLabel)
        self.PologovaTravmaSplitter.addWidget(self.PologovaTravmaNoCheckBox)
        self.PologovaTravmaSplitter.addWidget(self.PologovaTravmaYesCheckBox)
        self.PologovaTravmaSplitter.addWidget(self.PologovaTravmaJakaSameLabel)
        self.PologovaTravmaSplitter.addWidget(
            self.PologovaTravmaJakaSameLineEdit)

        # 8) СДР: 					а) ні  б) так
        self.SDRLabel = QLabel('    8. СДР:')
        self.SDRLabel.setFixedHeight(15)
        self.SDRLabel.setFixedWidth(400)

        self.SDRNoCheckBox = QCheckBox('Ні')
        self.SDRNoCheckBox.setChecked(1)
        self.SDRNoCheckBox.setFixedWidth(100)
        self.SDRNoCheckBox.stateChanged.connect(self.SDRNoFunc)

        self.SDRYesCheckBox = QCheckBox('Так')
        self.SDRYesCheckBox.setEnabled(0)
        self.SDRYesCheckBox.stateChanged.connect(self.SDRYesFunc)

        self.SDRSplitter = QSplitter(Qt.Horizontal)
        self.SDRSplitter.addWidget(self.SDRLabel)
        self.SDRSplitter.addWidget(self.SDRNoCheckBox)
        self.SDRSplitter.addWidget(self.SDRYesCheckBox)

        # 9) внутрішньоутробне інфікування: а) ні  б) так
        self.VnytrishnoytrobneInfikyvannaLabel = QLabel(
            '    9. Внутрішньоутробне інфікування:')
        self.VnytrishnoytrobneInfikyvannaLabel.setFixedHeight(15)
        self.VnytrishnoytrobneInfikyvannaLabel.setFixedWidth(400)

        self.VnytrishnoytrobneInfikyvannaNoCheckBox = QCheckBox('Ні')
        self.VnytrishnoytrobneInfikyvannaNoCheckBox.setChecked(1)
        self.VnytrishnoytrobneInfikyvannaNoCheckBox.setFixedWidth(100)
        self.VnytrishnoytrobneInfikyvannaNoCheckBox.stateChanged.connect(
            self.VnytrishnoytrobneInfikyvannaNoFunc)

        self.VnytrishnoytrobneInfikyvannaYesCheckBox = QCheckBox('Так')
        self.VnytrishnoytrobneInfikyvannaYesCheckBox.setEnabled(0)
        self.VnytrishnoytrobneInfikyvannaYesCheckBox.stateChanged.connect(
            self.VnytrishnoytrobneInfikyvannaYesFunc)

        self.VnytrishnoytrobneInfikyvannaSplitter = QSplitter(Qt.Horizontal)
        self.VnytrishnoytrobneInfikyvannaSplitter.addWidget(
            self.VnytrishnoytrobneInfikyvannaLabel)
        self.VnytrishnoytrobneInfikyvannaSplitter.addWidget(
            self.VnytrishnoytrobneInfikyvannaNoCheckBox)
        self.VnytrishnoytrobneInfikyvannaSplitter.addWidget(
            self.VnytrishnoytrobneInfikyvannaYesCheckBox)

        # 10) геморагічні ускладнення:		а) ні  б) так
        self.GemoragichniYskladnennaLabel = QLabel(
            '    10. Геморагічні ускладнення:')
        self.GemoragichniYskladnennaLabel.setFixedHeight(15)
        self.GemoragichniYskladnennaLabel.setFixedWidth(400)

        self.GemoragichniYskladnennaNoCheckBox = QCheckBox('Ні')
        self.GemoragichniYskladnennaNoCheckBox.setChecked(1)
        self.GemoragichniYskladnennaNoCheckBox.setFixedWidth(100)
        self.GemoragichniYskladnennaNoCheckBox.stateChanged.connect(
            self.GemoragichniYskladnennaNoFunc)

        self.GemoragichniYskladnennaYesCheckBox = QCheckBox('Так')
        self.GemoragichniYskladnennaYesCheckBox.setEnabled(0)
        self.GemoragichniYskladnennaYesCheckBox.stateChanged.connect(
            self.GemoragichniYskladnennaYesFunc)

        self.GemoragichniYskladnennaSplitter = QSplitter(Qt.Horizontal)
        self.GemoragichniYskladnennaSplitter.addWidget(
            self.GemoragichniYskladnennaLabel)
        self.GemoragichniYskladnennaSplitter.addWidget(
            self.GemoragichniYskladnennaNoCheckBox)
        self.GemoragichniYskladnennaSplitter.addWidget(
            self.GemoragichniYskladnennaYesCheckBox)

        # 11) анемія: а) ні  б) І ступеня  в) II ступеня  г) IIІ ступеня
        self.AnemiaLabel = QLabel('    11. Aнемія:')
        self.AnemiaLabel.setFixedHeight(15)
        self.AnemiaLabel.setFixedWidth(400)

        self.AnemiaNoCheckBox = QCheckBox('Ні')
        self.AnemiaNoCheckBox.setChecked(1)
        # self.AnemiaNoCheckBox.setFixedWidth(100)
        self.AnemiaNoCheckBox.stateChanged.connect(self.AnemiaNoFunc)

        self.AnemiaIStypenaCheckBox = QCheckBox('І ступеня')
        self.AnemiaIStypenaCheckBox.setEnabled(0)
        self.AnemiaIStypenaCheckBox.stateChanged.connect(
            self.AnemiaIStypenaFunc)

        self.AnemiaIIStypenaCheckBox = QCheckBox('II ступеня')
        self.AnemiaIIStypenaCheckBox.setEnabled(0)
        self.AnemiaIIStypenaCheckBox.stateChanged.connect(
            self.AnemiaIIStypenaFunc)

        self.AnemiaIIIStypenaCheckBox = QCheckBox('IIІ ступеня')
        self.AnemiaIIIStypenaCheckBox.setEnabled(0)
        self.AnemiaIIIStypenaCheckBox.stateChanged.connect(
            self.AnemiaIIIStypenaFunc)

        self.AnemiaSplitter = QSplitter(Qt.Horizontal)
        self.AnemiaSplitter.addWidget(self.AnemiaLabel)
        self.AnemiaSplitter.addWidget(self.AnemiaNoCheckBox)
        self.AnemiaSplitter.addWidget(self.AnemiaIStypenaCheckBox)
        self.AnemiaSplitter.addWidget(self.AnemiaIIStypenaCheckBox)
        self.AnemiaSplitter.addWidget(self.AnemiaIIIStypenaCheckBox)

        # 12) гіпербілірубінемія: а) ні  б) так  в) рівень білірубіну___________
        self.GiperBilirybinemiaLabel = QLabel('    12. Гіпербілірубінемія:')
        self.GiperBilirybinemiaLabel.setFixedHeight(15)
        self.GiperBilirybinemiaLabel.setFixedWidth(400)

        self.GiperBilirybinemiaNoCheckBox = QCheckBox('Ні')
        self.GiperBilirybinemiaNoCheckBox.setChecked(1)
        self.GiperBilirybinemiaNoCheckBox.setFixedWidth(100)
        self.GiperBilirybinemiaNoCheckBox.stateChanged.connect(
            self.GiperBilirybinemiaNoFunc)

        self.GiperBilirybinemiaYesCheckBox = QCheckBox('Так')
        self.GiperBilirybinemiaYesCheckBox.setEnabled(0)
        self.GiperBilirybinemiaYesCheckBox.stateChanged.connect(
            self.GiperBilirybinemiaYesFunc)

        self.GiperBilirybinemiaRivenBilirybinyLabel = QLabel(
            'Рівень білірубіну:')
        self.GiperBilirybinemiaRivenBilirybinyLabel.hide()

        self.GiperBilirybinemiaRivenBilirybinyLineEdit = QLineEdit()
        self.GiperBilirybinemiaRivenBilirybinyLineEdit.setFixedWidth(100)
        self.GiperBilirybinemiaRivenBilirybinyLineEdit.setMinimumWidth(100)
        self.GiperBilirybinemiaRivenBilirybinyLineEdit.setMaximumWidth(200)
        self.GiperBilirybinemiaRivenBilirybinyLineEdit.hide()

        self.GiperBilirybinemiaSplitter = QSplitter(Qt.Horizontal)
        self.GiperBilirybinemiaSplitter.addWidget(self.GiperBilirybinemiaLabel)
        self.GiperBilirybinemiaSplitter.addWidget(
            self.GiperBilirybinemiaNoCheckBox)
        self.GiperBilirybinemiaSplitter.addWidget(
            self.GiperBilirybinemiaYesCheckBox)
        self.GiperBilirybinemiaSplitter.addWidget(
            self.GiperBilirybinemiaRivenBilirybinyLabel)
        self.GiperBilirybinemiaSplitter.addWidget(
            self.GiperBilirybinemiaRivenBilirybinyLineEdit)

        # 13) асфіксія: а)ні   б) легка   в) середня   г) важка
        self.AsfiksiaLabel = QLabel('    13. Aсфіксія:')
        self.AsfiksiaLabel.setFixedHeight(15)
        self.AsfiksiaLabel.setFixedWidth(400)

        self.AsfiksiaNoCheckBox = QCheckBox('Ні')
        self.AsfiksiaNoCheckBox.setChecked(1)
        # self.AnemiaNoCheckBox.setFixedWidth(100)
        self.AsfiksiaNoCheckBox.stateChanged.connect(self.AsfiksiaNoFunc)

        self.AsfiksiaLegkaCheckBox = QCheckBox('Легка')
        self.AsfiksiaLegkaCheckBox.setEnabled(0)
        self.AsfiksiaLegkaCheckBox.stateChanged.connect(self.AsfiksiaLegkaFunc)

        self.AsfiksiaSerednaCheckBox = QCheckBox('Середня')
        self.AsfiksiaSerednaCheckBox.setEnabled(0)
        self.AsfiksiaSerednaCheckBox.stateChanged.connect(
            self.AsfiksiaSerednaFunc)

        self.AsfiksiaVajkaCheckBox = QCheckBox('Важка')
        self.AsfiksiaVajkaCheckBox.setEnabled(0)
        self.AsfiksiaVajkaCheckBox.stateChanged.connect(self.AsfiksiaVajkaFunc)

        self.AsfiksiaSplitter = QSplitter(Qt.Horizontal)
        self.AsfiksiaSplitter.addWidget(self.AsfiksiaLabel)
        self.AsfiksiaSplitter.addWidget(self.AsfiksiaNoCheckBox)
        self.AsfiksiaSplitter.addWidget(self.AsfiksiaLegkaCheckBox)
        self.AsfiksiaSplitter.addWidget(self.AsfiksiaSerednaCheckBox)
        self.AsfiksiaSplitter.addWidget(self.AsfiksiaVajkaCheckBox)

        # 14) порушення кардіо-респіраторної адаптації: а)ні   б) так.
        self.PoryshennaKardioRespiratornoiAdaptaciiLabel = QLabel(
            '    14. Порушення кардіо-респіраторної адаптації:')
        self.PoryshennaKardioRespiratornoiAdaptaciiLabel.setFixedHeight(15)
        self.PoryshennaKardioRespiratornoiAdaptaciiLabel.setFixedWidth(400)

        self.PoryshennaKardioRespiratornoiAdaptaciiNoCheckBox = QCheckBox('Ні')
        self.PoryshennaKardioRespiratornoiAdaptaciiNoCheckBox.setChecked(1)
        self.PoryshennaKardioRespiratornoiAdaptaciiNoCheckBox.setFixedWidth(
            100)
        self.PoryshennaKardioRespiratornoiAdaptaciiNoCheckBox.stateChanged.connect(
            self.PoryshennaKardioRespiratornoiAdaptaciiNoFunc)

        self.PoryshennaKardioRespiratornoiAdaptaciiYesCheckBox = QCheckBox(
            'Так')
        self.PoryshennaKardioRespiratornoiAdaptaciiYesCheckBox.setEnabled(0)
        self.PoryshennaKardioRespiratornoiAdaptaciiYesCheckBox.stateChanged.connect(
            self.PoryshennaKardioRespiratornoiAdaptaciiYesFunc)

        self.PoryshennaKardioRespiratornoiAdaptaciiSplitter = QSplitter(
            Qt.Horizontal)
        self.PoryshennaKardioRespiratornoiAdaptaciiSplitter.addWidget(
            self.PoryshennaKardioRespiratornoiAdaptaciiLabel)
        self.PoryshennaKardioRespiratornoiAdaptaciiSplitter.addWidget(
            self.PoryshennaKardioRespiratornoiAdaptaciiNoCheckBox)
        self.PoryshennaKardioRespiratornoiAdaptaciiSplitter.addWidget(
            self.PoryshennaKardioRespiratornoiAdaptaciiYesCheckBox)

        # 15) втрата маси тіла___________грам
        self.VtrataMasuTilaLabel = QLabel('    15. Втрата маси тіла:')
        self.VtrataMasuTilaLabel.setFixedHeight(15)
        self.VtrataMasuTilaLabel.setFixedWidth(400)

        self.VtrataMasuTilaLineEdit = QLineEdit()
        self.VtrataMasuTilaLineEdit.setFixedWidth(100)

        self.VtrataMasuTilaGramLabel = QLabel('грам')

        self.VtrataMasuTilaSplitter = QSplitter(Qt.Horizontal)
        self.VtrataMasuTilaSplitter.addWidget(self.VtrataMasuTilaLabel)
        self.VtrataMasuTilaSplitter.addWidget(self.VtrataMasuTilaLineEdit)
        self.VtrataMasuTilaSplitter.addWidget(self.VtrataMasuTilaGramLabel)

        # 16) Вітамін К введено 				а) так б)ні	термін ________
        self.VitaminKVvedenoLabel = QLabel('    16. Вітамін К введено:')
        self.VitaminKVvedenoLabel.setFixedHeight(15)
        self.VitaminKVvedenoLabel.setFixedWidth(400)

        self.VitaminKVvedenoNoCheckBox = QCheckBox('Ні')
        self.VitaminKVvedenoNoCheckBox.setEnabled(0)
        self.VitaminKVvedenoNoCheckBox.setFixedWidth(100)
        self.VitaminKVvedenoNoCheckBox.stateChanged.connect(
            self.VitaminKVvedenoNoFunc)

        self.VitaminKVvedenoYesCheckBox = QCheckBox('Так')
        self.VitaminKVvedenoYesCheckBox.setChecked(1)
        self.VitaminKVvedenoYesCheckBox.stateChanged.connect(
            self.VitaminKVvedenoYesFunc)

        self.VitaminKVvedenoTerminLabel = QLabel('Термін:')
        # self.VitaminKVvedenoTerminLabel.hide()

        self.VitaminKVvedenoTerminLineEdit = QLineEdit()
        self.VitaminKVvedenoTerminLineEdit.setFixedWidth(100)
        self.VitaminKVvedenoTerminLineEdit.setMinimumWidth(300)
        # self.VitaminKVvedenoTerminLineEdit.hide()

        self.VitaminKVvedenoSplitter = QSplitter(Qt.Horizontal)
        self.VitaminKVvedenoSplitter.addWidget(self.VitaminKVvedenoLabel)
        self.VitaminKVvedenoSplitter.addWidget(self.VitaminKVvedenoNoCheckBox)
        self.VitaminKVvedenoSplitter.addWidget(self.VitaminKVvedenoYesCheckBox)
        self.VitaminKVvedenoSplitter.addWidget(self.VitaminKVvedenoTerminLabel)
        self.VitaminKVvedenoSplitter.addWidget(
            self.VitaminKVvedenoTerminLineEdit)

        # 17) виписаний на_____________добу
        self.VupusanuiNaLabel = QLabel('    17. Виписаний на:')
        self.VupusanuiNaLabel.setFixedHeight(15)
        self.VupusanuiNaLabel.setFixedWidth(400)

        self.VupusanuiNaLineEdit = QLineEdit()
        self.VupusanuiNaLineEdit.setFixedWidth(100)

        self.VupusanuiNaDobyLabel = QLabel('добу')

        self.VupusanuiNaSplitter = QSplitter(Qt.Horizontal)
        self.VupusanuiNaSplitter.addWidget(self.VupusanuiNaLabel)
        self.VupusanuiNaSplitter.addWidget(self.VupusanuiNaLineEdit)
        self.VupusanuiNaSplitter.addWidget(self.VupusanuiNaDobyLabel)

        # 18) неонатальна смерть: 			а) ні  б) на ______добу
        self.NeonatalnaSmertLabel = QLabel('    18. Неонатальна смерть:')
        self.NeonatalnaSmertLabel.setFixedHeight(15)
        self.NeonatalnaSmertLabel.setFixedWidth(400)

        self.NeonatalnaSmertNoCheckBox = QCheckBox('Ні')
        self.NeonatalnaSmertNoCheckBox.setChecked(1)
        self.NeonatalnaSmertNoCheckBox.setFixedWidth(100)
        self.NeonatalnaSmertNoCheckBox.stateChanged.connect(
            self.NeonatalnaSmertNoFunc)

        self.NeonatalnaSmertYesCheckBox = QCheckBox('Так')
        self.NeonatalnaSmertYesCheckBox.setEnabled(0)
        self.NeonatalnaSmertYesCheckBox.stateChanged.connect(
            self.NeonatalnaSmertYesFunc)

        self.NeonatalnaSmertTerminLabel = QLabel('На добу:')
        self.NeonatalnaSmertTerminLabel.hide()

        self.NeonatalnaSmertTerminLineEdit = QLineEdit()
        self.NeonatalnaSmertTerminLineEdit.setFixedWidth(100)
        self.NeonatalnaSmertTerminLineEdit.setMinimumWidth(300)
        self.NeonatalnaSmertTerminLineEdit.hide()

        self.NeonatalnaSmertSplitter = QSplitter(Qt.Horizontal)
        self.NeonatalnaSmertSplitter.addWidget(self.NeonatalnaSmertLabel)
        self.NeonatalnaSmertSplitter.addWidget(self.NeonatalnaSmertNoCheckBox)
        self.NeonatalnaSmertSplitter.addWidget(self.NeonatalnaSmertYesCheckBox)
        self.NeonatalnaSmertSplitter.addWidget(self.NeonatalnaSmertTerminLabel)
        self.NeonatalnaSmertSplitter.addWidget(
            self.NeonatalnaSmertTerminLineEdit)

        # 19) причина смерті за результатами аутопсії___
        self.PruchunaSmertiZaRezyltatomAytopsiiLabel = QLabel(
            '    19. Причина смерті за результатами аутопсії:')
        self.PruchunaSmertiZaRezyltatomAytopsiiLabel.setFixedHeight(15)
        self.PruchunaSmertiZaRezyltatomAytopsiiLabel.setFixedWidth(250)
        self.PruchunaSmertiZaRezyltatomAytopsiiLabel.setEnabled(0)

        self.PruchunaSmertiZaRezyltatomAytopsiiLineEdit = QLineEdit()
        self.PruchunaSmertiZaRezyltatomAytopsiiLineEdit.setEnabled(0)

        self.PruchunaSmertiZaRezyltatomAytopsiiSplitter = QSplitter(
            Qt.Horizontal)
        self.PruchunaSmertiZaRezyltatomAytopsiiSplitter.addWidget(
            self.PruchunaSmertiZaRezyltatomAytopsiiLabel)
        self.PruchunaSmertiZaRezyltatomAytopsiiSplitter.addWidget(
            self.PruchunaSmertiZaRezyltatomAytopsiiLineEdit)

        # Финальный сплиттер пункта VIII. Стан новонародженого та перебіг раннього неонатального періоду.
        self.PynktVIIISplitter = QSplitter(Qt.Vertical)
        self.PynktVIIISplitter.addWidget(
            self.StanNovonarodgennogoTaNeoPeriodLabel)
        self.PynktVIIISplitter.addWidget(self.NaroduvsaSplitter)
        self.PynktVIIISplitter.addWidget(self.PruchunaMertvonarodgennaSplitter)
        self.PynktVIIISplitter.addWidget(self.ZrilistNovonarodgennogoSplitter)
        self.PynktVIIISplitter.addWidget(self.MasaZristKoeficientSplitter)
        self.PynktVIIISplitter.addWidget(self.GipotrofiaPlodaSplitter)
        self.PynktVIIISplitter.addWidget(self.OcinkaZaShkaloyApgarSplitter)
        self.PynktVIIISplitter.addWidget(
            self.NovonarodjenuiZVadamuRozvutkySplitter)
        self.PynktVIIISplitter.addWidget(self.PologovaTravmaSplitter)
        self.PynktVIIISplitter.addWidget(self.SDRSplitter)
        self.PynktVIIISplitter.addWidget(
            self.VnytrishnoytrobneInfikyvannaSplitter)
        self.PynktVIIISplitter.addWidget(self.GemoragichniYskladnennaSplitter)
        self.PynktVIIISplitter.addWidget(self.AnemiaSplitter)
        self.PynktVIIISplitter.addWidget(self.GiperBilirybinemiaSplitter)
        self.PynktVIIISplitter.addWidget(self.AsfiksiaSplitter)
        self.PynktVIIISplitter.addWidget(
            self.PoryshennaKardioRespiratornoiAdaptaciiSplitter)
        self.PynktVIIISplitter.addWidget(self.VtrataMasuTilaSplitter)
        self.PynktVIIISplitter.addWidget(self.VitaminKVvedenoSplitter)
        self.PynktVIIISplitter.addWidget(self.VupusanuiNaSplitter)
        self.PynktVIIISplitter.addWidget(self.NeonatalnaSmertSplitter)
        self.PynktVIIISplitter.addWidget(
            self.PruchunaSmertiZaRezyltatomAytopsiiSplitter)

        # ІХ.Післяпологовий період.
        self.PislapologovuiPeriodLabel = QLabel('  IX) Післяпологовий період.')
        self.PislapologovuiPeriodLabel.setFixedHeight(30)
        self.PislapologovuiPeriodLabel.setStyleSheet(
            """QLabel{font-size:8pt; font-weight:600; color:#aa0000;}""")

        # 1.	Перебіг: а)  нормальний , б) ускладнений
        self.PislapologovuiPerebigLabel = QLabel('    1. Перебіг:')
        self.PislapologovuiPerebigLabel.setFixedHeight(15)
        self.PislapologovuiPerebigLabel.setFixedWidth(400)

        self.PislapologovuiPerebigNoCheckBox = QCheckBox('Нормальний')
        self.PislapologovuiPerebigNoCheckBox.setChecked(1)
        self.PislapologovuiPerebigNoCheckBox.setFixedWidth(100)
        self.PislapologovuiPerebigNoCheckBox.stateChanged.connect(
            self.PislapologovuiPerebigNoFunc)

        self.PislapologovuiPerebigYesCheckBox = QCheckBox('Ускладнений')
        self.PislapologovuiPerebigYesCheckBox.setEnabled(0)
        self.PislapologovuiPerebigYesCheckBox.stateChanged.connect(
            self.PislapologovuiPerebigYesFunc)

        self.PislapologovuiPerebigSplitter = QSplitter(Qt.Horizontal)
        self.PislapologovuiPerebigSplitter.addWidget(
            self.PislapologovuiPerebigLabel)
        self.PislapologovuiPerebigSplitter.addWidget(
            self.PislapologovuiPerebigNoCheckBox)
        self.PislapologovuiPerebigSplitter.addWidget(
            self.PislapologovuiPerebigYesCheckBox)

        # 2.	Чи проводилась профілактика/терапія ТЕУ: а) так б)ні
        self.ProfilaktukaTerapiaTEYPynktIXLabel = QLabel(
            '    2. Чи проводилась профілактика/терапія ТЕУ:')
        self.ProfilaktukaTerapiaTEYPynktIXLabel.setFixedHeight(15)
        self.ProfilaktukaTerapiaTEYPynktIXLabel.setFixedWidth(400)

        self.ProfilaktukaTerapiaTEYPynktIXNoCheckBox = QCheckBox('Ні')
        self.ProfilaktukaTerapiaTEYPynktIXNoCheckBox.setChecked(1)
        self.ProfilaktukaTerapiaTEYPynktIXNoCheckBox.setFixedWidth(100)
        self.ProfilaktukaTerapiaTEYPynktIXNoCheckBox.stateChanged.connect(
            self.ProfilaktukaTerapiaTEYPynktIXNoFunc)

        self.ProfilaktukaTerapiaTEYPynktIXYesCheckBox = QCheckBox('Так')
        self.ProfilaktukaTerapiaTEYPynktIXYesCheckBox.setEnabled(0)
        self.ProfilaktukaTerapiaTEYPynktIXYesCheckBox.stateChanged.connect(
            self.ProfilaktukaTerapiaTEYPynktIXYesFunc)

        self.ProfilaktukaTerapiaTEYPynktIXSplitter = QSplitter(Qt.Horizontal)
        self.ProfilaktukaTerapiaTEYPynktIXSplitter.addWidget(
            self.ProfilaktukaTerapiaTEYPynktIXLabel)
        self.ProfilaktukaTerapiaTEYPynktIXSplitter.addWidget(
            self.ProfilaktukaTerapiaTEYPynktIXNoCheckBox)
        self.ProfilaktukaTerapiaTEYPynktIXSplitter.addWidget(
            self.ProfilaktukaTerapiaTEYPynktIXYesCheckBox)

        # 2.1. Еластична компресія: 				    а) так б)ні	в) клас __
        self.ElastuchnaKompressiaPynktIXLabel = QLabel(
            '       2.1. Еластична компресія:')
        self.ElastuchnaKompressiaPynktIXLabel.setFixedHeight(15)
        self.ElastuchnaKompressiaPynktIXLabel.setFixedWidth(400)

        self.ElastuchnaKompressiaPynktIXNoCheckBox = QCheckBox('Ні')
        self.ElastuchnaKompressiaPynktIXNoCheckBox.setChecked(1)
        self.ElastuchnaKompressiaPynktIXNoCheckBox.setFixedWidth(100)
        self.ElastuchnaKompressiaPynktIXNoCheckBox.stateChanged.connect(
            self.ElastuchnaKompressiaPynktIXNoFunc)

        self.ElastuchnaKompressiaPynktIXYesCheckBox = QCheckBox('Так')
        self.ElastuchnaKompressiaPynktIXYesCheckBox.setEnabled(0)
        self.ElastuchnaKompressiaPynktIXYesCheckBox.setFixedWidth(40)
        self.ElastuchnaKompressiaPynktIXYesCheckBox.stateChanged.connect(
            self.ElastuchnaKompressiaPynktIXYesFunc)

        self.ElastuchnaKompressiaPynktIXKlasLabel = QLabel('Клас:')
        self.ElastuchnaKompressiaPynktIXKlasLabel.hide()
        self.ElastuchnaKompressiaPynktIXKlasLabel.setFixedWidth(40)
        self.ElastuchnaKompressiaPynktIXKlasLabel.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter)

        self.ElastuchnaKompressiaPynktIXKlasLineEdit = QLineEdit()
        self.ElastuchnaKompressiaPynktIXKlasLineEdit.setFixedWidth(100)
        self.ElastuchnaKompressiaPynktIXKlasLineEdit.setMinimumWidth(300)
        self.ElastuchnaKompressiaPynktIXKlasLineEdit.hide()

        self.ElastuchnaKompressiaPynktIXSplitter = QSplitter(Qt.Horizontal)
        self.ElastuchnaKompressiaPynktIXSplitter.addWidget(
            self.ElastuchnaKompressiaPynktIXLabel)
        self.ElastuchnaKompressiaPynktIXSplitter.addWidget(
            self.ElastuchnaKompressiaPynktIXNoCheckBox)
        self.ElastuchnaKompressiaPynktIXSplitter.addWidget(
            self.ElastuchnaKompressiaPynktIXYesCheckBox)
        self.ElastuchnaKompressiaPynktIXSplitter.addWidget(
            self.ElastuchnaKompressiaPynktIXKlasLabel)
        self.ElastuchnaKompressiaPynktIXSplitter.addWidget(
            self.ElastuchnaKompressiaPynktIXKlasLineEdit)

        # 2.2. Медикаментозна профілактика / терапія	    а) так б)ні
        self.MedukamentoznaProfilaktukaPynktIXLabel = QLabel(
            '       2.2. Медикаментозна профілактика/терапія:')
        self.MedukamentoznaProfilaktukaPynktIXLabel.setFixedHeight(15)
        self.MedukamentoznaProfilaktukaPynktIXLabel.setFixedWidth(400)

        self.MedukamentoznaProfilaktukaPynktIXNoCheckBox = QCheckBox('Ні')
        self.MedukamentoznaProfilaktukaPynktIXNoCheckBox.setChecked(1)
        self.MedukamentoznaProfilaktukaPynktIXNoCheckBox.setFixedWidth(100)
        self.MedukamentoznaProfilaktukaPynktIXNoCheckBox.stateChanged.connect(
            self.MedukamentoznaProfilaktukaPynktIXNoFunc)

        self.MedukamentoznaProfilaktukaPynktIXYesCheckBox = QCheckBox('Так')
        self.MedukamentoznaProfilaktukaPynktIXYesCheckBox.setEnabled(0)
        self.MedukamentoznaProfilaktukaPynktIXYesCheckBox.stateChanged.connect(
            self.MedukamentoznaProfilaktukaPynktIXYesFunc)

        # 2.2.1. Назва препарата ___________________________________
        self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyLabel = QLabel(
            '   2.2.1 Назва препарата:')
        self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyLabel.hide()

        self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyLineEdit = QLineEdit(
        )
        self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyLineEdit.hide()
        self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyLineEdit.setMinimumWidth(
            200)

        # 2.2.2.Режим прийому ____________________________________
        self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyLabel = QLabel(
            '   2.2.2 Режим прийому:')
        self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyLabel.hide()

        self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyLineEdit = QLineEdit(
        )
        self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyLineEdit.hide()
        self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyLineEdit.setMinimumWidth(
            200)

        # 2.2.3. Термін коли призначено _____________________________
        self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznachenoLabel = QLabel(
            '   2.2.3 Термін коли призначено:')
        self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznachenoLabel.hide()

        self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznachenoLineEdit = QLineEdit(
        )
        self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznachenoLineEdit.hide(
        )
        self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznachenoLineEdit.setMinimumWidth(
            200)

        self.MedukamentoznaProfilaktukaPynktIXSplitter = QSplitter(
            Qt.Horizontal)
        self.MedukamentoznaProfilaktukaPynktIXSplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktIXLabel)
        self.MedukamentoznaProfilaktukaPynktIXSplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktIXNoCheckBox)
        self.MedukamentoznaProfilaktukaPynktIXSplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktIXYesCheckBox)
        self.MedukamentoznaProfilaktukaPynktIXSplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyLabel)
        self.MedukamentoznaProfilaktukaPynktIXSplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyLineEdit)
        self.MedukamentoznaProfilaktukaPynktIXSplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyLabel)
        self.MedukamentoznaProfilaktukaPynktIXSplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyLineEdit)
        self.MedukamentoznaProfilaktukaPynktIXSplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznachenoLabel)
        self.MedukamentoznaProfilaktukaPynktIXSplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznachenoLineEdit
        )

        # Хірургічне лікування : а) так б)ні
        self.HiryrgichneLikyvannaPynktIXLabel = QLabel(
            '       2.3. Хірургічне лікування:')
        self.HiryrgichneLikyvannaPynktIXLabel.setFixedHeight(15)
        self.HiryrgichneLikyvannaPynktIXLabel.setFixedWidth(400)

        self.HiryrgichneLikyvannaPynktIXNoCheckBox = QCheckBox('Ні')
        self.HiryrgichneLikyvannaPynktIXNoCheckBox.setChecked(1)
        self.HiryrgichneLikyvannaPynktIXNoCheckBox.setFixedWidth(100)
        self.HiryrgichneLikyvannaPynktIXNoCheckBox.stateChanged.connect(
            self.HiryrgichneLikyvannaPynktIXNoFunc)

        self.HiryrgichneLikyvannaPynktIXYesCheckBox = QCheckBox('Так')
        self.HiryrgichneLikyvannaPynktIXYesCheckBox.setEnabled(0)
        self.HiryrgichneLikyvannaPynktIXYesCheckBox.setFixedWidth(40)
        self.HiryrgichneLikyvannaPynktIXYesCheckBox.stateChanged.connect(
            self.HiryrgichneLikyvannaPynktIXYesFunc)

        # 2.3.1.Назва операції та дата _______________________________________
        self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiLabel = QLabel(
            '      2.3.1 Назва операції та дата:')
        self.HiryrgichneLikyvannaPynktIXYesCheckBox.setFixedWidth(100)
        self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiLabel.hide()

        self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiLineEdit = QLineEdit(
        )
        self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiLineEdit.hide()
        self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiLineEdit.setMinimumWidth(
            200)

        self.HiryrgichneLikyvannaPynktIXSplitter = QSplitter(Qt.Horizontal)
        self.HiryrgichneLikyvannaPynktIXSplitter.addWidget(
            self.HiryrgichneLikyvannaPynktIXLabel)
        self.HiryrgichneLikyvannaPynktIXSplitter.addWidget(
            self.HiryrgichneLikyvannaPynktIXNoCheckBox)
        self.HiryrgichneLikyvannaPynktIXSplitter.addWidget(
            self.HiryrgichneLikyvannaPynktIXYesCheckBox)
        self.HiryrgichneLikyvannaPynktIXSplitter.addWidget(
            self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiLabel)
        self.HiryrgichneLikyvannaPynktIXSplitter.addWidget(
            self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiLineEdit)

        # 3.	Тривалість проведеної профілактики _____________________
        self.TruvalistProvedenoiProfilaktuktPynktIXLabel = QLabel(
            '    3. Тривалість проведеної профілактики:')
        self.TruvalistProvedenoiProfilaktuktPynktIXLabel.setFixedHeight(15)
        self.TruvalistProvedenoiProfilaktuktPynktIXLabel.setFixedWidth(400)

        self.TruvalistProvedenoiProfilaktuktPynktIXLineEdit = QLineEdit()
        self.TruvalistProvedenoiProfilaktuktPynktIXLineEdit.setMaximumWidth(
            200)

        self.TruvalistProvedenoiProfilaktuktPynktIXSplitter = QSplitter(
            Qt.Horizontal)
        self.TruvalistProvedenoiProfilaktuktPynktIXSplitter.addWidget(
            self.TruvalistProvedenoiProfilaktuktPynktIXLabel)
        self.TruvalistProvedenoiProfilaktuktPynktIXSplitter.addWidget(
            self.TruvalistProvedenoiProfilaktuktPynktIXLineEdit)

        # 4.	Наявність ускладнень від проведеної профілактики: а) так б)ні
        self.YskladnennaVidProfilaktukyPynktIXLabel = QLabel(
            '    4. Наявність ускладнень від проведеної профілактики:')
        self.YskladnennaVidProfilaktukyPynktIXLabel.setFixedHeight(15)
        self.YskladnennaVidProfilaktukyPynktIXLabel.setFixedWidth(400)

        self.YskladnennaVidProfilaktukyPynktIXNoCheckBox = QCheckBox('Ні')
        self.YskladnennaVidProfilaktukyPynktIXNoCheckBox.setChecked(1)
        self.YskladnennaVidProfilaktukyPynktIXNoCheckBox.setFixedWidth(100)
        self.YskladnennaVidProfilaktukyPynktIXNoCheckBox.stateChanged.connect(
            self.YskladnennaVidProfilaktukyPynktIXNoFunc)

        self.YskladnennaVidProfilaktukyPynktIXYesCheckBox = QCheckBox('Так')
        self.YskladnennaVidProfilaktukyPynktIXYesCheckBox.setEnabled(0)
        self.YskladnennaVidProfilaktukyPynktIXYesCheckBox.setFixedWidth(40)
        self.YskladnennaVidProfilaktukyPynktIXYesCheckBox.stateChanged.connect(
            self.YskladnennaVidProfilaktukyPynktIXYesFunc)

        # Ускладення: _______________________________________________

        self.YskladnennaVidProfilaktukyPynktIXYskladnennaLabel = QLabel(
            'Ускладення:')
        self.YskladnennaVidProfilaktukyPynktIXYskladnennaLabel.setFixedWidth(
            70)
        self.YskladnennaVidProfilaktukyPynktIXYskladnennaLabel.hide()

        self.YskladnennaVidProfilaktukyPynktIXYskladnennaLineEdit = QLineEdit()
        self.YskladnennaVidProfilaktukyPynktIXYskladnennaLineEdit.hide()
        self.YskladnennaVidProfilaktukyPynktIXYskladnennaLineEdit.setMinimumWidth(
            200)

        self.YskladnennaVidProfilaktukyPynktIXSplitter = QSplitter(
            Qt.Horizontal)
        self.YskladnennaVidProfilaktukyPynktIXSplitter.addWidget(
            self.YskladnennaVidProfilaktukyPynktIXLabel)
        self.YskladnennaVidProfilaktukyPynktIXSplitter.addWidget(
            self.YskladnennaVidProfilaktukyPynktIXNoCheckBox)
        self.YskladnennaVidProfilaktukyPynktIXSplitter.addWidget(
            self.YskladnennaVidProfilaktukyPynktIXYesCheckBox)
        self.YskladnennaVidProfilaktukyPynktIXSplitter.addWidget(
            self.YskladnennaVidProfilaktukyPynktIXYskladnennaLabel)
        self.YskladnennaVidProfilaktukyPynktIXSplitter.addWidget(
            self.YskladnennaVidProfilaktukyPynktIXYskladnennaLineEdit)

        # 5.	Тромбоемболічні ускладнення :
        self.TromboembolichniYskladnennaPynktIXLabel = QLabel(
            '    5. Тромбоемболічні ускладнення:')
        self.TromboembolichniYskladnennaPynktIXLabel.setFixedHeight(15)
        self.TromboembolichniYskladnennaPynktIXLabel.setFixedWidth(400)

        self.TromboembolichniYskladnennaPynktIXNoCheckBox = QCheckBox('Ні')
        self.TromboembolichniYskladnennaPynktIXNoCheckBox.setChecked(1)
        self.TromboembolichniYskladnennaPynktIXNoCheckBox.setFixedWidth(100)
        self.TromboembolichniYskladnennaPynktIXNoCheckBox.stateChanged.connect(
            self.TromboembolichniYskladnennaPynktIXNoFunc)

        self.TromboembolichniYskladnennaPynktIXYesCheckBox = QCheckBox('Так')
        self.TromboembolichniYskladnennaPynktIXYesCheckBox.setEnabled(0)
        self.TromboembolichniYskladnennaPynktIXYesCheckBox.setFixedWidth(40)
        self.TromboembolichniYskladnennaPynktIXYesCheckBox.stateChanged.connect(
            self.TromboembolichniYskladnennaPynktIXYesFunc)

        # 5.1	вид ТЕУ ___________________________________________________
        # 5.2	термін винекнення___________________________________________
        # 5.3	Терапія ТЕУ________________________________________________

        self.TromboembolichniYskladnennaPynktIXVudTeyLabel = QLabel('Вид ТЕУ:')
        self.TromboembolichniYskladnennaPynktIXVudTeyLabel.setFixedWidth(50)
        self.TromboembolichniYskladnennaPynktIXVudTeyLabel.hide()
        self.TromboembolichniYskladnennaPynktIXVudTeyLineEdit = QLineEdit()
        self.TromboembolichniYskladnennaPynktIXVudTeyLineEdit.hide()

        self.TromboembolichniYskladnennaPynktIXTerminVunuknennaLabel = QLabel(
            'Термін виникнення:')
        self.TromboembolichniYskladnennaPynktIXTerminVunuknennaLabel.setFixedWidth(
            100)
        self.TromboembolichniYskladnennaPynktIXTerminVunuknennaLabel.hide()
        self.TromboembolichniYskladnennaPynktIXTerminVunuknennaLineEdit = QLineEdit(
        )
        self.TromboembolichniYskladnennaPynktIXTerminVunuknennaLineEdit.hide()

        self.TromboembolichniYskladnennaPynktIXTerapiaTEYLabel = QLabel(
            'Терапія ТЕУ:')
        self.TromboembolichniYskladnennaPynktIXTerapiaTEYLabel.setFixedWidth(
            60)
        self.TromboembolichniYskladnennaPynktIXTerapiaTEYLabel.hide()
        self.TromboembolichniYskladnennaPynktIXTerapiaTEYLineEdit = QLineEdit()
        self.TromboembolichniYskladnennaPynktIXTerapiaTEYLineEdit.hide()

        self.TromboembolichniYskladnennaPynktIXSplitter = QSplitter(
            Qt.Horizontal)
        self.TromboembolichniYskladnennaPynktIXSplitter.addWidget(
            self.TromboembolichniYskladnennaPynktIXLabel)
        self.TromboembolichniYskladnennaPynktIXSplitter.addWidget(
            self.TromboembolichniYskladnennaPynktIXNoCheckBox)
        self.TromboembolichniYskladnennaPynktIXSplitter.addWidget(
            self.TromboembolichniYskladnennaPynktIXYesCheckBox)
        self.TromboembolichniYskladnennaPynktIXSplitter.addWidget(
            self.TromboembolichniYskladnennaPynktIXVudTeyLabel)
        self.TromboembolichniYskladnennaPynktIXSplitter.addWidget(
            self.TromboembolichniYskladnennaPynktIXVudTeyLineEdit)
        self.TromboembolichniYskladnennaPynktIXSplitter.addWidget(
            self.TromboembolichniYskladnennaPynktIXTerminVunuknennaLabel)
        self.TromboembolichniYskladnennaPynktIXSplitter.addWidget(
            self.TromboembolichniYskladnennaPynktIXTerminVunuknennaLineEdit)
        self.TromboembolichniYskladnennaPynktIXSplitter.addWidget(
            self.TromboembolichniYskladnennaPynktIXTerapiaTEYLabel)
        self.TromboembolichniYskladnennaPynktIXSplitter.addWidget(
            self.TromboembolichniYskladnennaPynktIXTerapiaTEYLineEdit)

        # 6.	Мастит:                                                                        а) так; б) ні
        self.MastutPynktIXLabel = QLabel('    6. Мастит:')
        self.MastutPynktIXLabel.setFixedHeight(15)
        self.MastutPynktIXLabel.setFixedWidth(400)

        self.MastutPynktIXNoCheckBox = QCheckBox('Ні')
        self.MastutPynktIXNoCheckBox.setChecked(1)
        self.MastutPynktIXNoCheckBox.setFixedWidth(100)
        self.MastutPynktIXNoCheckBox.stateChanged.connect(
            self.MastutPynktIXNoFunc)

        self.MastutPynktIXYesCheckBox = QCheckBox('Так')
        self.MastutPynktIXYesCheckBox.setEnabled(0)
        self.MastutPynktIXYesCheckBox.stateChanged.connect(
            self.MastutPynktIXYesFunc)

        self.MastutPynktIXSplitter = QSplitter(Qt.Horizontal)
        self.MastutPynktIXSplitter.addWidget(self.MastutPynktIXLabel)
        self.MastutPynktIXSplitter.addWidget(self.MastutPynktIXNoCheckBox)
        self.MastutPynktIXSplitter.addWidget(self.MastutPynktIXYesCheckBox)

        # 7.	Субінволюція матки:                                                 а) так; б) ні
        self.SubinvolyciaMatkuPynktIXLabel = QLabel(
            '    7. Субінволюція матки:')
        self.SubinvolyciaMatkuPynktIXLabel.setFixedHeight(15)
        self.SubinvolyciaMatkuPynktIXLabel.setFixedWidth(400)

        self.SubinvolyciaMatkuPynktIXNoCheckBox = QCheckBox('Ні')
        self.SubinvolyciaMatkuPynktIXNoCheckBox.setChecked(1)
        self.SubinvolyciaMatkuPynktIXNoCheckBox.setFixedWidth(100)
        self.SubinvolyciaMatkuPynktIXNoCheckBox.stateChanged.connect(
            self.SubinvolyciaMatkuPynktIXNoFunc)

        self.SubinvolyciaMatkuPynktIXYesCheckBox = QCheckBox('Так')
        self.SubinvolyciaMatkuPynktIXYesCheckBox.setEnabled(0)
        self.SubinvolyciaMatkuPynktIXYesCheckBox.stateChanged.connect(
            self.SubinvolyciaMatkuPynktIXYesFunc)

        self.SubinvolyciaMatkuPynktIXSplitter = QSplitter(Qt.Horizontal)
        self.SubinvolyciaMatkuPynktIXSplitter.addWidget(
            self.SubinvolyciaMatkuPynktIXLabel)
        self.SubinvolyciaMatkuPynktIXSplitter.addWidget(
            self.SubinvolyciaMatkuPynktIXNoCheckBox)
        self.SubinvolyciaMatkuPynktIXSplitter.addWidget(
            self.SubinvolyciaMatkuPynktIXYesCheckBox)

        # 8.	Ендометрит:                                                                а) так; б) ні
        self.EndometrutPynktIXLabel = QLabel('    8. Ендометрит:')
        self.EndometrutPynktIXLabel.setFixedHeight(15)
        self.EndometrutPynktIXLabel.setFixedWidth(400)

        self.EndometrutPynktIXNoCheckBox = QCheckBox('Ні')
        self.EndometrutPynktIXNoCheckBox.setChecked(1)
        self.EndometrutPynktIXNoCheckBox.setFixedWidth(100)
        self.EndometrutPynktIXNoCheckBox.stateChanged.connect(
            self.EndometrutPynktIXNoFunc)

        self.EndometrutPynktIXYesCheckBox = QCheckBox('Так')
        self.EndometrutPynktIXYesCheckBox.setEnabled(0)
        self.EndometrutPynktIXYesCheckBox.stateChanged.connect(
            self.EndometrutPynktIXYesFunc)

        self.EndometrutPynktIXSplitter = QSplitter(Qt.Horizontal)
        self.EndometrutPynktIXSplitter.addWidget(self.EndometrutPynktIXLabel)
        self.EndometrutPynktIXSplitter.addWidget(
            self.EndometrutPynktIXNoCheckBox)
        self.EndometrutPynktIXSplitter.addWidget(
            self.EndometrutPynktIXYesCheckBox)

        # 9.	Пізня післяпологова кровотеча:                                а) так; б) ні
        self.PiznaPologovaKrovotechaPynktIXLabel = QLabel(
            '    9. Пізня післяпологова кровотеча:')
        self.PiznaPologovaKrovotechaPynktIXLabel.setFixedHeight(15)
        self.PiznaPologovaKrovotechaPynktIXLabel.setFixedWidth(400)

        self.PiznaPologovaKrovotechaPynktIXNoCheckBox = QCheckBox('Ні')
        self.PiznaPologovaKrovotechaPynktIXNoCheckBox.setChecked(1)
        self.PiznaPologovaKrovotechaPynktIXNoCheckBox.setFixedWidth(100)
        self.PiznaPologovaKrovotechaPynktIXNoCheckBox.stateChanged.connect(
            self.PiznaPologovaKrovotechaPynktIXNoFunc)

        self.PiznaPologovaKrovotechaPynktIXYesCheckBox = QCheckBox('Так')
        self.PiznaPologovaKrovotechaPynktIXYesCheckBox.setEnabled(0)
        self.PiznaPologovaKrovotechaPynktIXYesCheckBox.stateChanged.connect(
            self.PiznaPologovaKrovotechaPynktIXYesFunc)

        self.PiznaPologovaKrovotechaPynktIXSplitter = QSplitter(Qt.Horizontal)
        self.PiznaPologovaKrovotechaPynktIXSplitter.addWidget(
            self.PiznaPologovaKrovotechaPynktIXLabel)
        self.PiznaPologovaKrovotechaPynktIXSplitter.addWidget(
            self.PiznaPologovaKrovotechaPynktIXNoCheckBox)
        self.PiznaPologovaKrovotechaPynktIXSplitter.addWidget(
            self.PiznaPologovaKrovotechaPynktIXYesCheckBox)

        # 10.	Сепсис:                                                                         а) так; б) ні
        self.SepsusPynktIXLabel = QLabel('    10. Сепсис:')
        self.SepsusPynktIXLabel.setFixedHeight(15)
        self.SepsusPynktIXLabel.setFixedWidth(400)

        self.SepsusPynktIXNoCheckBox = QCheckBox('Ні')
        self.SepsusPynktIXNoCheckBox.setChecked(1)
        self.SepsusPynktIXNoCheckBox.setFixedWidth(100)
        self.SepsusPynktIXNoCheckBox.stateChanged.connect(
            self.SepsusPynktIXNoFunc)

        self.SepsusPynktIXYesCheckBox = QCheckBox('Так')
        self.SepsusPynktIXYesCheckBox.setEnabled(0)
        self.SepsusPynktIXYesCheckBox.stateChanged.connect(
            self.SepsusPynktIXYesFunc)

        self.SepsusPynktIXSplitter = QSplitter(Qt.Horizontal)
        self.SepsusPynktIXSplitter.addWidget(self.SepsusPynktIXLabel)
        self.SepsusPynktIXSplitter.addWidget(self.SepsusPynktIXNoCheckBox)
        self.SepsusPynktIXSplitter.addWidget(self.SepsusPynktIXYesCheckBox)

        # 11.	Розходження швів:                                                      а) так; б) ні
        self.RoshodgennaShvivPynktIXLabel = QLabel('    11. Розходження швів:')
        self.RoshodgennaShvivPynktIXLabel.setFixedHeight(15)
        self.RoshodgennaShvivPynktIXLabel.setFixedWidth(400)

        self.RoshodgennaShvivPynktIXNoCheckBox = QCheckBox('Ні')
        self.RoshodgennaShvivPynktIXNoCheckBox.setChecked(1)
        self.RoshodgennaShvivPynktIXNoCheckBox.setFixedWidth(100)
        self.RoshodgennaShvivPynktIXNoCheckBox.stateChanged.connect(
            self.RoshodgennaShvivPynktIXNoFunc)

        self.RoshodgennaShvivPynktIXYesCheckBox = QCheckBox('Так')
        self.RoshodgennaShvivPynktIXYesCheckBox.setEnabled(0)
        self.RoshodgennaShvivPynktIXYesCheckBox.stateChanged.connect(
            self.RoshodgennaShvivPynktIXYesFunc)

        self.RoshodgennaShvivPynktIXSplitter = QSplitter(Qt.Horizontal)
        self.RoshodgennaShvivPynktIXSplitter.addWidget(
            self.RoshodgennaShvivPynktIXLabel)
        self.RoshodgennaShvivPynktIXSplitter.addWidget(
            self.RoshodgennaShvivPynktIXNoCheckBox)
        self.RoshodgennaShvivPynktIXSplitter.addWidget(
            self.RoshodgennaShvivPynktIXYesCheckBox)

        # 12.	Інші: ________________________________________________________
        self.InshiPynktIXLabel = QLabel('    12. Інші:')
        self.InshiPynktIXLabel.setFixedHeight(15)
        self.InshiPynktIXLabel.setFixedWidth(400)

        self.InshiPynktIXLineEdit = QLineEdit()

        self.InshiPynktIXSplitter = QSplitter(Qt.Horizontal)
        self.InshiPynktIXSplitter.addWidget(self.InshiPynktIXLabel)
        self.InshiPynktIXSplitter.addWidget(self.InshiPynktIXLineEdit)

        # 13.	Хірургічні втручання в перші 6 тиж після пологів: а) так; б) ні
        self.HirVtyrchannaVPershi6TugnivPynktIXLabel = QLabel(
            '    13. Хірургічні втручання в перші 6 тиж після пологів:')
        self.HirVtyrchannaVPershi6TugnivPynktIXLabel.setFixedHeight(15)
        self.HirVtyrchannaVPershi6TugnivPynktIXLabel.setFixedWidth(400)

        self.HirVtyrchannaVPershi6TugnivPynktIXNoCheckBox = QCheckBox('Ні')
        self.HirVtyrchannaVPershi6TugnivPynktIXNoCheckBox.setChecked(1)
        self.HirVtyrchannaVPershi6TugnivPynktIXNoCheckBox.setFixedWidth(100)
        self.HirVtyrchannaVPershi6TugnivPynktIXNoCheckBox.stateChanged.connect(
            self.HirVtyrchannaVPershi6TugnivPynktIXNoFunc)

        self.HirVtyrchannaVPershi6TugnivPynktIXYesCheckBox = QCheckBox('Так')
        self.HirVtyrchannaVPershi6TugnivPynktIXYesCheckBox.setEnabled(0)
        self.HirVtyrchannaVPershi6TugnivPynktIXYesCheckBox.stateChanged.connect(
            self.HirVtyrchannaVPershi6TugnivPynktIXYesFunc)

        self.HirVtyrchannaVPershi6TugnivPynktIXSplitter = QSplitter(
            Qt.Horizontal)
        self.HirVtyrchannaVPershi6TugnivPynktIXSplitter.addWidget(
            self.HirVtyrchannaVPershi6TugnivPynktIXLabel)
        self.HirVtyrchannaVPershi6TugnivPynktIXSplitter.addWidget(
            self.HirVtyrchannaVPershi6TugnivPynktIXNoCheckBox)
        self.HirVtyrchannaVPershi6TugnivPynktIXSplitter.addWidget(
            self.HirVtyrchannaVPershi6TugnivPynktIXYesCheckBox)

        # 14.	Виписка додому:                         а) так; б) ні;                          _______добу
        self.VupuskaDodomyPynktIXLabel = QLabel('    14. Виписка додому:')
        self.VupuskaDodomyPynktIXLabel.setFixedHeight(15)
        self.VupuskaDodomyPynktIXLabel.setFixedWidth(400)

        self.VupuskaDodomyPynktIXNoCheckBox = QCheckBox('Ні')
        self.VupuskaDodomyPynktIXNoCheckBox.setEnabled(0)
        self.VupuskaDodomyPynktIXNoCheckBox.setFixedWidth(100)
        self.VupuskaDodomyPynktIXNoCheckBox.stateChanged.connect(
            self.VupuskaDodomyPynktIXNoFunc)

        self.VupuskaDodomyPynktIXYesCheckBox = QCheckBox('Так')
        self.VupuskaDodomyPynktIXYesCheckBox.setChecked(1)

        self.VupuskaDodomyPynktIXYesCheckBox.stateChanged.connect(
            self.VupuskaDodomyPynktIXYesFunc)

        self.VupuskaDodomyPynktIXDobyLineEdit = QLineEdit()
        self.VupuskaDodomyPynktIXDobyLineEdit.setFixedWidth(40)
        self.VupuskaDodomyPynktIXDobyLineEdit.setInputMask("D00")

        self.VupuskaDodomyPynktIXDobyLabel = QLabel('добу')
        self.VupuskaDodomyPynktIXDobyLabel.setAlignment(
            Qt.AlignLeft | Qt.AlignVCenter)

        self.VupuskaDodomyPynktIXSplitter = QSplitter(Qt.Horizontal)
        self.VupuskaDodomyPynktIXSplitter.addWidget(
            self.VupuskaDodomyPynktIXLabel)
        self.VupuskaDodomyPynktIXSplitter.addWidget(
            self.VupuskaDodomyPynktIXNoCheckBox)
        self.VupuskaDodomyPynktIXSplitter.addWidget(
            self.VupuskaDodomyPynktIXYesCheckBox)
        self.VupuskaDodomyPynktIXSplitter.addWidget(
            self.VupuskaDodomyPynktIXDobyLineEdit)
        self.VupuskaDodomyPynktIXSplitter.addWidget(
            self.VupuskaDodomyPynktIXDobyLabel)

        # 15.	Переведена в інший стаціонар: а) так; б) ні                           _______добу
        self.PerevedennaVInshuiStacionarPynktIXLabel = QLabel(
            '    15. Переведена в інший стаціонар:')
        self.PerevedennaVInshuiStacionarPynktIXLabel.setFixedHeight(15)
        self.PerevedennaVInshuiStacionarPynktIXLabel.setFixedWidth(400)

        self.PerevedennaVInshuiStacionarPynktIXNoCheckBox = QCheckBox('Ні')
        self.PerevedennaVInshuiStacionarPynktIXNoCheckBox.setChecked(1)
        self.PerevedennaVInshuiStacionarPynktIXNoCheckBox.setFixedWidth(100)
        self.PerevedennaVInshuiStacionarPynktIXNoCheckBox.stateChanged.connect(
            self.PerevedennaVInshuiStacionarPynktIXNoFunc)

        self.PerevedennaVInshuiStacionarPynktIXYesCheckBox = QCheckBox('Так')
        self.PerevedennaVInshuiStacionarPynktIXYesCheckBox.setEnabled(0)
        self.PerevedennaVInshuiStacionarPynktIXYesCheckBox.stateChanged.connect(
            self.PerevedennaVInshuiStacionarPynktIXYesFunc)

        self.PerevedennaVInshuiStacionarPynktIXDobyLineEdit = QLineEdit()
        self.PerevedennaVInshuiStacionarPynktIXDobyLineEdit.setFixedWidth(40)
        self.PerevedennaVInshuiStacionarPynktIXDobyLineEdit.setEnabled(0)
        self.PerevedennaVInshuiStacionarPynktIXDobyLineEdit.setInputMask("D00")

        self.PerevedennaVInshuiStacionarPynktIXDobyLabel = QLabel('добу')
        self.PerevedennaVInshuiStacionarPynktIXDobyLabel.setEnabled(0)
        self.PerevedennaVInshuiStacionarPynktIXDobyLabel.setAlignment(
            Qt.AlignLeft | Qt.AlignVCenter)

        self.PerevedennaVInshuiStacionarPynktIXSplitter = QSplitter(
            Qt.Horizontal)
        self.PerevedennaVInshuiStacionarPynktIXSplitter.addWidget(
            self.PerevedennaVInshuiStacionarPynktIXLabel)
        self.PerevedennaVInshuiStacionarPynktIXSplitter.addWidget(
            self.PerevedennaVInshuiStacionarPynktIXNoCheckBox)
        self.PerevedennaVInshuiStacionarPynktIXSplitter.addWidget(
            self.PerevedennaVInshuiStacionarPynktIXYesCheckBox)
        self.PerevedennaVInshuiStacionarPynktIXSplitter.addWidget(
            self.PerevedennaVInshuiStacionarPynktIXDobyLineEdit)
        self.PerevedennaVInshuiStacionarPynktIXSplitter.addWidget(
            self.PerevedennaVInshuiStacionarPynktIXDobyLabel)

        self.ChangeDateLabel = QLabel(
            '    Дата та час заповнення реєстраційної карти:')
        self.ChangeDate = QDateTimeEdit()
        self.ChangeDate.setDateTime(QDateTime.currentDateTime())
        self.ChangeDate.setEnabled(0)

        self.WhoCangeLabel = QLabel('    Заповняв:')
        self.WhoChange = QLabel(WhoCangeParam)
        self.WhoCangeSplitter = QSplitter(Qt.Horizontal)
        self.WhoCangeSplitter.addWidget(self.ChangeDateLabel)
        self.WhoCangeSplitter.addWidget(self.ChangeDate)
        self.WhoCangeSplitter.addWidget(self.WhoCangeLabel)
        self.WhoCangeSplitter.addWidget(self.WhoChange)

        # Финальный сплиттер пункта ІХ.Післяпологовий період.
        self.PynktIXSplitter = QSplitter(Qt.Vertical)
        self.PynktIXSplitter.addWidget(self.PislapologovuiPeriodLabel)
        self.PynktIXSplitter.addWidget(self.PislapologovuiPerebigSplitter)
        self.PynktIXSplitter.addWidget(
            self.ProfilaktukaTerapiaTEYPynktIXSplitter)
        self.PynktIXSplitter.addWidget(
            self.ElastuchnaKompressiaPynktIXSplitter)
        self.PynktIXSplitter.addWidget(
            self.MedukamentoznaProfilaktukaPynktIXSplitter)
        self.PynktIXSplitter.addWidget(
            self.HiryrgichneLikyvannaPynktIXSplitter)
        self.PynktIXSplitter.addWidget(
            self.TruvalistProvedenoiProfilaktuktPynktIXSplitter)
        self.PynktIXSplitter.addWidget(
            self.YskladnennaVidProfilaktukyPynktIXSplitter)
        self.PynktIXSplitter.addWidget(
            self.TromboembolichniYskladnennaPynktIXSplitter)
        self.PynktIXSplitter.addWidget(self.MastutPynktIXSplitter)
        self.PynktIXSplitter.addWidget(self.SubinvolyciaMatkuPynktIXSplitter)
        self.PynktIXSplitter.addWidget(self.EndometrutPynktIXSplitter)
        self.PynktIXSplitter.addWidget(
            self.PiznaPologovaKrovotechaPynktIXSplitter)
        self.PynktIXSplitter.addWidget(self.SepsusPynktIXSplitter)
        self.PynktIXSplitter.addWidget(self.RoshodgennaShvivPynktIXSplitter)
        self.PynktIXSplitter.addWidget(self.InshiPynktIXSplitter)
        self.PynktIXSplitter.addWidget(
            self.HirVtyrchannaVPershi6TugnivPynktIXSplitter)
        self.PynktIXSplitter.addWidget(self.VupuskaDodomyPynktIXSplitter)
        self.PynktIXSplitter.addWidget(
            self.PerevedennaVInshuiStacionarPynktIXSplitter)
        self.PynktIXSplitter.addWidget(self.WhoCangeSplitter)

        # кнопка записи информации в БД
        self.InsertToDBButton = QPushButton('Внести інформацію в базу данних')
        self.InsertToDBButton.clicked.connect(self.InsertToDBFunc)
        # self.InsertToDBButton.clicked.connect(self.ResetToDefaultValue)

        # Финальный сплиттер вкладки
        self.splitterFinal = QSplitter(Qt.Vertical)
        self.splitterFinal.addWidget(self.splitter6)
        self.splitterFinal.addWidget(self.splitter7)
        self.splitterFinal.addWidget(self.splitter8)
        self.splitterFinal.addWidget(self.splitter9)
        self.splitterFinal.addWidget(self.splitter12)
        self.splitterFinal.addWidget(self.PynctIIISplitter)
        self.splitterFinal.addWidget(self.PynkIVSplitter)
        self.splitterFinal.addWidget(self.PynkVSplitter)
        self.splitterFinal.addWidget(self.PynktVISplitter)
        self.splitterFinal.addWidget(self.PerebigDannuhPologivSplitter)
        self.splitterFinal.addWidget(self.PynktVIIISplitter)
        self.splitterFinal.addWidget(self.PynktIXSplitter)
        self.splitterFinal.addWidget(self.InsertToDBButton)

        # self.splitterFinal.setStyleSheet("QSplitter::handle{background: green;}")
        # self.splitterFinal.setStyleSheet("QSplitter{background: white;}")

        ######Часть для форматирования при раскрытии на весь экран
        self.Label1forTestSplitters = QLabel(" ")
        self.Label1forTestSplitters.show()
        self.Label2forTestSplitters = QLabel(" ")

        self.TestSplitter1 = QSplitter(Qt.Horizontal)
        self.TestSplitter1.addWidget(self.Label1forTestSplitters)

        self.TestSplitter2 = QSplitter(Qt.Horizontal)
        self.TestSplitter2.addWidget(self.Label2forTestSplitters)

        self.SplitterForFormating = QSplitter(Qt.Horizontal)
        self.SplitterForFormating.addWidget(self.TestSplitter1)
        self.SplitterForFormating.addWidget(self.splitterFinal)
        self.SplitterForFormating.addWidget(self.TestSplitter2)
        self.SplitterForFormating.setObjectName('SplitterForFormating')
        self.SplitterForFormating.setStyleSheet(
            """QSplitter#SplitterForFormating::handle {background: #DCDCDC; border-style:
            outset; border-width: 1px; border-color: #828282; border-radius: 3px;}"""
        )
        ######

        self.scroll1tab = QScrollArea()
        self.scroll1tab.setWidgetResizable(1)
        self.scroll1tab.setEnabled(1)
        self.scroll1tab.setWidget(self.SplitterForFormating)
        #self.scroll1tab.setWidget(self.splitterFinal)

        self.tab1hbox = QHBoxLayout()
        self.tab1hbox.setContentsMargins(5, 5, 5, 5)
        self.tab1hbox.addWidget(self.scroll1tab)
        self.tab1.setLayout(self.tab1hbox)

        # 2 tab
        self.SeachFormFirstNameLabel = QLabel("Ім'я:")
        self.SeachFormFirstNameLabel.setFixedHeight(20)
        self.SeachFormFirstNameLineEdit = QLineEdit()
        self.SeachFormFirstNameLineEdit.setFixedHeight(20)

        self.SeachFormLastNameLabel = QLabel("Прізвище:")
        self.SeachFormLastNameLabel.setFixedHeight(20)
        self.SeachFormLastNameLineedit = QLineEdit()
        self.SeachFormLastNameLineedit.setFixedHeight(20)

        self.SeachFormFatherNameLabel = QLabel("Побатькові:")
        self.SeachFormFatherNameLabel.setFixedHeight(20)
        self.SeachFormFatherNameLineEdit = QLineEdit()
        self.SeachFormFatherNameLineEdit.setFixedHeight(20)

        self.SeachFormHistoryNumberLabel = QLabel(
            "№ Історії вагітності/пологів:")
        self.SeachFormHistoryNumberLabel.setFixedHeight(20)
        self.SeachFormHistoryNumberLineEdit = QLineEdit()
        self.SeachFormHistoryNumberLineEdit.setFixedHeight(20)

        self.SeachFormAgeLabel = QLabel("Вік:")
        self.SeachFormAgeLabel.setFixedHeight(20)
        self.SeachFormAgeLineEdit = QLineEdit()
        self.SeachFormAgeLineEdit.setInputMask("D00")
        self.SeachFormAgeLineEdit.setFixedHeight(20)

        self.SeachButton = QPushButton("Пошук")
        self.SeachButton.clicked.connect(self.SeachInfo)

        self.SeachSplitter1 = QSplitter(Qt.Vertical)
        self.SeachSplitter1.addWidget(self.SeachFormFirstNameLabel)
        self.SeachSplitter1.addWidget(self.SeachFormFirstNameLineEdit)
        self.SeachSplitter1.addWidget(self.SeachFormHistoryNumberLabel)
        self.SeachSplitter1.addWidget(self.SeachFormHistoryNumberLineEdit)

        self.SeachSplitter2 = QSplitter(Qt.Vertical)
        self.SeachSplitter2.addWidget(self.SeachFormLastNameLabel)
        self.SeachSplitter2.addWidget(self.SeachFormLastNameLineedit)
        self.SeachSplitter2.addWidget(self.SeachFormAgeLabel)
        self.SeachSplitter2.addWidget(self.SeachFormAgeLineEdit)

        self.SeachSplitter3 = QSplitter(Qt.Vertical)
        self.SeachSplitter3.addWidget(self.SeachFormFatherNameLabel)
        self.SeachSplitter3.addWidget(self.SeachFormFatherNameLineEdit)
        self.SeachSplitter3.addWidget(self.SeachButton)

        self.SeachHeaderSplitter = QSplitter(Qt.Horizontal)
        self.SeachHeaderSplitter.addWidget(self.SeachSplitter1)
        self.SeachHeaderSplitter.addWidget(self.SeachSplitter2)
        self.SeachHeaderSplitter.addWidget(self.SeachSplitter3)

        # self.SeachHeaderSplitter.setStyleSheet()

        self.WievDataButton = QPushButton("Показати виділений рядок")
        self.WievDataButton.clicked.connect(self.SeachWievData)

        self.SeachResultTable = QTableWidget()
        self.SeachResultTable.setRowCount(1)
        self.SeachResultTable.setColumnCount(139)
        self.SeachResultTable.setAlternatingRowColors(1)

        self.tab2FinalSplitter = QSplitter(Qt.Vertical)
        self.tab2FinalSplitter.addWidget(self.SeachHeaderSplitter)
        self.tab2FinalSplitter.addWidget(self.SeachResultTable)
        self.tab2FinalSplitter.addWidget(self.WievDataButton)

        self.scroll1tab2 = QScrollArea()
        self.scroll1tab2.setWidgetResizable(1)
        self.scroll1tab2.setEnabled(1)
        self.scroll1tab2.setWidget(self.tab2FinalSplitter)

        self.tab2 = QWidget()

        self.tab2hbox = QHBoxLayout()
        self.tab2hbox.setContentsMargins(5, 5, 5, 5)
        self.tab2hbox.addWidget(self.scroll1tab2)
        self.tab2.setLayout(self.tab2hbox)

        # 3 tab
        self.tab3 = QWidget()

        self.CreateUserLoginLabel = QLabel("Логін:")
        self.CreateUserLoginLabel.setFixedHeight(20)
        self.CreateUserLoginLineEdit = QLineEdit()
        self.CreateUserLoginLineEdit.setFixedHeight(20)

        self.CreateUserPasswordLabel = QLabel("Пароль:")
        self.CreateUserPasswordLabel.setFixedHeight(20)
        self.CreateUserPasswordLineEdit = QLineEdit()
        self.CreateUserPasswordLineEdit.setFixedHeight(20)

        self.CreateUserPIBLabel = QLabel("П.І.Б.")
        self.CreateUserPIBLabel.setFixedHeight(20)
        self.CreateUserPIBLineEdit = QLineEdit()
        self.CreateUserPIBLineEdit.setFixedHeight(20)

        self.CreateUserPrivilegesLabel = QLabel("Права доступу:")
        self.CreateUserPrivilegesLabel.setFixedHeight(20)
        self.CreateUserPrivilegesComboBox = QComboBox()
        self.CreateUserPrivilegesComboBox.addItem('User')
        self.CreateUserPrivilegesComboBox.addItem('Administrator')
        self.CreateUserPrivilegesComboBox.setFixedHeight(20)

        self.CreateUserButton = QPushButton("Створити користувача")
        self.CreateUserButton.clicked.connect(self.CreateUser)

        self.CreateUsersSplitter1 = QSplitter(Qt.Vertical)
        self.CreateUsersSplitter1.addWidget(self.CreateUserLoginLabel)
        self.CreateUsersSplitter1.addWidget(self.CreateUserLoginLineEdit)

        self.CreateUsersSplitter2 = QSplitter(Qt.Vertical)
        self.CreateUsersSplitter2.addWidget(self.CreateUserPasswordLabel)
        self.CreateUsersSplitter2.addWidget(self.CreateUserPasswordLineEdit)

        self.CreateUsersSplitter3 = QSplitter(Qt.Vertical)
        self.CreateUsersSplitter3.addWidget(self.CreateUserPIBLabel)
        self.CreateUsersSplitter3.addWidget(self.CreateUserPIBLineEdit)

        self.CreateUsersSplitter4 = QSplitter(Qt.Vertical)
        self.CreateUsersSplitter4.addWidget(self.CreateUserPrivilegesLabel)
        self.CreateUsersSplitter4.addWidget(self.CreateUserPrivilegesComboBox)

        self.CreateUsersSplitter = QSplitter(Qt.Horizontal)
        self.CreateUsersSplitter.addWidget(self.CreateUsersSplitter1)
        self.CreateUsersSplitter.addWidget(self.CreateUsersSplitter2)
        self.CreateUsersSplitter.addWidget(self.CreateUsersSplitter3)
        self.CreateUsersSplitter.addWidget(self.CreateUsersSplitter4)
        self.CreateUsersSplitter.addWidget(self.CreateUserButton)

        self.tab3FinalSplitter = QSplitter(Qt.Horizontal)
        self.tab3FinalSplitter.addWidget(self.CreateUsersSplitter)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(1)
        self.scroll.setEnabled(1)

        # self.scroll.setStyleSheet("""QScrollArea{background: #32CC99;}""")
        # self.splitter60.setStyleSheet("{background: #32CC99;}")

        self.scroll.setWidget(self.tab3FinalSplitter)
        self.tab3hbox = QHBoxLayout()

        self.tab3hbox.setContentsMargins(5, 5, 5, 5)
        self.tab3hbox.addWidget(self.scroll)
        self.tab3.setLayout(self.tab3hbox)

        # 4 tab
        self.tab4 = QWidget()

        self.PynktIIIStatystykaLabel = QLabel("I. Медикаментозна профілактика/терапія ТЕУ до вагітності.")
        self.PynktIIIStatystykaLabel.setFixedHeight(20)
        self.PynktIIIStatystykaLabel.setStyleSheet(
            """QLabel{font-size:8pt; font-weight:600; color:#aa0000;}""")

        self.PynktIIIStatystykaGoButton = QPushButton("Розрахувати")
        self.PynktIIIStatystykaGoButton.setFixedHeight(20)

        self.PynktIIIStatystykaTable = QTableWidget()
        self.PynktIIIStatystykaTable.setRowCount(1)
        self.PynktIIIStatystykaTable.setColumnCount(2)
        self.PynktIIIStatystykaTable.setAlternatingRowColors(1)

        self.PynktVIStatystykaLabel = QLabel("ІI. Медикаментозна профілактика/терапія ТЕУ під час вагітності.")
        self.PynktVIStatystykaLabel.setFixedHeight(20)
        self.PynktVIStatystykaLabel.setStyleSheet(
            """QLabel{font-size:8pt; font-weight:600; color:#aa0000;}""")

        self.PynktVIStatystykaLabel_1 = QLabel("    1. Медикаментозна профілактика.")
        self.PynktVIStatystykaLabel_1.setFixedHeight(20)

        self.PynktVIStatystykaTable_1 = QTableWidget()
        self.PynktVIStatystykaTable_1.setRowCount(1)
        self.PynktVIStatystykaTable_1.setColumnCount(3)
        self.PynktVIStatystykaTable_1.setAlternatingRowColors(1)

        self.PynktVIStatystykaLabel_2 = QLabel("    2. Кількість ускладнень що виникли")
        self.PynktVIStatystykaLabel_2.setFixedHeight(20)

        self.PynktVIStatystykaTable_2 = QTableWidget()
        self.PynktVIStatystykaTable_2.setRowCount(1)
        self.PynktVIStatystykaTable_2.setColumnCount(2)
        self.PynktVIStatystykaTable_2.setAlternatingRowColors(1)

        self.PynktVIStatystykaGoButton = QPushButton("Розрахувати")
        self.PynktVIStatystykaGoButton.setFixedHeight(20)

        self.PynktIXStatystykaLabel = QLabel("ІIІ. Медикаментозна профілактика/терапія ТЕУ у післяпологовий період")
        self.PynktIXStatystykaLabel.setFixedHeight(20)
        self.PynktIXStatystykaLabel.setStyleSheet(
            """QLabel{font-size:8pt; font-weight:600; color:#aa0000;}""")

        self.PynktIXStatystykaGoButton = QPushButton("Розрахувати")
        self.PynktIXStatystykaGoButton.setFixedHeight(20)

        self.PynktIXStatystykaTable = QTableWidget()
        self.PynktIXStatystykaTable.setRowCount(1)
        self.PynktIXStatystykaTable.setColumnCount(3)
        self.PynktIXStatystykaTable.setAlternatingRowColors(1)

        self.StatystykaSplitter1 = QSplitter(Qt.Vertical)
        self.StatystykaSplitter1.addWidget(self.PynktIIIStatystykaLabel)
        self.StatystykaSplitter1.addWidget(self.PynktIIIStatystykaGoButton)
        self.StatystykaSplitter1.addWidget(self.PynktIIIStatystykaTable)

        self.StatystykaSplitter2 = QSplitter(Qt.Vertical)
        self.StatystykaSplitter2.addWidget(self.PynktVIStatystykaLabel)
        self.StatystykaSplitter2.addWidget(self.PynktVIStatystykaGoButton)
        self.StatystykaSplitter2.addWidget(self.PynktVIStatystykaLabel_1)
        self.StatystykaSplitter2.addWidget(self.PynktVIStatystykaTable_1)
        self.StatystykaSplitter2.addWidget(self.PynktVIStatystykaLabel_2)
        self.StatystykaSplitter2.addWidget(self.PynktVIStatystykaTable_2)

        self.StatystykaSplitter3 = QSplitter(Qt.Vertical)
        self.StatystykaSplitter3.addWidget(self.PynktIXStatystykaLabel)
        self.StatystykaSplitter3.addWidget(self.PynktIXStatystykaGoButton)
        self.StatystykaSplitter3.addWidget(self.PynktIXStatystykaTable)

        self.StatystykaFinalSplitter = QSplitter(Qt.Vertical)
        self.StatystykaFinalSplitter.addWidget(self.StatystykaSplitter1)
        self.StatystykaFinalSplitter.addWidget(self.StatystykaSplitter2)
        self.StatystykaFinalSplitter.addWidget(self.StatystykaSplitter3)

        self.tab4FinalSplitter = QSplitter(Qt.Horizontal)
        self.tab4FinalSplitter.addWidget(self.StatystykaFinalSplitter)

        self.scrolltab4 = QScrollArea()
        self.scrolltab4.setWidgetResizable(1)
        self.scrolltab4.setEnabled(1)
        self.scrolltab4.setWidget(self.StatystykaFinalSplitter)

        self.tab4hbox = QHBoxLayout()
        self.tab4hbox.setContentsMargins(5, 5, 5, 5)
        self.tab4hbox.addWidget(self.scrolltab4)
        self.tab4.setLayout(self.tab4hbox)

        self.bottomLeftTabWidget.addTab(self.tab1, "Внесення даних")
        self.bottomLeftTabWidget.addTab(self.tab2, "Перегляд даних")
        self.bottomLeftTabWidget.addTab(self.tab4, "Статистика")
        self.bottomLeftTabWidget.addTab(self.tab3, "Адміністрування")



        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.bottomLeftTabWidget, 1, 0)
        self.setLayout(self.grid)

        self.setGeometry(500, 30, 1000, 900)
        self.setWindowTitle('Реєстраційна карта')
        self.show()
        if privileges == 'App_user':
            self.bottomLeftTabWidget.removeTab(2)
            self.bottomLeftTabWidget.removeTab(0)

            # Валидатор данных и запись в БД

    def InsertToDBFunc(self):
        self.ErrorCount = 0

        self.PasportniDaniTitle = '\nI. Паспортні дані.'

        self.FirstName = self.FirstNameLineEdit.text()
        self.FirstName = self.FirstName.strip()
        if self.FirstName == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage('Необхідно ввести ім"я пацієнта!')
        else:
            self.FirstName = "Ім'я: " + self.FirstName
        self.FirstName = self.FirstName.strip()

        self.LastName = self.LastNameLineEdit.text()
        self.LastName = self.LastName.strip()
        if self.LastName == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage('Необхідно ввести прізвище пацієнта!')
        else:
            self.LastName = "Прізвище: " + self.LastName
        self.LastName = self.LastName.strip()

        self.FatherName = self.FatherNameLineEdit.text()
        self.FatherName = self.FatherName.strip()
        if self.FatherName == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage('Необхідно ввести по батькові пацієнта!')
        else:
            self.FatherName = "По батькові: " + self.FatherName
        self.FatherName = self.FatherName.strip()

        self.PasportniDani = "1. П.І.Б.:" + self.FirstName + "; " + self.LastName + "; " + self.FatherName + "."
        self.PasportniDani = self.PasportniDani.replace("'", "''")

        self.HistoryNumber = self.HistoryNumberLineEdit.text()
        self.HistoryNumber = self.HistoryNumber.strip()
        if self.HistoryNumber == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage('Необхідно ввести № історії вагітності/пологів!')
        else:
            self.HistoryNumber = '2. № Історії вагітності/пологів: ' + self.HistoryNumber
        self.HistoryNumber = self.HistoryNumber.replace("'", "''")

        self.Age = self.AgeLineEdit.text()
        self.Age = self.Age.strip()
        if self.Age == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage('Необхідно ввести вік пацієнта!')
        else:
            self.Age = '3. Вік: ' + self.Age

        self.Address = ''
        self.Address = self.AddressLineEdit.text()
        self.Address = self.Address.strip()
        if self.Address == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage('Необхідно ввести адресу пацієнта!')
        else:
            self.Address = '4. Адреса: ' + self.Address
        self.Address = self.Address.replace("'", "''")

        self.Proffesional = ''
        if self.ProffesionalDontWorkCheckBox.isChecked():
            self.Proffesional = 'не працює.'
        elif self.ProffesionalStadyCheckBox.isChecked():
            self.Proffesional = 'навчається.'
        elif self.ProffesionalWhiteCollarWorkerCheckBox.isChecked():
            self.Proffesional = 'службовець.'
        elif self.ProffesionalEmployeeCheckBox.isChecked():
            self.Proffesional = 'робітник.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage('Необхідно вибрати професійну діяльність!')
        self.Proffesional = '5. Професійна діяльність: ' + self.Proffesional

        self.Disability = ''
        if self.DisabilityNoneCheckBox.isChecked():
            self.Disability = 'немає.'
        elif self.DisabilityILevelCheckBox.isChecked():
            self.Disability = 'I група.'
        elif self.DisabilityIILevelCheckBox.isChecked():
            self.Disability = 'II група.'
        elif self.DisabilityIIILevelCheckBox.isChecked():
            self.Disability = 'III група.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage('Необхідно вибрати інвалідність!')
        self.Disability = '6. Інвалідність: ' + self.Disability

        self.ReceduvyTromboemboliiTitle = '\nII. Наявність постійних факторів ризику ТЕУ.'

        self.ReceduvyTromboembolii = ''
        if self.ReceduvyTromboemboliiNoCheckBox.isChecked():
            self.ReceduvyTromboembolii = '1. Рецедиви тромбоемболіі в минулому: ні.'
        else:
            self.ReceduvyTromboembolii = '1. Рецедиви тромбоемболіі в минулому: так.'

        self.TromboemboliiAndEstrogens = ''
        if self.TromboemboliiAndEstrogensNoCheckBox.isChecked():
            self.TromboemboliiAndEstrogens = "2. Тромбоемболії, неспровоковані або пов'язані з прийомом естрогенів: ні."
        else:
            self.TromboemboliiAndEstrogens = "2. Тромбоемболії, неспровоковані або пов'язані з прийомом естрогенів: так."
        self.TromboemboliiAndEstrogens = self.TromboemboliiAndEstrogens.replace(
            "'", "''")

        self.TromboemboliaSprovokovana = ''
        if self.TromboemboliaSprovokovanaNoCheckBox.isChecked():
            self.TromboemboliaSprovokovana = '3. Тромбоемболія спровокована: ні.'
        else:
            self.TromboemboliaSprovokovana = '3. Тромбоемболія спровокована: так.'

        self.SimeinuiAnamnezTromboembolii = ''
        if self.SimeinuiAnamnezTromboemboliiNoCheckBox.isChecked():
            self.SimeinuiAnamnezTromboembolii = '4. Сімейний анамнез тромбоемболії: ні.'
        else:
            self.SimeinuiAnamnezTromboembolii = '4. Сімейний анамнез тромбоемболії: так.'

        self.VstanovlennaTrombofilia = ''
        if self.VstanovlennaTrombofiliaNoCheckBox.isChecked():
            self.VstanovlennaTrombofilia = '5. Встановлена тромбофілія: ні.'
        else:
            self.VstanovlennaTrombofilia = '5. Встановлена тромбофілія: так.'

        self.SypytniZahvoryvanna = ''
        if self.SypytniZahvoryvannaNoCheckBox.isChecked():
            self.SypytniZahvoryvanna = 'ні'
        else:
            self.SypytniZahvoryvanna = self.SypytniZahvoryvanna + 'так'
            if self.SypytniSercevoSydunniCheckBox.isChecked():
                self.SypytniZahvoryvanna = self.SypytniZahvoryvanna + '; серцево-судинні'

            if self.SypytniBronhoLegeneviCheckBox.isChecked():
                self.SypytniZahvoryvanna = self.SypytniZahvoryvanna + '; бронхо-легеневі'

            if self.SypytniSCHVCheckBox.isChecked():
                self.SypytniZahvoryvanna = self.SypytniZahvoryvanna + '; СЧВ'

            if self.SypytniRAKCheckBox.isChecked():
                self.SypytniZahvoryvanna = self.SypytniZahvoryvanna + '; Рак'

            if self.SypytniNefrotuchnuiSundromCheckBox.isChecked():
                self.SypytniZahvoryvanna = self.SypytniZahvoryvanna + '; Нефротичний синдром'

            if self.SypytniSerpovudnoKlitynnaAnemiaCheckBox.isChecked():
                self.SypytniZahvoryvanna = self.SypytniZahvoryvanna + '; Серповидно-клітинна анемія'

            if self.SypytniVnytrishnoVenneVvedennaMedukamentivCheckBox.isChecked(
            ):
                self.SypytniZahvoryvanna = self.SypytniZahvoryvanna + '; Внутрішньовенне введення медикаментів'

            if self.SypytniOtherCheckBox.isChecked():
                self.SypytniZahvoryvanna = self.SypytniZahvoryvanna + '; інші:'
                self.SypytniOther = self.SypytniOtherLineEdit.text()
                self.SypytniOther = self.SypytniOther.strip()
                self.SypytniZahvoryvanna = self.SypytniZahvoryvanna + self.SypytniOther
        self.SypytniZahvoryvanna = '6. Супутні захворювання: ' + self.SypytniZahvoryvanna
        self.SypytniZahvoryvanna = self.SypytniZahvoryvanna.replace("'", "''")

        self.OldMore35 = ''
        if self.OldMore35NoCheckBox.isChecked():
            self.OldMore35 = '7. Вік > 35 років: ні.'
        else:
            self.OldMore35 = '7. Вік > 35 років: так.'

        self.Ogirinna = ''
        if self.OgirinnaNoCheckBox.isChecked():
            self.Ogirinna = '8. Ожиріння: ні.'
        else:
            self.Ogirinna = '8. Ожиріння: так.'

        self.VagitnistMore3 = ''
        if self.VagitnistMore3NoCheckBox.isChecked():
            self.VagitnistMore3 = '9. Вагітність ≥ 3: ні.'
        else:
            self.VagitnistMore3 = '9. Вагітність ≥ 3: так.'

        self.Kyrinna = ''
        if self.KyrinnaNoCheckBox.isChecked():
            self.Kyrinna = '10. Куріння: ні.'
        else:
            self.Kyrinna = '10. Куріння: так.'

        self.VelykiVarikozniVenu = ''
        if self.VelykiVarikozniVenuNoCheckBox.isChecked():
            self.VelykiVarikozniVenu = '11. Великі варикозні вени: ні.'
        else:
            self.VelykiVarikozniVenu = '11. Великі варикозні вени: так.'

        self.ProvedennaProfTEYdpVagitnosti = ''
        if self.ProvedennaProfTEYdpVagitnostiLabelNoCheckBox.isChecked():
            self.ProvedennaProfTEYdpVagitnosti = '\nIII. Проведення профілактики/терапії ТЕУ до вагітності: ні.'
        else:
            self.ProvedennaProfTEYdpVagitnosti = '\nIII. Проведення профілактики/терапії ТЕУ до вагітності: так.'

        self.ElastychnaKompresia = ''
        if self.ElastychnaKompresiaNoCheckBox.isChecked():
            self.ElastychnaKompresia = '1. Еластична компресія: ні.'
        else:
            self.ElastychnaKompresia = '1. Еластична компресія: так; клас: '
            self.ElastychnaKompresiaLevel = ''
            self.ElastychnaKompresiaLevel = self.ElastychnaKompresiaLevelLineEdit.text(
            )
            self.ElastychnaKompresiaLevel = self.ElastychnaKompresiaLevel.strip(
            )
            if self.ElastychnaKompresiaLevel == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно заповнити клас еластичної компресії в пункті "ІІІ. Проведення профілактики/терапії ТЕУ до вагітності"!'
                )
            else:
                self.ElastychnaKompresia = self.ElastychnaKompresia + self.ElastychnaKompresiaLevel
        self.ElastychnaKompresia = self.ElastychnaKompresia.replace("'", "''")

        self.MedukamentoznaProfilaktuka = ''
        if self.MedukamentoznaProfilaktukaNoCheckBox.isChecked():
            self.MedukamentoznaProfilaktuka = self.MedukamentoznaProfilaktuka + '2. Медикаментозна профілактика: ні.'
        else:
            self.MedukamentoznaProfilaktuka = self.MedukamentoznaProfilaktuka + '2. Медикаментозна профілактика: так.'

        self.MedukamentoznaProfilaktukaNazvaPreperaty = '2.1. Медикаментозна профілактика не проводилась.'
        if self.MedukamentoznaProfilaktukaYesCheckBox.isChecked():
            self.MedukamentoznaProfilaktukaNazvaPreperatyText = ''
            self.MedukamentoznaProfilaktukaNazvaPreperatyText = self.MedukamentoznaProfilaktukaNazvaPreperatyLineEdit.text(
            )
            self.MedukamentoznaProfilaktukaNazvaPreperatyText = self.MedukamentoznaProfilaktukaNazvaPreperatyText.strip(
            )

            if self.MedukamentoznaProfilaktukaNazvaPreperatyText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно заповнити назву препарату для медикаментозної профілактики в пункті "ІІІ. Проведення профілактики/терапії ТЕУ до вагітності"!'
                )
            else:
                self.MedukamentoznaProfilaktukaNazvaPreperaty = '2.1. Назва препарата: ' + self.MedukamentoznaProfilaktukaNazvaPreperatyText
        self.MedukamentoznaProfilaktukaNazvaPreperaty = self.MedukamentoznaProfilaktukaNazvaPreperaty.replace(
            "'", "''")

        self.MedukamentoznaProfilaktukaRegymPrujomy = '2.2. Медикаментозна профілактика не проводилась.'
        if self.MedukamentoznaProfilaktukaYesCheckBox.isChecked():
            self.MedukamentoznaProfilaktukaRegymPrujomyText = ''
            self.MedukamentoznaProfilaktukaRegymPrujomyText = self.MedukamentoznaProfilaktukaRegymPrujomyLineEdit.text(
            )
            self.MedukamentoznaProfilaktukaRegymPrujomyText = self.MedukamentoznaProfilaktukaRegymPrujomyText.strip(
            )

            if self.MedukamentoznaProfilaktukaRegymPrujomy == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно заповнити режим прийому препарату для медикаментозної профілактики в пункті "ІІІ. Проведення профілактики/терапії ТЕУ до вагітності"!'
                )
            else:
                self.MedukamentoznaProfilaktukaRegymPrujomy = '2.2. Режим прийому: ' + self.MedukamentoznaProfilaktukaRegymPrujomyText
        self.MedukamentoznaProfilaktukaRegymPrujomy = self.MedukamentoznaProfilaktukaRegymPrujomy.replace(
            "'", "''")

        self.HiryrgichneLikyvanna = ''
        if self.HiryrgichneLikyvannaNoCheckBox.isChecked():
            self.HiryrgichneLikyvanna = self.HiryrgichneLikyvanna + '3. Хірургічне лікування: ні.'
        else:
            self.HiryrgichneLikyvanna = '3. Хірургічне лікування: так; назва операції та рік: '
            self.HiryrgichneLikyvannaNazvaOpericii = ''
            self.HiryrgichneLikyvannaNazvaOpericii = self.HiryrgichneLikyvannaNazvaOpericiiLineEdit.text(
            )
            self.HiryrgichneLikyvannaNazvaOpericii = self.HiryrgichneLikyvannaNazvaOpericii.strip(
            )
            if self.HiryrgichneLikyvannaNazvaOpericii == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно заповнити назву операції та рік її проведення в пункті "ІІІ. Проведення профілактики/терапії ТЕУ до вагітності"!'
                )
            else:
                self.HiryrgichneLikyvanna = self.HiryrgichneLikyvanna + self.HiryrgichneLikyvannaNazvaOpericii
        self.HiryrgichneLikyvanna = self.HiryrgichneLikyvanna.replace(
            "'", "''")

        self.TryvalistProvedennoiProfilaktyky = '4. Тривалість проведеної профілактики: профілактика не проводилась.'
        if self.ProvedennaProfTEYdpVagitnostiLabelYesCheckBox.isChecked():
            self.TryvalistProvedennoiProfilaktyky = self.TryvalistProvedennoiProfilaktykyLineEdit.text(
            )
            self.TryvalistProvedennoiProfilaktyky = self.TryvalistProvedennoiProfilaktyky.strip(
            )
            if self.TryvalistProvedennoiProfilaktyky == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно заповнити тривалість проведеної профілактики в пункті "ІІІ. Проведення профілактики/терапії ТЕУ до вагітності"!'
                )
            else:
                self.TryvalistProvedennoiProfilaktyky = '4. Тривалість проведеної профілактики: ' + self.TryvalistProvedennoiProfilaktyky
        self.TryvalistProvedennoiProfilaktyky = self.TryvalistProvedennoiProfilaktyky.replace(
            "'", "''")

        self.YskladneenaVidProfilaktyku = ''
        if self.YskladneenaVidProfilaktykuNoCheckBox.isChecked():
            self.YskladneenaVidProfilaktyku = '5. Наявність ускладнень від проведеної профілактики: ні.'
        else:
            self.YskladneenaVidProfilaktyku = '5. Наявність ускладнень від проведеної профілактики: так; ускладнення: '
            self.YskladneenaVidProfilaktykuNajavnist = ''
            self.YskladneenaVidProfilaktykuNajavnist = self.YskladneenaVidProfilaktykuNajavnistLineEdit.text(
            )
            self.YskladneenaVidProfilaktykuNajavnist = self.YskladneenaVidProfilaktykuNajavnist.strip(
            )
            if self.YskladneenaVidProfilaktykuNajavnist == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно заповнити ускладнення від проведеної профілактики в пункті "ІІІ. Проведення профілактики/терапії ТЕУ до вагітності"!'
                )
            else:
                self.YskladneenaVidProfilaktyku = self.YskladneenaVidProfilaktyku + self.YskladneenaVidProfilaktykuNajavnist
        self.YskladneenaVidProfilaktyku = self.YskladneenaVidProfilaktyku.replace(
            "'", "''")

        self.AkysherskiiAnamnez = '\nІV. Акушерський анамнез.'

        self.DanaVagitnist = ''
        if self.DanaVagitnisPryrodnaCheckBox.isChecked():
            self.DanaVagitnist = '1. Дана вагітність: природна.'
        elif self.DanaVagitnisIndykovanaCheckBox.isChecked():
            self.DanaVagitnist = '1. Дана вагітність: індукована.'
        elif self.DanaVagitnisEKZCheckBox.isChecked():
            self.DanaVagitnist = '1. Дана вагітність: ЕКЗ.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати вид даної вагітності в пункті "ІV. Акушерський анамнез."!'
            )

        self.DanaVagitnistZaRahynkom = ''
        self.DanaVagitnistZaRahynkom = self.DanaVagitnistZaRahynkomLineEdit.text(
        )
        self.DanaVagitnistZaRahynkom = self.DanaVagitnistZaRahynkom.strip()
        if self.DanaVagitnistZaRahynkom == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно заповнити рахунок даної вагітності в пункті "ІV. Акушерський анамнез."!'
            )
        self.DanaVagitnistZaRahynkom = "1. Дана вагітність за рахунком: " + self.DanaVagitnistZaRahynkom

        self.DaniPologuZaRahynkom = ''
        self.DaniPologuZaRahynkom = self.DaniPologuZaRahynkomLineEdit.text()
        self.DaniPologuZaRahynkom = self.DaniPologuZaRahynkom.strip()
        if self.DaniPologuZaRahynkom == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно заповнити рахунок даних пологів в пункті "ІV. Акушерський анамнез."!'
            )
        self.DaniPologuZaRahynkom = "3. Дані пологи за рахунком: " + self.DaniPologuZaRahynkom

        self.PoperedniPologuZavershulus = ''
        if self.PoperedniPologuZavershulusPologamuCheckBox.isChecked():
            self.PoperedniPologuZavershulus = '4. Попередні вагітності завершились: пологами.'
        elif self.PoperedniPologuZavershulusAbortomShtychnumCheckBox.isChecked(
        ):
            self.PoperedniPologuZavershulus = '4. Попередні вагітності завершились: аборт самовільний.'
        elif self.PoperedniPologuZavershulusAbortomSamovilnumCheckBox.isChecked(
        ):
            self.PoperedniPologuZavershulus = '4. Попередні вагітності завершились: аборт штучний.'
        elif self.PoperednihPologivNeByloP4CheckBox.isChecked():
            self.PoperedniPologuZavershulus = '4. Попередні вагітності завершились: попередніх пологів не було.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати завершення попередньої вагітності в пункті "ІV. Акушерський анамнез."!'
            )

        self.PoperedniPologu = ''
        if self.PoperedniPologuFiziologichniCheckBox.isChecked():
            self.PoperedniPologu = 'фізіологічні.'
        elif self.PoperedniPologuPatologichniCheckBox.isChecked():
            self.PoperedniPologu = 'патологічні.'
        elif self.PoperednihPologivNeByloP5CheckBox.isChecked():
            self.PoperedniPologu = 'попередніх пологів не було.'
        elif self.PoperedniPologuYskladneniCheckBox.isChecked():
            self.PoperedniPologu = 'ускладені.'
            self.PoperedniPologuYskladneni = ''
            self.PoperedniPologuYskladneni = self.PoperedniPologuYskladneniLineEdit.text(
            )
            self.PoperedniPologuYskladneni = self.PoperedniPologuYskladneni.strip(
            )
            if self.PoperedniPologuYskladneni == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно заповнити ускладнення попередніх пологів в пункті "ІV. Акушерський анамнез."!'
                )
            else:
                self.PoperedniPologu = self.PoperedniPologu + ': ' + str(
                    self.PoperedniPologuYskladneni)
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати завершення попередньої вагітності в пункті "ІV. Акушерський анамнез."!'
            )
        self.PoperedniPologu = "5. Попередні пологи: " + self.PoperedniPologu

        self.NayavnistGuvyhDitey = ''
        if self.NayavnistGuvyhDiteyNoCheckBox.isChecked():
            self.NayavnistGuvyhDitey = self.NayavnistGuvyhDitey + '6. Наявність живих дітей: ні.'
        else:
            self.NayavnistGuvyhDitey = self.NayavnistGuvyhDitey + '6. Наявність живих дітей: так.'

        self.VPerebigDannoiVagitnosti = '\nV. Перебіг даної вагітності.'

        self.Vagitnist = ''
        if self.VagitnistOdnoplidnaCheckBox.isChecked():
            self.Vagitnist = '1. Вагітність: одноплідна.'
        else:
            self.Vagitnist = '1. Вагітність: багатоплідна.'

        self.NaOblikyVGinochiiKonsyltacii = ''
        self.NaOblikyVGinochiiKonsyltacii = self.NaOblikyVGinochiiKonsyltaciiLineEdit.text(
        )
        self.NaOblikyVGinochiiKonsyltacii = self.NaOblikyVGinochiiKonsyltacii.strip(
        )
        if self.NaOblikyVGinochiiKonsyltacii == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вказати термін, з якого вагітна знаходиться на обліку в жіночій консультації в пункті "V. Перебіг даної вагітності."!'
            )
        self.NaOblikyVGinochiiKonsyltacii = "2. На обліку в жіночій консультації з: " + self.NaOblikyVGinochiiKonsyltacii + " тижнів."

        self.ZagrozaPereruvannaVagitnosti = ''
        if self.ZagrozaPereruvannaVagitnostiNoCheckBox.isChecked():
            self.ZagrozaPereruvannaVagitnosti = self.ZagrozaPereruvannaVagitnosti + 'ні.'
        else:
            self.ZagrozaPereruvannaVagitnosti = self.ZagrozaPereruvannaVagitnosti + 'так; в терміні вагітності:'
            self.ZagrozaPereruvannaVagitnostiYTermini = self.ZagrozaPereruvannaVagitnostiYTerminiLineEdit.text(
            )
            self.ZagrozaPereruvannaVagitnostiYTermini = self.ZagrozaPereruvannaVagitnostiYTermini.strip(
            )
            if self.ZagrozaPereruvannaVagitnostiYTermini == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати термін на якому була загроза переривання вагітності, в пункті "V. Перебіг даної вагітності."!'
                )
            else:
                self.ZagrozaPereruvannaVagitnosti = self.ZagrozaPereruvannaVagitnosti + self.ZagrozaPereruvannaVagitnostiYTermini + " тижнів."
        self.ZagrozaPereruvannaVagitnosti = "3. Загроза переривання вагітності: " + self.ZagrozaPereruvannaVagitnosti

        self.ZagrozaPeredchasnuhPologiv = ''
        if self.ZagrozaPeredchasnuhPologivNoCheckBox.isChecked():
            self.ZagrozaPeredchasnuhPologiv = self.ZagrozaPeredchasnuhPologiv + 'ні.'
        else:
            self.ZagrozaPeredchasnuhPologiv = self.ZagrozaPeredchasnuhPologiv + 'так; в терміні вагітності:'
            self.ZagrozaPeredchasnuhPologivYTermini = self.ZagrozaPeredchasnuhPologivYTerminiLineEdit.text(
            )
            self.ZagrozaPeredchasnuhPologivYTermini = self.ZagrozaPeredchasnuhPologivYTermini.strip(
            )
            if self.ZagrozaPeredchasnuhPologivYTermini == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати термін на якому була загроза передчасних пологів, в пункті "V. Перебіг даної вагітності."!'
                )
            else:
                self.ZagrozaPeredchasnuhPologiv = self.ZagrozaPeredchasnuhPologiv + self.ZagrozaPeredchasnuhPologivYTermini + " тижнів."
        self.ZagrozaPeredchasnuhPologiv = '4. Загроза передчасних пологів: ' + self.ZagrozaPeredchasnuhPologiv

        self.ZagrozaPeredchasnuhPologivP4_1 = ''
        if self.ZagrozaPeredchasnuhPologivYesCheckBox.isChecked():
            if self.ZagrozaPereruvannaVagitnostiVidsharyvannaHorionaCheckBox.isChecked(
            ):
                self.ZagrozaPeredchasnuhPologivP4_1 = self.ZagrozaPeredchasnuhPologivP4_1 + " Відшарування хоріона;"

            if self.ZagrozaPereruvannaVagitnostiKrovomazannaCheckBox.isChecked(
            ):
                self.ZagrozaPeredchasnuhPologivP4_1 = self.ZagrozaPeredchasnuhPologivP4_1 + " Кровомазання;"

            if self.ZagrozaPereruvannaVagitnostiICNCheckBox.isChecked():
                self.ZagrozaPeredchasnuhPologivP4_1 = self.ZagrozaPeredchasnuhPologivP4_1 + " ІЦН;"
        else:
            self.ZagrozaPeredchasnuhPologivP4_1 = 'Загроза передчасних пологів відсутня'
        self.ZagrozaPeredchasnuhPologivP4_1 = '4.1. : ' + self.ZagrozaPeredchasnuhPologivP4_1

        self.GestozIPolovunuVagitnosti = ''
        if self.GestozIPolovunuVagitnostiNoCheckBox.isChecked():
            self.GestozIPolovunuVagitnosti = self.GestozIPolovunuVagitnosti + '5. Гестоз І половини вагітності: ні.'
        else:
            self.GestozIPolovunuVagitnosti = self.GestozIPolovunuVagitnosti + '5. Гестоз І половини вагітності: так.'

        self.InshiPruchynyZnevodnenna = ''
        if self.InshiPruchynyZnevodnennaNoCheckBox.isChecked():
            self.InshiPruchynyZnevodnenna = self.InshiPruchynyZnevodnenna + 'ні.'
        elif self.InshiPruchynyZnevodnennaYesCheckBox.isChecked():
            self.InshiPruchynyZnevodnenna = self.InshiPruchynyZnevodnenna + 'так.'
        elif self.InshiPruchynyZnevodnennaVarVCheckBox.isChecked():
            self.InshiPruchynyZnevodnenna = self.InshiPruchynyZnevodnenna + 'Інше: '
            self.InshiPruchynyZnevodnennaText = self.InshiPruchynyZnevodnennaVarVLineEdit.text(
            )
            self.InshiPruchynyZnevodnennaText = self.InshiPruchynyZnevodnennaText.strip(
            )
            if self.InshiPruchynyZnevodnennaText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати інші причини зневоднення в пункті "V. Перебіг даної вагітності."!'
                )
            else:
                self.InshiPruchynyZnevodnenna = self.InshiPruchynyZnevodnenna + self.InshiPruchynyZnevodnennaText
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати підходящий варіант в інших причинах зневоднення в пункті "V. Перебіг даної вагітності."!'
            )
        self.InshiPruchynyZnevodnenna = '6. Інші причини зневоднення: ' + self.InshiPruchynyZnevodnenna
        self.InshiPruchynyZnevodnenna = self.InshiPruchynyZnevodnenna.replace(
            "'", "''")

        self.GestozIIPolovunuVagitnosti = ''
        if self.GestozIIPolovunuVagitnostiNoCheckBox.isChecked():
            self.GestozIIPolovunuVagitnosti = self.GestozIIPolovunuVagitnosti + '7. Гестоз II половини вагітності: ні.'
        elif self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.isChecked(
        ):
            self.GestozIIPolovunuVagitnosti = self.GestozIIPolovunuVagitnosti + '7. Гестоз II половини вагітності: прееклампсія легкого ступеня.'
        elif self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.isChecked(
        ):
            self.GestozIIPolovunuVagitnosti = self.GestozIIPolovunuVagitnosti + '7. Гестоз II половини вагітності: прееклампсія середнього ступеня.'
        elif self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.isChecked(
        ):
            self.GestozIIPolovunuVagitnosti = self.GestozIIPolovunuVagitnosti + '7. Гестоз II половини вагітності: прееклампсія важкого ступеня.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати підходящий варіант гестозу ІІ половини вагітності в пункті "V. Перебіг даної вагітності."!'
            )

        self.GestozIIPolovunuVagitnostiVTermini = 'гестоз ІІ половини вагітності відсутній.'
        if self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.isChecked(
        ) or self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.isChecked(
        ) or self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.isChecked(
        ):
            self.GestozIIPolovunuVagitnostiVTermini = 'гестоз ІІ половини вагітності діагностовано в терміні '
            self.GestozIIPolovunuDiagnostovanoVTermini = ''
            self.GestozIIPolovunuDiagnostovanoVTermini = self.GestozIIPolovunuDiagnostovanoVTerminiLineEdit.text(
            )
            self.GestozIIPolovunuDiagnostovanoVTermini = self.GestozIIPolovunuDiagnostovanoVTermini.strip(
            )
            if self.GestozIIPolovunuDiagnostovanoVTermini == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати термін, в якому діагностовано гестоз ІІ половини вагітності в пункті "V. Перебіг даної вагітності."!'
                )
            else:
                self.GestozIIPolovunuVagitnostiVTermini = self.GestozIIPolovunuVagitnostiVTermini + self.GestozIIPolovunuDiagnostovanoVTermini + " тижнів"
        self.GestozIIPolovunuVagitnostiVTermini = "8. Гестоз ІІ половини вагітності діагностовано в терміні: " + self.GestozIIPolovunuVagitnostiVTermini

        self.VunuknennaTEY = ''
        if self.VunuknennaTEYNoCheckBox.isChecked():
            self.VunuknennaTEY = self.VunuknennaTEY + '9. Винекнення ТЕУ: ні.'
        else:
            self.VunuknennaTEY = self.VunuknennaTEY + '9. Винекнення ТЕУ: так.'

        self.VudTEY = '9.1. Вид ТЕУ: ТЕУ не виникало.'
        if self.VunuknennaTEYYesCheckBox.isChecked():
            self.VudTEYText = self.VudTEYLineEdit.text()
            self.VudTEYText = self.VudTEYText.strip()
            if self.VudTEYText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати вид ТЕУ в пункті "V. Перебіг даної вагітності."!'
                )
            else:
                self.VudTEY = "9.1. Вид ТЕУ: " + self.VudTEYText
        self.VudTEY = self.VudTEY.replace("'", "''")

        self.TEYTerminVagitnosti = '9.2. термін вагітності: ТЕУ не виникало.'
        if self.VunuknennaTEYYesCheckBox.isChecked():
            self.TEYTerminVagitnostiText = self.TEYTerminVagitnostiLineEdit.text(
            )
            self.TEYTerminVagitnostiText = self.TEYTerminVagitnostiText.strip()
            if self.VudTEYText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати термін вагітності на якому виникло ТЕУ в пункті "V. Перебіг даної вагітності."!'
                )
            else:
                self.TEYTerminVagitnosti = "9.2. термін вагітності: " + self.TEYTerminVagitnostiText

        self.Bagatovodda = ''
        if self.BagatovoddaNoCheckBox.isChecked():
            self.Bagatovodda = self.Bagatovodda + '10. Багатоводдя: ні.'
        elif self.BagatovoddaPomirneCheckBox.isChecked():
            self.Bagatovodda = self.Bagatovodda + '10. Багатоводдя: помірне.'
        elif self.BagatovoddaVurageneCheckBox.isChecked():
            self.Bagatovodda = self.Bagatovodda + '10. Багатоводдя: виражене.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати підходящий варіант багатоводдя в пункті "V. Перебіг даної вагітності."!'
            )

        self.BagatovoddaDiagnostovanoVTerminVagitnosti = '10.1 Багатоводдя діагностовано з терміну вагітності: багатоводдя не діагностувалося.'
        if self.BagatovoddaPomirneCheckBox.isChecked(
        ) or self.BagatovoddaVurageneCheckBox.isChecked():
            self.BagatovoddaDiagnostovanoVTerminVagitnosti = self.BagatovoddaDiagnostovanoVTerminVagitnostiLineEdit.text(
            )
            self.BagatovoddaDiagnostovanoVTerminVagitnosti = self.BagatovoddaDiagnostovanoVTerminVagitnosti.strip(
            )
            if self.BagatovoddaDiagnostovanoVTerminVagitnosti == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно термін вагітності на якому було діагностовано багатоводдя в пункті "V. Перебіг даної вагітності."!'
                )
            else:
                self.BagatovoddaDiagnostovanoVTerminVagitnosti = "10.1 Багатоводдя діагностовано з терміну вагітності: " + self.BagatovoddaDiagnostovanoVTerminVagitnosti

        self.MaloVodda = ''
        if self.MaloVoddaNoCheckBox.isChecked():
            self.MaloVodda = self.MaloVodda + '11. Маловоддя: ні.'
        elif self.MaloVoddaPomirneCheckBox.isChecked():
            self.MaloVodda = self.MaloVodda + '11. Маловоддя: помірне.'
        elif self.MaloVoddaVurageneCheckBox.isChecked():
            self.MaloVodda = self.MaloVodda + '11. Маловоддя: виражене.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати підходящий варіант маловоддя в пункті "V. Перебіг даної вагітності."!'
            )

        self.MaloVoddaDiagnostovanoVTerminVagitnosti = '11.1 Маловоддя діагностовано з терміну вагітності: маловоддя не діагностувалося.'
        if self.MaloVoddaPomirneCheckBox.isChecked(
        ) or self.MaloVoddaVurageneCheckBox.isChecked():
            self.MaloVoddaDiagnostovanoVTerminVagitnosti = self.MaloVoddaDiagnostovanoVTerminVagitnostiLineEdit.text(
            )
            self.MaloVoddaDiagnostovanoVTerminVagitnosti = self.MaloVoddaDiagnostovanoVTerminVagitnosti.strip(
            )
            if self.MaloVoddaDiagnostovanoVTerminVagitnosti == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно термін вагітності на якому було діагностовано маловоддя в пункті "V. Перебіг даної вагітності."!'
                )
            else:
                self.MaloVoddaDiagnostovanoVTerminVagitnosti = "11.1 Маловоддя діагностовано з терміну вагітності: " + self.MaloVoddaDiagnostovanoVTerminVagitnosti

        self.DustressPloda = ''
        if self.DustressPlodaNoCheckBox.isChecked():
            self.DustressPloda = self.DustressPloda + '12. Дистрес плода (за доплерометрією): ні.'
        elif self.DustressPlodaVKompensaciiCheckBox.isChecked():
            self.DustressPloda = self.DustressPloda + '12. Дистрес плода (за доплерометрією): в стадіі компенсації.'
        elif self.DustressPlodaVSubKompensaciiCheckBox.isChecked():
            self.DustressPloda = self.DustressPloda + '12. Дистрес плода (за доплерометрією): в стадіі субкомпенсації.'
        elif self.DustressPlodaVDekompensaciiCheckBox.isChecked():
            self.DustressPloda = self.DustressPloda + '12. Дистрес плода (за доплерометрією): в стадіі декомпенсації.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати підходящий варіант дистресу плода в пункті "V. Перебіг даної вагітності."!'
            )

        self.ZatrumkaRozvutkyPloda = ''
        if self.ZatrumkaRozvutkyPlodaNoCheckBox.isChecked():
            self.ZatrumkaRozvutkyPloda = self.ZatrumkaRozvutkyPloda + 'ні.'
        elif self.ZatrumkaRozvutkyPlodaSumetrychnaFormaCheckBox.isChecked():
            self.ZatrumkaRozvutkyPloda = self.ZatrumkaRozvutkyPloda + 'симетрична форма'
        elif self.ZatrumkaRozvutkyPlodaAsumetruchnaFormaCheckBox.isChecked():
            self.ZatrumkaRozvutkyPloda = self.ZatrumkaRozvutkyPloda + 'асиметрична форма'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати підходящий варіант затримки розвитку плода в пункті "V. Перебіг даної вагітності."!'
            )

        self.ZatrumkaRozvutkyPlodaVTermini = ''
        if self.ZatrumkaRozvutkyPlodaSumetrychnaFormaCheckBox.isChecked(
        ) or self.ZatrumkaRozvutkyPlodaAsumetruchnaFormaCheckBox.isChecked():
            self.ZatrumkaRozvutkyPlodaVTermini = self.ZatrumkaRozvutkyPlodaVTerminiLineEdit.text(
            )
            self.ZatrumkaRozvutkyPlodaVTermini = self.ZatrumkaRozvutkyPlodaVTermini.strip(
            )
            if self.ZatrumkaRozvutkyPlodaVTermini == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно термін вагітності на якому було діагностовано затримку розвитку плода в пункті "V. Перебіг даної вагітності."!'
                )
            else:
                self.ZatrumkaRozvutkyPlodaVTermini = '; в терміні ' + self.ZatrumkaRozvutkyPlodaVTermini + ' тижнів.'
        self.ZatrumkaRozvutkyPloda = self.ZatrumkaRozvutkyPloda + self.ZatrumkaRozvutkyPlodaVTermini
        self.ZatrumkaRozvutkyPloda = self.ZatrumkaRozvutkyPloda.strip()
        self.ZatrumkaRozvutkyPloda = "13. Затримка росту плода: " + self.ZatrumkaRozvutkyPloda

        self.NajavnistSustemnoiInfekcii = ''
        if self.NajavnistSustemnoiInfekciiNoCheckBox.isChecked():
            self.NajavnistSustemnoiInfekcii = '14. Наявність системної інфекції: ні.'
        else:
            self.NajavnistSustemnoiInfekcii = '14. Наявність системної інфекції: так.'

        self.PatologiaPlacentu = ''
        if self.PatologiaPlacentuNoCheckBox.isChecked():
            self.PatologiaPlacentu = '15. Патологія плаценти: ні.'
        elif self.PatologiaPlacentuGipoplaziaCheckBox.isChecked():
            self.PatologiaPlacentu = '15. Патологія плаценти: гіпоплазія.'
        elif self.PatologiaPlacentuGiperplaziaCheckBox.isChecked():
            self.PatologiaPlacentu = '15. Патологія плаценти: гіперплазія.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати підходящий варіант патології плаценти в пункті "V. Перебіг даної вагітності."!'
            )

        self.PatologiaLocalizaciiPlacentu = ''
        if self.PatologiaLocalizaciiPlacentuNoCheckBox.isChecked():
            self.PatologiaLocalizaciiPlacentu = '15.1. Паталогія  локалізації плаценти: ні.'
        elif self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaCheckBox.isChecked(
        ):
            self.PatologiaLocalizaciiPlacentu = '15.1. Паталогія  локалізації плаценти: низька плацентація.'
        elif self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaCheckBox.isChecked(
        ):
            self.PatologiaLocalizaciiPlacentu = '15.1. Паталогія  локалізації плаценти: крайове передлежання.'
        elif self.PatologiaLocalizaciiPlacentuPovnePeredlegannaCheckBox.isChecked(
        ):
            self.PatologiaLocalizaciiPlacentu = '15.1. Паталогія  локалізації плаценти: повне передлежання.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати підходящий варіант патології локалізації плаценти в пункті "V. Перебіг даної вагітності."!'
            )

        self.PeredchasneVadsharyvannaPlacentu = ''
        if self.PeredchasneVadsharyvannaPlacentuNoCheckBox.isChecked():
            self.PeredchasneVadsharyvannaPlacentu = '16. Передчасне відшарування плаценти: ні.'
        else:
            self.PeredchasneVadsharyvannaPlacentu = '16. Передчасне відшарування плаценти: так.'

        self.HiryrgichniVtyrchannaPidChasVagitnosti = ''
        if self.HiryrgichniVtyrchannaPidChasVagitnostiNoCheckBox.isChecked():
            self.HiryrgichniVtyrchannaPidChasVagitnosti = '17. Хірургічні втручання під час вагітності: ні.'
        else:
            self.HiryrgichniVtyrchannaPidChasVagitnosti = '17. Хірургічні втручання під час вагітності: так.'

        self.TruvalaImmobilizacia = ''
        if self.TruvalaImmobilizaciaNoCheckBox.isChecked():
            self.TruvalaImmobilizacia = '18. Тривала іммобілізація: ні.'
        else:
            self.TruvalaImmobilizacia = '18. Тривала іммобілізація: так.'

        self.ZavershennaDannoiVagitnosti = ''
        if self.ZavershennaDannoiVagitnostiPologuVTerminiCheckBox.isChecked():
            self.ZavershennaDannoiVagitnosti = self.ZavershennaDannoiVagitnosti + 'Пологи в терміні: '
            self.ZavershennaDannoiVagitnostiPologuVTermini = self.ZavershennaDannoiVagitnostiPologuVTerminiLineEdit.text(
            )
            self.ZavershennaDannoiVagitnostiPologuVTermini = self.ZavershennaDannoiVagitnostiPologuVTermini.strip(
            )
            if self.ZavershennaDannoiVagitnostiPologuVTermini == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати термін на якому відбулися пологи в пункті "V. Перебіг даної вагітності."!'
                )
            # else:
            #     self.ZavershennaDannoiVagitnostiPologuVTermini = self.ZavershennaDannoiVagitnostiPologuVTermini
            self.ZavershennaDannoiVagitnosti = self.ZavershennaDannoiVagitnosti + self.ZavershennaDannoiVagitnostiPologuVTermini + ' тижнів'

        elif self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokCheckBox.isChecked(
        ):
            self.ZavershennaDannoiVagitnosti = self.ZavershennaDannoiVagitnosti + 'Переривання за медичними показаннями в терміні '
            self.ZavershennaDannoiVagitnostiPereryvannaZaMedPok = self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokLineEdit.text(
            )
            self.ZavershennaDannoiVagitnostiPereryvannaZaMedPok = self.ZavershennaDannoiVagitnostiPereryvannaZaMedPok.strip(
            )
            if self.ZavershennaDannoiVagitnostiPereryvannaZaMedPok == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати термін на якому відбулося переривання вагітності за медичними показаннями в пункті "V. Перебіг даної вагітності."!'
                )
            # else:
            #     self.ZavershennaDannoiVagitnostiPereryvannaZaMedPok = self.ZavershennaDannoiVagitnostiPereryvannaZaMedPok
            self.ZavershennaDannoiVagitnosti = self.ZavershennaDannoiVagitnosti + self.ZavershennaDannoiVagitnostiPereryvannaZaMedPok + ' тижнів'

        elif self.ZavershennaDannoiVagitnostiSamovilnuiVukudenCheckBox.isChecked(
        ):
            self.ZavershennaDannoiVagitnosti = self.ZavershennaDannoiVagitnosti + 'Самовільний викидень в терміні '
            self.ZavershennaDannoiVagitnostiSamovilnuiVukuden = self.ZavershennaDannoiVagitnostiSamovilnuiVukudenLineEdit.text(
            )
            self.ZavershennaDannoiVagitnostiSamovilnuiVukuden = self.ZavershennaDannoiVagitnostiSamovilnuiVukuden.strip(
            )
            if self.ZavershennaDannoiVagitnostiSamovilnuiVukuden == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати термін на якому самовільний викидень в пункті "V. Перебіг даної вагітності."!'
                )
            # else:
            #     self.ZavershennaDannoiVagitnostiSamovilnuiVukuden = self.ZavershennaDannoiVagitnostiSamovilnuiVukuden
            self.ZavershennaDannoiVagitnosti = self.ZavershennaDannoiVagitnosti + self.ZavershennaDannoiVagitnostiSamovilnuiVukuden + ' тижнів'

        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати підходящий варіант завершення даної вагітності плаценти в пункті "V. Перебіг даної вагітності."!'
            )
        self.ZavershennaDannoiVagitnosti = "19. Завершення даної вагітності: " + self.ZavershennaDannoiVagitnosti
        self.ZavershennaDannoiVagitnosti = self.ZavershennaDannoiVagitnosti.replace(
            "'", "''")

        self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnosti = ''
        if self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiNoCheckBox.isChecked(
        ):
            self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnosti = '\nVІ. Проведення профілактики/терапії ТЕУ під час вагітності: ні.'
        else:
            self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnosti = '\nVІ. Проведення профілактики/терапії ТЕУ під час вагітності: так.'

        self.PokazuDlaProvedennaProfilaktuky = 'Покази до проведення профілактики: проведення профілактики/терапії ТЕУ під час вагітності не проводилося'
        if self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiYesCheckBox.isChecked(
        ):
            self.PokazuDlaProvedennaProfilaktukyText = self.PokazuDlaProvedennaProfilaktukyLineEdit.text(
            )
            self.PokazuDlaProvedennaProfilaktukyText = self.PokazuDlaProvedennaProfilaktukyText.strip(
            )
            if self.PokazuDlaProvedennaProfilaktukyText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно заповнити покази для проведення профілактики в пункті "VІ Проведення профілактики/терапії ТЕУ під час вагітності"!'
                )
            else:
                self.PokazuDlaProvedennaProfilaktuky = 'Покази до проведення профілактики: ' + self.PokazuDlaProvedennaProfilaktukyText
        self.PokazuDlaProvedennaProfilaktuky = self.PokazuDlaProvedennaProfilaktuky.replace(
            "'", "''")

        self.ElastychnaKompresiaPynktVI = ''
        if self.ElastychnaKompresiaPynktVINoCheckBox.isChecked():
            self.ElastychnaKompresiaPynktVI = '1. Еластична компресія: ні.'
        else:
            self.ElastychnaKompresiaPynktVI = '1. Еластична компресія: так; клас: '
            self.ElastychnaKompresiaPynktVILevel = self.ElastychnaKompresiaPynktVILevelLineEdit.text(
            )
            self.ElastychnaKompresiaPynktVILevel = self.ElastychnaKompresiaPynktVILevel.strip(
            )
            if self.ElastychnaKompresiaPynktVILevel == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно заповнити клас еластичної компрессії в пункті "VІ Проведення профілактики/терапії ТЕУ під час вагітності"!'
                )
            # else:
            #     self.ElastychnaKompresiaPynktVILevel = self.ElastychnaKompresiaPynktVILevel
            self.ElastychnaKompresiaPynktVI = self.ElastychnaKompresiaPynktVI + self.ElastychnaKompresiaPynktVILevel
        self.ElastychnaKompresiaPynktVI = self.ElastychnaKompresiaPynktVI.replace(
            "'", "''")

        self.MedukamentoznaProfilaktukaPynktVI = ''
        if self.MedukamentoznaProfilaktukaPynktVINoCheckBox.isChecked():
            self.MedukamentoznaProfilaktukaPynktVI = self.MedukamentoznaProfilaktukaPynktVI + '2. Медикаментозна профілактика: ні.'
        else:
            self.MedukamentoznaProfilaktukaPynktVI = self.MedukamentoznaProfilaktukaPynktVI + '2. Медикаментозна профілактика: так.'

        self.MedukamentoznaProfilaktukaPynktVINazvaPreperaty = '2.1 Назва препарату: медикаментозна профілактика не проводилась.'
        if self.MedukamentoznaProfilaktukaPynktVIYesCheckBox.isChecked():
            self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyText = self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLineEdit.text(
            )
            self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyText = self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyText.strip(
            )
            if self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно заповнити назву препарату для медикаментозної профілактики в пункті "VІ Проведення профілактики/терапії ТЕУ під час вагітності"!'
                )
            else:
                self.MedukamentoznaProfilaktukaPynktVINazvaPreperaty = '2.1 Назва препарату: ' + self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyText
        self.MedukamentoznaProfilaktukaPynktVINazvaPreperaty = self.MedukamentoznaProfilaktukaPynktVINazvaPreperaty.replace(
            "'", "''")

        self.MedukamentoznaProfilaktukaPynktVIRegymPrujomy = '2.2 Режим прийому: медикаментозна профілактика не проводилась.'
        if self.MedukamentoznaProfilaktukaPynktVIYesCheckBox.isChecked():
            self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyText = self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLineEdit.text(
            )
            self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyText = self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyText.strip(
            )
            if self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно заповнити режим прийому препарату для медикаментозної профілактики в пункті "VІ Проведення профілактики/терапії ТЕУ під час вагітності"!'
                )
            else:
                self.MedukamentoznaProfilaktukaPynktVIRegymPrujomy = '2.2 Режим прийому: ' + self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyText
        self.MedukamentoznaProfilaktukaPynktVIRegymPrujomy = self.MedukamentoznaProfilaktukaPynktVIRegymPrujomy.replace(
            "'", "''")

        self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznacheno = '2.3 Термін коли призначено: медикаментозна профілактика не проводилась.'
        if self.MedukamentoznaProfilaktukaPynktVIYesCheckBox.isChecked():
            self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoText = self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLineEdit.text(
            )
            self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoText = self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoText.strip(
            )
            if self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно заповнити режим прийому препарату для медикаментозної профілактики в пункті "VІ Проведення профілактики/терапії ТЕУ під час вагітності"!'
                )
            else:
                self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznacheno = '2.3 Термін коли призначено: ' + self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoText
        self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznacheno = self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznacheno.replace(
            "'", "''")

        self.HiryrgichneLikyvannaPynktVI = ''
        if self.HiryrgichneLikyvannaPynktVINoCheckBox.isChecked():
            self.HiryrgichneLikyvannaPynktVI = '3. Хірургічне лікування: ні.'
        else:
            self.HiryrgichneLikyvannaPynktVI = 'так; назва операції та дата: '
            self.HiryrgichneLikyvannaNazvaOpericiiPynktVI = self.HiryrgichneLikyvannaNazvaOpericiiPynktVILineEdit.text(
            )
            self.HiryrgichneLikyvannaNazvaOpericiiPynktVI = self.HiryrgichneLikyvannaNazvaOpericiiPynktVI.strip(
            )
            if self.HiryrgichneLikyvannaNazvaOpericiiPynktVI == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно заповнити назву операції та дату в пункті "VІ Проведення профілактики/терапії ТЕУ під час вагітності"!'
                )
            # else:
            #     self.HiryrgichneLikyvannaNazvaOpericiiPynktVI = self.HiryrgichneLikyvannaNazvaOpericiiPynktVI
            self.HiryrgichneLikyvannaPynktVI = self.HiryrgichneLikyvannaPynktVI + self.HiryrgichneLikyvannaNazvaOpericiiPynktVI
        self.HiryrgichneLikyvannaPynktVI = self.HiryrgichneLikyvannaPynktVI.replace(
            "'", "''")

        self.TryvalistProvedennoiProfilaktykyPynktVI = '4. Тривалість проведеної профілактики: проведення профілактики/терапії ТЕУ під час вагітності не проводилося.'
        if self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiYesCheckBox.isChecked(
        ):
            self.TryvalistProvedennoiProfilaktykyPynktVI = ''
            self.TryvalistProvedennoiProfilaktykyPynktVIText = self.TryvalistProvedennoiProfilaktykyPynktVILineEdit.text(
            )
            self.TryvalistProvedennoiProfilaktykyPynktVIText = self.TryvalistProvedennoiProfilaktykyPynktVIText.strip(
            )
            if self.TryvalistProvedennoiProfilaktykyPynktVIText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно заповнити тривалість проведеної профілактики в пункті "VІ Проведення профілактики/терапії ТЕУ під час вагітності"!'
                )
            else:
                # self.TryvalistProvedennoiProfilaktykyPynktVIText = self.TryvalistProvedennoiProfilaktykyPynktVIText
                self.TryvalistProvedennoiProfilaktykyPynktVI = "4. Тривалість проведеної профілактики: " + self.TryvalistProvedennoiProfilaktykyPynktVIText
        self.TryvalistProvedennoiProfilaktykyPynktVI = self.TryvalistProvedennoiProfilaktykyPynktVI.replace(
            "'", "''")

        self.YskladneenaVidProfilaktykuPynktVI = ''
        if self.YskladneenaVidProfilaktykuPynktVINoCheckBox.isChecked():
            self.YskladneenaVidProfilaktykuPynktVI = '5. Наявність ускладнень від проведеної профілактики: ні.'
        else:
            self.YskladneenaVidProfilaktykuPynktVI = '5. Наявність ускладнень від проведеної профілактики: так; назва операції та дата: '
            self.YskladneenaVidProfilaktykuPynktVIText = self.HiryrgichneLikyvannaNazvaOpericiiPynktVILineEdit.text(
            )
            self.YskladneenaVidProfilaktykuPynktVIText = self.YskladneenaVidProfilaktykuPynktVIText.strip(
            )
            if self.YskladneenaVidProfilaktykuPynktVIText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно заповнити назву операції та дату в пункті "VІ Проведення профілактики/терапії ТЕУ під час вагітності"!'
                )
            # else:
                # self.YskladneenaVidProfilaktykuPynktVIText = self.YskladneenaVidProfilaktykuPynktVIText
            self.YskladneenaVidProfilaktykuPynktVI = self.YskladneenaVidProfilaktykuPynktVI + self.YskladneenaVidProfilaktykuPynktVIText
        self.YskladneenaVidProfilaktykuPynktVI = self.YskladneenaVidProfilaktykuPynktVI.replace(
            "'", "''")

        self.TerapiyVidminenoZaGodDoPologivPynktVI = '6. Терапію відмінено за: проведення профілактики/терапії ТЕУ під час вагітності не проводилося.'
        if self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiYesCheckBox.isChecked(
        ):
            self.TerapiyVidminenoZaGodDoPologivPynktVIText = self.TerapiyVidminenoZaGodDoPologivPynktVILineEdit.text(
            )
            self.TerapiyVidminenoZaGodDoPologivPynktVIText = self.TerapiyVidminenoZaGodDoPologivPynktVIText.strip(
            )
            if self.TerapiyVidminenoZaGodDoPologivPynktVIText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно за скільки годин до пологів було відмінено терапію в пункті "VІ Проведення профілактики/терапії ТЕУ під час вагітності"!'
                )
            else:
                # self.TerapiyVidminenoZaGodDoPologivPynktVIText = self.TerapiyVidminenoZaGodDoPologivPynktVIText
                self.TerapiyVidminenoZaGodDoPologivPynktVI = '6. Терапію відмінено за: ' + self.TerapiyVidminenoZaGodDoPologivPynktVIText

        self.PerebigDanuhPologiv = "\nVII. Перебіг даних пологів."

        self.PologuVaginalni = ''
        if self.PologuVaginalniNoCheckBox.isChecked():
            self.PologuVaginalni = '1. Пологи вагінальні: ні.'
        elif self.PologuVaginalniSpomtanniCheckBox.isChecked():
            self.PologuVaginalni = '1. Пологи вагінальні: спонтанні.'
        elif self.PologuVaginalniIndykovaniCheckBox.isChecked():
            self.PologuVaginalni = '1. Пологи вагінальні: індуковані.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати потрібний варіант вагінальних пологів в пункті "VII. Перебіг даних пологів"!'
            )

        self.PologuAbdominalni = ''
        if self.PologuAbdominalniNoCheckBox.isChecked():
            self.PologuAbdominalni = self.PologuAbdominalni + '2. Пологи абдомінальні: ні.'
        elif self.PologuAbdominalniPlanovuiKRCheckBox.isChecked():
            self.PologuAbdominalni = self.PologuAbdominalni + '2. Пологи абдомінальні: плановий КР.'
        elif self.PologuAbdominalniYrgentbuiKRCheckBox.isChecked():
            self.PologuAbdominalni = self.PologuAbdominalni + '2. Пологи абдомінальні: кргентний КР.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати потрібний варіант абдомінальних пологів в пункті "VII. Перебіг даних пологів"!'
            )

        self.PokazannaDlaAbdominalnogoRozrodjenna = ''
        self.PokazannaDlaAbdominalnogoRozrodjennaText = self.PokazannaDlaAbdominalnogoRozrodjennaLineEdit.text(
        )
        self.PokazannaDlaAbdominalnogoRozrodjennaText = self.PokazannaDlaAbdominalnogoRozrodjennaText.strip(
        )
        if self.PokazannaDlaAbdominalnogoRozrodjennaText == '':
            self.PokazannaDlaAbdominalnogoRozrodjenna = '3. Показання до абдомінального розродження: відсутні.'
        else:
            self.PokazannaDlaAbdominalnogoRozrodjenna = "3. Показання до абдомінального розродження: " + self.PokazannaDlaAbdominalnogoRozrodjennaText
        self.PokazannaDlaAbdominalnogoRozrodjenna = self.PokazannaDlaAbdominalnogoRozrodjenna.replace(
            "'", "''")

        self.PoryshennaPologovoiDialnosti = ''
        if self.PoryshennaPologovoiDialnostiNoCheckBox.isChecked():
            self.PoryshennaPologovoiDialnosti = '4. Порушення пологової діяльності: ні.'
        elif self.PoryshennaPologovoiDialnostiStrimkiPologuCheckBox.isChecked(
        ):
            self.PoryshennaPologovoiDialnosti = '4. Порушення пологової діяльності: стрімкі пологи.'
        elif self.PoryshennaPologovoiDialnostiDuskoordunaciaCheckBox.isChecked(
        ):
            self.PoryshennaPologovoiDialnosti = '4. Порушення пологової діяльності: дискоординація.'
        elif self.PoryshennaPologovoiDialnostiSlabkistCheckBox.isChecked():
            self.PoryshennaPologovoiDialnosti = '4. Порушення пологової діяльності: слабкість.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати потрібний варіант порушення пологової діяльності в пункті "VII. Перебіг даних пологів"!'
            )

        self.KorekciaAnomaliiPologovoiDialnosti = ''
        if self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.isChecked():
            self.KorekciaAnomaliiPologovoiDialnosti = '5. Корекція аномалій пологової діяльності: ні.'
        elif self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox.isChecked(
        ):
            self.KorekciaAnomaliiPologovoiDialnosti = '5. Корекція аномалій пологової діяльності: бета-міметики.'
        elif self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox.isChecked(
        ):
            self.KorekciaAnomaliiPologovoiDialnosti = '5. Корекція аномалій пологової діяльності: окситоцин.'
        elif self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox.isChecked(
        ):
            self.KorekciaAnomaliiPologovoiDialnosti = '5. Корекція аномалій пологової діяльності: ензапрост.'
        elif self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox.isChecked(
        ):
            self.KorekciaAnomaliiPologovoiDialnosti = '5. Корекція аномалій пологової діяльності: окситоцин з ензапростом.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати потрібний варіант  корекції аномалій пологової діяльності в пункті "VII. Перебіг даних пологів"!'
            )

        self.VuluvNavkoloplodovuhVod = ''
        if self.VuluvNavkoloplodovuhVodSvoechasnuiCheckBox.isChecked():
            self.VuluvNavkoloplodovuhVod = '6. Вилив навколоплодових вод: своєчасний.'
        elif self.VuluvNavkoloplodovuhVodRaniiCheckBox.isChecked():
            self.VuluvNavkoloplodovuhVod = '6. Вилив навколоплодових вод: ранній.'
        elif self.VuluvNavkoloplodovuhVodPeredchasnuiCheckBox.isChecked():
            self.VuluvNavkoloplodovuhVod = '6. Вилив навколоплодових вод: передчасний.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати потрібний варіант виливу навколоплодових вод в пункті "VII. Перебіг даних пологів"!'
            )

        self.DustressPlodaVPologah = ''
        if self.DustressPlodaVPologahNoCheckBox.isChecked():
            self.DustressPlodaVPologah = '7. Дистрес плода в пологах: ні.'
        elif self.DustressPlodaVPologahVIPeriodiCheckBox.isChecked():
            self.DustressPlodaVPologah = '7. Дистрес плода в пологах: в І періоді.'
        elif self.DustressPlodaVPologahVIIPeriodiCheckBox.isChecked():
            self.DustressPlodaVPologah = '7. Дистрес плода в пологах: в ІІ періоді.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати потрібний варіант дистресу плода під час пологів в пункті "VII. Перебіг даних пологів"!'
            )

        self.GipotonichnaKrovotecha = ''
        if self.GipotonichnaKrovotechaNoCheckBox.isChecked():
            self.GipotonichnaKrovotecha = '8. Гіпотонічна кровотеча: ні.'
        elif self.GipotonichnaKrovotechaVIIIPeriodiCheckBox.isChecked():
            self.GipotonichnaKrovotecha = '8. Гіпотонічна кровотеча: в ІII періоді'
        elif self.GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiCheckBox.isChecked(
        ):
            self.GipotonichnaKrovotecha = '8. Гіпотонічна кровотеча: в ранньому післяпологовому періоді.'
        elif self.GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiCheckBox.isChecked(
        ):
            self.GipotonichnaKrovotecha = '8. Гіпотонічна кровотеча: в пізньому післяпологовому періоді.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати потрібний варіант гіпотонічної в пункті "VII. Перебіг даних пологів"!'
            )

        self.AnomaliiPrukriplennaPlacentu = ''
        if self.AnomaliiPrukriplennaPlacentuNoCheckBox.isChecked():
            self.AnomaliiPrukriplennaPlacentu = '9. Аномалії прикріплення плаценти: ні.'
        elif self.AnomaliiPrukriplennaPlacentuAdherensCheckBox.isChecked():
            self.AnomaliiPrukriplennaPlacentu = '9. Аномалії прикріплення плаценти: adherens.'
        elif self.AnomaliiPrukriplennaPlacentuAcretaCheckBox.isChecked():
            self.AnomaliiPrukriplennaPlacentu = '9. Аномалії прикріплення плаценти: acreta.'
        elif self.AnomaliiPrukriplennaPlacentuPercretaCheckBox.isChecked():
            self.AnomaliiPrukriplennaPlacentu = '9. Аномалії прикріплення плаценти: percreta.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати потрібний варіант аномалії прикріплення плаценти в пункті "VII. Перебіг даних пологів"!'
            )

        self.DefektPoslidy = ''
        if self.DefektPoslidyNoCheckBox.isChecked():
            self.DefektPoslidy = '10. Дефект посліду: ні.'
        else:
            self.DefektPoslidy = '10. Дефект посліду: так.'

        self.DefektObolonok = ''
        if self.DefektObolonokNoCheckBox.isChecked():
            self.DefektObolonok = '11. Дефект оболонок: ні.'
        else:
            self.DefektObolonok = '11. Дефект оболонок: так.'

        self.AnomaliiPrukriplennaPypovunu = ''
        if self.AnomaliiPrukriplennaPypovunuNoCheckBox.isChecked():
            self.AnomaliiPrukriplennaPypovunu = self.AnomaliiPrukriplennaPypovunu + '12. Аномалії прикріплення пуповини: ні.'
        else:
            self.AnomaliiPrukriplennaPypovunu = self.AnomaliiPrukriplennaPypovunu + '12. Аномалії прикріплення пуповини: так.'

        self.OperatuvnaDopomoga = ''
        if self.OperatuvnaDopomogaNoCheckBox.isChecked():
            self.OperatuvnaDopomoga = self.OperatuvnaDopomoga + 'ні.'
        elif self.OperatuvnaDopomogaRychnaReviziaCheckBox.isChecked():
            self.OperatuvnaDopomoga = self.OperatuvnaDopomoga + 'Ручна ревізія стінок порожнини матки; '
        elif self.OperatuvnaDopomogaInstrymentalnaReviziaCheckBox.isChecked():
            self.OperatuvnaDopomoga = self.OperatuvnaDopomoga + 'Інструментальна ревізія стінок порожнини матки; '
        elif self.OperatuvnaDopomogaRychneVidokremlennaCheckBox.isChecked():
            self.OperatuvnaDopomoga = self.OperatuvnaDopomoga + 'Ручне відокремлення плаценти та видалення посліду;'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати потрібний варіант оперативної допомоги в пункті "VII. Перебіг даних пологів"!'
            )
        self.OperatuvnaDopomoga = self.OperatuvnaDopomoga.strip()
        self.OperatuvnaDopomoga = '13. Оперативна допомога: ' + self.OperatuvnaDopomoga

        self.RozruvuPologovuhShlahiv = ''
        if self.RozruvuPologovuhShlahivNoCheckBox.isChecked():
            self.RozruvuPologovuhShlahiv = self.RozruvuPologovuhShlahiv + 'ні.'
        elif self.RozruvuPologovuhShlahivPromejunuCheckBox.isChecked():
            self.RozruvuPologovuhShlahiv = self.RozruvuPologovuhShlahiv + 'промежини; '
        elif self.RozruvuPologovuhShlahivPihvuCheckBox.isChecked():
            self.RozruvuPologovuhShlahiv = self.RozruvuPologovuhShlahiv + 'піхви; '
        elif self.RozruvuPologovuhShlahivShuikiMatkuCheckBox.isChecked():
            self.RozruvuPologovuhShlahiv = self.RozruvuPologovuhShlahiv + 'шийки матки;'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вибрати потрібний варіант розриву пологових шляхів в пункті "VII. Перебіг даних пологів"!'
            )
        self.StypinRozruvu = ''
        if self.RozruvuPologovuhShlahivPromejunuCheckBox.isChecked(
        ) or self.RozruvuPologovuhShlahivPihvuCheckBox.isChecked(
        ) or self.RozruvuPologovuhShlahivShuikiMatkuCheckBox.isChecked():
            self.StypinRozruvu = self.StypinRozruvyPologovuhShlahivLineEdit.text(
            )
            self.StypinRozruvu = self.StypinRozruvu.strip()
            self.StypinRozruvu = ' ступінь: ' + self.StypinRozruvu

        self.RozruvuPologovuhShlahiv = self.RozruvuPologovuhShlahiv.strip()
        self.RozruvuPologovuhShlahiv = '14. Розриви пологових шляхів: ' + self.RozruvuPologovuhShlahiv + self.StypinRozruvu

        self.EpizoAboPerineotomia = ''
        if self.EpizoAboPerineotomiaNoCheckBox.isChecked():
            self.EpizoAboPerineotomia = '15. Епізіо- або перінеотомія: ні.'
        else:
            self.EpizoAboPerineotomia = '15. Епізіо- або перінеотомія: так.'

        self.KrovovtrataVPologah = ''
        self.KrovovtrataVPologahText = self.KrovovtrataVPologahLineEdit.text()
        self.KrovovtrataVPologahText = self.KrovovtrataVPologahText.strip()
        if self.KrovovtrataVPologahText != '':
            self.KrovovtrataVPologah = '16. Крововтрата в пологах: ' + self.KrovovtrataVPologahText
            self.KrovovtrataVPologah = self.KrovovtrataVPologah.strip()
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно заповнити крововтрату в полгах в пункті "VII. Перебіг даних пологів"!'
            )
        self.KrovovtrataVPologah = self.KrovovtrataVPologah.replace("'", "''")

        self.TruvalistPologiv = '17. Тривалість пологів загальна: '
        self.TruvalistPologivZagalnaGodun = self.TruvalistPologivZagalnaGodunLineEdit.text(
        )
        self.TruvalistPologivZagalnaGodun = self.TruvalistPologivZagalnaGodun.strip(
        )
        if self.TruvalistPologivZagalnaGodun != '':
            self.TruvalistPologiv = self.TruvalistPologiv + self.TruvalistPologivZagalnaGodun + ' годин '

        self.TruvalistPologivZagalnaHvulun = self.TruvalistPologivZagalnaHvulunLineEdit.text(
        )
        self.TruvalistPologivZagalnaHvulun = self.TruvalistPologivZagalnaHvulun.strip(
        )
        if self.TruvalistPologivZagalnaHvulun != '':
            self.TruvalistPologiv = self.TruvalistPologiv + self.TruvalistPologivZagalnaHvulun + ' хвилин '
        self.TruvalistPologiv = self.TruvalistPologiv.strip()
        if self.TruvalistPologivZagalnaGodun == '' and self.TruvalistPologivZagalnaHvulun == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вказати загальну тривалість пологів в пункті "VII. Перебіг даних пологів"!'
            )

        self.TruvalistPologiv = self.TruvalistPologiv + '; - Ι період: '
        self.TruvalistPologivIPeriodGodun = self.TruvalistPologivIPeriodLineEdit.text(
        )
        self.TruvalistPologivIPeriodGodun = self.TruvalistPologivIPeriodGodun.strip(
        )
        if self.TruvalistPologivIPeriodGodun != '':
            self.TruvalistPologiv = self.TruvalistPologiv + self.TruvalistPologivIPeriodGodun + ' годин, '

        self.TruvalistPologivIPeriodHvulun = self.TruvalistPologivIPeriodHvulunLineEdit.text(
        )
        self.TruvalistPologivIPeriodHvulun = self.TruvalistPologivIPeriodHvulun.strip(
        )
        if self.TruvalistPologivIPeriodHvulun != '':
            self.TruvalistPologiv = self.TruvalistPologiv + self.TruvalistPologivIPeriodHvulun + ' хвилин '
        self.TruvalistPologiv = self.TruvalistPologiv.strip()
        if self.TruvalistPologivIPeriodGodun == '' and self.TruvalistPologivIPeriodHvulun == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вказати тривалість І періоду пологів в пункті "VII. Перебіг даних пологів"!'
            )

        self.TruvalistPologiv = self.TruvalistPologiv + '; - ΙI період: '
        self.TruvalistPologivIIPeriodGodun = self.TruvalistPologivIIPeriodLineEdit.text(
        )
        self.TruvalistPologivIIPeriodGodun = self.TruvalistPologivIIPeriodGodun.strip(
        )
        if self.TruvalistPologivIIPeriodGodun != '':
            self.TruvalistPologiv = self.TruvalistPologiv + self.TruvalistPologivIIPeriodGodun + ' годин, '

        self.TruvalistPologivIIPeriodHvulun = self.TruvalistPologivIIPeriodHvulunLineEdit.text(
        )
        self.TruvalistPologivIIPeriodHvulun = self.TruvalistPologivIIPeriodHvulun.strip(
        )
        if self.TruvalistPologivIIPeriodHvulun != '':
            self.TruvalistPologiv = self.TruvalistPologiv + self.TruvalistPologivIIPeriodHvulun + ' хвилин '
        self.TruvalistPologiv = self.TruvalistPologiv.strip()
        if self.TruvalistPologivIIPeriodGodun == '' and self.TruvalistPologivIIPeriodHvulun == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вказати тривалість ІI періоду пологів в пункті "VII. Перебіг даних пологів"!'
            )

        self.TruvalistPologiv = self.TruvalistPologiv + '; - ΙII період: '
        self.TruvalistPologivIIIPeriodGodun = self.TruvalistPologivIIIPeriodLineEdit.text(
        )
        self.TruvalistPologivIIIPeriodGodun = self.TruvalistPologivIIIPeriodGodun.strip(
        )
        if self.TruvalistPologivIIIPeriodGodun != '':
            self.TruvalistPologiv = self.TruvalistPologiv + self.TruvalistPologivIIIPeriodGodun + ' годин, '

        self.TruvalistPologivIIIPeriodHvulun = self.TruvalistPologivIIIPeriodHvulunLineEdit.text(
        )
        self.TruvalistPologivIIIPeriodHvulun = self.TruvalistPologivIIIPeriodHvulun.strip(
        )
        if self.TruvalistPologivIIIPeriodHvulun != '':
            self.TruvalistPologiv = self.TruvalistPologiv + self.TruvalistPologivIIIPeriodHvulun + ' хвилин '
        self.TruvalistPologiv = self.TruvalistPologiv.strip()
        if self.TruvalistPologivIIIPeriodGodun == '' and self.TruvalistPologivIIIPeriodHvulun == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вказати тривалість ІII періоду пологів в пункті "VII. Перебіг даних пологів"!'
            )

        self.StanNovonarodgennogoTaNeoPeriodTitleLable = '\nVIII. Стан новонародженого та перебіг раннього неонатального періоду.'

        self.Naroduvsa = '1. Народився: '
        if self.NaroduvsaGuvuiCheckBox.isChecked():
            self.Naroduvsa = self.Naroduvsa + 'живий.'
        else:
            self.Naroduvsa = self.Naroduvsa + 'мертвий.'

        self.PruchunaMertvonarodgenna = '2. Причина мертвонародження: народився живий.'
        if self.NaroduvsaMertvuiCheckBox.isChecked():
            if self.PruchunaMertvonarodgennaAntenatalnaCheckBox.isChecked():
                self.PruchunaMertvonarodgenna = '2. Причина мертвонародження антенатальна.'
            else:
                self.PruchunaMertvonarodgenna = '2. Причина мертвонародження інтранатальна.'

        self.ZrilistNovonarodgennogo = '3. Зрілість новонародженого: '
        if self.ZrilistNovonarodgennogoDonoshenuiCheckBox.isChecked():
            self.ZrilistNovonarodgennogo = self.ZrilistNovonarodgennogo + 'доношений.'
        elif self.ZrilistNovonarodgennogoNedonoshenuiCheckBox.isChecked():
            self.ZrilistNovonarodgennogo = self.ZrilistNovonarodgennogo + 'недоношений.'
        elif self.ZrilistNovonarodgennogoPerenoshenuiCheckBox.isChecked():
            self.ZrilistNovonarodgennogo = self.ZrilistNovonarodgennogo + 'переношений.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вказати зрілість новонародженого в пункті "VIII. Стан новонародженого та перебіг раннього неонатального періоду"!'
            )

        self.ParametruNovonarodgennogo = ''

        self.MasaNovonarodgenogo = self.MasaNovonarodgenogoLineEdit.text()
        self.MasaNovonarodgenogo = self.MasaNovonarodgenogo.strip()
        if self.MasaNovonarodgenogo == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вказати масу новонародженого в пункті "VIII. Стан новонародженого та перебіг раннього неонатального періоду"!'
            )

        self.ZristNovonarodgenogo = self.ZristNovonarodgenogoLineEdit.text()
        self.ZristNovonarodgenogo = self.ZristNovonarodgenogo.strip()
        if self.ZristNovonarodgenogo == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вказати зріст новонародженого в пункті "VIII. Стан новонародженого та перебіг раннього неонатального періоду"!'
            )

        self.KoeficientNovonarodgenogo = self.KoeficientNovonarodgenogoLineEdit.text(
        )
        self.KoeficientNovonarodgenogo = self.KoeficientNovonarodgenogo.strip()
        if self.KoeficientNovonarodgenogo == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вказати коефіцієнт новонародженого в пункті "VIII. Стан новонародженого та перебіг раннього неонатального періоду"!'
            )
        self.ParametruNovonarodgennogo = '4. Маса: ' + self.MasaNovonarodgenogo + '; зріст: ' + self.ZristNovonarodgenogo + '; коефіцієнт: ' + self.KoeficientNovonarodgenogo + '.'
        self.ParametruNovonarodgennogo = self.ParametruNovonarodgennogo.replace(
            "'", "''")

        self.GipotrofiaPloda = ''
        if self.GipotrofiaPlodaNoCheckBox.isChecked():
            self.GipotrofiaPloda = '4.1. Гіпотрофія плода: ні.'
        else:
            self.GipotrofiaPloda = '4.1. Гіпотрофія плода: так.'

        self.OcinkaZaShkaloyApgar = ''
        self.OcinkaZaShkaloyApgarNaPerHv = self.OcinkaZaShkaloyApgarNaPerHvLineEdit.text(
        )
        self.OcinkaZaShkaloyApgarNaPerHv = self.OcinkaZaShkaloyApgarNaPerHv.strip(
        )
        if self.OcinkaZaShkaloyApgarNaPerHv == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вказати оцінку новонародженого за шкалою апгар на 1 хвилині в пункті "VIII. Стан новонародженого та перебіг раннього неонатального періоду"!'
            )

        self.OcinkaZaShkaloyApgarNa5Hv = self.OcinkaZaShkaloyApgarNa5HvLineEdit.text(
        )
        self.OcinkaZaShkaloyApgarNa5Hv = self.OcinkaZaShkaloyApgarNa5Hv.strip()
        if self.OcinkaZaShkaloyApgarNa5Hv == '':
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вказати оцінку новонародженого за шкалою апгар на 5 хвилині в пункті "VIII. Стан новонародженого та перебіг раннього неонатального періоду"!'
            )

        self.OcinkaZaShkaloyApgar = '5. Оцінка за шкалою Апгар: на першій хвилині ' + self.OcinkaZaShkaloyApgarNaPerHv + '; на 5 хвилині: ' + self.OcinkaZaShkaloyApgarNa5Hv + '.'

        self.NovonarodjenuiZVadamuRozvutky = ''
        if self.NovonarodjenuiZVadamuRozvutkyNoCheckBox.isChecked():
            self.NovonarodjenuiZVadamuRozvutky = '6. Новонароджений з вадами розвиту:  ні.'
        else:
            self.NovonarodjenuiZVadamuRozvutkyJakiSame = self.NovonarodjenuiZVadamuRozvutkyJakiSameLineEdit.text(
            )
            self.NovonarodjenuiZVadamuRozvutkyJakiSame = self.NovonarodjenuiZVadamuRozvutkyJakiSame.strip(
            )
            if self.NovonarodjenuiZVadamuRozvutkyJakiSame == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати з якими саме вадами народився новонароджений в пункті "VIII. Стан новонародженого та перебіг раннього неонатального періоду"!'
                )
            else:
                self.NovonarodjenuiZVadamuRozvutky = '6. Новонароджений з вадами розвиту:  так; які саме: ' + self.NovonarodjenuiZVadamuRozvutkyJakiSame
        self.NovonarodjenuiZVadamuRozvutky = self.NovonarodjenuiZVadamuRozvutky.replace(
            "'", "''")

        self.PologovaTravma = ''
        if self.PologovaTravmaNoCheckBox.isChecked():
            self.PologovaTravma = '7. Пологова травма:  ні.'
        else:
            self.PologovaTravmaJakaSame = self.PologovaTravmaJakaSameLineEdit.text(
            )
            self.PologovaTravmaJakaSame = self.PologovaTravmaJakaSame.strip()
            if self.PologovaTravmaJakaSame == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати з якими саме вадами народився новонароджений в пункті "VIII. Стан новонародженого та перебіг раннього неонатального періоду"!'
                )
            else:
                self.PologovaTravma = '7. Пологова травма:  так; якa саме: ' + self.PologovaTravmaJakaSame
        self.PologovaTravma = self.PologovaTravma.replace("'", "''")

        self.SDR = ''
        if self.SDRNoCheckBox.isChecked():
            self.SDR = '8. СДР: ні.'
        else:
            self.SDR = '8. СДР: так.'

        self.VnytrishnoytrobneInfikyvanna = ''
        if self.VnytrishnoytrobneInfikyvannaNoCheckBox.isChecked():
            self.VnytrishnoytrobneInfikyvanna = '9. Внутрішньоутробне інфікування: ні.'
        else:
            self.VnytrishnoytrobneInfikyvanna = '9. Внутрішньоутробне інфікування: так.'

        self.GemoragichniYskladnenna = ''
        if self.GemoragichniYskladnennaNoCheckBox.isChecked():
            self.GemoragichniYskladnenna = '10. Геморагічні ускладнення: ні.'
        else:
            self.GemoragichniYskladnenna = '10. Геморагічні ускладнення: так.'

        self.Anemia = ''
        if self.AnemiaNoCheckBox.isChecked():
            self.Anemia = '11. Aнемія: ні.'
        elif self.AnemiaIStypenaCheckBox.isChecked():
            self.Anemia = '11. Aнемія: І ступеня.'
        elif self.AnemiaIIStypenaCheckBox.isChecked():
            self.Anemia = '11. Aнемія: ІІ ступеня.'
        elif self.AnemiaIIIStypenaCheckBox.isChecked():
            self.Anemia = '11. Aнемія: ІІІ ступеня.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вказати підходящий варіант анемії в пункті "VIII. Стан новонародженого та перебіг раннього неонатального періоду"!'
            )

        # self.GiperBilirybinemia = ''
        # self.GiperBilirybinemiaRivenBilirybiny = self.GiperBilirybinemiaRivenBilirybinyLineEdit.text(
        # )
        # self.GiperBilirybinemiaRivenBilirybiny = self.GiperBilirybinemiaRivenBilirybiny.strip(
        # )
        # if self.GiperBilirybinemiaRivenBilirybiny == '':
        #     self.ErrorCount = self.ErrorCount + 1
        #     self.Error_mesage(
        #         'Необхідно вказати рівень білірубіну в пункті "VIII. Стан новонародженого та перебіг раннього неонатального періоду"!'
        #     )
        # else:
        #     if self.GiperBilirybinemiaNoCheckBox.isChecked():
        #         self.GiperBilirybinemia = '12. Гіпербілірубінемія: ні; рівень білірубіну: ' + self.GiperBilirybinemiaRivenBilirybiny + '.'
        #
        #     else:
        #         self.GiperBilirybinemia = '12. Гіпербілірубінемія: так; рівень білірубіну: ' + self.GiperBilirybinemiaRivenBilirybiny + '.'
        # self.GiperBilirybinemia = self.GiperBilirybinemia.replace("'", "''")

        self.GiperBilirybinemia = ''
        if self.GiperBilirybinemiaNoCheckBox.isChecked():
            self.GiperBilirybinemia = '12. Гіпербілірубінемія: ні;'
        else:
            self.GiperBilirybinemiaRivenBilirybiny = self.GiperBilirybinemiaRivenBilirybinyLineEdit.text(
            )
            self.GiperBilirybinemiaRivenBilirybiny = self.GiperBilirybinemiaRivenBilirybiny.strip(
            )
            if self.GiperBilirybinemiaRivenBilirybiny == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати рівень білірубіну в пункті "VIII. Стан новонародженого та перебіг раннього неонатального періоду"!'
                )
            else:
                self.GiperBilirybinemia = '12. Гіпербілірубінемія: так; рівень білірубіну: ' + self.GiperBilirybinemiaRivenBilirybiny + '.'
        self.GiperBilirybinemia = self.GiperBilirybinemia.replace("'", "''")

        self.Asfiksia = ''
        if self.AsfiksiaNoCheckBox.isChecked():
            self.Asfiksia = '13. Aсфіксія: ні.'
        elif self.AsfiksiaLegkaCheckBox.isChecked():
            self.Asfiksia = '13. Aсфіксія: легка.'
        elif self.AsfiksiaSerednaCheckBox.isChecked():
            self.Asfiksia = '13. Aсфіксія: середня.'
        elif self.AsfiksiaVajkaCheckBox.isChecked():
            self.Asfiksia = '13. Aсфіксія: важка.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вказати підходящий варіант асфіксії в пункті "VIII. Стан новонародженого та перебіг раннього неонатального періоду"!'
            )

        self.PoryshennaKardioRespiratornoiAdaptacii = ''
        if self.PoryshennaKardioRespiratornoiAdaptaciiNoCheckBox.isChecked():
            self.PoryshennaKardioRespiratornoiAdaptacii = '14. Порушення кардіо-респіраторної адаптації: ні.'
        else:
            self.PoryshennaKardioRespiratornoiAdaptacii = '14. Порушення кардіо-респіраторної адаптації: так.'

        self.VtrataMasuTila = '15. Втрата маси тіла: ні.'
        self.VtrataMasuTilaText = self.VtrataMasuTilaLineEdit.text()
        self.VtrataMasuTilaText = self.VtrataMasuTilaText.strip()
        if self.VtrataMasuTilaText != '':
            self.VtrataMasuTila = '15. Втрата маси тіла: ' + self.VtrataMasuTilaText
        self.VtrataMasuTila = self.VtrataMasuTila.replace("'", "''")

        self.VitaminKVvedeno = ''
        if self.VitaminKVvedenoNoCheckBox.isChecked():
            self.VitaminKVvedeno = '16. Вітамін К введено: ні.'
        else:
            self.VitaminKVvedenoText = self.VitaminKVvedenoTerminLineEdit.text(
            )
            self.VitaminKVvedenoText = self.VitaminKVvedenoText.strip()
            if self.VitaminKVvedenoText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати термін на якому було введено вітамін К в пункті "VIII. Стан новонародженого та перебіг раннього неонатального періоду"!'
                )
            else:
                self.VitaminKVvedeno = "16. Вітамін К введено: так; в терміні: " + self.VitaminKVvedenoText + '.'
        self.VitaminKVvedeno = self.VitaminKVvedeno.replace("'", "''")

        self.VupusanuiNa = ''
        self.VupusanuiNaText = self.VupusanuiNaLineEdit.text()
        self.VupusanuiNaText = self.VupusanuiNaText.strip()
        if self.VupusanuiNaText != '':
            self.VupusanuiNa = '17. Виписаний на: ' + self.VupusanuiNaText + ' добу.'
        else:
            self.ErrorCount = self.ErrorCount + 1
            self.Error_mesage(
                'Необхідно вказати добу на яку було виписано в пункті "VIII. Стан новонародженого та перебіг раннього неонатального періоду"!'
            )
        self.VupusanuiNa = self.VupusanuiNa.replace("'", "''")

        self.NeonatalnaSmert = ''
        if self.NeonatalnaSmertNoCheckBox.isChecked():
            self.NeonatalnaSmert = '18. Неонатальна смерть: ні.'
        else:
            self.NeonatalnaSmertText = self.NeonatalnaSmertTerminLineEdit.text(
            )
            self.NeonatalnaSmertText = self.NeonatalnaSmertText.strip()
            if self.NeonatalnaSmertText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати добу на яку відбулася неонатальна смерть в пункті "VIII. Стан новонародженого та перебіг раннього неонатального періоду"!'
                )
            else:
                self.NeonatalnaSmert = '18. Неонатальна смерть: так; на добу: ' + self.NeonatalnaSmertText
        self.NeonatalnaSmert = self.NeonatalnaSmert.replace("'", "''")

        self.PruchunaSmertiZaRezyltatomAytopsii = '19. Причина смерті за результатами аутопсії: неонатальної смерті не було.'
        if self.NeonatalnaSmertYesCheckBox.isChecked():
            self.PruchunaSmertiZaRezyltatomAytopsiiText = self.PruchunaSmertiZaRezyltatomAytopsiiLineEdit.text(
            )
            self.PruchunaSmertiZaRezyltatomAytopsiiText = self.PruchunaSmertiZaRezyltatomAytopsiiText.strip(
            )
            if self.PruchunaSmertiZaRezyltatomAytopsiiText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати причину смерті за результатами аутопсії в пункті "VIII. Стан новонародженого та перебіг раннього неонатального періоду"!'
                )
            else:
                self.PruchunaSmertiZaRezyltatomAytopsii = '19. Причина смерті за результатами аутопсії: ' + self.PruchunaSmertiZaRezyltatomAytopsiiText
        self.PruchunaSmertiZaRezyltatomAytopsii = self.PruchunaSmertiZaRezyltatomAytopsii.replace(
            "'", "''")

        self.PislapologovuiPeriod = '\nІX.Післяпологовий період.'

        self.PislapologovuiPerebig = ''
        if self.PislapologovuiPerebigNoCheckBox.isChecked():
            self.PislapologovuiPerebig = '1. Перебіг: нормальний.'
        else:
            self.PislapologovuiPerebig = '1. Перебіг: ускладнений.'

        self.ProfilaktukaTerapiaTEYPynktI = ''
        if self.ProfilaktukaTerapiaTEYPynktIXNoCheckBox.isChecked():
            self.ProfilaktukaTerapiaTEYPynktI = '2. Чи проводилась профілактика/терапія ТЕУ: ні.'
        else:
            self.ProfilaktukaTerapiaTEYPynktI = '2. Чи проводилась профілактика/терапія ТЕУ: так.'

        self.ElastuchnaKompressiaPynktIX = ''
        if self.ElastuchnaKompressiaPynktIXNoCheckBox.isChecked():
            self.ElastuchnaKompressiaPynktIX = '2.1. Еластична компресія: ні.'
        else:
            self.ElastuchnaKompressiaPynktIXText = self.ElastuchnaKompressiaPynktIXKlasLineEdit.text(
            )
            self.ElastuchnaKompressiaPynktIXText = self.ElastuchnaKompressiaPynktIXText.strip(
            )
            if self.ElastuchnaKompressiaPynktIXText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати клас еластичної компресії в пункті "ІХ.Післяпологовий період"!'
                )
            else:
                self.ElastuchnaKompressiaPynktIX = '2.1. Еластична компресія: так; клас ' + self.ElastuchnaKompressiaPynktIXText
        self.ElastuchnaKompressiaPynktIX = self.ElastuchnaKompressiaPynktIX.replace(
            "'", "''")
        # print(self.ElastuchnaKompressiaPynktIX)

        self.MedukamentoznaProfilaktukaPynktIX = ''
        if self.MedukamentoznaProfilaktukaPynktIXNoCheckBox.isChecked():
            self.MedukamentoznaProfilaktukaPynktIX = '2.2. Медикаментозна профілактика/терапія: ні.'
        else:
            self.MedukamentoznaProfilaktukaPynktIX = '2.2. Медикаментозна профілактика/терапія: так.'
        # print(self.MedukamentoznaProfilaktukaPynktIX)

        self.MedukamentoznaProfilaktukaPynktIXNazvaPreparaty = '2.2.1. Назва препарата: медикаментозна профілактика/терапія не проводилася.'
        if self.MedukamentoznaProfilaktukaPynktIXYesCheckBox.isChecked():
            self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyText = self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyLineEdit.text(
            )
            self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyText = self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyText.strip(
            )
            if self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати назву препарату в пункті "ІХ.Післяпологовий період"!'
                )
            else:
                self.MedukamentoznaProfilaktukaPynktIXNazvaPreparaty = '2.2.1. Назва препарата: ' + self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyText
        self.MedukamentoznaProfilaktukaPynktIXNazvaPreparaty = self.MedukamentoznaProfilaktukaPynktIXNazvaPreparaty.replace(
            "'", "''")
        # print(self.MedukamentoznaProfilaktukaPynktIXNazvaPreparaty)

        self.MedukamentoznaProfilaktukaPynktIXRegumPrujomy = '2.2.2. Режим прийому: медикаментозна профілактика/терапія не проводилася.'
        if self.MedukamentoznaProfilaktukaPynktIXYesCheckBox.isChecked():
            self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyText = self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyLineEdit.text(
            )
            self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyText = self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyText.strip(
            )
            if self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати режим прийому препарату в пункті "ІХ.Післяпологовий період"!'
                )
            else:
                self.MedukamentoznaProfilaktukaPynktIXRegumPrujomy = '2.2.2. Режим прийому: ' + self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyText
        self.MedukamentoznaProfilaktukaPynktIXRegumPrujomy = self.MedukamentoznaProfilaktukaPynktIXRegumPrujomy.replace(
            "'", "''")
        # print(self.MedukamentoznaProfilaktukaPynktIXRegumPrujomy)

        self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznacheno = '2.2.3. Термін коли призначено: медикаментозна профілактика/терапія не проводилася.'
        if self.MedukamentoznaProfilaktukaPynktIXYesCheckBox.isChecked():
            self.MedukamentoznaProfilaktukaPynktITerminKoluPruznachenoText = self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznachenoLineEdit.text(
            )
            self.MedukamentoznaProfilaktukaPynktITerminKoluPruznachenoText = self.MedukamentoznaProfilaktukaPynktITerminKoluPruznachenoText.strip(
            )
            if self.MedukamentoznaProfilaktukaPynktITerminKoluPruznachenoText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати термін коли призначено препарат в пункті "ІХ.Післяпологовий період"!'
                )
            else:
                self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznacheno = '2.2.3. Термін коли призначено: ' + self.MedukamentoznaProfilaktukaPynktITerminKoluPruznachenoText
        self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznacheno = self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznacheno.replace(
            "'", "''")
        # print(self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznacheno)

        self.HiryrgichneLikyvannaPynktIX = ''
        if self.HiryrgichneLikyvannaPynktIXNoCheckBox.isChecked():
            self.HiryrgichneLikyvannaPynktIX = '2.3. Хірургічне лікування: ні.'
        else:
            self.HiryrgichneLikyvannaPynktIX = '2.3. Хірургічне лікування: так.'
        # print(self.HiryrgichneLikyvannaPynktIX)

        self.HiryrgichneLikyvannaPynktIXTerminNazvaOperacii = '2.3.1. Назва операції та дата: хірургічне лікування не проводилося.'
        if self.HiryrgichneLikyvannaPynktIXYesCheckBox.isChecked():
            self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiText = self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiLineEdit.text(
            )
            self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiText = self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiText.strip(
            )
            if self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати назву та дату операції в пункті "ІХ.Післяпологовий період"!'
                )
            else:
                self.HiryrgichneLikyvannaPynktIXTerminNazvaOperacii = '2.3.1.Назва операції та дата: ' + self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiText
        self.HiryrgichneLikyvannaPynktIXTerminNazvaOperacii = self.HiryrgichneLikyvannaPynktIXTerminNazvaOperacii.replace(
            "'", "''")
        # print(self.HiryrgichneLikyvannaPynktIXTerminNazvaOperacii)

        self.TruvalistProvedenoiProfilaktuktPynktIX = '3. Тривалість проведеної профілактики: профілактика не проводилась.'
        self.TruvalistProvedenoiProfilaktuktPynktIXText = self.TruvalistProvedenoiProfilaktuktPynktIXLineEdit.text(
        )
        self.TruvalistProvedenoiProfilaktuktPynktIXText = self.TruvalistProvedenoiProfilaktuktPynktIXText.strip(
        )
        if self.TruvalistProvedenoiProfilaktuktPynktIXText != '':
            self.TruvalistProvedenoiProfilaktuktPynktIX = '3. Тривалість проведеної профілактики: ' + self.TruvalistProvedenoiProfilaktuktPynktIXText
        self.TruvalistProvedenoiProfilaktuktPynktIX = self.TruvalistProvedenoiProfilaktuktPynktIX.replace(
            "'", "''")
        # print(self.TruvalistProvedenoiProfilaktuktPynktIX)

        self.YskladnennaVidProfilaktukyPynktIX = ''
        if self.YskladnennaVidProfilaktukyPynktIXNoCheckBox.isChecked():
            self.YskladnennaVidProfilaktukyPynktIX = '4. Наявність ускладнень від проведеної профілактики: ні.'
        else:
            self.YskladnennaVidProfilaktukyPynktIXText = self.YskladnennaVidProfilaktukyPynktIXYskladnennaLineEdit.text(
            )
            self.YskladnennaVidProfilaktukyPynktIXText = self.YskladnennaVidProfilaktukyPynktIXText.strip(
            )
            if self.YskladnennaVidProfilaktukyPynktIXText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно ускладнення від проведеної профілактики в пункті "ІХ.Післяпологовий період"!'
                )
            else:
                self.YskladnennaVidProfilaktukyPynktIX = '4. Наявність ускладнень від проведеної профілактики: так; ускладнення: ' + self.YskladnennaVidProfilaktukyPynktIXText
        self.YskladnennaVidProfilaktukyPynktIX = self.YskladnennaVidProfilaktukyPynktIX.replace(
            "'", "''")
        # print(self.YskladnennaVidProfilaktukyPynktIX)

        self.TromboembolichniYskladnennaPynktIX = ''
        if self.TromboembolichniYskladnennaPynktIXNoCheckBox.isChecked():
            self.TromboembolichniYskladnennaPynktIX = '5. Тромбоемболічні ускладнення: ні.'
        else:
            self.TromboembolichniYskladnennaPynktIX = '5. Тромбоемболічні ускладнення: так.'
        # print(self.TromboembolichniYskladnennaPynktIX)

        self.TromboembolichniYskladnennaPynktIXVudTey = '5.1. Вид ТЕУ: тромбоемболічні ускладнення відсутні.'
        if self.TromboembolichniYskladnennaPynktIXYesCheckBox.isChecked():
            self.TromboembolichniYskladnennaPynktIXVudTeyText = self.TromboembolichniYskladnennaPynktIXVudTeyLineEdit.text(
            )
            self.TromboembolichniYskladnennaPynktIXVudTeyText = self.TromboembolichniYskladnennaPynktIXVudTeyText.strip(
            )
            if self.TromboembolichniYskladnennaPynktIXVudTeyText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати вид ТЕУ в пункті "ІХ.Післяпологовий період"!'
                )
            else:
                self.TromboembolichniYskladnennaPynktIXVudTey = '5.1. Вид ТЕУ: ' + self.TromboembolichniYskladnennaPynktIXVudTeyText
        self.TromboembolichniYskladnennaPynktIXVudTey = self.TromboembolichniYskladnennaPynktIXVudTey.replace(
            "'", "''")
        # print(self.TromboembolichniYskladnennaPynktIXVudTey)

        self.TromboembolichniYskladnennaPynktIXTerminVunuknenna = '5.2. Термін винекнення: тромбоемболічні ускладнення відсутні.'
        if self.TromboembolichniYskladnennaPynktIXYesCheckBox.isChecked():
            self.TromboembolichniYskladnennaPynktIXTerminVunuknennaText = self.TromboembolichniYskladnennaPynktIXTerminVunuknennaLineEdit.text(
            )
            self.TromboembolichniYskladnennaPynktIXTerminVunuknennaText = self.TromboembolichniYskladnennaPynktIXTerminVunuknennaText.strip(
            )
            if self.TromboembolichniYskladnennaPynktIXTerminVunuknennaText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати термін виникнення ТЕУ в пункті "ІХ.Післяпологовий період"!'
                )
            else:
                self.TromboembolichniYskladnennaPynktIXTerminVunuknenna = '5.2. Термін винекнення: ' + self.TromboembolichniYskladnennaPynktIXTerminVunuknennaText
        self.TromboembolichniYskladnennaPynktIXTerminVunuknenna = self.TromboembolichniYskladnennaPynktIXTerminVunuknenna.replace(
            "'", "''")
        # print(self.TromboembolichniYskladnennaPynktIXTerminVunuknenna)

        self.TromboembolichniYskladnennaPynktIXTerapiaTEY = '5.3. Терапія ТЕУ: тромбоемболічні ускладнення відсутні.'
        if self.TromboembolichniYskladnennaPynktIXYesCheckBox.isChecked():
            self.TromboembolichniYskladnennaPynktIXTerapiaTEYText = self.TromboembolichniYskladnennaPynktIXTerapiaTEYLineEdit.text(
            )
            self.TromboembolichniYskladnennaPynktIXTerapiaTEYText = self.TromboembolichniYskladnennaPynktIXTerapiaTEYText.strip(
            )
            if self.TromboembolichniYskladnennaPynktIXTerapiaTEYText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати терапію ТЕУ в пункті "ІХ.Післяпологовий період"!'
                )
            else:
                self.TromboembolichniYskladnennaPynktIXTerapiaTEY = '5.3. Терапія ТЕУ: ' + self.TromboembolichniYskladnennaPynktIXTerapiaTEYText
        self.TromboembolichniYskladnennaPynktIXTerapiaTEY = self.TromboembolichniYskladnennaPynktIXTerapiaTEY.replace(
            "'", "''")
        # print(self.TromboembolichniYskladnennaPynktIXTerapiaTEY)

        self.MastutPynktIX = ''
        if self.MastutPynktIXNoCheckBox.isChecked():
            self.MastutPynktIX = '6. Мастит: ні.'
        else:
            self.MastutPynktIX = '6. Мастит: так.'
        # print(self.MastutPynktIX)

        self.SubinvolyciaMatkuPynktIX = ''
        if self.SubinvolyciaMatkuPynktIXNoCheckBox.isChecked():
            self.SubinvolyciaMatkuPynktIX = '7. Субінволюція матки: ні.'
        else:
            self.SubinvolyciaMatkuPynktIX = '7. Субінволюція матки: так.'
        # print(self.SubinvolyciaMatkuPynktIX)

        self.EndometrutPynktIX = ''
        if self.EndometrutPynktIXNoCheckBox.isChecked():
            self.EndometrutPynktIX = '8. Ендометрит: ні.'
        else:
            self.EndometrutPynktIX = '8. Ендометрит: так.'
        # print(self.EndometrutPynktIX)

        self.PiznaPologovaKrovotechaPynktIX = ''
        if self.PiznaPologovaKrovotechaPynktIXNoCheckBox.isChecked():
            self.PiznaPologovaKrovotechaPynktIX = '9. Пізня післяпологова кровотеча: ні.'
        else:
            self.PiznaPologovaKrovotechaPynktIX = '9. Пізня післяпологова кровотеча: так.'
        # print(self.PiznaPologovaKrovotechaPynktIX)

        self.SepsusPynktIX = ''
        if self.SepsusPynktIXNoCheckBox.isChecked():
            self.SepsusPynktIX = '10. Сепсис: ні.'
        else:
            self.SepsusPynktIX = '10. Сепсис: так.'
        # print(self.SepsusPynktIX)

        self.RoshodgennaShvivPynktIX = ''
        if self.RoshodgennaShvivPynktIXNoCheckBox.isChecked():
            self.RoshodgennaShvivPynktIX = '11. Розходження швів: ні.'
        else:
            self.RoshodgennaShvivPynktIX = '11. Розходження швів: так.'
        # print(self.RoshodgennaShvivPynktIX)

        self.InshiPynktIX = '12. Інші: відсутні.'
        self.InshiPynktIXText = self.InshiPynktIXLineEdit.text()
        self.InshiPynktIXText = self.InshiPynktIXText.strip()
        if self.InshiPynktIXText != '':
            self.InshiPynktIX = '12. Інші: ' + self.InshiPynktIXText
        self.InshiPynktIX = self.InshiPynktIX.replace("'", "''")
        # print(self.InshiPynktIX)

        self.HirVtyrchannaVPershi6TugnivPynktIX = ''
        if self.HirVtyrchannaVPershi6TugnivPynktIXNoCheckBox.isChecked():
            self.HirVtyrchannaVPershi6TugnivPynktIX = '13. Хірургічні втручання в перші 6 тиж після пологів: ні.'
        else:
            self.HirVtyrchannaVPershi6TugnivPynktIX = '13. Хірургічні втручання в перші 6 тиж після пологів: так.'
        # print(self.HirVtyrchannaVPershi6TugnivPynktIX)

        self.VupuskaDodomyPynktIX = ''
        if self.VupuskaDodomyPynktIXNoCheckBox.isChecked():
            self.VupuskaDodomyPynktIX = '14. Виписка додому: ні.'
        else:
            self.VupuskaDodomyPynktIXText = self.VupuskaDodomyPynktIXDobyLineEdit.text(
            )
            self.VupuskaDodomyPynktIXText = self.VupuskaDodomyPynktIXText.strip(
            )
            if self.VupuskaDodomyPynktIXText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати термін виписки додому в пункті "ІХ.Післяпологовий період"!'
                )
            else:
                self.VupuskaDodomyPynktIX = '14. Виписка додому: так; на ' + self.VupuskaDodomyPynktIXText + " добу."
        # print(self.VupuskaDodomyPynktIX)

        self.PerevedennaVInshuiStacionarPynktIX = ''
        if self.PerevedennaVInshuiStacionarPynktIXNoCheckBox.isChecked():
            self.PerevedennaVInshuiStacionarPynktIX = '15. Переведена в інший стаціонар: ні.'
        else:
            self.PerevedennaVInshuiStacionarPynktIXText = self.PerevedennaVInshuiStacionarPynktIXDobyLineEdit.text(
            )
            self.PerevedennaVInshuiStacionarPynktIXText = self.PerevedennaVInshuiStacionarPynktIXText.strip(
            )
            if self.PerevedennaVInshuiStacionarPynktIXText == '':
                self.ErrorCount = self.ErrorCount + 1
                self.Error_mesage(
                    'Необхідно вказати термін переведення в інший стаціонар в пункті "ІХ.Післяпологовий період"!'
                )
            else:
                self.PerevedennaVInshuiStacionarPynktIX = '15. Переведена в інший стаціонар: так; на ' + self.PerevedennaVInshuiStacionarPynktIXText + " добу."
        # print(self.PerevedennaVInshuiStacionarPynktIX)

        self.ChangeDateRow = 'Дата та час заповнення реєстраційної карти: ' + self.ChangeDate.text(
        )
        # print(self.ChangeDateRow)

        self.WhoChangeRow = 'Заповняв: ' + self.WhoChange.text()
        self.WhoChangeRow = self.WhoChangeRow.replace("'", "''")
        # print(self.WhoChangeRow)

        # print("Kilkist pomulok: " + str(self.ErrorCount))
        if self.ErrorCount == 0:
            self.Error_mesage('Реєстраційну картку заповнено повністю!')

            try:
                cnx = self.ConnectToPregnantBD()
            except mysql.connector.DatabaseError as e:
                self.Info_mesage(str(e))

            try:
                cursor = cnx.cursor()
            except mysql.connector.DatabaseError as e:
                self.Info_mesage(str(e))
                cnx.close()

            query_to_insert = ("""
                    INSERT INTO Registry
                        (

                        PasportniDaniTitle,
                        PasportniDani,
                        HistoryNumber,
                        Age,
                        Address,
                        Proffesional,
                        Disability,
                        ReceduvyTromboemboliiTitle,
                        ReceduvyTromboembolii,
                        TromboemboliiAndEstrogens,
                        TromboemboliaSprovokovana,
                        SimeinuiAnamnezTromboembolii,
                        VstanovlennaTrombofilia,
                        SypytniZahvoryvanna,
                        OldMore35,
                        Ogirinna,
                        VagitnistMore3,
                        Kyrinna,
                        VelykiVarikozniVenu,
                        ProvedennaProfTEYdpVagitnosti,
                        ElastychnaKompresia,
                        MedukamentoznaProfilaktuka,
                        MedukamentoznaProfilaktukaNazvaPreperaty,
                        MedukamentoznaProfilaktukaRegymPrujomy,
                        HiryrgichneLikyvanna,
                        TryvalistProvedennoiProfilaktyky,
                        YskladneenaVidProfilaktyku,
                        AkysherskiiAnamnez,
                        DanaVagitnist,
                        DanaVagitnistZaRahynkom,
                        DaniPologuZaRahynkom,
                        PoperedniPologuZavershulus,
                        PoperedniPologu,
                        NayavnistGuvyhDitey,
                        VPerebigDannoiVagitnosti,
                        Vagitnist,
                        NaOblikyVGinochiiKonsyltacii,
                        ZagrozaPereruvannaVagitnosti,
                        ZagrozaPeredchasnuhPologiv,
                        ZagrozaPeredchasnuhPologivP4_1,
                        GestozIPolovunuVagitnosti,
                        InshiPruchynyZnevodnenna,
                        GestozIIPolovunuVagitnosti,
                        GestozIIPolovunuVagitnostiVTermini,
                        VunuknennaTEY,
                        VudTEY,
                        TEYTerminVagitnosti,
                        Bagatovodda,
                        BagatovoddaDiagnostovanoVTerminVagitnosti,
                        MaloVodda,
                        MaloVoddaDiagnostovanoVTerminVagitnosti,
                        DustressPloda,
                        ZatrumkaRozvutkyPloda,
                        NajavnistSustemnoiInfekcii,
                        PatologiaPlacentu,
                        PatologiaLocalizaciiPlacentu,
                        PeredchasneVadsharyvannaPlacentu,
                        HiryrgichniVtyrchannaPidChasVagitnosti,
                        TruvalaImmobilizacia,
                        ZavershennaDannoiVagitnosti,
                        ProvedennaProfilaktukuTerapiiTEYPidChasVagitnosti,
                        PokazuDlaProvedennaProfilaktuky,
                        ElastychnaKompresiaPynktVI,
                        MedukamentoznaProfilaktukaPynktVI,
                        MedukamentoznaProfilaktukaPynktVINazvaPreperaty,
                        MedukamentoznaProfilaktukaPynktVIRegymPrujomy,
                        MedukamentoznaProfilaktukaPynktVITerminKoluPruznacheno,
                        HiryrgichneLikyvannaPynktVI,
                        TryvalistProvedennoiProfilaktykyPynktVI,
                        YskladneenaVidProfilaktykuPynktVI,
                        TerapiyVidminenoZaGodDoPologivPynktVI,
                        PerebigDanuhPologiv,
                        PologuVaginalni,
                        PologuAbdominalni,
                        PokazannaDlaAbdominalnogoRozrodjenna,
                        PoryshennaPologovoiDialnosti,
                        KorekciaAnomaliiPologovoiDialnosti,
                        VuluvNavkoloplodovuhVod,
                        DustressPlodaVPologah,
                        GipotonichnaKrovotecha,
                        AnomaliiPrukriplennaPlacentu,
                        DefektPoslidy,
                        DefektObolonok,
                        AnomaliiPrukriplennaPypovunu,
                        OperatuvnaDopomoga,
                        RozruvuPologovuhShlahiv,
                        EpizoAboPerineotomia,
                        KrovovtrataVPologah,
                        TruvalistPologiv,
                        StanNovonarodgennogoTaNeoPeriodTitleLable,
                        Naroduvsa,
                        PruchunaMertvonarodgenna,
                        ZrilistNovonarodgennogo,
                        ParametruNovonarodgennogo,
                        GipotrofiaPloda,
                        OcinkaZaShkaloyApgar,
                        NovonarodjenuiZVadamuRozvutky,
                        PologovaTravma,
                        SDR,
                        VnytrishnoytrobneInfikyvanna,
                        GemoragichniYskladnenna,
                        Anemia,
                        GiperBilirybinemia,
                        Asfiksia,
                        PoryshennaKardioRespiratornoiAdaptacii,
                        VtrataMasuTila,
                        VitaminKVvedeno,
                        VupusanuiNa,
                        NeonatalnaSmert,
                        PruchunaSmertiZaRezyltatomAytopsii,
                        PislapologovuiPeriod,
                        PislapologovuiPerebig,
                        ProfilaktukaTerapiaTEYPynktI,
                        ElastuchnaKompressiaPynktIX,
                        MedukamentoznaProfilaktukaPynktIX,
                        MedukamentoznaProfilaktukaPynktIXNazvaPreparaty,
                        MedukamentoznaProfilaktukaPynktIXRegumPrujomy,
                        MedukamentoznaProfilaktukaPynktIXTerminKoluPruznacheno,
                        HiryrgichneLikyvannaPynktIX,
                        HiryrgichneLikyvannaPynktIXTerminNazvaOperacii,
                        TruvalistProvedenoiProfilaktuktPynktIX,
                        YskladnennaVidProfilaktukyPynktIX,
                        TromboembolichniYskladnennaPynktIX,
                        TromboembolichniYskladnennaPynktIXVudTey,
                        TromboembolichniYskladnennaPynktIXTerminVunuknenna,
                        TromboembolichniYskladnennaPynktIXTerapiaTEY,
                        MastutPynktIX,
                        SubinvolyciaMatkuPynktIX,
                        EndometrutPynktIX,
                        PiznaPologovaKrovotechaPynktIX,
                        SepsusPynktIX,
                        RoshodgennaShvivPynktIX,
                        InshiPynktIX,
                        HirVtyrchannaVPershi6TugnivPynktIX,
                        VupuskaDodomyPynktIX,
                        PerevedennaVInshuiStacionarPynktIX,
                        ChangeDateRow,
                        WhoChangeRow)
                        VALUES
                        (
                        '""" + self.PasportniDaniTitle + """',
                        '""" + self.PasportniDani + """',
                        '""" + self.HistoryNumber + """',
                        '""" + self.Age + """',
                        '""" + self.Address + """',
                        '""" + self.Proffesional + """',
                        '""" + self.Disability + """',
                        '""" + self.ReceduvyTromboemboliiTitle + """',
                        '""" + self.ReceduvyTromboembolii + """',
                        '""" + self.TromboemboliiAndEstrogens + """',
                        '""" + self.TromboemboliaSprovokovana + """',
                        '""" + self.SimeinuiAnamnezTromboembolii + """',
                        '""" + self.VstanovlennaTrombofilia + """',
                        '""" + self.SypytniZahvoryvanna + """',
                        '""" + self.OldMore35 + """',
                        '""" + self.Ogirinna + """',
                        '""" + self.VagitnistMore3 + """',
                        '""" + self.Kyrinna + """',
                        '""" + self.VelykiVarikozniVenu + """',
                        '""" + self.ProvedennaProfTEYdpVagitnosti + """',
                        '""" + self.ElastychnaKompresia + """',
                        '""" + self.MedukamentoznaProfilaktuka + """',
                        '""" + self.MedukamentoznaProfilaktukaNazvaPreperaty +
                               """',
                        '""" + self.MedukamentoznaProfilaktukaRegymPrujomy +
                               """',
                        '""" + self.HiryrgichneLikyvanna + """',
                        '""" + self.TryvalistProvedennoiProfilaktyky + """',
                        '""" + self.YskladneenaVidProfilaktyku + """',
                        '""" + self.AkysherskiiAnamnez + """',
                        '""" + self.DanaVagitnist + """',
                        '""" + self.DanaVagitnistZaRahynkom + """',
                        '""" + self.DaniPologuZaRahynkom + """',
                        '""" + self.PoperedniPologuZavershulus + """',
                        '""" + self.PoperedniPologu + """',
                        '""" + self.NayavnistGuvyhDitey + """',
                        '""" + self.VPerebigDannoiVagitnosti + """',
                        '""" + self.Vagitnist + """',
                        '""" + self.NaOblikyVGinochiiKonsyltacii + """',
                        '""" + self.ZagrozaPereruvannaVagitnosti + """',
                        '""" + self.ZagrozaPeredchasnuhPologiv + """',
                        '""" + self.ZagrozaPeredchasnuhPologivP4_1 + """',
                        '""" + self.GestozIPolovunuVagitnosti + """',
                        '""" + self.InshiPruchynyZnevodnenna + """',
                        '""" + self.GestozIIPolovunuVagitnosti + """',
                        '""" + self.GestozIIPolovunuVagitnostiVTermini + """',
                        '""" + self.VunuknennaTEY + """',
                        '""" + self.VudTEY + """',
                        '""" + self.TEYTerminVagitnosti + """',
                        '""" + self.Bagatovodda + """',
                        '""" + self.BagatovoddaDiagnostovanoVTerminVagitnosti +
                               """',
                        '""" + self.MaloVodda + """',
                        '""" + self.MaloVoddaDiagnostovanoVTerminVagitnosti +
                               """',
                        '""" + self.DustressPloda + """',
                        '""" + self.ZatrumkaRozvutkyPloda + """',
                        '""" + self.NajavnistSustemnoiInfekcii + """',
                        '""" + self.PatologiaPlacentu + """',
                        '""" + self.PatologiaLocalizaciiPlacentu + """',
                        '""" + self.PeredchasneVadsharyvannaPlacentu + """',
                        '""" + self.HiryrgichniVtyrchannaPidChasVagitnosti +
                               """',
                        '""" + self.TruvalaImmobilizacia + """',
                        '""" + self.ZavershennaDannoiVagitnosti + """',
                        '""" + self.
                               ProvedennaProfilaktukuTerapiiTEYPidChasVagitnosti
                               + """',
                        '""" + self.PokazuDlaProvedennaProfilaktuky + """',
                        '""" + self.ElastychnaKompresiaPynktVI + """',
                        '""" + self.MedukamentoznaProfilaktukaPynktVI + """',
                        '""" + self.
                               MedukamentoznaProfilaktukaPynktVINazvaPreperaty
                               + """',
                        '""" + self.
                               MedukamentoznaProfilaktukaPynktVIRegymPrujomy +
                               """',
                        '""" + self.
                               MedukamentoznaProfilaktukaPynktVITerminKoluPruznacheno
                               + """',
                        '""" + self.HiryrgichneLikyvannaPynktVI + """',
                        '""" + self.TryvalistProvedennoiProfilaktykyPynktVI +
                               """',
                        '""" + self.YskladneenaVidProfilaktykuPynktVI + """',
                        '""" + self.TerapiyVidminenoZaGodDoPologivPynktVI +
                               """',
                        '""" + self.PerebigDanuhPologiv + """',
                        '""" + self.PologuVaginalni + """',
                        '""" + self.PologuAbdominalni + """',
                        '""" + self.PokazannaDlaAbdominalnogoRozrodjenna +
                               """',
                        '""" + self.PoryshennaPologovoiDialnosti + """',
                        '""" + self.KorekciaAnomaliiPologovoiDialnosti + """',
                        '""" + self.VuluvNavkoloplodovuhVod + """',
                        '""" + self.DustressPlodaVPologah + """',
                        '""" + self.GipotonichnaKrovotecha + """',
                        '""" + self.AnomaliiPrukriplennaPlacentu + """',
                        '""" + self.DefektPoslidy + """',
                        '""" + self.DefektObolonok + """',
                        '""" + self.AnomaliiPrukriplennaPypovunu + """',
                        '""" + self.OperatuvnaDopomoga + """',
                        '""" + self.RozruvuPologovuhShlahiv + """',
                        '""" + self.EpizoAboPerineotomia + """',
                        '""" + self.KrovovtrataVPologah + """',
                        '""" + self.TruvalistPologiv + """',
                        '""" + self.StanNovonarodgennogoTaNeoPeriodTitleLable +
                               """',
                        '""" + self.Naroduvsa + """',
                        '""" + self.PruchunaMertvonarodgenna + """',
                        '""" + self.ZrilistNovonarodgennogo + """',
                        '""" + self.ParametruNovonarodgennogo + """',
                        '""" + self.GipotrofiaPloda + """',
                        '""" + self.OcinkaZaShkaloyApgar + """',
                        '""" + self.NovonarodjenuiZVadamuRozvutky + """',
                        '""" + self.PologovaTravma + """',
                        '""" + self.SDR + """',
                        '""" + self.VnytrishnoytrobneInfikyvanna + """',
                        '""" + self.GemoragichniYskladnenna + """',
                        '""" + self.Anemia + """',
                        '""" + self.GiperBilirybinemia + """',
                        '""" + self.Asfiksia + """',
                        '""" + self.PoryshennaKardioRespiratornoiAdaptacii +
                               """',
                        '""" + self.VtrataMasuTila + """',
                        '""" + self.VitaminKVvedeno + """',
                        '""" + self.VupusanuiNa + """',
                        '""" + self.NeonatalnaSmert + """',
                        '""" + self.PruchunaSmertiZaRezyltatomAytopsii + """',
                        '""" + self.PislapologovuiPeriod + """',
                        '""" + self.PislapologovuiPerebig + """',
                        '""" + self.ProfilaktukaTerapiaTEYPynktI + """',
                        '""" + self.ElastuchnaKompressiaPynktIX + """',
                        '""" + self.MedukamentoznaProfilaktukaPynktIX + """',
                        '""" + self.
                               MedukamentoznaProfilaktukaPynktIXNazvaPreparaty
                               + """',
                        '""" + self.
                               MedukamentoznaProfilaktukaPynktIXRegumPrujomy +
                               """',
                        '""" + self.
                               MedukamentoznaProfilaktukaPynktIXTerminKoluPruznacheno
                               + """',
                        '""" + self.HiryrgichneLikyvannaPynktIX + """',
                        '""" + self.
                               HiryrgichneLikyvannaPynktIXTerminNazvaOperacii +
                               """',
                        '""" + self.TruvalistProvedenoiProfilaktuktPynktIX +
                               """',
                        '""" + self.YskladnennaVidProfilaktukyPynktIX + """',
                        '""" + self.TromboembolichniYskladnennaPynktIX + """',
                        '""" + self.TromboembolichniYskladnennaPynktIXVudTey +
                               """',
                        '""" + self.
                               TromboembolichniYskladnennaPynktIXTerminVunuknenna
                               + """',
                        '""" + self.TromboembolichniYskladnennaPynktIXTerapiaTEY
                               + """',
                        '""" + self.MastutPynktIX + """',
                        '""" + self.SubinvolyciaMatkuPynktIX + """',
                        '""" + self.EndometrutPynktIX + """',
                        '""" + self.PiznaPologovaKrovotechaPynktIX + """',
                        '""" + self.SepsusPynktIX + """',
                        '""" + self.RoshodgennaShvivPynktIX + """',
                        '""" + self.InshiPynktIX + """',
                        '""" + self.HirVtyrchannaVPershi6TugnivPynktIX + """',
                        '""" + self.VupuskaDodomyPynktIX + """',
                        '""" + self.PerevedennaVInshuiStacionarPynktIX + """',
                        '""" + self.ChangeDateRow + """',
                        '""" + self.WhoChangeRow + """'
                        )
            """)
            try:
                cursor.execute(query_to_insert)
            except mysql.connector.DatabaseError as e:
                self.Info_mesage(str(e))
                cursor.close()
                cnx.close()
            cnx.commit()
            cursor.close()
            cnx.close()
            self.Info_mesage('Дані успішно внесені в БД!')

            self.ResetToDefaultValue()

            # Сброс полей на стартовые позиции при правильно заполнении всех полей self.ErrorCount = 0

    def ResetToDefaultValue(self):
        self.FirstNameLineEdit.setText('')
        self.LastNameLineEdit.setText('')
        self.FatherNameLineEdit.setText('')
        self.HistoryNumberLineEdit.setText('')
        self.AgeLineEdit.setText('')
        self.AddressLineEdit.setText('')

        self.ProffesionalDontWorkCheckBox.setEnabled(1)
        self.ProffesionalDontWorkCheckBox.setChecked(0)
        self.ProffesionalStadyCheckBox.setEnabled(1)
        self.ProffesionalStadyCheckBox.setChecked(0)
        self.ProffesionalWhiteCollarWorkerCheckBox.setEnabled(1)
        self.ProffesionalWhiteCollarWorkerCheckBox.setChecked(0)
        self.ProffesionalEmployeeCheckBox.setEnabled(1)
        self.ProffesionalEmployeeCheckBox.setChecked(0)

        self.DisabilityNoneCheckBox.setChecked(1)
        self.DisabilityNoneCheckBox.setEnabled(1)
        self.DisabilityILevelCheckBox.setChecked(0)
        self.DisabilityILevelCheckBox.setEnabled(0)
        self.DisabilityIILevelCheckBox.setChecked(0)
        self.DisabilityIILevelCheckBox.setEnabled(0)
        self.DisabilityIIILevelCheckBox.setChecked(0)
        self.DisabilityIIILevelCheckBox.setEnabled(0)

        self.ReceduvyTromboemboliiNoCheckBox.setEnabled(1)
        self.ReceduvyTromboemboliiNoCheckBox.setChecked(1)
        self.ReceduvyTromboemboliiYesCheckBox.setChecked(0)
        self.ReceduvyTromboemboliiYesCheckBox.setEnabled(0)

        self.TromboemboliiAndEstrogensNoCheckBox.setChecked(1)
        self.TromboemboliiAndEstrogensNoCheckBox.setEnabled(1)
        self.TromboemboliiAndEstrogensYesCheckBox.setChecked(0)
        self.TromboemboliiAndEstrogensYesCheckBox.setEnabled(0)

        self.TromboemboliaSprovokovanaNoCheckBox.setEnabled(1)
        self.TromboemboliaSprovokovanaNoCheckBox.setChecked(1)
        self.TromboemboliaSprovokovanaYesCheckBox.setEnabled(0)
        self.TromboemboliaSprovokovanaYesCheckBox.setChecked(0)

        self.SimeinuiAnamnezTromboemboliiNoCheckBox.setChecked(1)
        self.SimeinuiAnamnezTromboemboliiNoCheckBox.setEnabled(1)
        self.SimeinuiAnamnezTromboemboliiYesCheckBox.setEnabled(0)
        self.SimeinuiAnamnezTromboemboliiYesCheckBox.setChecked(0)

        self.VstanovlennaTrombofiliaNoCheckBox.setChecked(1)
        self.VstanovlennaTrombofiliaNoCheckBox.setEnabled(1)
        self.VstanovlennaTrombofiliaYesCheckBox.setEnabled(0)
        self.VstanovlennaTrombofiliaYesCheckBox.setChecked(0)

        # self.SypytniZahvoryvannaNoCheckBox.setChecked(1)
        # self.SypytniZahvoryvannaNoCheckBox.setEnabled(1)
        # self.SypytniZahvoryvannaYesCheckBox.setEnabled(0)
        self.SypytniZahvoryvannaYesCheckBox.setChecked(0)
        # self.SypytniZahvoryvannaLabel.setFixedWidth(400)
        # self.SypytniZahvoryvannaYesCheckBox.setFixedWidth(100)
        # self.SypytniSercevoSydunniCheckBox.hide()
        # self.SypytniSercevoSydunniCheckBox.setChecked(0)
        # self.SypytniBronhoLegeneviCheckBox.hide()
        # self.SypytniBronhoLegeneviCheckBox.setChecked(0)
        # self.SypytniSCHVCheckBox.hide()
        # self.SypytniSCHVCheckBox.setChecked(0)
        # self.SypytniRAKCheckBox.hide()
        # self.SypytniRAKCheckBox.setChecked(0)
        # self.SypytniNefrotuchnuiSundromCheckBox.hide()
        # self.SypytniNefrotuchnuiSundromCheckBox.setChecked(0)
        # self.SypytniSerpovudnoKlitynnaAnemiaCheckBox.hide()
        # self.SypytniSerpovudnoKlitynnaAnemiaCheckBox.setChecked(0)
        # self.SypytniVnytrishnoVenneVvedennaMedukamentivCheckBox.hide()
        # self.SypytniVnytrishnoVenneVvedennaMedukamentivCheckBox.setChecked(0)
        # self.SypytniOtherLineEdit.hide()
        # self.SypytniOtherLineEdit.setText('')
        # self.SypytniOtherCheckBox.hide()
        # self.SypytniOtherCheckBox.setChecked(0)

        self.OldMore35YesCheckBox.setChecked(0)
        self.OgirinnaYesCheckBox.setChecked(0)
        self.VagitnistMore3YesCheckBox.setChecked(0)
        self.KyrinnaYesCheckBox.setChecked(0)
        self.VelykiVarikozniVenuYesCheckBox.setChecked(0)
        self.ProvedennaProfTEYdpVagitnostiLabelYesCheckBox.setChecked(0)
        self.ProvedennaProfTEYdpVagitnostiLabelYesCheckBox.setEnabled(0)

        self.DanaVagitnisPryrodnaCheckBox.setEnabled(1)
        self.DanaVagitnisPryrodnaCheckBox.setChecked(1)
        self.DanaVagitnisIndykovanaCheckBox.setChecked(0)
        self.DanaVagitnisIndykovanaCheckBox.setEnabled(0)
        self.DanaVagitnisEKZCheckBox.setChecked(0)
        self.DanaVagitnisEKZCheckBox.setEnabled(0)

        self.DanaVagitnistZaRahynkomLineEdit.setText('')

        self.DaniPologuZaRahynkomLineEdit.setText('')

        self.PoperedniPologuZavershulusPologamuCheckBox.setEnabled(1)
        self.PoperedniPologuZavershulusPologamuCheckBox.setChecked(1)
        self.PoperedniPologuZavershulusAbortomSamovilnumCheckBox.setChecked(0)
        self.PoperedniPologuZavershulusAbortomSamovilnumCheckBox.setEnabled(0)
        self.PoperedniPologuZavershulusAbortomShtychnumCheckBox.setChecked(0)
        self.PoperedniPologuZavershulusAbortomShtychnumCheckBox.setEnabled(0)

        self.PoperedniPologuFiziologichniCheckBox.setChecked(1)
        self.PoperedniPologuFiziologichniCheckBox.setEnabled(1)
        self.PoperedniPologuPatologichniCheckBox.setChecked(0)
        self.PoperedniPologuPatologichniCheckBox.setEnabled(0)
        self.PoperedniPologuYskladneniCheckBox.setChecked(0)
        self.PoperedniPologuYskladneniCheckBox.setEnabled(0)
        self.PoperedniPologuYskladneniLineEdit.hide()

        self.NayavnistGuvyhDiteyYesCheckBox.setChecked(0)
        self.VagitnistBagatodnoplidnaCheckBox.setChecked(0)
        self.NaOblikyVGinochiiKonsyltaciiLineEdit.setText('')
        self.ZagrozaPereruvannaVagitnostiYesCheckBox.setChecked(0)
        self.ZagrozaPeredchasnuhPologivYesCheckBox.setChecked(0)
        self.GestozIPolovunuVagitnostiYesCheckBox.setChecked(0)

        self.InshiPruchynyZnevodnennaYesCheckBox.setChecked(0)
        self.InshiPruchynyZnevodnennaYesCheckBox.setEnabled(0)
        self.InshiPruchynyZnevodnennaNoCheckBox.setChecked(1)
        self.InshiPruchynyZnevodnennaNoCheckBox.setEnabled(1)
        self.InshiPruchynyZnevodnennaVarVLineEdit.hide()
        self.InshiPruchynyZnevodnennaVarVCheckBox.setChecked(0)
        self.InshiPruchynyZnevodnennaVarVCheckBox.setEnabled(0)

        self.GestozIIPolovunuVagitnostiNoCheckBox.setChecked(1)
        self.GestozIIPolovunuVagitnostiNoCheckBox.setEnabled(1)
        self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.setChecked(
            0)
        self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.setEnabled(
            0)
        self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.setChecked(
            0)
        self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.setEnabled(
            0)
        self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.setChecked(
            0)
        self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.setEnabled(
            0)

        self.VunuknennaTEYYesCheckBox.setChecked(0)

        self.BagatovoddaNoCheckBox.setChecked(1)
        self.BagatovoddaNoCheckBox.setEnabled(1)
        self.BagatovoddaPomirneCheckBox.setEnabled(0)
        self.BagatovoddaPomirneCheckBox.setChecked(0)
        self.BagatovoddaVurageneCheckBox.setEnabled(0)
        self.BagatovoddaVurageneCheckBox.setChecked(0)

        self.MaloVoddaNoCheckBox.setChecked(1)
        self.MaloVoddaNoCheckBox.setEnabled(1)
        self.MaloVoddaPomirneCheckBox.setEnabled(0)
        self.MaloVoddaPomirneCheckBox.setChecked(0)
        self.MaloVoddaVurageneCheckBox.setEnabled(0)
        self.MaloVoddaVurageneCheckBox.setChecked(0)

        self.DustressPlodaNoCheckBox.setChecked(1)
        self.DustressPlodaNoCheckBox.setEnabled(1)
        self.DustressPlodaVKompensaciiCheckBox.setChecked(0)
        self.DustressPlodaVSubKompensaciiCheckBox.setChecked(0)
        self.DustressPlodaVSubKompensaciiCheckBox.setEnabled(0)
        self.DustressPlodaVDekompensaciiCheckBox.setChecked(0)
        self.DustressPlodaVDekompensaciiCheckBox.setEnabled(0)

        self.ZatrumkaRozvutkyPlodaNoCheckBox.setChecked(1)
        self.ZatrumkaRozvutkyPlodaNoCheckBox.setEnabled(1)
        self.ZatrumkaRozvutkyPlodaSumetrychnaFormaCheckBox.setChecked(0)
        self.ZatrumkaRozvutkyPlodaSumetrychnaFormaCheckBox.setEnabled(0)
        self.ZatrumkaRozvutkyPlodaAsumetruchnaFormaCheckBox.setChecked(0)
        self.ZatrumkaRozvutkyPlodaAsumetruchnaFormaCheckBox.setEnabled(0)

        self.NajavnistSustemnoiInfekciiYesCheckBox.setChecked(0)

        self.PatologiaPlacentuNoCheckBox.setChecked(1)
        self.PatologiaPlacentuNoCheckBox.setEnabled(1)
        self.PatologiaPlacentuGipoplaziaCheckBox.setChecked(0)
        self.PatologiaPlacentuGipoplaziaCheckBox.setEnabled(0)
        self.PatologiaPlacentuGiperplaziaCheckBox.setChecked(0)
        self.PatologiaPlacentuGiperplaziaCheckBox.setEnabled(0)

        self.PatologiaLocalizaciiPlacentuNoCheckBox.setChecked(1)
        self.PatologiaLocalizaciiPlacentuNoCheckBox.setEnabled(1)
        self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaCheckBox.setChecked(0)
        self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaCheckBox.setEnabled(0)
        self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaCheckBox.setChecked(
            0)
        self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaCheckBox.setEnabled(
            0)
        self.PatologiaLocalizaciiPlacentuPovnePeredlegannaCheckBox.setChecked(
            0)
        self.PatologiaLocalizaciiPlacentuPovnePeredlegannaCheckBox.setEnabled(
            0)

        self.PeredchasneVadsharyvannaPlacentuYesCheckBox.setChecked(0)
        self.HiryrgichniVtyrchannaPidChasVagitnostiYesCheckBox.setChecked(0)
        self.TruvalaImmobilizaciaYesCheckBox.setChecked(0)

        self.ZavershennaDannoiVagitnostiPologuVTerminiCheckBox.setChecked(1)
        self.ZavershennaDannoiVagitnostiPologuVTerminiCheckBox.setEnabled(1)
        self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokCheckBox.setChecked(
            0)
        self.ZavershennaDannoiVagitnostiSamovilnuiVukudenCheckBox.setChecked(0)

        self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiYesCheckBox.setChecked(
            0)

        self.PologuVaginalniNoCheckBox.setChecked(1)
        self.PologuVaginalniNoCheckBox.setEnabled(1)
        self.PologuVaginalniSpomtanniCheckBox.setChecked(0)
        self.PologuVaginalniIndykovaniCheckBox.setChecked(0)

        self.PologuAbdominalniNoCheckBox.setChecked(1)
        self.PologuAbdominalniNoCheckBox.setEnabled(1)
        self.PologuAbdominalniPlanovuiKRCheckBox.setChecked(0)
        self.PologuAbdominalniYrgentbuiKRCheckBox.setChecked(0)

        self.PokazannaDlaAbdominalnogoRozrodjennaLineEdit.setText('')

        self.PoryshennaPologovoiDialnostiNoCheckBox.setChecked(1)
        self.PoryshennaPologovoiDialnostiNoCheckBox.setEnabled(1)
        self.PoryshennaPologovoiDialnostiStrimkiPologuCheckBox.setChecked(0)
        self.PoryshennaPologovoiDialnostiDuskoordunaciaCheckBox.setChecked(0)
        self.PoryshennaPologovoiDialnostiSlabkistCheckBox.setChecked(0)

        self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.setChecked(1)
        self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.setEnabled(1)
        self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox.setChecked(
            0)
        self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox.setChecked(0)
        self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox.setChecked(0)

        self.VuluvNavkoloplodovuhVodSvoechasnuiCheckBox.setChecked(1)
        self.VuluvNavkoloplodovuhVodSvoechasnuiCheckBox.setEnabled(1)
        self.VuluvNavkoloplodovuhVodRaniiCheckBox.setChecked(0)
        self.VuluvNavkoloplodovuhVodPeredchasnuiCheckBox.setChecked(0)

        self.DustressPlodaVPologahNoCheckBox.setChecked(1)
        self.DustressPlodaVPologahNoCheckBox.setEnabled(1)
        self.DustressPlodaVPologahVIPeriodiCheckBox.setChecked(0)
        self.DustressPlodaVPologahVIIPeriodiCheckBox.setChecked(0)

        self.GipotonichnaKrovotechaNoCheckBox.setChecked(1)
        self.GipotonichnaKrovotechaNoCheckBox.setEnabled(1)
        self.GipotonichnaKrovotechaVIIIPeriodiCheckBox.setChecked(0)
        self.GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiCheckBox.setChecked(
            0)
        self.GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiCheckBox.setChecked(
            0)

        self.AnomaliiPrukriplennaPlacentuNoCheckBox.setChecked(1)
        self.AnomaliiPrukriplennaPlacentuNoCheckBox.setEnabled(1)
        self.AnomaliiPrukriplennaPlacentuAdherensCheckBox.setChecked(0)
        self.AnomaliiPrukriplennaPlacentuAcretaCheckBox.setChecked(0)
        self.AnomaliiPrukriplennaPlacentuPercretaCheckBox.setChecked(0)

        self.DefektPoslidyYesCheckBox.setChecked(0)
        self.DefektPoslidyYesCheckBox.setEnabled(0)
        self.DefektObolonokYesCheckBox.setChecked(0)
        self.DefektObolonokYesCheckBox.setEnabled(0)
        self.AnomaliiPrukriplennaPypovunuObolonkoveCheckBox.setChecked(0)
        self.AnomaliiPrukriplennaPypovunuObolonkoveCheckBox.setEnabled(0)
        self.OperatuvnaDopomogaNoCheckBox.setChecked(1)
        self.RozruvuPologovuhShlahivNoCheckBox.setChecked(1)
        self.EpizoAboPerineotomiaYesCheckBox.setChecked(0)
        self.KrovovtrataVPologahLineEdit.setText('')

        self.TruvalistPologivZagalnaGodunLineEdit.setText('')
        self.TruvalistPologivZagalnaHvulunLineEdit.setText('')
        self.TruvalistPologivIPeriodLineEdit.setText('')
        self.TruvalistPologivIPeriodHvulunLineEdit.setText('')
        self.TruvalistPologivIIPeriodLineEdit.setText('')
        self.TruvalistPologivIIPeriodHvulunLineEdit.setText('')
        self.TruvalistPologivIIIPeriodLineEdit.setText('')
        self.TruvalistPologivIIIPeriodHvulunLineEdit.setText('')

        self.NaroduvsaMertvuiCheckBox.setChecked(0)

        self.ZrilistNovonarodgennogoDonoshenuiCheckBox.setChecked(1)
        self.ZrilistNovonarodgennogoDonoshenuiCheckBox.setEnabled(1)
        self.ZrilistNovonarodgennogoNedonoshenuiCheckBox.setChecked(0)
        self.ZrilistNovonarodgennogoNedonoshenuiCheckBox.setEnabled(1)
        self.ZrilistNovonarodgennogoPerenoshenuiCheckBox.setChecked(0)
        self.ZrilistNovonarodgennogoPerenoshenuiCheckBox.setEnabled(1)

        self.MasaNovonarodgenogoLineEdit.setText('')
        self.ZristNovonarodgenogoLineEdit.setText('')
        self.KoeficientNovonarodgenogoLineEdit.setText('')

        self.GipotrofiaPlodaYesCheckBox.setChecked(0)

        self.OcinkaZaShkaloyApgarNaPerHvLineEdit.setText('')
        self.OcinkaZaShkaloyApgarNa5HvLineEdit.setText('')

        self.NovonarodjenuiZVadamuRozvutkyYesCheckBox.setChecked(0)
        self.PologovaTravmaYesCheckBox.setChecked(0)
        self.SDRYesCheckBox.setChecked(0)
        self.VnytrishnoytrobneInfikyvannaYesCheckBox.setChecked(0)
        self.GemoragichniYskladnennaYesCheckBox.setChecked(0)

        self.AnemiaNoCheckBox.setChecked(1)
        self.AnemiaNoCheckBox.setEnabled(1)
        self.AnemiaIStypenaCheckBox.setChecked(0)
        self.AnemiaIIStypenaCheckBox.setChecked(0)
        self.AnemiaIIIStypenaCheckBox.setChecked(0)

        self.GiperBilirybinemiaYesCheckBox.setChecked(0)
        self.GiperBilirybinemiaRivenBilirybinyLineEdit.setText('')

        self.AsfiksiaNoCheckBox.setChecked(1)
        self.AsfiksiaNoCheckBox.setEnabled(1)
        self.AsfiksiaLegkaCheckBox.setChecked(0)
        self.AsfiksiaSerednaCheckBox.setChecked(0)
        self.AsfiksiaVajkaCheckBox.setChecked(0)

        self.PoryshennaKardioRespiratornoiAdaptaciiYesCheckBox.setChecked(0)
        self.VtrataMasuTilaLineEdit.setText('')
        self.VitaminKVvedenoYesCheckBox.setChecked(0)
        self.VupusanuiNaLineEdit.setText('')
        self.NeonatalnaSmertYesCheckBox.setChecked(0)
        self.PislapologovuiPerebigYesCheckBox.setChecked(0)
        self.ProfilaktukaTerapiaTEYPynktIXYesCheckBox.setChecked(0)
        self.ElastuchnaKompressiaPynktIXYesCheckBox.setChecked(0)
        self.MedukamentoznaProfilaktukaPynktIXYesCheckBox.setChecked(0)
        self.HiryrgichneLikyvannaPynktIXYesCheckBox.setChecked(0)
        self.TruvalistProvedenoiProfilaktuktPynktIXLineEdit.setText('')
        self.YskladnennaVidProfilaktukyPynktIXYesCheckBox.setChecked(0)
        self.TromboembolichniYskladnennaPynktIXYesCheckBox.setChecked(0)
        self.MastutPynktIXYesCheckBox.setChecked(0)
        self.SubinvolyciaMatkuPynktIXYesCheckBox.setChecked(0)
        self.EndometrutPynktIXYesCheckBox.setChecked(0)
        self.PiznaPologovaKrovotechaPynktIXYesCheckBox.setChecked(0)
        self.SepsusPynktIXYesCheckBox.setChecked(0)
        self.RoshodgennaShvivPynktIXYesCheckBox.setChecked(0)
        self.InshiPynktIXLineEdit.setText('')
        self.HirVtyrchannaVPershi6TugnivPynktIXYesCheckBox.setChecked(0)
        self.VupuskaDodomyPynktIXNoCheckBox.setChecked(0)
        self.VupuskaDodomyPynktIXDobyLineEdit.setText('')
        self.PerevedennaVInshuiStacionarPynktIXYesCheckBox.setChecked(0)
        self.PerevedennaVInshuiStacionarPynktIXDobyLineEdit.setText('')

    def SeachInfo(self):

        try:
            cnx = self.ConnectToPregnantBD()
        except mysql.connector.DatabaseError as e:
            self.Info_mesage(str(e))

        try:
            seach_cursor = cnx.cursor()
            # seach_cursor = cnx.cursor(buffered=True)
        except mysql.connector.DatabaseError as e:
            self.Info_mesage(str(e))
            cnx.close()

        self.FirstNameToSelect = self.SeachFormFirstNameLineEdit.text()
        self.FirstNameToSelect = self.FirstNameToSelect.strip()
        self.FirstNameToSelect = self.FirstNameToSelect.replace("'", "''")

        self.LastNameToSelect = self.SeachFormLastNameLineedit.text()
        self.LastNameToSelect = self.LastNameToSelect.strip()
        self.LastNameToSelect = self.LastNameToSelect.replace("'", "''")

        self.FatherNameToSelect = self.SeachFormFatherNameLineEdit.text()
        self.FatherNameToSelect = self.FatherNameToSelect.strip()
        self.FatherNameToSelect = self.FatherNameToSelect.replace("'", "''")

        self.PasportniDaniToSelect = "like '%" + self.FirstNameToSelect + "%" + self.LastNameToSelect + "%" + self.FatherNameToSelect + "%'"

        self.HistoryNumberToSelect = self.SeachFormHistoryNumberLineEdit.text()
        self.HistoryNumberToSelect = self.HistoryNumberToSelect.strip()
        self.HistoryNumberToSelect = self.HistoryNumberToSelect.replace(
            "'", "''")
        if self.HistoryNumberToSelect == '':
            self.HistoryNumberToSelect = 'is not NULL'
        else:
            self.HistoryNumberToSelect = "like '%" + self.HistoryNumberToSelect + "%'"

        self.AgeToSelect = self.SeachFormAgeLineEdit.text()
        self.AgeToSelect = self.AgeToSelect.strip()

        if self.AgeToSelect == '':
            self.AgeToSelect = 'is not NULL'
        else:
            self.AgeToSelect = "like '%" + self.AgeToSelect + "%'"

        if self.PasportniDaniToSelect == "like '%%%%'" and self.HistoryNumberToSelect == 'is not NULL' and self.AgeToSelect == 'is not NULL':
            self.Error_mesage("Усі поля поля для пошуку порожні!")
            try:
                seach_cursor.close()
                cnx.close()
            except mysql.connector.DatabaseError as e:
                self.Info_mesage(str(e))

        else:

            query_to_seach = (
                """select * from Registry R where R.PasportniDani """ +
                self.PasportniDaniToSelect + " and R.HistoryNumber " +
                self.HistoryNumberToSelect + " and R.Age " + self.AgeToSelect)
            # print(query_to_seach)

            try:
                seach_cursor.execute(query_to_seach)
            except mysql.connector.DatabaseError as e:
                self.Info_mesage(str(e))
                seach_cursor.close()
                cnx.close()

            try:
                i = 0
                for column_description in seach_cursor.description:
                    self.SeachResultTable.setHorizontalHeaderItem(
                        i,
                        QTableWidgetItem(
                            str("{:<13}".format(*column_description))))
                    i = i + 1
            except mysql.connector.DatabaseError as e:
                self.Info_mesage(str(e))

            self.SeachResultTable.setRowCount(0)

            for row, form in enumerate(seach_cursor):
                self.SeachResultTable.insertRow(row)
                for column, item in enumerate(form):
                    self.SeachResultTable.setItem(row, column,
                                                  QTableWidgetItem(str(item)))
            # self.SeachResultTable.resizeColumnsToContents()
            # self.SeachResultTable.setColumnWidth(1, 300)

            try:
                seach_cursor.close()
            except mysql.connector.DatabaseError as e:
                self.Info_mesage(str(e))
            cnx.close()

    def SeachWievData(self):
        self.DedicatedRow = self.SeachResultTable.currentRow()

        if self.DedicatedRow >= 0:
            self.FirstItem = self.SeachResultTable.item(0, 0)

            if self.FirstItem is not None:
                self.WievText = BigTextRedactor()
                self.WievText.setGeometry(300, 300, 700, 600)
                i = 0
                j = self.SeachResultTable.currentRow()
                while i < int(self.SeachResultTable.columnCount()):
                    CellText = self.SeachResultTable.item(j, i)
                    OrderItemText = CellText.text()
                    try:
                        # if str(OrderItemText[1]) == 'V' or str(OrderItemText[1]) == 'I' \
                        #         or str(OrderItemText).find('ІX.Післяпологовий') != -1 \
                        #         or str(OrderItemText).find('ІV. Акушерський анамнез.') != -1:
                        if str(OrderItemText).find('V') != -1 or str(OrderItemText).find('I') != -1 \
                                or str(OrderItemText).find('ІX.Післяпологовий') != -1 \
                                or str(OrderItemText).find('ІV. Акушерський анамнез.') != -1:
                            self.WievText.BigDataText.insertPlainText("\n")
                            self.WievText.BigDataText.insertHtml("<b>" + OrderItemText + "</b>\n")
                            self.WievText.BigDataText.insertPlainText("\n")
                        else:
                            self.WievText.BigDataText.insertPlainText(OrderItemText + "\n")
                    except Exception as e:
                        self.Info_mesage(str(e))
                    i = i + 1

                self.WievText.CloseBigDataTextButton.clicked.connect(
                    self.WievText.close)
            else:
                self.Error_mesage("Виділений рядок порожній!")
        else:
            self.Error_mesage("Необхідно виділити потрібний запис!")

    def CreateUser(self):
        self.CreatingUserErrorCount = 0

        self.LiginToCreate = self.CreateUserLoginLineEdit.text()
        self.LiginToCreate = self.LiginToCreate.strip()
        if self.LiginToCreate == '':
            self.Error_mesage(
                "Необхідно заповнити логін майбутнього користувача!")
            self.CreatingUserErrorCount = self.CreatingUserErrorCount + 1

        self.PasswordToCreate = self.CreateUserPasswordLineEdit.text()
        self.PasswordToCreate = self.PasswordToCreate.strip()
        if self.PasswordToCreate == '':
            self.Error_mesage(
                "Необхідно заповнити пароль майбутнього користувача!")
            self.CreatingUserErrorCount = self.CreatingUserErrorCount + 1

        self.PIBToCreate = self.CreateUserPIBLineEdit.text()
        self.PIBToCreate = self.PIBToCreate.strip()
        if self.PIBToCreate == '':
            self.Error_mesage(
                "Необхідно заповнити П.І.Б. майбутнього користувача!")
            self.CreatingUserErrorCount = self.CreatingUserErrorCount + 1

        self.RoleToCreate = self.CreateUserPrivilegesComboBox.currentText()

        if self.CreatingUserErrorCount == 0:

            try:
                cnx = self.ConnectToPregnantBD()
            except mysql.connector.DatabaseError as e:
                self.Info_mesage(str(e))

            try:
                cursor = cnx.cursor()
            except mysql.connector.DatabaseError as e:
                self.Info_mesage(str(e))
                cnx.close()
            # #query = ("SELECT s.Role from authorization s where s.Login="+"'"+self.Login+"' and s.Password='"+self.Password+"'")
            query_to_insert = ("""
                                INSERT INTO authorization
                                    (
                                    Login, Password, Role, pib
                                    )
                                    VALUES
                                    (
                                    '""" + self.LiginToCreate + """',
                                    '""" + self.PasswordToCreate + """',
                                    '""" + self.RoleToCreate + """',
                                    '""" + self.PIBToCreate + """'
                                    )
                        """)
            try:
                cursor.execute(query_to_insert)
                try:
                    cnx.commit()
                    cursor.close()
                    cnx.close()
                    self.Info_mesage('Користувач успішно створений!')
                except mysql.connector.DatabaseError as e:
                    self.Info_mesage(str(e))
                    cursor.close()
                    cnx.close()

            except mysql.connector.DatabaseError as e:
                self.Info_mesage(str(e))
                cursor.close()
                cnx.close()

    # Блок обработчика событий по П5 (проффесиональная деятельность)
    def ProffesionalDontWork(self):
        if self.ProffesionalDontWorkCheckBox.isChecked():
            self.ProffesionalStadyCheckBox.setEnabled(0)
            self.ProffesionalWhiteCollarWorkerCheckBox.setEnabled(0)
            self.ProffesionalEmployeeCheckBox.setEnabled(0)
        else:
            self.ProffesionalStadyCheckBox.setEnabled(1)
            self.ProffesionalWhiteCollarWorkerCheckBox.setEnabled(1)
            self.ProffesionalEmployeeCheckBox.setEnabled(1)

    def ProffesionalStady(self):
        if self.ProffesionalStadyCheckBox.isChecked():
            self.ProffesionalDontWorkCheckBox.setEnabled(0)
            self.ProffesionalWhiteCollarWorkerCheckBox.setEnabled(0)
            self.ProffesionalEmployeeCheckBox.setEnabled(0)
        else:
            self.ProffesionalDontWorkCheckBox.setEnabled(1)
            self.ProffesionalWhiteCollarWorkerCheckBox.setEnabled(1)
            self.ProffesionalEmployeeCheckBox.setEnabled(1)

    def ProffesionalWhiteCollar(self):
        if self.ProffesionalWhiteCollarWorkerCheckBox.isChecked():
            self.ProffesionalStadyCheckBox.setEnabled(0)
            self.ProffesionalDontWorkCheckBox.setEnabled(0)
            self.ProffesionalEmployeeCheckBox.setEnabled(0)
        else:
            self.ProffesionalStadyCheckBox.setEnabled(1)
            self.ProffesionalDontWorkCheckBox.setEnabled(1)
            self.ProffesionalEmployeeCheckBox.setEnabled(1)

    def ProffesionalEmployee(self):
        if self.ProffesionalEmployeeCheckBox.isChecked():
            self.ProffesionalStadyCheckBox.setEnabled(0)
            self.ProffesionalWhiteCollarWorkerCheckBox.setEnabled(0)
            self.ProffesionalDontWorkCheckBox.setEnabled(0)
        else:
            self.ProffesionalStadyCheckBox.setEnabled(1)
            self.ProffesionalWhiteCollarWorkerCheckBox.setEnabled(1)
            self.ProffesionalDontWorkCheckBox.setEnabled(1)

            # Обработчик событий по инвалидности

    def DisabilityNoneFunc(self):
        if self.DisabilityNoneCheckBox.isChecked():
            self.DisabilityILevelCheckBox.setEnabled(0)
            self.DisabilityIILevelCheckBox.setEnabled(0)
            self.DisabilityIIILevelCheckBox.setEnabled(0)
        else:
            self.DisabilityILevelCheckBox.setEnabled(1)
            self.DisabilityIILevelCheckBox.setEnabled(1)
            self.DisabilityIIILevelCheckBox.setEnabled(1)

    def DisabilityILevelFunc(self):
        if self.DisabilityILevelCheckBox.isChecked():
            self.DisabilityNoneCheckBox.setEnabled(0)
            self.DisabilityIILevelCheckBox.setEnabled(0)
            self.DisabilityIIILevelCheckBox.setEnabled(0)
        else:
            self.DisabilityNoneCheckBox.setEnabled(1)
            self.DisabilityIILevelCheckBox.setEnabled(1)
            self.DisabilityIIILevelCheckBox.setEnabled(1)

    def DisabilityIILevelFunc(self):
        if self.DisabilityIILevelCheckBox.isChecked():
            self.DisabilityNoneCheckBox.setEnabled(0)
            self.DisabilityILevelCheckBox.setEnabled(0)
            self.DisabilityIIILevelCheckBox.setEnabled(0)
        else:
            self.DisabilityNoneCheckBox.setEnabled(1)
            self.DisabilityILevelCheckBox.setEnabled(1)
            self.DisabilityIIILevelCheckBox.setEnabled(1)

    def DisabilityIIILevelFunc(self):
        if self.DisabilityIIILevelCheckBox.isChecked():
            self.DisabilityNoneCheckBox.setEnabled(0)
            self.DisabilityIILevelCheckBox.setEnabled(0)
            self.DisabilityILevelCheckBox.setEnabled(0)
        else:
            self.DisabilityNoneCheckBox.setEnabled(1)
            self.DisabilityIILevelCheckBox.setEnabled(1)
            self.DisabilityILevelCheckBox.setEnabled(1)

            # обработчик событий по рецедивам тромбоемболии в прошлом

    def ReceduvyTromboemboliiYesFunc(self):
        if self.ReceduvyTromboemboliiYesCheckBox.isChecked():
            self.ReceduvyTromboemboliiNoCheckBox.setEnabled(0)
        else:
            self.ReceduvyTromboemboliiNoCheckBox.setEnabled(1)
            self.ReceduvyTromboemboliiNoCheckBox.setChecked(1)

    def ReceduvyTromboemboliiNoFunc(self):
        if self.ReceduvyTromboemboliiNoCheckBox.isChecked():
            self.ReceduvyTromboemboliiYesCheckBox.setEnabled(0)
        else:
            self.ReceduvyTromboemboliiYesCheckBox.setEnabled(1)
            self.ReceduvyTromboemboliiYesCheckBox.setChecked(1)

            # обработчик событий 2.	Тромбоемболії, неспровоковані або пов'язані з прийомом естрогенів

    def TromboemboliiAndEstrogensYesFunc(self):
        if self.TromboemboliiAndEstrogensYesCheckBox.isChecked():
            self.TromboemboliiAndEstrogensNoCheckBox.setEnabled(0)
        else:
            self.TromboemboliiAndEstrogensNoCheckBox.setEnabled(1)
            self.TromboemboliiAndEstrogensNoCheckBox.setChecked(1)

    def TromboemboliiAndEstrogensNoFunc(self):
        if self.TromboemboliiAndEstrogensNoCheckBox.isChecked():
            self.TromboemboliiAndEstrogensYesCheckBox.setEnabled(0)
        else:
            self.TromboemboliiAndEstrogensYesCheckBox.setEnabled(1)
            self.TromboemboliiAndEstrogensYesCheckBox.setChecked(1)

            # обработчик событий 3.	тромбоемболія спровокована

    def TromboemboliaSprovokovanaYesFunc(self):
        if self.TromboemboliaSprovokovanaYesCheckBox.isChecked():
            self.TromboemboliaSprovokovanaNoCheckBox.setEnabled(0)
        else:
            self.TromboemboliaSprovokovanaNoCheckBox.setEnabled(1)
            self.TromboemboliaSprovokovanaNoCheckBox.setChecked(1)

    def TromboemboliaSprovokovanaNoFunc(self):
        if self.TromboemboliaSprovokovanaNoCheckBox.isChecked():
            self.TromboemboliaSprovokovanaYesCheckBox.setEnabled(0)
        else:
            self.TromboemboliaSprovokovanaYesCheckBox.setEnabled(1)
            self.TromboemboliaSprovokovanaYesCheckBox.setChecked(1)

            # обработчик событий 4.	Сімейний анамнез тромбоемболії

    def SimeinuiAnamnezTromboemboliiNoFunc(self):
        if self.SimeinuiAnamnezTromboemboliiNoCheckBox.isChecked():
            self.SimeinuiAnamnezTromboemboliiYesCheckBox.setEnabled(0)
        else:
            self.SimeinuiAnamnezTromboemboliiYesCheckBox.setEnabled(1)
            self.SimeinuiAnamnezTromboemboliiYesCheckBox.setChecked(1)

    def SimeinuiAnamnezTromboemboliiYesFunc(self):
        if self.SimeinuiAnamnezTromboemboliiYesCheckBox.isChecked():
            self.SimeinuiAnamnezTromboemboliiNoCheckBox.setEnabled(0)
        else:
            self.SimeinuiAnamnezTromboemboliiNoCheckBox.setEnabled(1)
            self.SimeinuiAnamnezTromboemboliiNoCheckBox.setChecked(1)

            # обработчик событий 5.	встановлена тромбофілія

    def VstanovlennaTrombofiliaNoFunc(self):
        if self.VstanovlennaTrombofiliaNoCheckBox.isChecked():
            self.VstanovlennaTrombofiliaYesCheckBox.setEnabled(0)
        else:
            self.VstanovlennaTrombofiliaYesCheckBox.setEnabled(1)
            self.VstanovlennaTrombofiliaYesCheckBox.setChecked(1)

    def VstanovlennaTrombofiliaYesFunc(self):
        if self.VstanovlennaTrombofiliaYesCheckBox.isChecked():
            self.VstanovlennaTrombofiliaNoCheckBox.setEnabled(0)
        else:
            self.VstanovlennaTrombofiliaNoCheckBox.setEnabled(1)
            self.VstanovlennaTrombofiliaNoCheckBox.setChecked(1)

    def SypytniZahvoryvannaNoFunc(self):
        if self.SypytniZahvoryvannaNoCheckBox.isChecked():
            self.SypytniZahvoryvannaYesCheckBox.setEnabled(0)
            self.SypytniSercevoSydunniCheckBox.hide()
            self.SypytniBronhoLegeneviCheckBox.hide()
            self.SypytniSCHVCheckBox.hide()
            self.SypytniRAKCheckBox.hide()
            self.SypytniNefrotuchnuiSundromCheckBox.hide()
            self.SypytniSerpovudnoKlitynnaAnemiaCheckBox.hide()
            self.SypytniVnytrishnoVenneVvedennaMedukamentivCheckBox.hide()
            self.SypytniOtherLineEdit.hide()
            self.SypytniOtherCheckBox.hide()
        else:
            self.SypytniZahvoryvannaYesCheckBox.setEnabled(1)
            self.SypytniZahvoryvannaYesCheckBox.setChecked(1)
            self.SypytniZahvoryvannaLabel.setFixedWidth(150)
            self.splitter17 = QSplitter(Qt.Horizontal)
            self.splitter17.addWidget(self.SypytniSercevoSydunniCheckBox)
            self.splitter17.addWidget(self.SypytniBronhoLegeneviCheckBox)
            self.splitter17.addWidget(self.SypytniSCHVCheckBox)
            self.splitter17.addWidget(self.SypytniRAKCheckBox)
            self.splitter17.addWidget(self.SypytniNefrotuchnuiSundromCheckBox)
            self.splitter17.addWidget(
                self.SypytniSerpovudnoKlitynnaAnemiaCheckBox)
            self.splitter17.addWidget(
                self.SypytniVnytrishnoVenneVvedennaMedukamentivCheckBox)
            self.splitter17.addWidget(self.SypytniOtherLineSplitter)
            self.splitter16.addWidget(self.splitter17)
            self.SypytniZahvoryvannaNoCheckBox.hide()
            self.SypytniSercevoSydunniCheckBox.show()
            self.SypytniBronhoLegeneviCheckBox.show()
            self.SypytniSCHVCheckBox.show()
            self.SypytniRAKCheckBox.show()
            self.SypytniNefrotuchnuiSundromCheckBox.show()
            self.SypytniSerpovudnoKlitynnaAnemiaCheckBox.show()
            self.SypytniVnytrishnoVenneVvedennaMedukamentivCheckBox.show()
            self.SypytniOtherCheckBox.show()

    def SypytniZahvoryvannaYesFunc(self):
        if self.SypytniZahvoryvannaYesCheckBox.isChecked():
            self.SypytniZahvoryvannaNoCheckBox.hide()

        else:
            self.SypytniZahvoryvannaNoCheckBox.show()
            self.SypytniZahvoryvannaNoCheckBox.setChecked(1)
            self.SypytniZahvoryvannaLabel.setFixedWidth(400)

    def SypytniOtherCheckBoxFunc(self):
        if self.SypytniOtherCheckBox.isChecked():
            self.SypytniOtherTextRedaktorOpen()
        else:
            self.SypytniOtherLineEdit.hide()

    def SypytniOtherTextRedaktorOpen(self):
        self.BigTextRedactorForm = BigTextRedactor()
        self.OtherText = self.SypytniOtherLineEdit.text()
        self.BigTextRedactorForm.BigDataText.setText(self.OtherText)
        self.BigTextRedactorForm.show()
        self.BigTextRedactorForm.CloseBigDataTextButton.clicked.connect(
            self.SypytniOtherTextRedaktorClose)

    def SypytniOtherTextRedaktorClose(self):
        self.BigTextRedactorForm.close()
        self.data = self.BigTextRedactorForm.BigDataText.toPlainText()
        self.SypytniOtherLineEdit.show()
        self.SypytniOtherLineEdit.setText(self.data)

    # обработчик событий 7.	Вік> 35 років

    def OldMore35YesFunc(self):
        if self.OldMore35YesCheckBox.isChecked():
            self.OldMore35NoCheckBox.setEnabled(0)
        else:
            self.OldMore35NoCheckBox.setEnabled(1)
            self.OldMore35NoCheckBox.setChecked(1)

    def OldMore35NoFunc(self):
        if self.OldMore35NoCheckBox.isChecked():
            self.OldMore35YesCheckBox.setEnabled(0)
        else:
            self.OldMore35YesCheckBox.setEnabled(1)
            self.OldMore35YesCheckBox.setChecked(1)

            # обработчик событий 8.	Ожиріння (ІМТ> 30)

    def OgirinnaYesFunc(self):
        if self.OgirinnaYesCheckBox.isChecked():
            self.OgirinnaNoCheckBox.setEnabled(0)
        else:
            self.OgirinnaNoCheckBox.setEnabled(1)
            self.OgirinnaNoCheckBox.setChecked(1)

    def OgirinnaNoFunc(self):
        if self.OgirinnaNoCheckBox.isChecked():
            self.OgirinnaYesCheckBox.setEnabled(0)
        else:
            self.OgirinnaYesCheckBox.setEnabled(1)
            self.OgirinnaYesCheckBox.setChecked(1)

            # обработчик событий       9.     Вагітність  ≥3

    def VagitnistMore3YesFunc(self):
        if self.VagitnistMore3YesCheckBox.isChecked():
            self.VagitnistMore3NoCheckBox.setEnabled(0)
        else:
            self.VagitnistMore3NoCheckBox.setEnabled(1)
            self.VagitnistMore3NoCheckBox.setChecked(1)

    def VagitnistMore3NoFunc(self):
        if self.VagitnistMore3NoCheckBox.isChecked():
            self.VagitnistMore3YesCheckBox.setEnabled(0)
        else:
            self.VagitnistMore3YesCheckBox.setEnabled(1)
            self.VagitnistMore3YesCheckBox.setChecked(1)

            # обработчик событий   10.	Куріння

    def KyrinnaYesFunc(self):
        if self.KyrinnaYesCheckBox.isChecked():
            self.KyrinnaNoCheckBox.setEnabled(0)
        else:
            self.KyrinnaNoCheckBox.setEnabled(1)
            self.KyrinnaNoCheckBox.setChecked(1)

    def KyrinnaNoFunc(self):
        if self.KyrinnaNoCheckBox.isChecked():
            self.KyrinnaYesCheckBox.setEnabled(0)
        else:
            self.KyrinnaYesCheckBox.setEnabled(1)
            self.KyrinnaYesCheckBox.setChecked(1)

            # обработчик событий 11. Великі варикозні вени

    def VelykiVarikozniVenuYesFunc(self):
        if self.VelykiVarikozniVenuYesCheckBox.isChecked():
            self.VelykiVarikozniVenuNoCheckBox.setEnabled(0)
        else:
            self.VelykiVarikozniVenuNoCheckBox.setEnabled(1)
            self.VelykiVarikozniVenuNoCheckBox.setChecked(1)

    def VelykiVarikozniVenuNoFunc(self):
        if self.VelykiVarikozniVenuNoCheckBox.isChecked():
            self.VelykiVarikozniVenuYesCheckBox.setEnabled(0)
        else:
            self.VelykiVarikozniVenuYesCheckBox.setEnabled(1)
            self.VelykiVarikozniVenuYesCheckBox.setChecked(1)

            # Обработчик ІІІ. Проведення профілактики/терапії ТЕУ до вагітності: а) так б)ні

    def ProvedennaProfTEYdpVagitnostiLabelYesFunc(self):
        if self.ProvedennaProfTEYdpVagitnostiLabelYesCheckBox.isChecked():
            pass
        else:
            self.ProvedennaProfTEYdpVagitnostiLabelNoCheckBox.setEnabled(1)
            self.ProvedennaProfTEYdpVagitnostiLabelNoCheckBox.setChecked(1)
            self.ProvedennaProfTEYdpVagitnostiLabelYesCheckBox.setEnabled(1)
            self.ElastychnaKompresiaLabel.setEnabled(0)

            self.ElastychnaKompresiaNoCheckBox.show()
            self.ElastychnaKompresiaNoCheckBox.setEnabled(0)
            self.ElastychnaKompresiaNoCheckBox.setChecked(1)

            self.ElastychnaKompresiaYesCheckBox.setEnabled(0)
            self.ElastychnaKompresiaYesCheckBox.setChecked(0)
            self.ElastychnaKompresiaNoCheckBox.setEnabled(0)

            self.ElastychnaKompresiaLevelLabel.hide()
            self.ElastychnaKompresiaLevelLineEdit.hide()

            self.MedukamentoznaProfilaktukaLabel.setEnabled(0)
            self.MedukamentoznaProfilaktukaLabel.setFixedWidth(400)

            self.MedukamentoznaProfilaktukaNoCheckBox.show()
            self.MedukamentoznaProfilaktukaNoCheckBox.setEnabled(0)
            self.MedukamentoznaProfilaktukaNoCheckBox.setChecked(1)

            self.MedukamentoznaProfilaktukaYesCheckBox.setEnabled(0)
            self.MedukamentoznaProfilaktukaYesCheckBox.setChecked(0)
            self.MedukamentoznaProfilaktukaNoCheckBox.setEnabled(0)

            self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyLabel.hide()
            self.MedukamentoznaProfilaktukaNazvaPreperatyLineEdit.hide()

            self.MedukamentoznaProfilaktukaRegymPrujomyLabel.hide()
            self.MedukamentoznaProfilaktukaRegymPrujomyLineEdit.hide()

            self.HiryrgichneLikyvannaLabel.setEnabled(0)
            self.HiryrgichneLikyvannaLabel.setFixedWidth(400)

            self.HiryrgichneLikyvannaNoCheckBox.setEnabled(0)
            self.HiryrgichneLikyvannaNoCheckBox.show()
            self.HiryrgichneLikyvannaNoCheckBox.setChecked(1)

            self.HiryrgichneLikyvannaYesCheckBox.setChecked(0)
            self.HiryrgichneLikyvannaYesCheckBox.setEnabled(0)
            self.HiryrgichneLikyvannaNoCheckBox.setEnabled(0)

            self.HiryrgichneLikyvannaNazvaOpericiiLabel.hide()
            self.HiryrgichneLikyvannaNazvaOpericiiLineEdit.hide()

            self.TryvalistProvedennoiProfilaktykyLabel.setEnabled(0)
            self.TryvalistProvedennoiProfilaktykyLineEdit.setEnabled(0)
            self.TryvalistProvedennoiProfilaktykyLineEdit.setText('')

            self.YskladneenaVidProfilaktykuLabel.setEnabled(0)
            self.YskladneenaVidProfilaktykuLabel.setFixedWidth(400)

            self.YskladneenaVidProfilaktykuNoCheckBox.setEnabled(0)
            self.YskladneenaVidProfilaktykuNoCheckBox.setChecked(1)
            self.YskladneenaVidProfilaktykuNoCheckBox.show()

            self.YskladneenaVidProfilaktykuYesCheckBox.setEnabled(0)
            self.YskladneenaVidProfilaktykuYesCheckBox.setChecked(0)
            self.YskladneenaVidProfilaktykuNoCheckBox.setEnabled(0)

            self.YskladneenaVidProfilaktykuNajavnistLabel.hide()

            self.YskladneenaVidProfilaktykuNajavnistLineEdit.hide()

    def ProvedennaProfTEYdpVagitnostiLabelNoFunc(self):
        if self.ProvedennaProfTEYdpVagitnostiLabelNoCheckBox.isChecked():
            pass
        else:
            self.ProvedennaProfTEYdpVagitnostiLabelYesCheckBox.setEnabled(1)
            self.ProvedennaProfTEYdpVagitnostiLabelYesCheckBox.setChecked(1)
            self.ProvedennaProfTEYdpVagitnostiLabelNoCheckBox.setEnabled(0)
            self.ElastychnaKompresiaLabel.setEnabled(1)
            self.ElastychnaKompresiaNoCheckBox.setEnabled(1)
            self.MedukamentoznaProfilaktukaLabel.setEnabled(1)
            self.MedukamentoznaProfilaktukaNoCheckBox.setEnabled(1)
            self.HiryrgichneLikyvannaLabel.setEnabled(1)
            self.HiryrgichneLikyvannaNoCheckBox.setEnabled(1)
            self.TryvalistProvedennoiProfilaktykyLabel.setEnabled(1)
            self.TryvalistProvedennoiProfilaktykyLineEdit.setEnabled(1)
            self.YskladneenaVidProfilaktykuLabel.setEnabled(1)
            self.YskladneenaVidProfilaktykuNoCheckBox.setEnabled(1)

            # 1)Обработчик	Еластична компресія ElastychnaKompresiaYesYesFunc

    def ElastychnaKompresiaYesFunc(self):
        if self.ElastychnaKompresiaYesCheckBox.isChecked():
            pass
        else:
            self.ElastychnaKompresiaNoCheckBox.setEnabled(1)
            self.ElastychnaKompresiaNoCheckBox.setChecked(1)
            self.ElastychnaKompresiaYesCheckBox.setEnabled(0)
            self.ElastychnaKompresiaLevelLabel.hide()
            self.ElastychnaKompresiaLevelLineEdit.hide()

    def ElastychnaKompresiaNoFunc(self):
        if self.ElastychnaKompresiaNoCheckBox.isChecked():
            pass
        else:
            self.ElastychnaKompresiaYesCheckBox.setEnabled(1)
            self.ElastychnaKompresiaYesCheckBox.setChecked(1)
            self.ElastychnaKompresiaNoCheckBox.setEnabled(0)
            self.ElastychnaKompresiaLevelLabel.show()
            self.ElastychnaKompresiaLevelLabel.setEnabled(1)
            self.ElastychnaKompresiaLevelLineEdit.show()
            self.ElastychnaKompresiaLevelLineEdit.setEnabled(1)
            self.ElastychnaKompresiaLevelLineEdit.setFixedWidth(30)
            self.ElastychnaKompresiaLevelLineEdit.setFixedHeight(15)

            # Обработчик MedukamentoznaProfilaktukaYesFunc 2)	Медикаментозна профілактика

    def MedukamentoznaProfilaktukaYesFunc(self):
        if self.MedukamentoznaProfilaktukaYesCheckBox.isChecked():
            pass
        else:
            self.MedukamentoznaProfilaktukaNoCheckBox.show()
            self.MedukamentoznaProfilaktukaNoCheckBox.setEnabled(1)
            self.MedukamentoznaProfilaktukaNoCheckBox.setChecked(1)
            self.MedukamentoznaProfilaktukaYesCheckBox.setEnabled(0)
            self.MedukamentoznaProfilaktukaLabel.setFixedWidth(400)
            self.MedukamentoznaProfilaktukaNazvaPreperatyLabel.hide()
            self.MedukamentoznaProfilaktukaNazvaPreperatyLineEdit.hide()
            self.MedukamentoznaProfilaktukaRegymPrujomyLabel.hide()
            self.MedukamentoznaProfilaktukaRegymPrujomyLineEdit.hide()

    def MedukamentoznaProfilaktukaNoFunc(self):
        if self.MedukamentoznaProfilaktukaNoCheckBox.isChecked():
            pass
        else:
            self.MedukamentoznaProfilaktukaYesCheckBox.setEnabled(1)
            self.MedukamentoznaProfilaktukaYesCheckBox.setChecked(1)
            self.MedukamentoznaProfilaktukaNoCheckBox.setEnabled(0)
            self.MedukamentoznaProfilaktukaNoCheckBox.hide()
            self.MedukamentoznaProfilaktukaLabel.setFixedWidth(200)
            self.MedukamentoznaProfilaktukaNazvaPreperatyLabel.setFixedWidth(
                110)
            self.MedukamentoznaProfilaktukaRegymPrujomyLabel.setFixedWidth(100)
            self.MedukamentoznaProfilaktukaNazvaPreperatyLabel.show()
            self.MedukamentoznaProfilaktukaNazvaPreperatyLabel.setEnabled(1)
            self.MedukamentoznaProfilaktukaNazvaPreperatyLineEdit.setMinimumWidth(
                200)
            self.MedukamentoznaProfilaktukaNazvaPreperatyLineEdit.show()
            self.MedukamentoznaProfilaktukaRegymPrujomyLabel.show()
            self.MedukamentoznaProfilaktukaRegymPrujomyLineEdit.setMinimumWidth(
                200)
            self.MedukamentoznaProfilaktukaRegymPrujomyLineEdit.show()

            # Обработчик ElastychnaKompresiaYesFunc 3)	Хірургічне лікування :		          а) так б)ні

    def HiryrgichneLikyvannaYesFunc(self):
        if self.HiryrgichneLikyvannaYesCheckBox.isChecked():
            pass
        else:
            self.HiryrgichneLikyvannaNoCheckBox.show()
            self.HiryrgichneLikyvannaNoCheckBox.setEnabled(1)
            self.HiryrgichneLikyvannaNoCheckBox.setChecked(1)
            self.HiryrgichneLikyvannaYesCheckBox.setEnabled(0)
            self.HiryrgichneLikyvannaLabel.setFixedWidth(400)
            self.HiryrgichneLikyvannaNazvaOpericiiLabel.setFixedWidth(400)
            self.HiryrgichneLikyvannaNazvaOpericiiLabel.hide()
            self.HiryrgichneLikyvannaNazvaOpericiiLineEdit.hide()

    def HiryrgichneLikyvannaNoFunc(self):
        if self.HiryrgichneLikyvannaNoCheckBox.isChecked():
            pass
        else:
            self.HiryrgichneLikyvannaYesCheckBox.setEnabled(1)
            self.HiryrgichneLikyvannaYesCheckBox.setChecked(1)
            self.HiryrgichneLikyvannaNoCheckBox.setEnabled(0)
            self.HiryrgichneLikyvannaNoCheckBox.hide()
            self.HiryrgichneLikyvannaLabel.setFixedWidth(200)
            self.HiryrgichneLikyvannaNazvaOpericiiLabel.setFixedWidth(110)
            self.HiryrgichneLikyvannaNazvaOpericiiLabel.show()
            self.HiryrgichneLikyvannaNazvaOpericiiLabel.setEnabled(1)
            self.HiryrgichneLikyvannaNazvaOpericiiLineEdit.setMinimumWidth(200)
            self.HiryrgichneLikyvannaNazvaOpericiiLineEdit.show()

            # Обработчик 5)	Наявність ускладнень від проведеної профілактики: а) так б)ні Ускладення:_______________________________________________

    def YskladneenaVidProfilaktykuYesFunc(self):
        if self.YskladneenaVidProfilaktykuYesCheckBox.isChecked():
            self.YskladneenaVidProfilaktykuNoCheckBox.setEnabled(0)
        else:
            self.YskladneenaVidProfilaktykuNoCheckBox.show()
            self.YskladneenaVidProfilaktykuNoCheckBox.setEnabled(1)
            self.YskladneenaVidProfilaktykuNoCheckBox.setChecked(1)
            self.YskladneenaVidProfilaktykuYesCheckBox.setChecked(0)
            self.YskladneenaVidProfilaktykuYesCheckBox.setEnabled(0)
            self.YskladneenaVidProfilaktykuLabel.setFixedWidth(400)
            self.YskladneenaVidProfilaktykuNajavnistLabel.setFixedWidth(400)
            self.YskladneenaVidProfilaktykuNajavnistLabel.hide()
            self.YskladneenaVidProfilaktykuNajavnistLineEdit.hide()

    def YskladneenaVidProfilaktykuNoFunc(self):
        if self.YskladneenaVidProfilaktykuNoCheckBox.isChecked():
            self.YskladneenaVidProfilaktykuYesCheckBox.setEnabled(0)
        else:
            # print('ddd')
            self.YskladneenaVidProfilaktykuYesCheckBox.setEnabled(1)
            self.YskladneenaVidProfilaktykuYesCheckBox.setChecked(1)
            self.YskladneenaVidProfilaktykuNoCheckBox.setChecked(0)
            self.YskladneenaVidProfilaktykuNoCheckBox.setEnabled(0)
            self.YskladneenaVidProfilaktykuNoCheckBox.hide()
            self.YskladneenaVidProfilaktykuLabel.setFixedWidth(300)
            # self.YskladneenaVidProfilaktykuNajavnistLabel.setFixedWidth(110)
            self.YskladneenaVidProfilaktykuNajavnistLabel.show()
            self.YskladneenaVidProfilaktykuNajavnistLabel.setMinimumWidth(70)
            self.YskladneenaVidProfilaktykuNajavnistLineEdit.setMinimumWidth(
                300)
            self.YskladneenaVidProfilaktykuNajavnistLineEdit.show()
            self.YskladneenaVidProfilaktykuNajavnistLineEdit.show()

            # Обработчик 1)	Дана вагітність: а) природна  б) індукована  в) ЕКЗ. DanaVagitnisPryrodnaFunc

    def DanaVagitnisPryrodnaFunc(self):
        if self.DanaVagitnisPryrodnaCheckBox.isChecked():
            self.DanaVagitnisIndykovanaCheckBox.setEnabled(0)
            self.DanaVagitnisEKZCheckBox.setEnabled(0)
        else:
            self.DanaVagitnisIndykovanaCheckBox.setEnabled(1)
            self.DanaVagitnisEKZCheckBox.setEnabled(1)

    def DanaVagitnisIndykovanaFunc(self):
        if self.DanaVagitnisIndykovanaCheckBox.isChecked():
            self.DanaVagitnisEKZCheckBox.setEnabled(0)
            self.DanaVagitnisPryrodnaCheckBox.setEnabled(0)
        else:
            self.DanaVagitnisEKZCheckBox.setEnabled(1)
            self.DanaVagitnisPryrodnaCheckBox.setEnabled(1)

    def DanaVagitnisEKZFunc(self):
        if self.DanaVagitnisEKZCheckBox.isChecked():
            self.DanaVagitnisPryrodnaCheckBox.setEnabled(0)
            self.DanaVagitnisIndykovanaCheckBox.setEnabled(0)
        else:
            self.DanaVagitnisPryrodnaCheckBox.setEnabled(1)
            self.DanaVagitnisIndykovanaCheckBox.setEnabled(1)

            # Обработчик 4)	Попередні вагітності завершились

    def PoperedniPologuZavershulusPologamuFunc(self):
        if self.PoperedniPologuZavershulusPologamuCheckBox.isChecked():
            self.PoperedniPologuZavershulusAbortomSamovilnumCheckBox.setEnabled(
                0)
            self.PoperedniPologuZavershulusAbortomShtychnumCheckBox.setEnabled(
                0)
            self.PoperednihPologivNeByloP4CheckBox.setEnabled(0)
        else:
            self.PoperedniPologuZavershulusAbortomSamovilnumCheckBox.setEnabled(
                1)
            self.PoperedniPologuZavershulusAbortomShtychnumCheckBox.setEnabled(
                1)
            self.PoperednihPologivNeByloP4CheckBox.setEnabled(1)

    def PoperedniPologuZavershulusAbortomSamovilnumFunc(self):
        if self.PoperedniPologuZavershulusAbortomSamovilnumCheckBox.isChecked(
        ):
            self.PoperedniPologuZavershulusAbortomShtychnumCheckBox.setEnabled(
                0)
            self.PoperedniPologuZavershulusPologamuCheckBox.setEnabled(0)
            self.PoperednihPologivNeByloP4CheckBox.setEnabled(0)
        else:
            self.PoperedniPologuZavershulusPologamuCheckBox.setEnabled(1)
            self.PoperedniPologuZavershulusAbortomShtychnumCheckBox.setEnabled(
                1)
            self.PoperednihPologivNeByloP4CheckBox.setEnabled(1)

    def PoperedniPologuZavershulusAbortomShtychnumFunc(self):
        if self.PoperedniPologuZavershulusAbortomShtychnumCheckBox.isChecked():
            self.PoperedniPologuZavershulusPologamuCheckBox.setEnabled(0)
            self.PoperedniPologuZavershulusAbortomSamovilnumCheckBox.setEnabled(
                0)
            self.PoperednihPologivNeByloP4CheckBox.setEnabled(0)
        else:
            self.PoperedniPologuZavershulusPologamuCheckBox.setEnabled(1)
            self.PoperedniPologuZavershulusAbortomSamovilnumCheckBox.setEnabled(
                1)
            self.PoperednihPologivNeByloP4CheckBox.setEnabled(1)

    def PoperednihPologivNeByloP4Func(self):
        if self.PoperednihPologivNeByloP4CheckBox.isChecked():
            self.PoperedniPologuZavershulusPologamuCheckBox.setEnabled(0)
            self.PoperedniPologuZavershulusAbortomSamovilnumCheckBox.setEnabled(
                0)
            self.PoperedniPologuZavershulusAbortomShtychnumCheckBox.setEnabled(
                0)
        else:
            self.PoperedniPologuZavershulusPologamuCheckBox.setEnabled(1)
            self.PoperedniPologuZavershulusAbortomSamovilnumCheckBox.setEnabled(
                1)
            self.PoperedniPologuZavershulusAbortomShtychnumCheckBox.setEnabled(
                1)

            # Обработчик 5)	Попередні пологи а) фізіологічні б) патологічні в)ускладені

    def PoperedniPologuFiziologichniFunc(self):
        if self.PoperedniPologuFiziologichniCheckBox.isChecked():
            self.PoperedniPologuPatologichniCheckBox.setEnabled(0)
            self.PoperedniPologuYskladneniCheckBox.setEnabled(0)
            self.PoperednihPologivNeByloP5CheckBox.setEnabled(0)
        else:
            self.PoperedniPologuPatologichniCheckBox.setEnabled(1)
            self.PoperedniPologuYskladneniCheckBox.setEnabled(1)
            self.PoperednihPologivNeByloP5CheckBox.setEnabled(1)

    def PoperedniPologuPatologichniFunc(self):
        if self.PoperedniPologuPatologichniCheckBox.isChecked():
            self.PoperedniPologuFiziologichniCheckBox.setEnabled(0)
            self.PoperedniPologuYskladneniCheckBox.setEnabled(0)
            self.PoperednihPologivNeByloP5CheckBox.setEnabled(0)
        else:
            self.PoperedniPologuFiziologichniCheckBox.setEnabled(1)
            self.PoperedniPologuYskladneniCheckBox.setEnabled(1)
            self.PoperednihPologivNeByloP5CheckBox.setEnabled(1)

    def PoperedniPologuYskladneniFunc(self):
        if self.PoperedniPologuYskladneniCheckBox.isChecked():
            self.PoperedniPologuFiziologichniCheckBox.setEnabled(0)
            self.PoperedniPologuPatologichniCheckBox.setEnabled(0)
            self.PoperednihPologivNeByloP5CheckBox.setEnabled(0)
            self.PoperedniPologuYskladneniLineEdit.show()
        else:
            self.PoperedniPologuFiziologichniCheckBox.setEnabled(1)
            self.PoperedniPologuPatologichniCheckBox.setEnabled(1)
            self.PoperednihPologivNeByloP5CheckBox.setEnabled(1)
            self.PoperedniPologuYskladneniLineEdit.hide()

    def PoperednihPologivNeByloP5Func(self):
        if self.PoperednihPologivNeByloP5CheckBox.isChecked():
            self.PoperedniPologuFiziologichniCheckBox.setEnabled(0)
            self.PoperedniPologuPatologichniCheckBox.setEnabled(0)
            self.PoperedniPologuYskladneniCheckBox.setEnabled(0)
        else:
            self.PoperedniPologuFiziologichniCheckBox.setEnabled(1)
            self.PoperedniPologuPatologichniCheckBox.setEnabled(1)
            self.PoperedniPologuYskladneniCheckBox.setEnabled(1)

            # Обработчик 6)	Наявність живих дітей а) так б) ні

    def NayavnistGuvyhDiteyYesFunc(self):
        if self.NayavnistGuvyhDiteyYesCheckBox.isChecked():
            self.NayavnistGuvyhDiteyNoCheckBox.setEnabled(0)
            self.NayavnistGuvyhDiteyNoCheckBox.setChecked(0)
        else:
            self.NayavnistGuvyhDiteyNoCheckBox.setEnabled(1)
            self.NayavnistGuvyhDiteyNoCheckBox.setChecked(1)
            self.NayavnistGuvyhDiteyYesCheckBox.setEnabled(0)

    def NayavnistGuvyhDiteyNoFunc(self):
        if self.NayavnistGuvyhDiteyNoCheckBox.isChecked():
            self.NayavnistGuvyhDiteyYesCheckBox.setEnabled(0)
        else:
            self.NayavnistGuvyhDiteyYesCheckBox.setEnabled(1)
            self.NayavnistGuvyhDiteyYesCheckBox.setChecked(1)
            self.NayavnistGuvyhDiteyNoCheckBox.setEnabled(0)
            self.NayavnistGuvyhDiteyNoCheckBox.setChecked(0)

            # Обработчик 1) Вагітність: а) одноплідна;  б) багатоплідна

    def VagitnistOdnoplidnaFunc(self):
        if self.VagitnistOdnoplidnaCheckBox.isChecked():
            self.VagitnistBagatodnoplidnaCheckBox.setEnabled(0)
            self.VagitnistBagatodnoplidnaCheckBox.setChecked(0)
        else:
            self.VagitnistBagatodnoplidnaCheckBox.setEnabled(1)
            self.VagitnistBagatodnoplidnaCheckBox.setChecked(1)
            self.VagitnistOdnoplidnaCheckBox.setEnabled(0)

    def VagitnistBagatoplidnaFunc(self):
        if self.VagitnistBagatodnoplidnaCheckBox.isChecked():
            self.VagitnistOdnoplidnaCheckBox.setEnabled(0)
            self.VagitnistOdnoplidnaCheckBox.setChecked(0)
        else:
            self.VagitnistOdnoplidnaCheckBox.setEnabled(1)
            self.VagitnistOdnoplidnaCheckBox.setChecked(1)
            self.VagitnistBagatodnoplidnaCheckBox.setEnabled(0)
            self.VagitnistBagatodnoplidnaCheckBox.setChecked(0)

            # Обработчик Загроза переривання вагітності: а) ні  б) в терміні вагітності ____.

    def ZagrozaPereruvannaVagitnostiYesFunc(self):
        if self.ZagrozaPereruvannaVagitnostiYesCheckBox.isChecked():
            self.ZagrozaPereruvannaVagitnostiNoCheckBox.setChecked(0)
            self.ZagrozaPereruvannaVagitnostiNoCheckBox.setEnabled(0)
        else:
            self.ZagrozaPereruvannaVagitnostiNoCheckBox.setEnabled(1)
            self.ZagrozaPereruvannaVagitnostiNoCheckBox.setChecked(1)
            self.ZagrozaPereruvannaVagitnostiYTerminiLabel.hide()
            self.ZagrozaPereruvannaVagitnostiYTerminiLineEdit.hide()

    def ZagrozaPereruvannaVagitnostiNoFunc(self):
        if self.ZagrozaPereruvannaVagitnostiNoCheckBox.isChecked():
            self.ZagrozaPereruvannaVagitnostiYesCheckBox.setChecked(0)
            self.ZagrozaPereruvannaVagitnostiYesCheckBox.setEnabled(0)
        else:
            self.ZagrozaPereruvannaVagitnostiYesCheckBox.setEnabled(1)
            self.ZagrozaPereruvannaVagitnostiYesCheckBox.setChecked(1)
            self.ZagrozaPereruvannaVagitnostiYesCheckBox.setFixedWidth(40)
            self.ZagrozaPereruvannaVagitnostiYTerminiLabel.show()
            self.ZagrozaPereruvannaVagitnostiYTerminiLabel.setFixedWidth(98)
            self.ZagrozaPereruvannaVagitnostiYTerminiLineEdit.show()
            self.ZagrozaPereruvannaVagitnostiYTerminiLineEdit.setFixedWidth(30)

            # Обработчик Загроза передчасних пологів:    а) ні  б) в терміні вагітності  ____. ZagrozaPeredchasnuhPologivNoFunc
            # 4.1 а відшарування хоріона; б) кровомазання в) ІЦН

    def ZagrozaPeredchasnuhPologivYesFunc(self):
        if self.ZagrozaPeredchasnuhPologivYesCheckBox.isChecked():
            self.ZagrozaPeredchasnuhPologivNoCheckBox.setChecked(0)
            self.ZagrozaPeredchasnuhPologivNoCheckBox.setEnabled(0)
        else:
            self.ZagrozaPeredchasnuhPologivNoCheckBox.setEnabled(1)
            self.ZagrozaPeredchasnuhPologivNoCheckBox.setChecked(1)
            self.ZagrozaPeredchasnuhPologivTerminiLabel.hide()
            self.ZagrozaPeredchasnuhPologivYTerminiLineEdit.hide()
            self.ZagrozaPereruvannaVagitnostiVidsharyvannaHorionaCheckBox.setEnabled(
                0)
            self.ZagrozaPereruvannaVagitnostiVidsharyvannaHorionaCheckBox.setChecked(
                0)
            self.ZagrozaPereruvannaVagitnostiKrovomazannaCheckBox.setEnabled(0)
            self.ZagrozaPereruvannaVagitnostiKrovomazannaCheckBox.setChecked(0)
            self.ZagrozaPereruvannaVagitnostiICNCheckBox.setEnabled(0)
            self.ZagrozaPereruvannaVagitnostiICNCheckBox.setChecked(0)
            self.ZagrozaPereruvannaVagitnostiP41Label.setEnabled(0)

    def ZagrozaPeredchasnuhPologivNoFunc(self):
        if self.ZagrozaPeredchasnuhPologivNoCheckBox.isChecked():
            self.ZagrozaPeredchasnuhPologivYesCheckBox.setChecked(0)
            self.ZagrozaPeredchasnuhPologivYesCheckBox.setEnabled(0)
        else:
            self.ZagrozaPeredchasnuhPologivYesCheckBox.setEnabled(1)
            self.ZagrozaPeredchasnuhPologivYesCheckBox.setChecked(1)
            self.ZagrozaPeredchasnuhPologivYesCheckBox.setFixedWidth(50)
            self.ZagrozaPeredchasnuhPologivTerminiLabel.show()
            self.ZagrozaPeredchasnuhPologivTerminiLabel.setFixedWidth(98)
            self.ZagrozaPeredchasnuhPologivYTerminiLineEdit.show()
            self.ZagrozaPeredchasnuhPologivYTerminiLineEdit.setFixedWidth(30)
            self.ZagrozaPereruvannaVagitnostiVidsharyvannaHorionaCheckBox.setEnabled(
                1)
            self.ZagrozaPereruvannaVagitnostiKrovomazannaCheckBox.setEnabled(1)
            self.ZagrozaPereruvannaVagitnostiICNCheckBox.setEnabled(1)
        self.ZagrozaPereruvannaVagitnostiP41Label.setEnabled(1)

    # Обработчик 5) Гестоз І половини вагітності: а) так  б) ні.
    def GestozIPolovunuVagitnostiNoFunc(self):
        if self.GestozIPolovunuVagitnostiNoCheckBox.isChecked():
            self.GestozIPolovunuVagitnostiYesCheckBox.setChecked(0)
            self.GestozIPolovunuVagitnostiYesCheckBox.setEnabled(0)
        else:
            self.GestozIPolovunuVagitnostiYesCheckBox.setChecked(1)
            self.GestozIPolovunuVagitnostiYesCheckBox.setEnabled(1)

    def GestozIPolovunuVagitnostiYesFunc(self):
        if self.GestozIPolovunuVagitnostiYesCheckBox.isChecked():
            self.GestozIPolovunuVagitnostiNoCheckBox.setEnabled(0)
            self.GestozIPolovunuVagitnostiNoCheckBox.setChecked(0)
        else:
            self.GestozIPolovunuVagitnostiNoCheckBox.setEnabled(1)
            self.GestozIPolovunuVagitnostiNoCheckBox.setChecked(1)

            # Обработчик 6) Інші причини зневоднення: а) так  б) ні; в)____________________ InshiPruchynyZnevodnennaVarVFunc

    def InshiPruchynyZnevodnennaNoFunc(self):
        if self.InshiPruchynyZnevodnennaNoCheckBox.isChecked():
            self.InshiPruchynyZnevodnennaYesCheckBox.setDisabled(1)
            self.InshiPruchynyZnevodnennaVarVCheckBox.setDisabled(1)
        else:
            self.InshiPruchynyZnevodnennaYesCheckBox.setEnabled(1)
            self.InshiPruchynyZnevodnennaVarVCheckBox.setEnabled(1)

    def InshiPruchynyZnevodnennaYesFunc(self):
        if self.InshiPruchynyZnevodnennaYesCheckBox.isChecked():
            self.InshiPruchynyZnevodnennaNoCheckBox.setDisabled(1)
            self.InshiPruchynyZnevodnennaVarVCheckBox.setDisabled(1)
        else:
            self.InshiPruchynyZnevodnennaNoCheckBox.setEnabled(1)
            self.InshiPruchynyZnevodnennaVarVCheckBox.setEnabled(1)

    def InshiPruchynyZnevodnennaVarVFunc(self):
        if self.InshiPruchynyZnevodnennaVarVCheckBox.isChecked():
            self.InshiPruchynyZnevodnennaNoCheckBox.setDisabled(1)
            self.InshiPruchynyZnevodnennaYesCheckBox.setDisabled(1)
            self.InshiPruchynyZnevodnennaVarVLineEdit.show()
            self.InshiPruchynyZnevodnennaVarVLineEdit.setEnabled(1)
        else:
            self.InshiPruchynyZnevodnennaNoCheckBox.setEnabled(1)
            self.InshiPruchynyZnevodnennaYesCheckBox.setEnabled(1)
            self.InshiPruchynyZnevodnennaVarVLineEdit.setDisabled(1)
            self.InshiPruchynyZnevodnennaVarVLineEdit.hide()

            # Обработчик Гестоз II половини вагітності GestozIIPolovunuVagitnostiNoFunc

    def GestozIIPolovunuVagitnostiNoFunc(self):
        if self.GestozIIPolovunuVagitnostiNoCheckBox.isChecked():
            self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.setChecked(
                0)
            self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.setEnabled(
                0)
            self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.setChecked(
                0)
            self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.setEnabled(
                0)
            self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.setChecked(
                0)
            self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.setEnabled(
                0)
            self.GestozIIPolovunuDiagnostovanoVTerminiLabel.setEnabled(0)
            self.GestozIIPolovunuDiagnostovanoVTerminiLineEdit.setText('')
            self.GestozIIPolovunuDiagnostovanoVTerminiLineEdit.setEnabled(0)
        else:
            self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.setEnabled(
                1)
            self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.setEnabled(
                1)
            self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.setEnabled(
                1)
            self.GestozIIPolovunuDiagnostovanoVTerminiLabel.setEnabled(1)
            self.GestozIIPolovunuDiagnostovanoVTerminiLineEdit.setEnabled(1)

    def GestozIIPolovunuVagitnostiProeklampsiaLegkogoStFunc(self):
        if self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.isChecked(
        ):
            self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.setEnabled(
                0)
            self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.setChecked(
                0)
            self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.setChecked(
                0)
            self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.setEnabled(
                0)
            self.GestozIIPolovunuVagitnostiNoCheckBox.setChecked(0)
            self.GestozIIPolovunuVagitnostiNoCheckBox.setEnabled(0)
        else:
            self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.setEnabled(
                1)
            self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.setEnabled(
                1)
            self.GestozIIPolovunuVagitnostiNoCheckBox.setEnabled(1)

    def GestozIIPolovunuVagitnostiProeklampsiaSerednogoStFunc(self):
        if self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.isChecked(
        ):
            self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.setEnabled(
                0)
            self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.setChecked(
                0)
            self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.setChecked(
                0)
            self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.setEnabled(
                0)
            self.GestozIIPolovunuVagitnostiNoCheckBox.setChecked(0)
            self.GestozIIPolovunuVagitnostiNoCheckBox.setEnabled(0)
        else:
            self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.setEnabled(
                1)
            self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.setEnabled(
                1)
            self.GestozIIPolovunuVagitnostiNoCheckBox.setEnabled(1)

    def GestozIIPolovunuVagitnostiProeklampsiaVagkogoStFunc(self):
        if self.GestozIIPolovunuVagitnostiProeklampsiaVagkogoStCheckBox.isChecked(
        ):
            self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.setEnabled(
                0)
            self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.setChecked(
                0)
            self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.setChecked(
                0)
            self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.setEnabled(
                0)
            self.GestozIIPolovunuVagitnostiNoCheckBox.setChecked(0)
            self.GestozIIPolovunuVagitnostiNoCheckBox.setEnabled(0)
        else:
            self.GestozIIPolovunuVagitnostiProeklampsiaLegkogoStCheckBox.setEnabled(
                1)
            self.GestozIIPolovunuVagitnostiProeklampsiaSerednogoStCheckBox.setEnabled(
                1)
            self.GestozIIPolovunuVagitnostiNoCheckBox.setEnabled(1)

            # Обработчик 9) Винекнення ТЕУ а) так  б) ні.

        # 9.1. Вид ТЕУ______________________________________________
        # 9.2. термін вагітності __________тиж

    def VunuknennaTEYYesFunc(self):
        if self.VunuknennaTEYYesCheckBox.isChecked():
            self.VunuknennaTEYYesCheckBox.setChecked(1)
        else:
            self.VunuknennaTEYYesCheckBox.setEnabled(0)
            self.VunuknennaTEYYesCheckBox.setChecked(0)
            self.VunuknennaTEYNoCheckBox.setEnabled(1)
            self.VunuknennaTEYNoCheckBox.setChecked(1)
            self.TEYTerminVagitnostiLabel.setEnabled(0)
            self.TEYTerminVagitnostiLineEdit.setEnabled(0)
            self.TEYTerminVagitnostiLineEdit.setText('')
            self.VudTEYLabel.setEnabled(0)
            self.VudTEYLineEdit.setEnabled(0)
            self.VudTEYLineEdit.setText('')

    def VunuknennaTEYNoFunc(self):
        if self.VunuknennaTEYNoCheckBox.isChecked():
            self.VunuknennaTEYNoCheckBox.setChecked(1)
        else:
            self.VunuknennaTEYYesCheckBox.setChecked(1)
            self.VunuknennaTEYYesCheckBox.setEnabled(1)
            self.VunuknennaTEYNoCheckBox.setEnabled(0)
            self.VunuknennaTEYNoCheckBox.setChecked(0)
            self.TEYTerminVagitnostiLabel.setEnabled(1)
            self.TEYTerminVagitnostiLineEdit.setEnabled(1)
            self.VudTEYLabel.setEnabled(1)
            self.VudTEYLineEdit.setEnabled(1)

            # Обработчик 10) Багатоводдя: а) ні  б) помірне в) виражене   BagatovoddaVurageneFunc BagatovoddaPomirneFunc BagatovoddaNoFunc

    def BagatovoddaVurageneFunc(self):
        if self.BagatovoddaVurageneCheckBox.isChecked():
            self.BagatovoddaPomirneCheckBox.setEnabled(0)
            self.BagatovoddaPomirneCheckBox.setChecked(0)
            self.BagatovoddaNoCheckBox.setChecked(0)
            self.BagatovoddaNoCheckBox.setEnabled(0)
            self.BagatovoddaDiagnostovanoVTerminVagitnostiLabel.setEnabled(1)
            self.BagatovoddaDiagnostovanoVTerminVagitnostiLineEdit.setEnabled(
                1)
        else:
            self.BagatovoddaPomirneCheckBox.setEnabled(1)
            self.BagatovoddaNoCheckBox.setEnabled(1)

    def BagatovoddaPomirneFunc(self):
        if self.BagatovoddaPomirneCheckBox.isChecked():
            self.BagatovoddaNoCheckBox.setEnabled(0)
            self.BagatovoddaNoCheckBox.setChecked(0)
            self.BagatovoddaVurageneCheckBox.setEnabled(0)
            self.BagatovoddaVurageneCheckBox.setChecked(0)
            self.BagatovoddaDiagnostovanoVTerminVagitnostiLabel.setEnabled(1)
            self.BagatovoddaDiagnostovanoVTerminVagitnostiLineEdit.setEnabled(
                1)
        else:
            self.BagatovoddaNoCheckBox.setEnabled(1)
            self.BagatovoddaVurageneCheckBox.setEnabled(1)

    def BagatovoddaNoFunc(self):
        if self.BagatovoddaNoCheckBox.isChecked():
            self.BagatovoddaPomirneCheckBox.setChecked(0)
            self.BagatovoddaPomirneCheckBox.setEnabled(0)
            self.BagatovoddaVurageneCheckBox.setEnabled(0)
            self.BagatovoddaVurageneCheckBox.setChecked(0)
            self.BagatovoddaDiagnostovanoVTerminVagitnostiLabel.setEnabled(0)
            self.BagatovoddaDiagnostovanoVTerminVagitnostiLineEdit.setText('')
            self.BagatovoddaDiagnostovanoVTerminVagitnostiLineEdit.setEnabled(
                0)
        else:
            self.BagatovoddaPomirneCheckBox.setEnabled(1)
            self.BagatovoddaVurageneCheckBox.setEnabled(1)

            # Обработчик 11) Маловоддя: а) ні  б) помірне  в) виражене

    def MaloVoddaVurageneFunc(self):
        if self.MaloVoddaVurageneCheckBox.isChecked():
            self.MaloVoddaPomirneCheckBox.setEnabled(0)
            self.MaloVoddaPomirneCheckBox.setChecked(0)
            self.MaloVoddaNoCheckBox.setChecked(0)
            self.MaloVoddaNoCheckBox.setEnabled(0)
            self.MaloVoddaDiagnostovanoVTerminVagitnostiLabel.setEnabled(1)
            self.MaloVoddaDiagnostovanoVTerminVagitnostiLineEdit.setEnabled(1)
        else:
            self.MaloVoddaPomirneCheckBox.setEnabled(1)
            self.MaloVoddaNoCheckBox.setEnabled(1)

    def MaloVoddaPomirneFunc(self):
        if self.MaloVoddaPomirneCheckBox.isChecked():
            self.MaloVoddaNoCheckBox.setEnabled(0)
            self.MaloVoddaNoCheckBox.setChecked(0)
            self.MaloVoddaVurageneCheckBox.setEnabled(0)
            self.MaloVoddaVurageneCheckBox.setChecked(0)
            self.MaloVoddaDiagnostovanoVTerminVagitnostiLabel.setEnabled(1)
            self.MaloVoddaDiagnostovanoVTerminVagitnostiLineEdit.setEnabled(1)
        else:
            self.MaloVoddaNoCheckBox.setEnabled(1)
            self.MaloVoddaVurageneCheckBox.setEnabled(1)

    def MaloVoddaNoFunc(self):
        if self.MaloVoddaNoCheckBox.isChecked():
            self.MaloVoddaPomirneCheckBox.setChecked(0)
            self.MaloVoddaPomirneCheckBox.setEnabled(0)
            self.MaloVoddaVurageneCheckBox.setEnabled(0)
            self.MaloVoddaVurageneCheckBox.setChecked(0)
            self.MaloVoddaDiagnostovanoVTerminVagitnostiLabel.setEnabled(0)
            self.MaloVoddaDiagnostovanoVTerminVagitnostiLineEdit.setText('')
            self.MaloVoddaDiagnostovanoVTerminVagitnostiLineEdit.setEnabled(0)
        else:
            self.MaloVoddaPomirneCheckBox.setEnabled(1)
            self.MaloVoddaVurageneCheckBox.setEnabled(1)

            # Обработчик 12) Дистрес плода (за доплерометрією): а) ні;
            # б) в ст. компенсації; в) в ст. субкомпенсації; г) в ст. декомпенсації
            # DustressPlodaNoFunc DustressPlodaVKompensaciiFunc DustressPlodaVSubKompensaciiFunc DustressPlodaVSubKompensaciiFunc

    def DustressPlodaNoFunc(self):
        if self.DustressPlodaNoCheckBox.isChecked():
            self.DustressPlodaVDekompensaciiCheckBox.setEnabled(0)
            self.DustressPlodaVKompensaciiCheckBox.setEnabled(0)
            self.DustressPlodaVSubKompensaciiCheckBox.setEnabled(0)
        else:
            self.DustressPlodaVDekompensaciiCheckBox.setEnabled(1)
            self.DustressPlodaVKompensaciiCheckBox.setEnabled(1)
            self.DustressPlodaVSubKompensaciiCheckBox.setEnabled(1)

    def DustressPlodaVKompensaciiFunc(self):
        if self.DustressPlodaVKompensaciiCheckBox.isChecked():
            self.DustressPlodaVSubKompensaciiCheckBox.setEnabled(0)
            self.DustressPlodaVDekompensaciiCheckBox.setEnabled(0)
            self.DustressPlodaNoCheckBox.setEnabled(0)
        else:
            self.DustressPlodaVSubKompensaciiCheckBox.setEnabled(1)
            self.DustressPlodaVDekompensaciiCheckBox.setEnabled(1)
            self.DustressPlodaNoCheckBox.setEnabled(1)

    def DustressPlodaVSubKompensaciiFunc(self):
        if self.DustressPlodaVSubKompensaciiCheckBox.isChecked():
            self.DustressPlodaNoCheckBox.setEnabled(0)
            self.DustressPlodaVDekompensaciiCheckBox.setEnabled(0)
            self.DustressPlodaVKompensaciiCheckBox.setEnabled(0)
        else:
            self.DustressPlodaNoCheckBox.setEnabled(1)
            self.DustressPlodaVDekompensaciiCheckBox.setEnabled(1)
            self.DustressPlodaVKompensaciiCheckBox.setEnabled(1)

    def DustressPlodaVDekompensaciiFunc(self):
        if self.DustressPlodaVDekompensaciiCheckBox.isChecked():
            self.DustressPlodaNoCheckBox.setEnabled(0)
            self.DustressPlodaVSubKompensaciiCheckBox.setEnabled(0)
            self.DustressPlodaVKompensaciiCheckBox.setEnabled(0)
        else:
            self.DustressPlodaNoCheckBox.setEnabled(1)
            self.DustressPlodaVSubKompensaciiCheckBox.setEnabled(1)
            self.DustressPlodaVKompensaciiCheckBox.setEnabled(1)

            # обработчик 13) Затримка росту плода: 		в терміні _______тиж ZatrumkaRozvutkyPlodaNoFunc ZatrumkaRozvutkyPlodaSumetrychnaFormaFunc ZatrumkaRozvutkyPlodaAsumetruchnaFormaFunc

    def ZatrumkaRozvutkyPlodaNoFunc(self):
        if self.ZatrumkaRozvutkyPlodaNoCheckBox.isChecked():
            self.ZatrumkaRozvutkyPlodaSumetrychnaFormaCheckBox.setEnabled(0)
            self.ZatrumkaRozvutkyPlodaSumetrychnaFormaCheckBox.setChecked(0)
            self.ZatrumkaRozvutkyPlodaAsumetruchnaFormaCheckBox.setEnabled(0)
            self.ZatrumkaRozvutkyPlodaAsumetruchnaFormaCheckBox.setChecked(0)
            self.ZatrumkaRozvutkyPlodaVTerminiLabel.hide()
            self.ZatrumkaRozvutkyPlodaVTerminiLineEdit.hide()
            self.ZatrumkaRozvutkyPlodaVTerminiLineEdit.setText('')
        else:
            self.ZatrumkaRozvutkyPlodaSumetrychnaFormaCheckBox.setEnabled(1)
            self.ZatrumkaRozvutkyPlodaAsumetruchnaFormaCheckBox.setEnabled(1)

    def ZatrumkaRozvutkyPlodaSumetrychnaFormaFunc(self):
        if self.ZatrumkaRozvutkyPlodaSumetrychnaFormaCheckBox.isChecked():
            self.ZatrumkaRozvutkyPlodaNoCheckBox.setEnabled(0)
            self.ZatrumkaRozvutkyPlodaNoCheckBox.setChecked(0)
            self.ZatrumkaRozvutkyPlodaAsumetruchnaFormaCheckBox.setEnabled(0)
            self.ZatrumkaRozvutkyPlodaAsumetruchnaFormaCheckBox.setChecked(0)
            self.ZatrumkaRozvutkyPlodaVTerminiLabel.show()
            self.ZatrumkaRozvutkyPlodaVTerminiLabel.setEnabled(1)
            self.ZatrumkaRozvutkyPlodaVTerminiLineEdit.show()
            self.ZatrumkaRozvutkyPlodaVTerminiLineEdit.setEnabled(1)
        else:
            self.ZatrumkaRozvutkyPlodaNoCheckBox.setEnabled(1)
            self.ZatrumkaRozvutkyPlodaNoCheckBox.setChecked(0)
            self.ZatrumkaRozvutkyPlodaAsumetruchnaFormaCheckBox.setEnabled(1)
            self.ZatrumkaRozvutkyPlodaAsumetruchnaFormaCheckBox.setChecked(0)
            self.ZatrumkaRozvutkyPlodaVTerminiLabel.hide()
            self.ZatrumkaRozvutkyPlodaVTerminiLabel.setEnabled(0)
            self.ZatrumkaRozvutkyPlodaVTerminiLineEdit.hide()
            self.ZatrumkaRozvutkyPlodaVTerminiLineEdit.setEnabled(0)

    def ZatrumkaRozvutkyPlodaAsumetruchnaFormaFunc(self):
        if self.ZatrumkaRozvutkyPlodaAsumetruchnaFormaCheckBox.isChecked():
            self.ZatrumkaRozvutkyPlodaNoCheckBox.setEnabled(0)
            self.ZatrumkaRozvutkyPlodaNoCheckBox.setChecked(0)
            self.ZatrumkaRozvutkyPlodaSumetrychnaFormaCheckBox.setEnabled(0)
            self.ZatrumkaRozvutkyPlodaSumetrychnaFormaCheckBox.setChecked(0)
            self.ZatrumkaRozvutkyPlodaVTerminiLabel.show()
            self.ZatrumkaRozvutkyPlodaVTerminiLabel.setEnabled(1)
            self.ZatrumkaRozvutkyPlodaVTerminiLineEdit.show()
            self.ZatrumkaRozvutkyPlodaVTerminiLineEdit.setEnabled(1)
        else:
            self.ZatrumkaRozvutkyPlodaNoCheckBox.setEnabled(1)
            self.ZatrumkaRozvutkyPlodaNoCheckBox.setChecked(0)
            self.ZatrumkaRozvutkyPlodaSumetrychnaFormaCheckBox.setEnabled(1)
            self.ZatrumkaRozvutkyPlodaSumetrychnaFormaCheckBox.setChecked(0)
            self.ZatrumkaRozvutkyPlodaVTerminiLabel.hide()
            self.ZatrumkaRozvutkyPlodaVTerminiLabel.setEnabled(0)
            self.ZatrumkaRozvutkyPlodaVTerminiLineEdit.hide()
            self.ZatrumkaRozvutkyPlodaVTerminiLineEdit.setEnabled(0)

            # Обработчик 14) Наявність системної інфекції : 		а) так; б) ні NajavnistSustemnoiInfekciiYesFunc NajavnistSustemnoiInfekciiNoFunc

    def NajavnistSustemnoiInfekciiYesFunc(self):
        if self.NajavnistSustemnoiInfekciiYesCheckBox.isChecked():
            self.NajavnistSustemnoiInfekciiNoCheckBox.setEnabled(0)
            self.NajavnistSustemnoiInfekciiNoCheckBox.setChecked(0)
        else:
            self.NajavnistSustemnoiInfekciiNoCheckBox.setEnabled(1)
            self.NajavnistSustemnoiInfekciiNoCheckBox.setChecked(1)

    def NajavnistSustemnoiInfekciiNoFunc(self):
        if self.NajavnistSustemnoiInfekciiNoCheckBox.isChecked():
            self.NajavnistSustemnoiInfekciiYesCheckBox.setEnabled(0)
            self.NajavnistSustemnoiInfekciiYesCheckBox.setChecked(0)
        else:
            self.NajavnistSustemnoiInfekciiYesCheckBox.setEnabled(1)
            self.NajavnistSustemnoiInfekciiYesCheckBox.setChecked(1)

            # Обработчик 15) Патологія плаценти 			а) ні б) гіпоплазія в) гіперплазія PatologiaPlacentuNoFunc PatologiaPlacentuGipoplaziaFunc  PatologiaPlacentuGiperplaziaFunc

    def PatologiaPlacentuNoFunc(self):
        if self.PatologiaPlacentuNoCheckBox.isChecked():
            self.PatologiaPlacentuGiperplaziaCheckBox.setEnabled(0)
            self.PatologiaPlacentuGiperplaziaCheckBox.setChecked(0)
            self.PatologiaPlacentuGipoplaziaCheckBox.setChecked(0)
            self.PatologiaPlacentuGipoplaziaCheckBox.setEnabled(0)
        else:
            self.PatologiaPlacentuGiperplaziaCheckBox.setEnabled(1)
            self.PatologiaPlacentuGipoplaziaCheckBox.setEnabled(1)

    def PatologiaPlacentuGipoplaziaFunc(self):
        if self.PatologiaPlacentuGipoplaziaCheckBox.isChecked():
            self.PatologiaPlacentuGiperplaziaCheckBox.setEnabled(0)
            self.PatologiaPlacentuGiperplaziaCheckBox.setChecked(0)
            self.PatologiaPlacentuNoCheckBox.setChecked(0)
            self.PatologiaPlacentuNoCheckBox.setEnabled(0)
        else:
            self.PatologiaPlacentuGiperplaziaCheckBox.setEnabled(1)
            self.PatologiaPlacentuNoCheckBox.setEnabled(1)

    def PatologiaPlacentuGiperplaziaFunc(self):
        if self.PatologiaPlacentuGiperplaziaCheckBox.isChecked():
            self.PatologiaPlacentuGipoplaziaCheckBox.setEnabled(0)
            self.PatologiaPlacentuGipoplaziaCheckBox.setChecked(0)
            self.PatologiaPlacentuNoCheckBox.setChecked(0)
            self.PatologiaPlacentuNoCheckBox.setEnabled(0)
        else:
            self.PatologiaPlacentuGipoplaziaCheckBox.setEnabled(1)
            self.PatologiaPlacentuNoCheckBox.setEnabled(1)

            # Обработчик15.1. Паталогія  локалізації плаценти:        а) ні;
            #  #PatologiaLocalizaciiPlacentuNoFunc  PatologiaLocalizaciiPlacentuNuzkaPlacentaciaFunc PatologiaLocalizaciiPlacentuKrajovePeredlegannaFunc  PatologiaLocalizaciiPlacentuPovnePeredlegannaFunc

    def PatologiaLocalizaciiPlacentuNoFunc(self):
        if self.PatologiaLocalizaciiPlacentuNoCheckBox.isChecked():
            self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaCheckBox.setEnabled(
                0)
            self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaCheckBox.setChecked(
                0)
            self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaCheckBox.setChecked(
                0)
            self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaCheckBox.setEnabled(
                0)
            self.PatologiaLocalizaciiPlacentuPovnePeredlegannaCheckBox.setChecked(
                0)
            self.PatologiaLocalizaciiPlacentuPovnePeredlegannaCheckBox.setEnabled(
                0)
        else:
            self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaCheckBox.setEnabled(
                1)
            self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaCheckBox.setEnabled(
                1)
            self.PatologiaLocalizaciiPlacentuPovnePeredlegannaCheckBox.setEnabled(
                1)

    def PatologiaLocalizaciiPlacentuNuzkaPlacentaciaFunc(self):
        if self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaCheckBox.isChecked(
        ):
            self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaCheckBox.setEnabled(
                0)
            self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaCheckBox.setChecked(
                0)
            self.PatologiaLocalizaciiPlacentuNoCheckBox.setChecked(0)
            self.PatologiaLocalizaciiPlacentuNoCheckBox.setEnabled(0)
            self.PatologiaLocalizaciiPlacentuPovnePeredlegannaCheckBox.setChecked(
                0)
            self.PatologiaLocalizaciiPlacentuPovnePeredlegannaCheckBox.setEnabled(
                0)
        else:
            self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaCheckBox.setEnabled(
                1)
            self.PatologiaLocalizaciiPlacentuNoCheckBox.setEnabled(1)
            self.PatologiaLocalizaciiPlacentuPovnePeredlegannaCheckBox.setEnabled(
                1)

    def PatologiaLocalizaciiPlacentuKrajovePeredlegannaFunc(self):
        if self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaCheckBox.isChecked(
        ):
            self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaCheckBox.setEnabled(
                0)
            self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaCheckBox.setChecked(
                0)
            self.PatologiaLocalizaciiPlacentuNoCheckBox.setChecked(0)
            self.PatologiaLocalizaciiPlacentuNoCheckBox.setEnabled(0)
            self.PatologiaLocalizaciiPlacentuPovnePeredlegannaCheckBox.setChecked(
                0)
            self.PatologiaLocalizaciiPlacentuPovnePeredlegannaCheckBox.setEnabled(
                0)
        else:
            self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaCheckBox.setEnabled(
                1)
            self.PatologiaLocalizaciiPlacentuNoCheckBox.setEnabled(1)
            self.PatologiaLocalizaciiPlacentuPovnePeredlegannaCheckBox.setEnabled(
                1)

    def PatologiaLocalizaciiPlacentuPovnePeredlegannaFunc(self):
        if self.PatologiaLocalizaciiPlacentuPovnePeredlegannaCheckBox.isChecked(
        ):
            self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaCheckBox.setEnabled(
                0)
            self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaCheckBox.setChecked(
                0)
            self.PatologiaLocalizaciiPlacentuNoCheckBox.setChecked(0)
            self.PatologiaLocalizaciiPlacentuNoCheckBox.setEnabled(0)
            self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaCheckBox.setChecked(
                0)
            self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaCheckBox.setEnabled(
                0)
        else:
            self.PatologiaLocalizaciiPlacentuNuzkaPlacentaciaCheckBox.setEnabled(
                1)
            self.PatologiaLocalizaciiPlacentuNoCheckBox.setEnabled(1)
            self.PatologiaLocalizaciiPlacentuKrajovePeredlegannaCheckBox.setEnabled(
                1)

            # Обработчик 16) Передчасне відшарування плаценти 	а) ні б) так PeredchasneVadsharyvannaPlacentuNoFunc PeredchasneVadsharyvannaPlacentuYesFunc

    def PeredchasneVadsharyvannaPlacentuNoFunc(self):
        if self.PeredchasneVadsharyvannaPlacentuNoCheckBox.isChecked():
            pass
        else:
            self.PeredchasneVadsharyvannaPlacentuYesCheckBox.setEnabled(1)
            self.PeredchasneVadsharyvannaPlacentuYesCheckBox.setChecked(1)
            self.PeredchasneVadsharyvannaPlacentuNoCheckBox.setEnabled(0)

    def PeredchasneVadsharyvannaPlacentuYesFunc(self):
        if self.PeredchasneVadsharyvannaPlacentuYesCheckBox.isChecked():
            pass
        else:
            self.PeredchasneVadsharyvannaPlacentuNoCheckBox.setEnabled(1)
            self.PeredchasneVadsharyvannaPlacentuNoCheckBox.setChecked(1)
            self.PeredchasneVadsharyvannaPlacentuYesCheckBox.setEnabled(0)

            # Обработчик 17) Хірургічні втручання під час вагітності: а) так; б) ні PeredchasneVadsharyvannaPlacentuNoFunc PeredchasneVadsharyvannaPlacentuYesFunc

    def HiryrgichniVtyrchannaPidChasVagitnostiNoFunc(self):
        if self.HiryrgichniVtyrchannaPidChasVagitnostiNoCheckBox.isChecked():
            pass
        else:
            self.HiryrgichniVtyrchannaPidChasVagitnostiYesCheckBox.setEnabled(
                1)
            self.HiryrgichniVtyrchannaPidChasVagitnostiYesCheckBox.setChecked(
                1)
            self.HiryrgichniVtyrchannaPidChasVagitnostiNoCheckBox.setEnabled(0)

    def HiryrgichniVtyrchannaPidChasVagitnostiYesFunc(self):
        if self.HiryrgichniVtyrchannaPidChasVagitnostiYesCheckBox.isChecked():
            pass
        else:
            self.HiryrgichniVtyrchannaPidChasVagitnostiNoCheckBox.setEnabled(1)
            self.HiryrgichniVtyrchannaPidChasVagitnostiNoCheckBox.setChecked(1)
            self.HiryrgichniVtyrchannaPidChasVagitnostiYesCheckBox.setEnabled(
                0)

            # Обработчик 18) Тривала іммобілізація: а) так; б) ні  TruvalaImmobilizaciaNoFunc TruvalaImmobilizaciaYesFunc

    def TruvalaImmobilizaciaNoFunc(self):
        """18) Тривала іммобілізація а) так"""
        if self.TruvalaImmobilizaciaNoCheckBox.isChecked():
            pass
        else:
            self.TruvalaImmobilizaciaYesCheckBox.setEnabled(1)
            self.TruvalaImmobilizaciaYesCheckBox.setChecked(1)
            self.TruvalaImmobilizaciaNoCheckBox.setEnabled(0)

    def TruvalaImmobilizaciaYesFunc(self):
        """18) Тривала іммобілізація а) ні"""
        if self.TruvalaImmobilizaciaYesCheckBox.isChecked():
            pass
        else:
            self.TruvalaImmobilizaciaNoCheckBox.setEnabled(1)
            self.TruvalaImmobilizaciaNoCheckBox.setChecked(1)
            self.TruvalaImmobilizaciaYesCheckBox.setEnabled(0)

            # Обработчик 19) Завершення даної вагітності
            # а) переривання за медичними показаннями в терміні_______.
            # б) самовільний викидень в терміні_______.
            # в) пологи в терміні_______.
            # ZavershennaDannoiVagitnostiPologuVTerminiFunc ZavershennaDannoiVagitnostiPereryvannaZaMedPokFunc ZavershennaDannoiVagitnostiSamovilnuiVukudenFunc

    def ZavershennaDannoiVagitnostiPologuVTerminiFunc(self):
        if self.ZavershennaDannoiVagitnostiPologuVTerminiCheckBox.isChecked():

            self.ZavershennaDannoiVagitnostiPologuVTerminiLineEdit.setEnabled(
                1)
            self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokCheckBox.setEnabled(
                0)
            self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokCheckBox.setChecked(
                0)
            self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokLineEdit.setEnabled(
                0)
            self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokLineEdit.setText(
                '')
            self.ZavershennaDannoiVagitnostiSamovilnuiVukudenCheckBox.setEnabled(
                0)
            self.ZavershennaDannoiVagitnostiSamovilnuiVukudenCheckBox.setChecked(
                0)
            self.ZavershennaDannoiVagitnostiSamovilnuiVukudenLineEdit.setEnabled(
                0)
            self.ZavershennaDannoiVagitnostiSamovilnuiVukudenLineEdit.setText(
                '')
        else:
            self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokCheckBox.setEnabled(
                1)
            self.ZavershennaDannoiVagitnostiSamovilnuiVukudenCheckBox.setEnabled(
                1)
            self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokLineEdit.setEnabled(
                1)
            self.ZavershennaDannoiVagitnostiSamovilnuiVukudenLineEdit.setEnabled(
                1)

    def ZavershennaDannoiVagitnostiPereryvannaZaMedPokFunc(self):
        if self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokCheckBox.isChecked(
        ):
            self.ZavershennaDannoiVagitnostiPologuVTerminiCheckBox.setEnabled(
                0)
            self.ZavershennaDannoiVagitnostiPologuVTerminiCheckBox.setChecked(
                0)
            self.ZavershennaDannoiVagitnostiPologuVTerminiLineEdit.setText('')
            self.ZavershennaDannoiVagitnostiPologuVTerminiLineEdit.setEnabled(
                0)
            self.ZavershennaDannoiVagitnostiSamovilnuiVukudenCheckBox.setChecked(
                0)
            self.ZavershennaDannoiVagitnostiSamovilnuiVukudenCheckBox.setEnabled(
                0)
            self.ZavershennaDannoiVagitnostiSamovilnuiVukudenLineEdit.setText(
                '')
            self.ZavershennaDannoiVagitnostiSamovilnuiVukudenLineEdit.setEnabled(
                0)
        else:
            self.ZavershennaDannoiVagitnostiPologuVTerminiCheckBox.setEnabled(
                1)
            self.ZavershennaDannoiVagitnostiPologuVTerminiLineEdit.setEnabled(
                1)
            self.ZavershennaDannoiVagitnostiSamovilnuiVukudenCheckBox.setEnabled(
                1)
            self.ZavershennaDannoiVagitnostiSamovilnuiVukudenLineEdit.setEnabled(
                1)

    def ZavershennaDannoiVagitnostiSamovilnuiVukudenFunc(self):
        if self.ZavershennaDannoiVagitnostiSamovilnuiVukudenCheckBox.isChecked(
        ):
            self.ZavershennaDannoiVagitnostiPologuVTerminiCheckBox.setEnabled(
                0)
            self.ZavershennaDannoiVagitnostiPologuVTerminiCheckBox.setChecked(
                0)
            self.ZavershennaDannoiVagitnostiPologuVTerminiLineEdit.setText('')
            self.ZavershennaDannoiVagitnostiPologuVTerminiLineEdit.setEnabled(
                0)
            self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokCheckBox.setChecked(
                0)
            self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokCheckBox.setEnabled(
                0)
            self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokLineEdit.setText(
                '')
            self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokLineEdit.setEnabled(
                0)
        else:
            self.ZavershennaDannoiVagitnostiPologuVTerminiCheckBox.setEnabled(
                1)
            self.ZavershennaDannoiVagitnostiPologuVTerminiLineEdit.setEnabled(
                1)
            self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokCheckBox.setEnabled(
                1)
            self.ZavershennaDannoiVagitnostiPereryvannaZaMedPokLineEdit.setEnabled(
                1)
            # Обработчик VІ Проведення профілактики/терапії ТЕУ під час вагітності: а) так б)ні ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiYesFunc ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiNoFunc

    def ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiNoFunc(self):
        if self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiNoCheckBox.isChecked(
        ):
            self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiYesCheckBox.setEnabled(
                0)
        else:
            self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiYesCheckBox.setEnabled(
                1)
            self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiYesCheckBox.setChecked(
                1)
            self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiNoCheckBox.setEnabled(
                0)
            self.PokazuDlaProvedennaProfilaktukyLabel.setEnabled(1)
            self.PokazuDlaProvedennaProfilaktukyLineEdit.setEnabled(1)
            self.ElastychnaKompresiaPynktVILabel.setEnabled(1)
            # self.ElastychnaKompresiaPynktVIYesCheckBox.setEnabled(1)
            self.ElastychnaKompresiaPynktVINoCheckBox.setEnabled(1)
            self.ElastychnaKompresiaPynktVILevelLabel.setEnabled(1)
            self.ElastychnaKompresiaPynktVILevelLineEdit.setEnabled(1)
            self.MedukamentoznaProfilaktukaPynktVILabel.setEnabled(1)
            # self.MedukamentoznaProfilaktukaPynktVIYesCheckBox.setEnabled(1)
            self.MedukamentoznaProfilaktukaPynktVINoCheckBox.setEnabled(1)
            self.HiryrgichneLikyvannaPynktVILabel.setEnabled(1)
            # self.HiryrgichneLikyvannaPynktVIYesCheckBox.setEnabled(1)
            self.HiryrgichneLikyvannaPynktVINoCheckBox.setEnabled(1)
            self.TryvalistProvedennoiProfilaktykyPynktVILabel.setEnabled(1)
            self.TryvalistProvedennoiProfilaktykyPynktVILineEdit.setEnabled(1)
            self.YskladneenaVidProfilaktykuPynktVILabel.setEnabled(1)
            # self.YskladneenaVidProfilaktykuPynktVIYesCheckBox.setEnabled(1)
            self.YskladneenaVidProfilaktykuPynktVINoCheckBox.setEnabled(1)
            self.YskladneenaVidProfilaktykuNajavnistPynktVILabel.setEnabled(1)
            self.YskladneenaVidProfilaktykuNajavnistPynktVILineEdit.setEnabled(
                1)
            self.TerapiyVidminenoZaGodDoPologivPynktVILabel.setEnabled(1)
            self.TerapiyVidminenoZaGodDoPologivPynktVILineEdit.setEnabled(1)
            self.TerapiyVidminenoZaGodDoPologivPynktVILabel2.setEnabled(1)

    def ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiYesFunc(self):
        if self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiYesCheckBox.isChecked(
        ):
            self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiNoCheckBox.setEnabled(
                0)
        else:
            self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiNoCheckBox.setEnabled(
                1)
            self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiNoCheckBox.setChecked(
                1)
            self.ProvedennaProfilaktukuTerapiiTEYPidChasVagitnostiYesCheckBox.setEnabled(
                0)

            self.PokazuDlaProvedennaProfilaktukyLabel.setEnabled(0)
            self.PokazuDlaProvedennaProfilaktukyLineEdit.setEnabled(0)
            self.PokazuDlaProvedennaProfilaktukyLineEdit.setText('')

            self.ElastychnaKompresiaPynktVILabel.setEnabled(0)
            self.ElastychnaKompresiaPynktVIYesCheckBox.setEnabled(0)
            self.ElastychnaKompresiaPynktVIYesCheckBox.setChecked(0)
            self.ElastychnaKompresiaPynktVINoCheckBox.setEnabled(0)
            self.ElastychnaKompresiaPynktVINoCheckBox.setChecked(1)
            self.ElastychnaKompresiaPynktVILevelLabel.setEnabled(0)
            self.ElastychnaKompresiaPynktVILevelLabel.hide()
            self.ElastychnaKompresiaPynktVILevelLineEdit.setEnabled(0)
            self.ElastychnaKompresiaPynktVILevelLineEdit.setText('')
            self.ElastychnaKompresiaPynktVILevelLineEdit.hide()

            self.MedukamentoznaProfilaktukaPynktVILabel.setEnabled(0)
            self.MedukamentoznaProfilaktukaPynktVIYesCheckBox.setEnabled(0)
            self.MedukamentoznaProfilaktukaPynktVIYesCheckBox.setChecked(0)
            self.MedukamentoznaProfilaktukaPynktVINoCheckBox.setEnabled(0)
            self.MedukamentoznaProfilaktukaPynktVINoCheckBox.setChecked(1)
            self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLabel.hide()
            self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLineEdit.setEnabled(
                0)
            self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLineEdit.setText(
                '')
            self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLineEdit.hide()
            self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLabel.setEnabled(
                0)
            self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLabel.hide()
            self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLineEdit.setEnabled(
                0)
            self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLineEdit.setText(
                '')
            self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLineEdit.hide()
            self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLabel.setEnabled(
                0)
            self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLabel.hide(
            )
            self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLineEdit.setEnabled(
                0)
            self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLineEdit.setText(
                '')
            self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLineEdit.hide(
            )

            self.HiryrgichneLikyvannaPynktVILabel.setEnabled(0)
            self.HiryrgichneLikyvannaPynktVIYesCheckBox.setEnabled(0)
            self.HiryrgichneLikyvannaPynktVIYesCheckBox.setChecked(0)
            self.HiryrgichneLikyvannaPynktVINoCheckBox.setEnabled(0)
            self.HiryrgichneLikyvannaPynktVINoCheckBox.setChecked(1)
            self.HiryrgichneLikyvannaNazvaOpericiiPynktVILabel.setEnabled(0)
            self.HiryrgichneLikyvannaNazvaOpericiiPynktVILabel.hide()
            self.HiryrgichneLikyvannaNazvaOpericiiPynktVILineEdit.setEnabled(0)
            self.HiryrgichneLikyvannaNazvaOpericiiPynktVILineEdit.setText('')
            self.HiryrgichneLikyvannaNazvaOpericiiPynktVILineEdit.setText('')
            self.HiryrgichneLikyvannaNazvaOpericiiPynktVILineEdit.hide()

            self.TryvalistProvedennoiProfilaktykyPynktVILabel.setEnabled(0)
            self.TryvalistProvedennoiProfilaktykyPynktVILineEdit.setEnabled(0)
            self.TryvalistProvedennoiProfilaktykyPynktVILineEdit.setText('')
            self.TryvalistProvedennoiProfilaktykyPynktVILineEdit.setText('')

            self.YskladneenaVidProfilaktykuPynktVILabel.setEnabled(0)
            self.YskladneenaVidProfilaktykuPynktVIYesCheckBox.setEnabled(0)
            self.YskladneenaVidProfilaktykuPynktVIYesCheckBox.setChecked(0)
            self.YskladneenaVidProfilaktykuPynktVINoCheckBox.setEnabled(0)
            self.YskladneenaVidProfilaktykuPynktVINoCheckBox.setChecked(1)
            self.YskladneenaVidProfilaktykuNajavnistPynktVILabel.setEnabled(0)
            self.YskladneenaVidProfilaktykuNajavnistPynktVILabel.hide()
            self.YskladneenaVidProfilaktykuNajavnistPynktVILineEdit.setEnabled(
                0)
            self.YskladneenaVidProfilaktykuNajavnistPynktVILineEdit.setText('')
            self.YskladneenaVidProfilaktykuNajavnistPynktVILineEdit.hide()

            self.TerapiyVidminenoZaGodDoPologivPynktVILabel.setEnabled(0)
            self.TerapiyVidminenoZaGodDoPologivPynktVILineEdit.setEnabled(0)
            self.TerapiyVidminenoZaGodDoPologivPynktVILineEdit.setText('')
            self.TerapiyVidminenoZaGodDoPologivPynktVILabel2.setEnabled(0)

    def ElastychnaKompresiaPynktVINoFunc(self):
        if self.ElastychnaKompresiaPynktVINoCheckBox.isChecked():
            pass
        else:
            self.ElastychnaKompresiaPynktVIYesCheckBox.setEnabled(1)
            self.ElastychnaKompresiaPynktVIYesCheckBox.setChecked(1)
            self.ElastychnaKompresiaPynktVINoCheckBox.setEnabled(0)
            self.ElastychnaKompresiaPynktVILevelLabel.show()
            self.ElastychnaKompresiaPynktVILevelLineEdit.show()

    def ElastychnaKompresiaPynktVIYesFunc(self):
        if self.ElastychnaKompresiaPynktVIYesCheckBox.isChecked():
            pass
        else:
            self.ElastychnaKompresiaPynktVINoCheckBox.setEnabled(1)
            self.ElastychnaKompresiaPynktVINoCheckBox.setChecked(1)
            self.ElastychnaKompresiaPynktVIYesCheckBox.setEnabled(0)
            self.ElastychnaKompresiaPynktVILevelLabel.hide()
            self.ElastychnaKompresiaPynktVILevelLineEdit.hide()
            # self.ElastychnaKompresiaPynktVILevelLineEdit.setText('')

    def MedukamentoznaProfilaktukaPynktVINoFunc(self):
        if self.MedukamentoznaProfilaktukaPynktVINoCheckBox.isChecked():
            pass
        else:
            self.MedukamentoznaProfilaktukaPynktVINoCheckBox.setEnabled(0)
            self.MedukamentoznaProfilaktukaPynktVIYesCheckBox.setEnabled(1)
            self.MedukamentoznaProfilaktukaPynktVIYesCheckBox.setChecked(1)
            self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLabel.show()
            self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLabel.setEnabled(
                1)
            self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLineEdit.show()
            self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLineEdit.setEnabled(
                1)
            self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLabel.show()
            self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLabel.setEnabled(
                1)
            self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLineEdit.show()
            self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLineEdit.setEnabled(
                1)
            self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLabel.show(
            )
            self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLabel.setEnabled(
                1)
            self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLineEdit.show(
            )
            self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLineEdit.setEnabled(
                1)

    def MedukamentoznaProfilaktukaPynktVIYesFunc(self):
        if self.MedukamentoznaProfilaktukaPynktVIYesCheckBox.isChecked():
            pass
        else:
            self.MedukamentoznaProfilaktukaPynktVIYesCheckBox.setEnabled(0)
            self.MedukamentoznaProfilaktukaPynktVINoCheckBox.setEnabled(1)
            self.MedukamentoznaProfilaktukaPynktVINoCheckBox.setChecked(1)
            self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLabel.hide()
            self.MedukamentoznaProfilaktukaPynktVINazvaPreperatyLineEdit.hide()
            self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLabel.hide()
            self.MedukamentoznaProfilaktukaPynktVIRegymPrujomyLineEdit.hide()
            self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLabel.hide(
            )
            self.MedukamentoznaProfilaktukaPynktVITerminKoluPruznachenoLineEdit.hide(
            )

    def HiryrgichneLikyvannaPynktVINoFunc(self):
        if self.HiryrgichneLikyvannaPynktVINoCheckBox.isChecked():
            pass
        else:
            self.HiryrgichneLikyvannaPynktVIYesCheckBox.setEnabled(1)
            self.HiryrgichneLikyvannaPynktVIYesCheckBox.setChecked(1)
            self.HiryrgichneLikyvannaPynktVINoCheckBox.setEnabled(0)
            self.HiryrgichneLikyvannaNazvaOpericiiPynktVILabel.show()
            self.HiryrgichneLikyvannaNazvaOpericiiPynktVILabel.setEnabled(1)
            self.HiryrgichneLikyvannaNazvaOpericiiPynktVILineEdit.show()
            self.HiryrgichneLikyvannaNazvaOpericiiPynktVILineEdit.setEnabled(1)

    def HiryrgichneLikyvannaPynktVIYesFunc(self):
        if self.HiryrgichneLikyvannaPynktVIYesCheckBox.isChecked():
            pass
        else:
            self.HiryrgichneLikyvannaPynktVINoCheckBox.setEnabled(1)
            self.HiryrgichneLikyvannaPynktVINoCheckBox.setChecked(1)
            self.HiryrgichneLikyvannaPynktVIYesCheckBox.setEnabled(0)
            self.HiryrgichneLikyvannaNazvaOpericiiPynktVILabel.hide()
            self.HiryrgichneLikyvannaNazvaOpericiiPynktVILineEdit.hide()

    def YskladneenaVidProfilaktykuPynktVINoFunc(self):
        if self.YskladneenaVidProfilaktykuPynktVINoCheckBox.isChecked():
            pass
        else:
            self.YskladneenaVidProfilaktykuPynktVIYesCheckBox.setEnabled(1)
            self.YskladneenaVidProfilaktykuPynktVIYesCheckBox.setChecked(1)
            self.YskladneenaVidProfilaktykuPynktVINoCheckBox.setEnabled(0)
            self.YskladneenaVidProfilaktykuNajavnistPynktVILabel.show()
            self.YskladneenaVidProfilaktykuNajavnistPynktVILineEdit.show()

    def YskladneenaVidProfilaktykuPynktVIYesFunc(self):
        if self.YskladneenaVidProfilaktykuPynktVIYesCheckBox.isChecked():
            pass
        else:
            self.YskladneenaVidProfilaktykuPynktVINoCheckBox.setEnabled(1)
            self.YskladneenaVidProfilaktykuPynktVINoCheckBox.setChecked(1)
            self.YskladneenaVidProfilaktykuPynktVIYesCheckBox.setEnabled(0)
            self.YskladneenaVidProfilaktykuNajavnistPynktVILabel.hide()
            self.YskladneenaVidProfilaktykuNajavnistPynktVILineEdit.hide()

            # Обработчик 1)	Пологи вагінальні а) ні, б) спонтанні, в) індуковані
            # PologuVaginalniNoFunc PologuVaginalniSpomtanniFunc PologuVaginalniIndykovaniFunc

    def PologuVaginalniNoFunc(self):
        if self.PologuVaginalniNoCheckBox.isChecked():
            self.PologuVaginalniSpomtanniCheckBox.setEnabled(0)
            self.PologuVaginalniIndykovaniCheckBox.setEnabled(0)
        else:
            self.PologuVaginalniSpomtanniCheckBox.setEnabled(1)
            self.PologuVaginalniIndykovaniCheckBox.setEnabled(1)

    def PologuVaginalniSpomtanniFunc(self):
        if self.PologuVaginalniSpomtanniCheckBox.isChecked():
            self.PologuVaginalniNoCheckBox.setEnabled(0)
            self.PologuVaginalniIndykovaniCheckBox.setEnabled(0)
        else:
            self.PologuVaginalniNoCheckBox.setEnabled(1)
            self.PologuVaginalniIndykovaniCheckBox.setEnabled(1)

    def PologuVaginalniIndykovaniFunc(self):
        if self.PologuVaginalniIndykovaniCheckBox.isChecked():
            self.PologuVaginalniNoCheckBox.setEnabled(0)
            self.PologuVaginalniSpomtanniCheckBox.setEnabled(0)
        else:
            self.PologuVaginalniNoCheckBox.setEnabled(1)
            self.PologuVaginalniSpomtanniCheckBox.setEnabled(1)

            # Обработчик 2)	Пологи абдомінальні а) ні, б) плановий КР, в) ургентний КР

    def PologuAbdominalniNoFunc(self):
        if self.PologuAbdominalniNoCheckBox.isChecked():
            self.PologuAbdominalniPlanovuiKRCheckBox.setEnabled(0)
            self.PologuAbdominalniYrgentbuiKRCheckBox.setEnabled(0)
        else:
            self.PologuAbdominalniPlanovuiKRCheckBox.setEnabled(1)
            self.PologuAbdominalniYrgentbuiKRCheckBox.setEnabled(1)

    def PologuAbdominalniPlanovuiKRFunc(self):
        if self.PologuAbdominalniPlanovuiKRCheckBox.isChecked():
            self.PologuAbdominalniNoCheckBox.setEnabled(0)
            self.PologuAbdominalniYrgentbuiKRCheckBox.setEnabled(0)
        else:
            self.PologuAbdominalniNoCheckBox.setEnabled(1)
            self.PologuAbdominalniYrgentbuiKRCheckBox.setEnabled(1)

    def PologuAbdominalniYrgentbuiKRCFunc(self):
        if self.PologuAbdominalniYrgentbuiKRCheckBox.isChecked():
            self.PologuAbdominalniNoCheckBox.setEnabled(0)
            self.PologuAbdominalniPlanovuiKRCheckBox.setEnabled(0)
        else:
            self.PologuAbdominalniNoCheckBox.setEnabled(1)
            self.PologuAbdominalniPlanovuiKRCheckBox.setEnabled(1)

            # Обработчик 4)	Порушення пологової діяльності а) ні, б) стрімкі пологи, в) дискоординація, г) слабкість
            # PoryshennaPologovoiDialnostiNoFunc PoryshennaPologovoiDialnostiStrimkiPologuFunc PoryshennaPologovoiDialnostiDuskoordunaciaFunc PoryshennaPologovoiDialnostiSlabkistFunc

    def PoryshennaPologovoiDialnostiNoFunc(self):
        if self.PoryshennaPologovoiDialnostiNoCheckBox.isChecked():
            self.PoryshennaPologovoiDialnostiStrimkiPologuCheckBox.setEnabled(
                0)
            self.PoryshennaPologovoiDialnostiStrimkiPologuCheckBox.setChecked(
                0)
            self.PoryshennaPologovoiDialnostiDuskoordunaciaCheckBox.setEnabled(
                0)
            self.PoryshennaPologovoiDialnostiDuskoordunaciaCheckBox.setChecked(
                0)
            self.PoryshennaPologovoiDialnostiSlabkistCheckBox.setEnabled(0)
            self.PoryshennaPologovoiDialnostiSlabkistCheckBox.setChecked(0)
        else:
            self.PoryshennaPologovoiDialnostiStrimkiPologuCheckBox.setEnabled(
                1)
            self.PoryshennaPologovoiDialnostiDuskoordunaciaCheckBox.setEnabled(
                1)
            self.PoryshennaPologovoiDialnostiSlabkistCheckBox.setEnabled(1)

    def PoryshennaPologovoiDialnostiStrimkiPologuFunc(self):
        if self.PoryshennaPologovoiDialnostiStrimkiPologuCheckBox.isChecked():
            self.PoryshennaPologovoiDialnostiNoCheckBox.setEnabled(0)
            self.PoryshennaPologovoiDialnostiNoCheckBox.setChecked(0)
            self.PoryshennaPologovoiDialnostiDuskoordunaciaCheckBox.setEnabled(
                0)
            self.PoryshennaPologovoiDialnostiDuskoordunaciaCheckBox.setChecked(
                0)
            self.PoryshennaPologovoiDialnostiSlabkistCheckBox.setEnabled(0)
            self.PoryshennaPologovoiDialnostiSlabkistCheckBox.setChecked(0)
        else:
            self.PoryshennaPologovoiDialnostiNoCheckBox.setEnabled(1)
            self.PoryshennaPologovoiDialnostiDuskoordunaciaCheckBox.setEnabled(
                1)
            self.PoryshennaPologovoiDialnostiSlabkistCheckBox.setEnabled(1)

    def PoryshennaPologovoiDialnostiDuskoordunaciaFunc(self):
        if self.PoryshennaPologovoiDialnostiDuskoordunaciaCheckBox.isChecked():
            self.PoryshennaPologovoiDialnostiNoCheckBox.setEnabled(0)
            self.PoryshennaPologovoiDialnostiNoCheckBox.setChecked(0)
            self.PoryshennaPologovoiDialnostiStrimkiPologuCheckBox.setEnabled(
                0)
            self.PoryshennaPologovoiDialnostiStrimkiPologuCheckBox.setChecked(
                0)
            self.PoryshennaPologovoiDialnostiSlabkistCheckBox.setEnabled(0)
            self.PoryshennaPologovoiDialnostiSlabkistCheckBox.setChecked(0)
        else:
            self.PoryshennaPologovoiDialnostiNoCheckBox.setEnabled(1)
            self.PoryshennaPologovoiDialnostiStrimkiPologuCheckBox.setEnabled(
                1)
            self.PoryshennaPologovoiDialnostiSlabkistCheckBox.setEnabled(1)

    def PoryshennaPologovoiDialnostiSlabkistFunc(self):
        if self.PoryshennaPologovoiDialnostiSlabkistCheckBox.isChecked():
            self.PoryshennaPologovoiDialnostiNoCheckBox.setEnabled(0)
            self.PoryshennaPologovoiDialnostiNoCheckBox.setChecked(0)
            self.PoryshennaPologovoiDialnostiStrimkiPologuCheckBox.setEnabled(
                0)
            self.PoryshennaPologovoiDialnostiStrimkiPologuCheckBox.setChecked(
                0)
            self.PoryshennaPologovoiDialnostiDuskoordunaciaCheckBox.setEnabled(
                0)
            self.PoryshennaPologovoiDialnostiDuskoordunaciaCheckBox.setChecked(
                0)
        else:
            self.PoryshennaPologovoiDialnostiNoCheckBox.setEnabled(1)
            self.PoryshennaPologovoiDialnostiStrimkiPologuCheckBox.setEnabled(
                1)
            self.PoryshennaPologovoiDialnostiDuskoordunaciaCheckBox.setEnabled(
                1)

            # Обработчик 5)	Корекція аномалій пологової діяльності а) ні, б) бета-міметики, в) окситоцин, г) ензапрост, д) окситоцин з ензапростом.
            # KorekciaAnomaliiPologovoiDialnostiNoFunc  KorekciaAnomaliiPologovoiDialnostiBetaMimetukuFunc
            # KorekciaAnomaliiPologovoiDialnostiOksutocunFunc KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomFunc

    def KorekciaAnomaliiPologovoiDialnostiNoFunc(self):
        if self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.isChecked():
            self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox.setChecked(
                0)
            self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox.setEnabled(
                0)

            self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox.setChecked(
                0)
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox.setEnabled(
                0)

            self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox.setChecked(
                0)
            self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox.setEnabled(
                0)

            self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox.setChecked(
                0)
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox.setEnabled(
                0)
        else:
            self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox.setEnabled(
                1)
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox.setEnabled(
                1)
            self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox.setEnabled(
                1)
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox.setEnabled(
                1)

    def KorekciaAnomaliiPologovoiDialnostiBetaMimetukuFunc(self):
        if self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox.isChecked(
        ):
            self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.setChecked(0)
            self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.setEnabled(0)

            self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox.setChecked(
                0)
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox.setEnabled(
                0)

            self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox.setChecked(
                0)
            self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox.setEnabled(
                0)

            self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox.setChecked(
                0)
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox.setEnabled(
                0)
        else:
            self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.setEnabled(1)
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox.setEnabled(
                1)
            self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox.setEnabled(
                1)
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox.setEnabled(
                1)

    def KorekciaAnomaliiPologovoiDialnostiOksutocunFunc(self):
        if self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox.isChecked(
        ):
            self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.setChecked(0)
            self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.setEnabled(0)

            self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox.setChecked(
                0)
            self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox.setEnabled(
                0)

            self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox.setChecked(
                0)
            self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox.setEnabled(
                0)

            self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox.setChecked(
                0)
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox.setEnabled(
                0)
        else:
            self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.setEnabled(1)
            self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox.setEnabled(
                1)
            self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox.setEnabled(
                1)
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox.setEnabled(
                1)

    def KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomFunc(self):
        if self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox.isChecked(
        ):
            self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.setChecked(0)
            self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.setEnabled(0)

            self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox.setChecked(
                0)
            self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox.setEnabled(
                0)

            self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox.setChecked(
                0)
            self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox.setEnabled(
                0)

            self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox.setChecked(
                0)
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox.setEnabled(
                0)
        else:
            self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.setEnabled(1)
            self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox.setEnabled(
                1)
            self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox.setEnabled(
                1)
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox.setEnabled(
                1)

    def KorekciaAnomaliiPologovoiDialnostiEnzaprostFunc(self):
        if self.KorekciaAnomaliiPologovoiDialnostiEnzaprostCheckBox.isChecked(
        ):
            self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.setChecked(0)
            self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.setEnabled(0)

            self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox.setChecked(
                0)
            self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox.setEnabled(
                0)

            self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox.setChecked(
                0)
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox.setEnabled(
                0)

            self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox.setChecked(
                0)
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox.setEnabled(
                0)
        else:
            self.KorekciaAnomaliiPologovoiDialnostiNoCheckBox.setEnabled(1)
            self.KorekciaAnomaliiPologovoiDialnostiBetaMimetukuCheckBox.setEnabled(
                1)
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunZEnzaprostomCheckBox.setEnabled(
                1)
            self.KorekciaAnomaliiPologovoiDialnostiOksutocunCheckBox.setEnabled(
                1)

            # Обработчик 6)	Вилив навколоплодових вод а) своєчасний, б) ранній, в) передчасний
            # VuluvNavkoloplodovuhVodSvoechasnuiFunc VuluvNavkoloplodovuhVodRaniiFunc  VuluvNavkoloplodovuhVodPeredchasnuiFunc

    def VuluvNavkoloplodovuhVodSvoechasnuiFunc(self):
        if self.VuluvNavkoloplodovuhVodSvoechasnuiCheckBox.isChecked():
            self.VuluvNavkoloplodovuhVodRaniiCheckBox.setEnabled(0)
            self.VuluvNavkoloplodovuhVodRaniiCheckBox.setChecked(0)
            self.VuluvNavkoloplodovuhVodPeredchasnuiCheckBox.setEnabled(0)
            self.VuluvNavkoloplodovuhVodPeredchasnuiCheckBox.setChecked(0)
        else:
            self.VuluvNavkoloplodovuhVodRaniiCheckBox.setEnabled(1)
            self.VuluvNavkoloplodovuhVodPeredchasnuiCheckBox.setEnabled(1)

    def VuluvNavkoloplodovuhVodRaniiFunc(self):
        if self.VuluvNavkoloplodovuhVodRaniiCheckBox.isChecked():
            self.VuluvNavkoloplodovuhVodSvoechasnuiCheckBox.setEnabled(0)
            self.VuluvNavkoloplodovuhVodSvoechasnuiCheckBox.setChecked(0)
            self.VuluvNavkoloplodovuhVodPeredchasnuiCheckBox.setEnabled(0)
            self.VuluvNavkoloplodovuhVodPeredchasnuiCheckBox.setChecked(0)
        else:
            self.VuluvNavkoloplodovuhVodSvoechasnuiCheckBox.setEnabled(1)
            self.VuluvNavkoloplodovuhVodPeredchasnuiCheckBox.setEnabled(1)

    def VuluvNavkoloplodovuhVodPeredchasnuiFunc(self):
        if self.VuluvNavkoloplodovuhVodPeredchasnuiCheckBox.isChecked():
            self.VuluvNavkoloplodovuhVodSvoechasnuiCheckBox.setEnabled(0)
            self.VuluvNavkoloplodovuhVodSvoechasnuiCheckBox.setChecked(0)
            self.VuluvNavkoloplodovuhVodRaniiCheckBox.setEnabled(0)
            self.VuluvNavkoloplodovuhVodRaniiCheckBox.setChecked(0)
        else:
            self.VuluvNavkoloplodovuhVodSvoechasnuiCheckBox.setEnabled(1)
            self.VuluvNavkoloplodovuhVodRaniiCheckBox.setEnabled(1)

            # Обработчик 7)	Дистрес плода в пологах а) ні, б) в І періоді, в) в ІІ періоді
            # DustressPlodaVPologahNoFunc DustressPlodaVPologahVIPeriodiFunc DustressPlodaVPologahVIIPeriodiFunc

    def DustressPlodaVPologahNoFunc(self):
        if self.DustressPlodaVPologahNoCheckBox.isChecked():
            self.DustressPlodaVPologahVIPeriodiCheckBox.setChecked(0)
            self.DustressPlodaVPologahVIPeriodiCheckBox.setEnabled(0)
            self.DustressPlodaVPologahVIIPeriodiCheckBox.setEnabled(0)
            self.DustressPlodaVPologahVIIPeriodiCheckBox.setChecked(0)
        else:
            self.DustressPlodaVPologahVIPeriodiCheckBox.setEnabled(1)
            self.DustressPlodaVPologahVIIPeriodiCheckBox.setEnabled(1)

    def DustressPlodaVPologahVIPeriodiFunc(self):
        if self.DustressPlodaVPologahVIPeriodiCheckBox.isChecked():
            self.DustressPlodaVPologahNoCheckBox.setChecked(0)
            self.DustressPlodaVPologahNoCheckBox.setEnabled(0)
            self.DustressPlodaVPologahVIIPeriodiCheckBox.setEnabled(0)
            self.DustressPlodaVPologahVIIPeriodiCheckBox.setChecked(0)
        else:
            self.DustressPlodaVPologahNoCheckBox.setEnabled(1)
            self.DustressPlodaVPologahVIIPeriodiCheckBox.setEnabled(1)

    def DustressPlodaVPologahVIIPeriodiFunc(self):
        if self.DustressPlodaVPologahVIIPeriodiCheckBox.isChecked():
            self.DustressPlodaVPologahNoCheckBox.setChecked(0)
            self.DustressPlodaVPologahNoCheckBox.setEnabled(0)
            self.DustressPlodaVPologahVIPeriodiCheckBox.setEnabled(0)
            self.DustressPlodaVPologahVIPeriodiCheckBox.setChecked(0)
        else:
            self.DustressPlodaVPologahNoCheckBox.setEnabled(1)
            self.DustressPlodaVPologahVIPeriodiCheckBox.setEnabled(1)

            # Обработчик 8)	Гіпотонічна кровотеча а) ні, б) в ІІІ періоді, в) в ранньому післяпологовому періоді, г) в пізньому післяпологовому періоді.

    def GipotonichnaKrovotechaNoFunc(self):
        if self.GipotonichnaKrovotechaNoCheckBox.isChecked():
            self.GipotonichnaKrovotechaVIIIPeriodiCheckBox.setChecked(0)
            self.GipotonichnaKrovotechaVIIIPeriodiCheckBox.setEnabled(0)
            self.GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiCheckBox.setEnabled(
                0)
            self.GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiCheckBox.setChecked(
                0)
            self.GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiCheckBox.setChecked(
                0)
            self.GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiCheckBox.setEnabled(
                0)
        else:
            self.GipotonichnaKrovotechaVIIIPeriodiCheckBox.setEnabled(1)
            self.GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiCheckBox.setEnabled(
                1)
            self.GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiCheckBox.setEnabled(
                1)

    def GipotonichnaKrovotechaVIIIPeriodiFunc(self):
        if self.GipotonichnaKrovotechaVIIIPeriodiCheckBox.isChecked():
            self.GipotonichnaKrovotechaNoCheckBox.setChecked(0)
            self.GipotonichnaKrovotechaNoCheckBox.setEnabled(0)
            self.GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiCheckBox.setEnabled(
                0)
            self.GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiCheckBox.setChecked(
                0)
            self.GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiCheckBox.setChecked(
                0)
            self.GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiCheckBox.setEnabled(
                0)
        else:
            self.GipotonichnaKrovotechaNoCheckBox.setEnabled(1)
            self.GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiCheckBox.setEnabled(
                1)
            self.GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiCheckBox.setEnabled(
                1)

    def GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiFunc(self):
        if self.GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiCheckBox.isChecked(
        ):
            self.GipotonichnaKrovotechaNoCheckBox.setChecked(0)
            self.GipotonichnaKrovotechaNoCheckBox.setEnabled(0)
            self.GipotonichnaKrovotechaVIIIPeriodiCheckBox.setEnabled(0)
            self.GipotonichnaKrovotechaVIIIPeriodiCheckBox.setChecked(0)
            self.GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiCheckBox.setChecked(
                0)
            self.GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiCheckBox.setEnabled(
                0)
        else:
            self.GipotonichnaKrovotechaNoCheckBox.setEnabled(1)
            self.GipotonichnaKrovotechaVIIIPeriodiCheckBox.setEnabled(1)
            self.GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiCheckBox.setEnabled(
                1)

    def GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiFunc(self):
        if self.GipotonichnaKrovotechaVPiznomyPislapologovomyPeriodiCheckBox.isChecked(
        ):
            self.GipotonichnaKrovotechaNoCheckBox.setChecked(0)
            self.GipotonichnaKrovotechaNoCheckBox.setEnabled(0)
            self.GipotonichnaKrovotechaVIIIPeriodiCheckBox.setEnabled(0)
            self.GipotonichnaKrovotechaVIIIPeriodiCheckBox.setChecked(0)
            self.GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiCheckBox.setChecked(
                0)
            self.GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiCheckBox.setEnabled(
                0)
        else:
            self.GipotonichnaKrovotechaNoCheckBox.setEnabled(1)
            self.GipotonichnaKrovotechaVIIIPeriodiCheckBox.setEnabled(1)
            self.GipotonichnaKrovotechaVRannomyPislapologovomyPeriodiCheckBox.setEnabled(
                1)

            # Обработчик 9)	Аномалії прикріплення плаценти а) ні, б) adherens, в) acreta, г) percreta.

    def AnomaliiPrukriplennaPlacentuNoFunc(self):
        if self.AnomaliiPrukriplennaPlacentuNoCheckBox.isChecked():
            self.AnomaliiPrukriplennaPlacentuAdherensCheckBox.setEnabled(0)
            self.AnomaliiPrukriplennaPlacentuAdherensCheckBox.setChecked(0)
            self.AnomaliiPrukriplennaPlacentuAcretaCheckBox.setEnabled(0)
            self.AnomaliiPrukriplennaPlacentuAcretaCheckBox.setChecked(0)
            self.AnomaliiPrukriplennaPlacentuPercretaCheckBox.setEnabled(0)
            self.AnomaliiPrukriplennaPlacentuPercretaCheckBox.setChecked(0)
        else:
            self.AnomaliiPrukriplennaPlacentuAdherensCheckBox.setEnabled(1)
            self.AnomaliiPrukriplennaPlacentuAcretaCheckBox.setEnabled(1)
            self.AnomaliiPrukriplennaPlacentuPercretaCheckBox.setEnabled(1)

    def AnomaliiPrukriplennaPlacentuAdherensFunc(self):
        if self.AnomaliiPrukriplennaPlacentuAdherensCheckBox.isChecked():
            self.AnomaliiPrukriplennaPlacentuNoCheckBox.setEnabled(0)
            self.AnomaliiPrukriplennaPlacentuNoCheckBox.setChecked(0)
            self.AnomaliiPrukriplennaPlacentuAcretaCheckBox.setEnabled(0)
            self.AnomaliiPrukriplennaPlacentuAcretaCheckBox.setChecked(0)
            self.AnomaliiPrukriplennaPlacentuPercretaCheckBox.setEnabled(0)
            self.AnomaliiPrukriplennaPlacentuPercretaCheckBox.setChecked(0)
        else:
            self.AnomaliiPrukriplennaPlacentuNoCheckBox.setEnabled(1)
            self.AnomaliiPrukriplennaPlacentuAcretaCheckBox.setEnabled(1)
            self.AnomaliiPrukriplennaPlacentuPercretaCheckBox.setEnabled(1)

    def AnomaliiPrukriplennaPlacentuAcretaFunc(self):
        if self.AnomaliiPrukriplennaPlacentuAcretaCheckBox.isChecked():
            self.AnomaliiPrukriplennaPlacentuNoCheckBox.setEnabled(0)
            self.AnomaliiPrukriplennaPlacentuNoCheckBox.setChecked(0)
            self.AnomaliiPrukriplennaPlacentuAdherensCheckBox.setEnabled(0)
            self.AnomaliiPrukriplennaPlacentuAdherensCheckBox.setChecked(0)
            self.AnomaliiPrukriplennaPlacentuPercretaCheckBox.setEnabled(0)
            self.AnomaliiPrukriplennaPlacentuPercretaCheckBox.setChecked(0)
        else:
            self.AnomaliiPrukriplennaPlacentuNoCheckBox.setEnabled(1)
            self.AnomaliiPrukriplennaPlacentuAdherensCheckBox.setEnabled(1)
            self.AnomaliiPrukriplennaPlacentuPercretaCheckBox.setEnabled(1)

    def AnomaliiPrukriplennaPlacentuPercretaFunc(self):
        if self.AnomaliiPrukriplennaPlacentuPercretaCheckBox.isChecked():
            self.AnomaliiPrukriplennaPlacentuNoCheckBox.setEnabled(0)
            self.AnomaliiPrukriplennaPlacentuNoCheckBox.setChecked(0)
            self.AnomaliiPrukriplennaPlacentuAdherensCheckBox.setEnabled(0)
            self.AnomaliiPrukriplennaPlacentuAdherensCheckBox.setChecked(0)
            self.AnomaliiPrukriplennaPlacentuAcretaCheckBox.setEnabled(0)
            self.AnomaliiPrukriplennaPlacentuAcretaCheckBox.setChecked(0)
        else:
            self.AnomaliiPrukriplennaPlacentuNoCheckBox.setEnabled(1)
            self.AnomaliiPrukriplennaPlacentuAdherensCheckBox.setEnabled(1)
            self.AnomaliiPrukriplennaPlacentuAcretaCheckBox.setEnabled(1)

            # Обработчик   10) Дефект посліду: а) ні  б) так
            # DefektPoslidyNoFunc DefektPoslidyYesFunc

    def DefektPoslidyNoFunc(self):
        if self.DefektPoslidyNoCheckBox.isChecked():
            pass
        else:
            self.DefektPoslidyYesCheckBox.setChecked(1)
            self.DefektPoslidyYesCheckBox.setEnabled(1)

    def DefektPoslidyYesFunc(self):
        if self.DefektPoslidyYesCheckBox.isChecked():
            pass
        else:
            self.DefektPoslidyNoCheckBox.setEnabled(1)
            self.DefektPoslidyNoCheckBox.setChecked(1)

            # Обработчик     11) Дефект оболонок: а) ні  б) так
            # DefektObolonokNoFunc

    def DefektObolonokNoFunc(self):
        if self.DefektObolonokNoCheckBox.isChecked():
            pass
        else:
            self.DefektObolonokYesCheckBox.setChecked(1)
            self.DefektObolonokYesCheckBox.setEnabled(1)

    def DefektObolonokYesFunc(self):
        if self.DefektObolonokYesCheckBox.isChecked():
            pass
        else:
            self.DefektObolonokNoCheckBox.setEnabled(1)
            self.DefektObolonokNoCheckBox.setChecked(1)

            # обработчик     12) Аномалії прикріплення пуповини: а) ні, б) оболонкове
            # AnomaliiPrukriplennaPypovunuNoFunc AnomaliiPrukriplennaPypovunuObolonkoveFunc

    def AnomaliiPrukriplennaPypovunuNoFunc(self):
        if self.AnomaliiPrukriplennaPypovunuNoCheckBox.isChecked():
            self.AnomaliiPrukriplennaPypovunuObolonkoveCheckBox.setChecked(0)
        else:
            self.AnomaliiPrukriplennaPypovunuObolonkoveCheckBox.setChecked(1)
            self.AnomaliiPrukriplennaPypovunuObolonkoveCheckBox.setEnabled(1)

    def AnomaliiPrukriplennaPypovunuObolonkoveFunc(self):
        if self.AnomaliiPrukriplennaPypovunuObolonkoveCheckBox.isChecked():
            self.AnomaliiPrukriplennaPypovunuNoCheckBox.setEnabled(0)
        else:
            self.AnomaliiPrukriplennaPypovunuNoCheckBox.setEnabled(1)
            self.AnomaliiPrukriplennaPypovunuNoCheckBox.setChecked(1)

            #    13) Оперативна допомога: а) ні б) ручна ревізія стінок порожнини маткив) інструментальна ревізія стінок порожнини маткиг) ручне відокремлення плаценти та видалення посліду
            # OperatuvnaDopomogaNoFunc

    def OperatuvnaDopomogaNoFunc(self):
        if self.OperatuvnaDopomogaNoCheckBox.isChecked():
            self.OperatuvnaDopomogaRychnaReviziaCheckBox.setChecked(0)
            self.OperatuvnaDopomogaRychnaReviziaCheckBox.setEnabled(0)
            self.OperatuvnaDopomogaInstrymentalnaReviziaCheckBox.setChecked(0)
            self.OperatuvnaDopomogaInstrymentalnaReviziaCheckBox.setEnabled(0)
            self.OperatuvnaDopomogaRychneVidokremlennaCheckBox.setChecked(0)
            self.OperatuvnaDopomogaRychneVidokremlennaCheckBox.setEnabled(0)
        else:
            self.OperatuvnaDopomogaRychnaReviziaCheckBox.setEnabled(1)
            self.OperatuvnaDopomogaInstrymentalnaReviziaCheckBox.setEnabled(1)
            self.OperatuvnaDopomogaRychneVidokremlennaCheckBox.setEnabled(1)

            # Обработчик Розриви пологових шляхів: а) ні б) промежини в) піхви г) шийки матки

    def RozruvuPologovuhShlahivNoFunc(self):
        if self.RozruvuPologovuhShlahivNoCheckBox.isChecked():
            self.RozruvuPologovuhShlahivPromejunuCheckBox.setEnabled(0)
            self.RozruvuPologovuhShlahivPromejunuCheckBox.setChecked(0)
            self.RozruvuPologovuhShlahivPihvuCheckBox.setEnabled(0)
            self.RozruvuPologovuhShlahivPihvuCheckBox.setChecked(0)
            self.RozruvuPologovuhShlahivShuikiMatkuCheckBox.setEnabled(0)
            self.RozruvuPologovuhShlahivShuikiMatkuCheckBox.setChecked(0)
            self.StypinRozruvyPologovuhShlahivLabel.hide()
            self.StypinRozruvyPologovuhShlahivLineEdit.hide()
        else:
            self.RozruvuPologovuhShlahivPromejunuCheckBox.setEnabled(1)
            self.RozruvuPologovuhShlahivPihvuCheckBox.setEnabled(1)
            self.RozruvuPologovuhShlahivShuikiMatkuCheckBox.setEnabled(1)
            self.StypinRozruvyPologovuhShlahivLabel.show()
            self.StypinRozruvyPologovuhShlahivLineEdit.show()

            # Обработчик 15) Епізіо- або перінеотомія: а) так  б) ні
            # EpizoAboPerineotomiayNoFunc EpizoAboPerineotomiaYesFunc

    def EpizoAboPerineotomiaNoFunc(self):
        if self.EpizoAboPerineotomiaNoCheckBox.isChecked():
            pass
        else:
            self.EpizoAboPerineotomiaYesCheckBox.setEnabled(1)
            self.EpizoAboPerineotomiaYesCheckBox.setChecked(1)

    def EpizoAboPerineotomiaYesFunc(self):
        if self.EpizoAboPerineotomiaYesCheckBox.isChecked():
            pass
        else:
            self.EpizoAboPerineotomiaNoCheckBox.setEnabled(1)
            self.EpizoAboPerineotomiaNoCheckBox.setChecked(1)

            # Обработчик 1)	Народився а) живий, б) мертвий
            # NaroduvsaGuvuiFunc NaroduvsaMertvuiFunc

    def NaroduvsaGuvuiFunc(self):
        if self.NaroduvsaGuvuiCheckBox.isChecked():
            pass
        else:
            self.NaroduvsaMertvuiCheckBox.setEnabled(1)
            self.NaroduvsaMertvuiCheckBox.setChecked(1)
            self.NaroduvsaGuvuiCheckBox.setEnabled(0)
            self.PruchunaMertvonarodgennaLabel.setEnabled(1)
            self.PruchunaMertvonarodgennaAntenatalnaCheckBox.setEnabled(1)
            self.PruchunaMertvonarodgennaAntenatalnaCheckBox.setChecked(1)
            self.PruchunaMertvonarodgennaInternatalnaCheckBox.setChecked(0)

    def NaroduvsaMertvuiFunc(self):
        if self.NaroduvsaMertvuiCheckBox.isChecked():
            pass
        else:
            self.NaroduvsaGuvuiCheckBox.setEnabled(1)
            self.NaroduvsaGuvuiCheckBox.setChecked(1)
            self.NaroduvsaMertvuiCheckBox.setEnabled(0)

            self.PruchunaMertvonarodgennaLabel.setEnabled(0)

            self.PruchunaMertvonarodgennaInternatalnaCheckBox.setEnabled(0)
            self.PruchunaMertvonarodgennaAntenatalnaCheckBox.setEnabled(0)

            # Обработчик 2)	Причина мертвонародження а) антенатальна, б) інтранатальна
            # PruchunaMertvonarodgennaAntenatalnaFunc PruchunaMertvonarodgennaInternatalnaFunc

    def PruchunaMertvonarodgennaAntenatalnaFunc(self):
        if self.PruchunaMertvonarodgennaAntenatalnaCheckBox.isChecked():
            pass
        else:
            self.PruchunaMertvonarodgennaInternatalnaCheckBox.setEnabled(1)
            self.PruchunaMertvonarodgennaInternatalnaCheckBox.setChecked(1)
            self.PruchunaMertvonarodgennaAntenatalnaCheckBox.setEnabled(0)

    def PruchunaMertvonarodgennaInternatalnaFunc(self):
        if self.PruchunaMertvonarodgennaInternatalnaCheckBox.isChecked():
            pass
        else:
            self.PruchunaMertvonarodgennaAntenatalnaCheckBox.setEnabled(1)
            self.PruchunaMertvonarodgennaAntenatalnaCheckBox.setChecked(1)
            self.PruchunaMertvonarodgennaInternatalnaCheckBox.setEnabled(0)

            # Обработчик 3)	Зрілість новонародженого: а) доношений; б)недоношений; в) переношений
            ##ZrilistNovonarodgennogoDonoshenuiFunc ZrilistNovonarodgennogoNedonoshenuiFunc ZrilistNovonarodgennogoPerenoshenuiFunc

    def ZrilistNovonarodgennogoDonoshenuiFunc(self):
        if self.ZrilistNovonarodgennogoDonoshenuiCheckBox.isChecked():
            self.ZrilistNovonarodgennogoNedonoshenuiCheckBox.setEnabled(0)
            self.ZrilistNovonarodgennogoPerenoshenuiCheckBox.setEnabled(0)
        else:
            self.ZrilistNovonarodgennogoNedonoshenuiCheckBox.setEnabled(1)
            self.ZrilistNovonarodgennogoPerenoshenuiCheckBox.setEnabled(1)

    def ZrilistNovonarodgennogoNedonoshenuiFunc(self):
        if self.ZrilistNovonarodgennogoNedonoshenuiCheckBox.isChecked():
            self.ZrilistNovonarodgennogoDonoshenuiCheckBox.setEnabled(0)
            self.ZrilistNovonarodgennogoPerenoshenuiCheckBox.setEnabled(0)
        else:
            self.ZrilistNovonarodgennogoDonoshenuiCheckBox.setEnabled(1)
            self.ZrilistNovonarodgennogoPerenoshenuiCheckBox.setEnabled(1)

    def ZrilistNovonarodgennogoPerenoshenuiFunc(self):
        if self.ZrilistNovonarodgennogoPerenoshenuiCheckBox.isChecked():
            self.ZrilistNovonarodgennogoDonoshenuiCheckBox.setEnabled(0)
            self.ZrilistNovonarodgennogoNedonoshenuiCheckBox.setEnabled(0)
        else:
            self.ZrilistNovonarodgennogoDonoshenuiCheckBox.setEnabled(1)
            self.ZrilistNovonarodgennogoNedonoshenuiCheckBox.setEnabled(1)

            # Обработчик        4.1. Гіпотрофія плода:  а) ні  б) так
            # GipotrofiaPlodaNoFunc GipotrofiaPlodaYesFunc

    def GipotrofiaPlodaNoFunc(self):
        if self.GipotrofiaPlodaNoCheckBox.isChecked():
            pass
        else:
            self.GipotrofiaPlodaYesCheckBox.setChecked(1)
            self.GipotrofiaPlodaYesCheckBox.setEnabled(1)
            self.GipotrofiaPlodaNoCheckBox.setEnabled(0)

    def GipotrofiaPlodaYesFunc(self):
        if self.GipotrofiaPlodaYesCheckBox.isChecked():
            pass
        else:
            self.GipotrofiaPlodaNoCheckBox.setEnabled(1)
            self.GipotrofiaPlodaNoCheckBox.setChecked(1)
            self.GipotrofiaPlodaYesCheckBox.setEnabled(0)

            # обработчик 6) новонароджений з вадами розвиту: а) ні  б) так  в) які саме
            # NovonarodjenuiZVadamuRozvutkyNoFunc NovonarodjenuiZVadamuRozvutkyYesFunc

    def NovonarodjenuiZVadamuRozvutkyNoFunc(self):
        if self.NovonarodjenuiZVadamuRozvutkyNoCheckBox.isChecked():
            pass
        else:
            self.NovonarodjenuiZVadamuRozvutkyYesCheckBox.setChecked(1)
            self.NovonarodjenuiZVadamuRozvutkyYesCheckBox.setEnabled(1)
            self.NovonarodjenuiZVadamuRozvutkyNoCheckBox.setEnabled(0)
            self.NovonarodjenuiZVadamuRozvutkyJakiSameLineEdit.show()
            self.NovonarodjenuiZVadamuRozvutkyJakiSameLabel.show()

    def NovonarodjenuiZVadamuRozvutkyYesFunc(self):
        if self.NovonarodjenuiZVadamuRozvutkyYesCheckBox.isChecked():
            pass
        else:
            self.NovonarodjenuiZVadamuRozvutkyNoCheckBox.setChecked(1)
            self.NovonarodjenuiZVadamuRozvutkyNoCheckBox.setEnabled(1)
            self.NovonarodjenuiZVadamuRozvutkyYesCheckBox.setEnabled(0)
            self.NovonarodjenuiZVadamuRozvutkyJakiSameLineEdit.hide()
            self.NovonarodjenuiZVadamuRozvutkyJakiSameLineEdit.setText('')
            self.NovonarodjenuiZVadamuRozvutkyJakiSameLabel.hide()

            # Обработчик 7) пологова травма: а) ні  б) так  в) яка саме ____________________
            # PologovaTravmaNoFunc PologovaTravmaYesFunc

    def PologovaTravmaNoFunc(self):
        if self.PologovaTravmaNoCheckBox.isChecked():
            pass
        else:
            self.PologovaTravmaYesCheckBox.setEnabled(1)
            self.PologovaTravmaYesCheckBox.setChecked(1)
            self.PologovaTravmaNoCheckBox.setEnabled(0)
            self.PologovaTravmaJakaSameLineEdit.show()
            self.PologovaTravmaJakaSameLabel.show()

    def PologovaTravmaYesFunc(self):
        if self.PologovaTravmaYesCheckBox.isChecked():
            pass
        else:
            self.PologovaTravmaNoCheckBox.setEnabled(1)
            self.PologovaTravmaNoCheckBox.setChecked(1)
            self.PologovaTravmaYesCheckBox.setEnabled(0)
            self.PologovaTravmaJakaSameLineEdit.hide()
            self.PologovaTravmaJakaSameLabel.hide()

            # Обработчик 8) СДР: 					а) ні  б) так
            # SDRNoFunc SDRYesFunc

    def SDRNoFunc(self):
        if self.SDRNoCheckBox.isChecked():
            pass
        else:
            self.SDRYesCheckBox.setEnabled(1)
            self.SDRYesCheckBox.setChecked(1)
            self.SDRNoCheckBox.setEnabled(0)

    def SDRYesFunc(self):
        if self.SDRYesCheckBox.isChecked():
            pass
        else:
            self.SDRNoCheckBox.setEnabled(1)
            self.SDRNoCheckBox.setChecked(1)
            self.SDRYesCheckBox.setEnabled(0)

            # Обработчик 9) внутрішньоутробне інфікування: а) ні  б) так
            # VnytrishnoytrobneInfikyvannaNoFunc VnytrishnoytrobneInfikyvannaYesFunc

    def VnytrishnoytrobneInfikyvannaNoFunc(self):
        if self.VnytrishnoytrobneInfikyvannaNoCheckBox.isChecked():
            pass
        else:
            self.VnytrishnoytrobneInfikyvannaYesCheckBox.setEnabled(1)
            self.VnytrishnoytrobneInfikyvannaYesCheckBox.setChecked(1)
            self.VnytrishnoytrobneInfikyvannaNoCheckBox.setEnabled(0)

    def VnytrishnoytrobneInfikyvannaYesFunc(self):
        if self.VnytrishnoytrobneInfikyvannaYesCheckBox.isChecked():
            pass
        else:
            self.VnytrishnoytrobneInfikyvannaNoCheckBox.setEnabled(1)
            self.VnytrishnoytrobneInfikyvannaNoCheckBox.setChecked(1)
            self.VnytrishnoytrobneInfikyvannaYesCheckBox.setEnabled(0)

            # Обработчик 10) геморагічні ускладнення:		а) ні  б) так
            # GemoragichniYskladnennaNoFunc GemoragichniYskladnennaYesFunc

    def GemoragichniYskladnennaNoFunc(self):
        if self.GemoragichniYskladnennaNoCheckBox.isChecked():
            pass
        else:
            self.GemoragichniYskladnennaNoCheckBox.setEnabled(0)
            self.GemoragichniYskladnennaYesCheckBox.setEnabled(1)
            self.GemoragichniYskladnennaYesCheckBox.setChecked(1)

    def GemoragichniYskladnennaYesFunc(self):
        if self.GemoragichniYskladnennaYesCheckBox.isChecked():
            pass
        else:
            self.GemoragichniYskladnennaYesCheckBox.setEnabled(0)
            self.GemoragichniYskladnennaNoCheckBox.setEnabled(1)
            self.GemoragichniYskladnennaNoCheckBox.setChecked(1)

            # Обработчик 11) анемія: а) ні  б) І ступеня  в) II ступеня  г) IIІ ступеня
            # AnemiaNoFunc AnemiaIStypenaFunc  AnemiaIIStypenaFunc AnemiaIIIStypenaFunc

    def AnemiaNoFunc(self):
        if self.AnemiaNoCheckBox.isChecked():
            self.AnemiaIStypenaCheckBox.setEnabled(0)
            self.AnemiaIIIStypenaCheckBox.setEnabled(0)
            self.AnemiaIIStypenaCheckBox.setEnabled(0)
        else:
            self.AnemiaIStypenaCheckBox.setEnabled(1)
            self.AnemiaIIIStypenaCheckBox.setEnabled(1)
            self.AnemiaIIStypenaCheckBox.setEnabled(1)

    def AnemiaIStypenaFunc(self):
        if self.AnemiaIStypenaCheckBox.isChecked():
            self.AnemiaNoCheckBox.setEnabled(0)
            self.AnemiaIIIStypenaCheckBox.setEnabled(0)
            self.AnemiaIIStypenaCheckBox.setEnabled(0)
        else:
            self.AnemiaNoCheckBox.setEnabled(1)
            self.AnemiaIIIStypenaCheckBox.setEnabled(1)
            self.AnemiaIIStypenaCheckBox.setEnabled(1)

    def AnemiaIIStypenaFunc(self):
        if self.AnemiaIIStypenaCheckBox.isChecked():
            self.AnemiaNoCheckBox.setEnabled(0)
            self.AnemiaIIIStypenaCheckBox.setEnabled(0)
            self.AnemiaIStypenaCheckBox.setEnabled(0)
        else:
            self.AnemiaNoCheckBox.setEnabled(1)
            self.AnemiaIIIStypenaCheckBox.setEnabled(1)
            self.AnemiaIStypenaCheckBox.setEnabled(1)

    def AnemiaIIIStypenaFunc(self):
        if self.AnemiaIIIStypenaCheckBox.isChecked():
            self.AnemiaNoCheckBox.setEnabled(0)
            self.AnemiaIIStypenaCheckBox.setEnabled(0)
            self.AnemiaIStypenaCheckBox.setEnabled(0)
        else:
            self.AnemiaNoCheckBox.setEnabled(1)
            self.AnemiaIIStypenaCheckBox.setEnabled(1)
            self.AnemiaIStypenaCheckBox.setEnabled(1)

            # Обработчик 12) гіпербілірубінемія: а) ні  б) так  в) рівень білірубіну___________

    def GiperBilirybinemiaNoFunc(self):
        if self.GiperBilirybinemiaNoCheckBox.isChecked():
            pass
        else:
            self.GiperBilirybinemiaYesCheckBox.setEnabled(1)
            self.GiperBilirybinemiaYesCheckBox.setChecked(1)
            self.GiperBilirybinemiaNoCheckBox.setEnabled(0)
            self.GiperBilirybinemiaRivenBilirybinyLineEdit.show()
            self.GiperBilirybinemiaRivenBilirybinyLabel.show()

    def GiperBilirybinemiaYesFunc(self):
        if self.GiperBilirybinemiaYesCheckBox.isChecked():
            pass
        else:
            self.GiperBilirybinemiaNoCheckBox.setEnabled(1)
            self.GiperBilirybinemiaNoCheckBox.setChecked(1)
            self.GiperBilirybinemiaYesCheckBox.setEnabled(0)
            self.GiperBilirybinemiaRivenBilirybinyLineEdit.hide()
            self.GiperBilirybinemiaRivenBilirybinyLabel.hide()

            # AsfiksiaNoFunc AsfiksiaLegkaFunc AsfiksiaSerednaFunc  AsfiksiaVajkaFunc

    def AsfiksiaNoFunc(self):
        if self.AsfiksiaNoCheckBox.isChecked():
            self.AsfiksiaLegkaCheckBox.setEnabled(0)
            self.AsfiksiaSerednaCheckBox.setEnabled(0)
            self.AsfiksiaVajkaCheckBox.setEnabled(0)
        else:
            self.AsfiksiaLegkaCheckBox.setEnabled(1)
            self.AsfiksiaSerednaCheckBox.setEnabled(1)
            self.AsfiksiaVajkaCheckBox.setEnabled(1)

    def AsfiksiaLegkaFunc(self):
        if self.AsfiksiaLegkaCheckBox.isChecked():
            self.AsfiksiaNoCheckBox.setEnabled(0)
            self.AsfiksiaSerednaCheckBox.setEnabled(0)
            self.AsfiksiaVajkaCheckBox.setEnabled(0)
        else:
            self.AsfiksiaNoCheckBox.setEnabled(1)
            self.AsfiksiaSerednaCheckBox.setEnabled(1)
            self.AsfiksiaVajkaCheckBox.setEnabled(1)

    def AsfiksiaSerednaFunc(self):
        if self.AsfiksiaSerednaCheckBox.isChecked():
            self.AsfiksiaLegkaCheckBox.setEnabled(0)
            self.AsfiksiaNoCheckBox.setEnabled(0)
            self.AsfiksiaVajkaCheckBox.setEnabled(0)
        else:
            self.AsfiksiaLegkaCheckBox.setEnabled(1)
            self.AsfiksiaNoCheckBox.setEnabled(1)
            self.AsfiksiaVajkaCheckBox.setEnabled(1)

    def AsfiksiaVajkaFunc(self):
        if self.AsfiksiaVajkaCheckBox.isChecked():
            self.AsfiksiaLegkaCheckBox.setEnabled(0)
            self.AsfiksiaNoCheckBox.setEnabled(0)
            self.AsfiksiaSerednaCheckBox.setEnabled(0)
        else:
            self.AsfiksiaLegkaCheckBox.setEnabled(1)
            self.AsfiksiaNoCheckBox.setEnabled(1)
            self.AsfiksiaSerednaCheckBox.setEnabled(1)

            # Обработчик 14) порушення кардіо-респіраторної адаптації: а)ні   б) так.
            # PoryshennaKardioRespiratornoiAdaptaciiNoFunc PoryshennaKardioRespiratornoiAdaptaciiYesFunc

    def PoryshennaKardioRespiratornoiAdaptaciiNoFunc(self):
        if self.PoryshennaKardioRespiratornoiAdaptaciiNoCheckBox.isChecked():
            pass
        else:
            self.PoryshennaKardioRespiratornoiAdaptaciiYesCheckBox.setEnabled(
                1)
            self.PoryshennaKardioRespiratornoiAdaptaciiYesCheckBox.setChecked(
                1)
            self.PoryshennaKardioRespiratornoiAdaptaciiNoCheckBox.setEnabled(0)

    def PoryshennaKardioRespiratornoiAdaptaciiYesFunc(self):
        if self.PoryshennaKardioRespiratornoiAdaptaciiYesCheckBox.isChecked():
            pass
        else:
            self.PoryshennaKardioRespiratornoiAdaptaciiNoCheckBox.setEnabled(1)
            self.PoryshennaKardioRespiratornoiAdaptaciiNoCheckBox.setChecked(1)
            self.PoryshennaKardioRespiratornoiAdaptaciiYesCheckBox.setEnabled(
                0)

            # 16) Вітамін К введено 				а) так б)ні	термін ________
            # VitaminKVvedenoNoFunc VitaminKVvedenoYesFunc

    def VitaminKVvedenoNoFunc(self):
        if self.VitaminKVvedenoNoCheckBox.isChecked():
            pass
        else:
            self.VitaminKVvedenoYesCheckBox.setEnabled(1)
            self.VitaminKVvedenoYesCheckBox.setChecked(1)
            self.VitaminKVvedenoNoCheckBox.setEnabled(0)
            self.VitaminKVvedenoTerminLabel.show()
            self.VitaminKVvedenoTerminLineEdit.show()

    def VitaminKVvedenoYesFunc(self):
        if self.VitaminKVvedenoYesCheckBox.isChecked():
            pass
        else:
            self.VitaminKVvedenoNoCheckBox.setEnabled(1)
            self.VitaminKVvedenoNoCheckBox.setChecked(1)
            self.VitaminKVvedenoYesCheckBox.setEnabled(0)
            self.VitaminKVvedenoTerminLabel.hide()
            self.VitaminKVvedenoTerminLineEdit.hide()
            self.VitaminKVvedenoTerminLineEdit.setText('')

            # Обработчик 18) неонатальна смерть: 			а) ні  б) на ______добу
            # NeonatalnaSmertNoFunc NeonatalnaSmertYesFunc

    def NeonatalnaSmertNoFunc(self):
        if self.NeonatalnaSmertNoCheckBox.isChecked():
            pass
        else:
            self.NeonatalnaSmertNoCheckBox.setEnabled(0)
            self.NeonatalnaSmertYesCheckBox.setEnabled(1)
            self.NeonatalnaSmertYesCheckBox.setChecked(1)
            self.NeonatalnaSmertTerminLabel.show()
            self.NeonatalnaSmertTerminLineEdit.show()
            self.PruchunaSmertiZaRezyltatomAytopsiiLabel.setEnabled(1)
            self.PruchunaSmertiZaRezyltatomAytopsiiLineEdit.setEnabled(1)

    def NeonatalnaSmertYesFunc(self):
        if self.NeonatalnaSmertYesCheckBox.isChecked():
            pass
        else:
            self.NeonatalnaSmertYesCheckBox.setEnabled(0)
            self.NeonatalnaSmertNoCheckBox.setEnabled(1)
            self.NeonatalnaSmertNoCheckBox.setChecked(1)
            self.NeonatalnaSmertTerminLabel.hide()
            self.NeonatalnaSmertTerminLineEdit.hide()
            self.NeonatalnaSmertTerminLineEdit.setText('')
            self.PruchunaSmertiZaRezyltatomAytopsiiLabel.setEnabled(0)
            self.PruchunaSmertiZaRezyltatomAytopsiiLineEdit.setEnabled(0)
            self.PruchunaSmertiZaRezyltatomAytopsiiLineEdit.setText('')

            # Обработчик 1.	Перебіг: а)  нормальний , б) ускладнений
            ##PislapologovuiPerebigNoFunc  PislapologovuiPerebigYesFunc

    def PislapologovuiPerebigNoFunc(self):
        if self.PislapologovuiPerebigNoCheckBox.isChecked():
            pass
        else:
            self.PislapologovuiPerebigNoCheckBox.setEnabled(0)
            self.PislapologovuiPerebigYesCheckBox.setEnabled(1)
            self.PislapologovuiPerebigYesCheckBox.setChecked(1)

    def PislapologovuiPerebigYesFunc(self):
        if self.PislapologovuiPerebigYesCheckBox.isChecked():
            pass
        else:
            self.PislapologovuiPerebigYesCheckBox.setEnabled(0)
            self.PislapologovuiPerebigNoCheckBox.setEnabled(1)
            self.PislapologovuiPerebigNoCheckBox.setChecked(1)

            # Обработчик 2.	Чи проводилась профілактика/терапія ТЕУ: а) так б)ні
            # ProfilaktukaTerapiaTEYPynktIXNoFunc ProfilaktukaTerapiaTEYPynktIXYesFunc

    def ProfilaktukaTerapiaTEYPynktIXNoFunc(self):
        if self.ProfilaktukaTerapiaTEYPynktIXNoCheckBox.isChecked():
            pass
        else:
            self.ProfilaktukaTerapiaTEYPynktIXNoCheckBox.setEnabled(0)
            self.ProfilaktukaTerapiaTEYPynktIXYesCheckBox.setEnabled(1)
            self.ProfilaktukaTerapiaTEYPynktIXYesCheckBox.setChecked(1)

    def ProfilaktukaTerapiaTEYPynktIXYesFunc(self):
        if self.ProfilaktukaTerapiaTEYPynktIXYesCheckBox.isChecked():
            pass
        else:
            self.ProfilaktukaTerapiaTEYPynktIXYesCheckBox.setEnabled(0)
            self.ProfilaktukaTerapiaTEYPynktIXNoCheckBox.setEnabled(1)
            self.ProfilaktukaTerapiaTEYPynktIXNoCheckBox.setChecked(1)
            # Обработчик 2.1. Еластична компресія: 				    а) так б)ні	в) клас __
            # ElastuchnaKompressiaPynktIXNoFunc ElastuchnaKompressiaPynktIXYesFunc

    def ElastuchnaKompressiaPynktIXNoFunc(self):
        if self.ElastuchnaKompressiaPynktIXNoCheckBox.isChecked():
            pass
        else:
            self.ElastuchnaKompressiaPynktIXNoCheckBox.setEnabled(0)
            self.ElastuchnaKompressiaPynktIXYesCheckBox.setEnabled(1)
            self.ElastuchnaKompressiaPynktIXYesCheckBox.setChecked(1)
            self.ElastuchnaKompressiaPynktIXKlasLabel.show()
            self.ElastuchnaKompressiaPynktIXKlasLineEdit.show()

    def ElastuchnaKompressiaPynktIXYesFunc(self):
        if self.ElastuchnaKompressiaPynktIXYesCheckBox.isChecked():
            pass
        else:
            self.ElastuchnaKompressiaPynktIXYesCheckBox.setEnabled(0)
            self.ElastuchnaKompressiaPynktIXNoCheckBox.setEnabled(1)
            self.ElastuchnaKompressiaPynktIXNoCheckBox.setChecked(1)
            self.ElastuchnaKompressiaPynktIXKlasLabel.hide()
            self.ElastuchnaKompressiaPynktIXKlasLineEdit.hide()

            # Обработчик Медикаментозна профілактика / терапія	    а) так б)ні .......
            # MedukamentoznaProfilaktukaPynktIXNoFunc MedukamentoznaProfilaktukaPynktIXYesFunc

    def MedukamentoznaProfilaktukaPynktIXNoFunc(self):
        if self.MedukamentoznaProfilaktukaPynktIXNoCheckBox.isChecked():
            pass
        else:
            self.MedukamentoznaProfilaktukaPynktIXNoCheckBox.setEnabled(0)
            self.MedukamentoznaProfilaktukaPynktIXNoCheckBox.setFixedWidth(40)
            self.MedukamentoznaProfilaktukaPynktIXYesCheckBox.setEnabled(1)
            self.MedukamentoznaProfilaktukaPynktIXYesCheckBox.setChecked(1)
            self.MedukamentoznaProfilaktukaPynktIXLabel.setFixedWidth(300)
            self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyLabel.show()
            self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyLineEdit.show()
            self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyLabel.show()
            self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyLineEdit.show()
            self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznachenoLabel.show(
            )
            self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznachenoLineEdit.show(
            )

    def MedukamentoznaProfilaktukaPynktIXYesFunc(self):
        if self.MedukamentoznaProfilaktukaPynktIXYesCheckBox.isChecked():
            pass
        else:
            self.MedukamentoznaProfilaktukaPynktIXYesCheckBox.setEnabled(0)
            self.MedukamentoznaProfilaktukaPynktIXNoCheckBox.setFixedWidth(100)
            self.MedukamentoznaProfilaktukaPynktIXNoCheckBox.setEnabled(1)
            self.MedukamentoznaProfilaktukaPynktIXNoCheckBox.setChecked(1)
            self.MedukamentoznaProfilaktukaPynktIXLabel.setFixedWidth(400)
            self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyLabel.hide()
            self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyLineEdit.hide()
            self.MedukamentoznaProfilaktukaPynktIXNazvaPreparatyLineEdit.setText(
                '')
            self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyLabel.hide()
            self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyLineEdit.hide()
            self.MedukamentoznaProfilaktukaPynktIXRegumPrujomyLineEdit.setText(
                '')
            self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznachenoLabel.hide(
            )
            self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznachenoLineEdit.hide(
            )
            self.MedukamentoznaProfilaktukaPynktIXTerminKoluPruznachenoLineEdit.setText(
                '')

            # Обработчик 2.3Хірургічне лікування : а) так б)ні
            # HiryrgichneLikyvannaPynktIXNoFunc  HiryrgichneLikyvannaPynktIXYesFunc

    def HiryrgichneLikyvannaPynktIXNoFunc(self):
        if self.HiryrgichneLikyvannaPynktIXNoCheckBox.isChecked():
            pass
        else:
            self.HiryrgichneLikyvannaPynktIXNoCheckBox.setEnabled(0)
            self.HiryrgichneLikyvannaPynktIXYesCheckBox.setEnabled(1)
            self.HiryrgichneLikyvannaPynktIXYesCheckBox.setChecked(1)
            self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiLabel.show()
            self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiLineEdit.show()

    def HiryrgichneLikyvannaPynktIXYesFunc(self):
        if self.HiryrgichneLikyvannaPynktIXYesCheckBox.isChecked():
            pass
        else:
            self.HiryrgichneLikyvannaPynktIXYesCheckBox.setEnabled(0)
            self.HiryrgichneLikyvannaPynktIXNoCheckBox.setEnabled(1)
            self.HiryrgichneLikyvannaPynktIXNoCheckBox.setChecked(1)
            self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiLabel.hide()
            self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiLineEdit.hide()
            self.HiryrgichneLikyvannaPynktIXTerminNazvaOperaciiLineEdit.setText(
                '')

            # Обработчик 4.	Наявність ускладнень від проведеної профілактики: а) так б)ні
            # YskladnennaVidProfilaktukyPynktIXNoFunc YskladnennaVidProfilaktukyPynktIXYesFunc

    def YskladnennaVidProfilaktukyPynktIXNoFunc(self):
        if self.YskladnennaVidProfilaktukyPynktIXNoCheckBox.isChecked():
            pass
        else:
            self.YskladnennaVidProfilaktukyPynktIXNoCheckBox.setEnabled(0)
            self.YskladnennaVidProfilaktukyPynktIXYesCheckBox.setEnabled(1)
            self.YskladnennaVidProfilaktukyPynktIXYesCheckBox.setChecked(1)
            self.YskladnennaVidProfilaktukyPynktIXYskladnennaLabel.show()
            self.YskladnennaVidProfilaktukyPynktIXYskladnennaLineEdit.show()

    def YskladnennaVidProfilaktukyPynktIXYesFunc(self):
        if self.YskladnennaVidProfilaktukyPynktIXYesCheckBox.isChecked():
            pass
        else:
            self.YskladnennaVidProfilaktukyPynktIXYesCheckBox.setEnabled(0)
            self.YskladnennaVidProfilaktukyPynktIXNoCheckBox.setEnabled(1)
            self.YskladnennaVidProfilaktukyPynktIXNoCheckBox.setChecked(1)
            self.YskladnennaVidProfilaktukyPynktIXYskladnennaLabel.hide()
            self.YskladnennaVidProfilaktukyPynktIXYskladnennaLineEdit.hide()
            self.YskladnennaVidProfilaktukyPynktIXYskladnennaLineEdit.setText(
                '')

            # Обработчик 5.	Тромбоемболічні ускладнення :
            # TromboembolichniYskladnennaPynktIXNoFunc  TromboembolichniYskladnennaPynktIXYesFunc

    def TromboembolichniYskladnennaPynktIXNoFunc(self):
        if self.TromboembolichniYskladnennaPynktIXNoCheckBox.isChecked():
            pass
        else:
            self.TromboembolichniYskladnennaPynktIXNoCheckBox.setEnabled(0)
            self.TromboembolichniYskladnennaPynktIXNoCheckBox.setFixedWidth(40)
            self.TromboembolichniYskladnennaPynktIXLabel.setFixedWidth(180)
            self.TromboembolichniYskladnennaPynktIXYesCheckBox.setEnabled(1)
            self.TromboembolichniYskladnennaPynktIXYesCheckBox.setChecked(1)
            self.TromboembolichniYskladnennaPynktIXVudTeyLabel.show()
            self.TromboembolichniYskladnennaPynktIXVudTeyLineEdit.show()
            self.TromboembolichniYskladnennaPynktIXVudTeyLineEdit.setFixedWidth(
                200)
            self.TromboembolichniYskladnennaPynktIXTerminVunuknennaLabel.show()
            self.TromboembolichniYskladnennaPynktIXTerminVunuknennaLineEdit.show(
            )
            self.TromboembolichniYskladnennaPynktIXTerminVunuknennaLineEdit.setFixedWidth(
                200)
            self.TromboembolichniYskladnennaPynktIXTerapiaTEYLabel.show()
            self.TromboembolichniYskladnennaPynktIXTerapiaTEYLineEdit.show()
            self.TromboembolichniYskladnennaPynktIXTerapiaTEYLineEdit.setFixedWidth(
                200)

    def TromboembolichniYskladnennaPynktIXYesFunc(self):
        if self.TromboembolichniYskladnennaPynktIXYesCheckBox.isChecked():
            pass
        else:
            self.TromboembolichniYskladnennaPynktIXYesCheckBox.setEnabled(0)
            self.TromboembolichniYskladnennaPynktIXLabel.setFixedWidth(400)
            self.TromboembolichniYskladnennaPynktIXNoCheckBox.setFixedWidth(
                100)
            self.TromboembolichniYskladnennaPynktIXNoCheckBox.setEnabled(1)
            self.TromboembolichniYskladnennaPynktIXNoCheckBox.setChecked(1)
            self.TromboembolichniYskladnennaPynktIXVudTeyLabel.hide()
            self.TromboembolichniYskladnennaPynktIXVudTeyLineEdit.hide()
            self.TromboembolichniYskladnennaPynktIXTerminVunuknennaLabel.hide()
            self.TromboembolichniYskladnennaPynktIXTerminVunuknennaLineEdit.hide(
            )
            self.TromboembolichniYskladnennaPynktIXTerapiaTEYLabel.hide()
            self.TromboembolichniYskladnennaPynktIXTerapiaTEYLineEdit.hide()

            # Обработчик 6.	Мастит:   а) так; б) ні

    def MastutPynktIXNoFunc(self):
        if self.MastutPynktIXNoCheckBox.isChecked():
            pass
        else:
            self.MastutPynktIXNoCheckBox.setEnabled(0)
            self.MastutPynktIXYesCheckBox.setEnabled(1)
            self.MastutPynktIXYesCheckBox.setChecked(1)

    def MastutPynktIXYesFunc(self):
        if self.MastutPynktIXYesCheckBox.isChecked():
            pass
        else:
            self.MastutPynktIXYesCheckBox.setEnabled(0)
            self.MastutPynktIXNoCheckBox.setEnabled(1)
            self.MastutPynktIXNoCheckBox.setChecked(1)

            #     Обработчик    7.	Субінволюція матки:     а) так; б) ні

    def SubinvolyciaMatkuPynktIXNoFunc(self):
        if self.SubinvolyciaMatkuPynktIXNoCheckBox.isChecked():
            pass
        else:
            self.SubinvolyciaMatkuPynktIXNoCheckBox.setEnabled(0)
            self.SubinvolyciaMatkuPynktIXYesCheckBox.setEnabled(1)
            self.SubinvolyciaMatkuPynktIXYesCheckBox.setChecked(1)

    def SubinvolyciaMatkuPynktIXYesFunc(self):
        if self.SubinvolyciaMatkuPynktIXYesCheckBox.isChecked():
            pass
        else:
            self.SubinvolyciaMatkuPynktIXYesCheckBox.setEnabled(0)
            self.SubinvolyciaMatkuPynktIXNoCheckBox.setEnabled(1)
            self.SubinvolyciaMatkuPynktIXNoCheckBox.setChecked(1)

            # Обработчик 8.	Ендометрит:  а) так; б) ні

    def EndometrutPynktIXNoFunc(self):
        if self.EndometrutPynktIXNoCheckBox.isChecked():
            pass
        else:
            self.EndometrutPynktIXNoCheckBox.setEnabled(0)
            self.EndometrutPynktIXYesCheckBox.setEnabled(1)
            self.EndometrutPynktIXYesCheckBox.setChecked(1)

    def EndometrutPynktIXYesFunc(self):
        if self.EndometrutPynktIXYesCheckBox.isChecked():
            pass
        else:
            self.EndometrutPynktIXYesCheckBox.setEnabled(0)
            self.EndometrutPynktIXNoCheckBox.setEnabled(1)
            self.EndometrutPynktIXNoCheckBox.setChecked(1)

            # Обработчик 9.	Пізня післяпологова кровотеча:  а) так; б) ні

    def PiznaPologovaKrovotechaPynktIXNoFunc(self):
        if self.PiznaPologovaKrovotechaPynktIXNoCheckBox.isChecked():
            pass
        else:
            self.PiznaPologovaKrovotechaPynktIXNoCheckBox.setEnabled(0)
            self.PiznaPologovaKrovotechaPynktIXYesCheckBox.setEnabled(1)
            self.PiznaPologovaKrovotechaPynktIXYesCheckBox.setChecked(1)

    def PiznaPologovaKrovotechaPynktIXYesFunc(self):
        if self.PiznaPologovaKrovotechaPynktIXYesCheckBox.isChecked():
            pass
        else:
            self.PiznaPologovaKrovotechaPynktIXYesCheckBox.setEnabled(0)
            self.PiznaPologovaKrovotechaPynktIXNoCheckBox.setEnabled(1)
            self.PiznaPologovaKrovotechaPynktIXNoCheckBox.setChecked(1)

            # Обработчик 10.	Сепсис:  а) так; б) ні

    def SepsusPynktIXNoFunc(self):
        if self.SepsusPynktIXNoCheckBox.isChecked():
            pass
        else:
            self.SepsusPynktIXNoCheckBox.setEnabled(0)
            self.SepsusPynktIXYesCheckBox.setEnabled(1)
            self.SepsusPynktIXYesCheckBox.setChecked(1)

    def SepsusPynktIXYesFunc(self):
        if self.SepsusPynktIXYesCheckBox.isChecked():
            pass
        else:
            self.SepsusPynktIXYesCheckBox.setEnabled(0)
            self.SepsusPynktIXNoCheckBox.setEnabled(1)
            self.SepsusPynktIXNoCheckBox.setChecked(1)

            # Обработчик 11.	Розходження швів:   а) так; б) ні

    def RoshodgennaShvivPynktIXNoFunc(self):
        if self.RoshodgennaShvivPynktIXNoCheckBox.isChecked():
            pass
        else:
            self.RoshodgennaShvivPynktIXNoCheckBox.setEnabled(0)
            self.RoshodgennaShvivPynktIXYesCheckBox.setEnabled(1)
            self.RoshodgennaShvivPynktIXYesCheckBox.setChecked(1)

    def RoshodgennaShvivPynktIXYesFunc(self):
        if self.RoshodgennaShvivPynktIXYesCheckBox.isChecked():
            pass
        else:
            self.RoshodgennaShvivPynktIXYesCheckBox.setEnabled(0)
            self.RoshodgennaShvivPynktIXNoCheckBox.setEnabled(1)
            self.RoshodgennaShvivPynktIXNoCheckBox.setChecked(1)

            # Обработчик 13.	Хірургічні втручання в перші 6 тиж після пологів: а) так; б) ні

    def HirVtyrchannaVPershi6TugnivPynktIXNoFunc(self):
        if self.HirVtyrchannaVPershi6TugnivPynktIXNoCheckBox.isChecked():
            pass
        else:
            self.HirVtyrchannaVPershi6TugnivPynktIXNoCheckBox.setEnabled(0)
            self.HirVtyrchannaVPershi6TugnivPynktIXYesCheckBox.setEnabled(1)
            self.HirVtyrchannaVPershi6TugnivPynktIXYesCheckBox.setChecked(1)

    def HirVtyrchannaVPershi6TugnivPynktIXYesFunc(self):
        if self.HirVtyrchannaVPershi6TugnivPynktIXYesCheckBox.isChecked():
            pass
        else:
            self.HirVtyrchannaVPershi6TugnivPynktIXYesCheckBox.setEnabled(0)
            self.HirVtyrchannaVPershi6TugnivPynktIXNoCheckBox.setEnabled(1)
            self.HirVtyrchannaVPershi6TugnivPynktIXNoCheckBox.setChecked(1)

            # Обработчик 14.	Виписка додому:    а) так; б) ні;                          _______добу

    def VupuskaDodomyPynktIXYesFunc(self):
        if self.VupuskaDodomyPynktIXYesCheckBox.isChecked():
            pass
        else:
            self.VupuskaDodomyPynktIXYesCheckBox.setEnabled(0)
            self.VupuskaDodomyPynktIXNoCheckBox.setEnabled(1)
            self.VupuskaDodomyPynktIXNoCheckBox.setChecked(1)
            self.VupuskaDodomyPynktIXDobyLabel.setEnabled(0)
            self.VupuskaDodomyPynktIXDobyLineEdit.setEnabled(0)
            self.VupuskaDodomyPynktIXDobyLineEdit.setText('')
            self.PerevedennaVInshuiStacionarPynktIXNoCheckBox.setChecked(0)

    def VupuskaDodomyPynktIXNoFunc(self):
        if self.VupuskaDodomyPynktIXNoCheckBox.isChecked():
            pass
        else:
            self.VupuskaDodomyPynktIXNoCheckBox.setEnabled(0)
            self.VupuskaDodomyPynktIXYesCheckBox.setEnabled(1)
            self.VupuskaDodomyPynktIXYesCheckBox.setChecked(1)
            self.VupuskaDodomyPynktIXDobyLabel.setEnabled(1)
            self.VupuskaDodomyPynktIXDobyLineEdit.setEnabled(1)

            # Обработчик 15.	Переведена в інший стаціонар: а) так; б) ні                           _______добу

    def PerevedennaVInshuiStacionarPynktIXNoFunc(self):
        if self.PerevedennaVInshuiStacionarPynktIXNoCheckBox.isChecked():
            pass
        else:
            self.PerevedennaVInshuiStacionarPynktIXNoCheckBox.setEnabled(0)
            self.PerevedennaVInshuiStacionarPynktIXYesCheckBox.setChecked(1)
            self.PerevedennaVInshuiStacionarPynktIXYesCheckBox.setEnabled(1)
            self.PerevedennaVInshuiStacionarPynktIXDobyLabel.setEnabled(1)
            self.PerevedennaVInshuiStacionarPynktIXDobyLineEdit.setEnabled(1)

    def PerevedennaVInshuiStacionarPynktIXYesFunc(self):
        if self.PerevedennaVInshuiStacionarPynktIXYesCheckBox.isChecked():
            pass
        else:
            self.PerevedennaVInshuiStacionarPynktIXYesCheckBox.setEnabled(0)
            self.PerevedennaVInshuiStacionarPynktIXNoCheckBox.setChecked(1)
            self.PerevedennaVInshuiStacionarPynktIXNoCheckBox.setEnabled(1)
            self.PerevedennaVInshuiStacionarPynktIXDobyLabel.setEnabled(0)
            self.PerevedennaVInshuiStacionarPynktIXDobyLineEdit.setEnabled(0)
            self.PerevedennaVInshuiStacionarPynktIXDobyLineEdit.setText('')
            self.VupuskaDodomyPynktIXNoCheckBox.setChecked(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PrimaryWindow()
    sys.exit(app.exec_())
