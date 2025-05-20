import sys
from PyQt5 import QtCore
from PIL import Image
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QAbstractItemView \
    ,  QMainWindow, QTableWidgetItem, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QTableWidget
from PyQt5.QtWidgets import QLabel, QAbstractItemView, QMessageBox, QHeaderView, QInputDialog

PASSWORD_SYMBOLS = "!%@#$^&*"
ENG = "qwertyuiopasdfghjklzxcvbnm"
NUM = "1234567890"
back = "#MainWindow{background-image: url('sup/bg.jpg'); no-repeat;}"



import socket


class DBClient:
    def __init__(self):
        self.server_address = ('ru.tuna.am', 27027)
        self.timeout = 0.5

    def execute_query(self, query, params=None):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                s.connect(self.server_address)
                query_data = f"{query}|||{params}" if params else query
                s.sendall(query_data.encode('utf-8'))
                data = b""
                while True:
                    try:
                        chunk = s.recv(4096)
                        if not chunk:
                            break
                        data += chunk
                    except socket.timeout:
                        break
                return eval(data.decode()) if data else None

        except Exception as e:
            return None


class Vxodtyt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_client = DBClient()
        self.setStyleSheet(back)
        self.main()

    def main(self):
        uic.loadUi("ui/enter.ui", self)
        self.setWindowTitle("ChessTraining")
        self.setWindowIcon(QIcon('sup/logo.png'))
        self.entmegabtn.clicked.connect(self.wave)
        self.regbtn.clicked.connect(self.register)

    def wave(self):
        self.user_login = self.login.text()
        self.user_password = self.password.text()
        result = self.db_client.execute_query('SELECT * FROM pass WHERE name = ? AND password = ?',
                                              (self.user_login, self.user_password))
        if result != []:
            if result[0][0]:
                val = self.get_val()
                if val == 1:
                    self.studyyy = TeacherChooseMenu()
                    self.studyyy.show()
                    self.hide()
                elif val == 0:
                    self.study = Choosemenu()
                    self.study.show()
                    self.hide()
            else:
                self.lab.setText("Имя пользователя или пароль неверные")
        else:
            self.lab.setText("Имя пользователя или пароль неверные")


    def get_val(self):
        try:
            result = self.db_client.execute_query(
                'SELECT val FROM pass WHERE name = ? AND password = ?',
                (self.user_login, self.user_password)
            )
            if not result:
                return None
            val = result[0][0]
            return val

        except Exception as e:
            return None

    def register(self):
        uic.loadUi("ui/t2.ui", self)
        self.setWindowTitle("ChessTraining")
        self.setWindowIcon(QIcon('sup/logo.png'))
        self.setStyleSheet(back)
        #self.asteach.clicked.connect(self.reguser)
        self.asuser.clicked.connect(self.reguser)
        self.commandLinkButton2.clicked.connect(self.back)

    def back(self):
        sen = self.sender()
        if sen.objectName() == "commandLinkButton2":
            self.main()
        if sen.objectName() == "commandLinkButton3":
            self.register()

    def reguser(self):
        send = self.sender()
        if send.text() == "Как ученик":
            self.flag = 0
       # elif send.text() == "Как учитель": # На время тестов, чтобы не сломать уроки все
          #  self.flag = 1
        uic.loadUi("ui/t3.ui", self)
        self.setWindowTitle("ChessTraining")
        self.setWindowIcon(QIcon('sup/logo.png'))
        self.setStyleSheet(back)
        self.registerbtn.clicked.connect(self.prov)
        self.commandLinkButton3.clicked.connect(self.back)


    def prov(self):
        flag1, flag2, flags, flagup, flagdo, n = False,  False,  False,  False,  False, False
        self.login_reg = self.loginreg.text()
        self.password_reg = self.passreg.text()
        result = self.db_client.execute_query('SELECT name FROM pass WHERE name = ?', (self.login_reg,))
        if not result:
            flag1 = True
        else:
            self.labeler.setText("Такой пользователь уже есть")
        if 7 < len(self.password_reg) < 17:
            flag2 = True
        for i in self.password_reg:
            if i in PASSWORD_SYMBOLS:
                flags = True
            elif i in NUM:
                n = True
            elif i == i.upper():
                flagup = True
            elif i == i.lower():
                flagdo = True
        if flagup and flags and flag2 and flag1 and flagdo and n:
            result = self.db_client.execute_query("INSERT INTO 'pass' (name, password, val) VALUES (?, ?, ?)",
                                                  (self.login_reg, self.password_reg, self.flag))
            self.main()
        elif not flag2 or not flagup or not flagdo or not flags:
            self.labeler.setText("Пароль не соответствует критериям")


class Choosemenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.studymain()

    def studymain(self):
        uic.loadUi("ui/mainchoose.ui", self)
        self.setWindowTitle("ChessTraining")
        self.setWindowIcon(QIcon('sup/logo.png'))
        self.setStyleSheet(back)
        self.commandLinkButton.clicked.connect(self.back)
        self.ychebniyplan.clicked.connect(self.LES)
        self.spravka.clicked.connect(self.SPR)

    def SPR(self):
        self.SPRA = Sprav()
        self.SPRA.show()
        self.hide()

    def LES(self):
        self.LESIK = Lessonsst()
        self.LESIK.show()
        self.hide()


    def back(self):
        self.backvxodtyt = Vxodtyt()
        self.backvxodtyt.show()
        self.hide()


class TeacherChooseMenu(Choosemenu):
    def __init__(self):
        super().__init__()
        self.studymain()

    def studymain(self):
        uic.loadUi("ui/teachmainchoose.ui", self)
        self.setWindowTitle("ChessTraining")
        self.setWindowIcon(QIcon('sup/logo.png'))
        self.setStyleSheet(back)
        self.ychebniyplant.clicked.connect(self.LES)
        self.spravkat.clicked.connect(self.SPR)
        self.teacherbtn.clicked.connect(self.teacher)
        self.commandLinkButton.clicked.connect(self.back)

    def teacher(self):
        self.t = Teach()
        self.t.show()
        self.hide()

    def SPR(self):
        self.SPRA = Sprav_Teach()
        self.SPRA.show()
        self.hide()


class Teach(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mane()

    def mane(self):
        uic.loadUi('ui/lessons_plans.ui', self)
        self.setWindowTitle("ChessTraining")
        self.setWindowIcon(QIcon('sup/logo.png'))
        self.setStyleSheet(back)
        self.addbtn.clicked.connect(self.addi)
        self.commandLinkButton.clicked.connect(self.back)
        self.db_client = DBClient()
        self.poiskbut.clicked.connect(self.update_result)
        self.openbtn.clicked.connect(self.open_less)
        self.modified = {}
        self.titles = None
        self.delbtn.clicked.connect(self.delete_elem)
        self.tableWidget.doubleClicked.connect(self.open_less_on_double_click)
        self.update_result()

    def delete_elem(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        valid = QMessageBox.question(
            self, '', "Действительно удалить элементы с id " + ",".join(ids),
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            result = self.db_client.execute_query("DELETE FROM study_plans WHERE name = ?",
                                                   (self.tableWidget.currentItem().text(), ))
            self.update_result()

    def open_less_on_double_click(self, index):
        """Вызывается при двойном клике на таблицу."""
        self.open_less()

    def open_less(self):
        if self.tableWidget.currentItem():
            title = self.tableWidget.currentItem().text()
            self.viewR = ViewLesson(title)
            self.viewR.show()
            self.le = Lessonsst()
            self.le.hide()

    def update_result(self):
        self.wenty = self.lessline.text()
        if self.wenty and self.diff.currentText() != "Выберите...":
            result = self.db_client.execute_query("SELECT name FROM study_plans WHERE namelc LIKE ? AND diff = ?",
                                      (self.wenty.lower() + "%", self.diff.currentText(),))
        elif self.wenty and self.diff.currentText() == "Выберите...":
            result = self.db_client.execute_query("SELECT name FROM study_plans WHERE namelc LIKE ?",
                                      (self.wenty.lower() + "%",))
        elif not self.wenty and self.diff.currentText() != "Выберите...":
            result = self.db_client.execute_query("SELECT name FROM study_plans WHERE diff = ?",
                                      (self.diff.currentText(),))
        else:
            result = self.db_client.execute_query("SELECT name FROM study_plans")
        if result != []:

            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(len(result[0]))
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
            self.modified = {}
        else:
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(0)
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
            self.modified = {}


    def back(self):
        self.t = TeacherChooseMenu()
        self.t.show()
        self.hide()

    def addi(self):
        self.addw = AddLess()
        self.addw.show()
        self.addl = Teach()
        self.addl.hide()


class AddLess(QMainWindow):
    def __init__(self):
        super().__init__()
        self.img1, self.img2, self.img3, self.img4, self.img5 = 0, 0, 0, 0, 0
        self.mane()


    def mane(self):
        uic.loadUi('ui/addless.ui', self)
        self.lab.hide()
        self.setWindowTitle("ChessTraining")
        self.setWindowIcon(QIcon('sup/logo.png'))
        self.setStyleSheet(back)
        self.db_client = DBClient()
        self.addbtn.clicked.connect(self.save)
        self.commandLinkButton1.clicked.connect(self.op)
        self.commandLinkButton2.clicked.connect(self.op)
        self.commandLinkButton3.clicked.connect(self.op)
        self.commandLinkButton4.clicked.connect(self.op)
        self.commandLinkButton5.clicked.connect(self.op)
        self.commandLinkButton.clicked.connect(self.back)

    def back(self):
        self.hide()

    def op(self):
        sen = self.sender()
        if sen.text()[-1] == "1":
            self.img1 = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0].split("/")[-1]
        if sen.text()[-1] == "2":
            self.img2 = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0].split("/")[-1]
        if sen.text()[-1] == "3":
            self.img3 = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0].split("/")[-1]
        if sen.text()[-1] == "4":
            self.img4 = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0].split("/")[-1]
        if sen.text()[-1] == "5":
            self.img5 = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0].split("/")[-1]

    def save(self):
        flag1, flag2, flag3, flag4 = True, True, True, True
        self.x1, self.x2, self.x3, self.x4, self.x5 = self.xod1.toPlainText(), self.xod2.toPlainText(), \
            self.xod3.toPlainText(), self.xod4.toPlainText(), self.xod5.toPlainText()
        self.lab.clear()
        if self.x1 and self.x2 and self.x3 and self.x4 and self.x5:
            pass
        else:
            self.lab.setText('Вы не заполнили урок до конца: не все ходы были записаны')
            self.lab.show()
            flag1 = False
        if self.img1 and self.img2 and self.img3 and self.img4 and self.img5:
            pass
        else:
            self.lab.show()
            self.lab.setText('Вы не заполнили урок до конца: не все фотографии были загружены')
            flag2 = False
        if self.name.text():
            pass
        else:
            self.lab.show()
            self.lab.setText('Вы не заполнили урок до конца: имя урока не указано')
            flag3 = False
        if self.info.toPlainText():
            pass
        else:
            self.lab.show()
            self.lab.setText('Вы не заполнили урок до конца: нет описания урока')
            flag4 = False
        self.com = self.diff.currentText()
        if flag1 and flag2 and flag3 and flag4:
            result = self.db_client.execute_query("INSERT INTO study_plans (name, tag, namelc, pict1, move1, pict2, move2, pict3, move3,\
            pict4, move4, pict5, move5, diff) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,\
             ?)", (self.name.text(), self.info.toPlainText(), self.name.text().lower(), self.img1, self.x1,
                   self.img2, self.x2, self.img3, self.x3, self.img4, self.x4, self.img5, self.x5, self.com))
            self.back()


class Lessonsst(QMainWindow):
    def __init__(self):
        super().__init__()
        self.windowmain()

    def windowmain(self):
        uic.loadUi("ui/lessons_st.ui", self)
        self.setWindowTitle("ChessTraining")
        self.setWindowIcon(QIcon('sup/logo.png'))
        self.setStyleSheet(back)
        self.send = self.sender()
        self.commandLinkButton.clicked.connect(self.back)
        self.db_client = DBClient()
        self.poiskbut.clicked.connect(self.update_result)
        self.openbtn.clicked.connect(self.open_less)
        self.modified = {}
        self.titles = None
        self.tableWidget.doubleClicked.connect(self.open_less_on_double_click)
        self.update_result()

    def open_less_on_double_click(self, index):
        """Вызывается при двойном клике на таблицу."""
        self.open_less()

    def open_less(self):
        if self.tableWidget.currentItem():
            title = self.tableWidget.currentItem().text()
            self.viewR = ViewLesson(title)
            self.viewR.show()
            self.le = Lessonsst()
            self.le.hide()

    def update_result(self):
        self.wenty = self.lessline.text()
        if self.wenty and self.diff.currentText() != "Выберите...":
            result = self.db_client.execute_query("SELECT name FROM study_plans WHERE namelc LIKE ? AND diff = ?",
                                      (self.wenty.lower() + "%", self.diff.currentText(),))
        elif self.wenty and self.diff.currentText() == "Выберите...":
            result = self.db_client.execute_query("SELECT name FROM study_plans WHERE namelc LIKE ?",
                                      (self.wenty.lower() + "%",))
        elif not self.wenty and self.diff.currentText() != "Выберите...":
            result = self.db_client.execute_query("SELECT name FROM study_plans WHERE diff = ?",
                                      (self.diff.currentText(),))
        else:
            result = self.db_client.execute_query("SELECT name FROM study_plans")
        if result != []:
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(len(result[0]))
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
            self.modified = {}
        else:
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(0)
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
            self.modified = {}

    def back(self):
        if self.send.objectName() == 'ychebniyplan':
            self.backStudy = Choosemenu()
            self.backStudy.show()
            self.hide()
        elif self.send.objectName() == 'ychebniyplant':
            self.backteachstudy = TeacherChooseMenu()
            self.backteachstudy.show()
            self.hide()


class ViewLesson(QMainWindow):
    def __init__(self, name):
        super().__init__()
        self.mane(name)

    def mane(self, name):
        uic.loadUi('ui/Lesstipo.ui', self)
        self.setWindowTitle("ChessTraining")
        self.setWindowIcon(QIcon('sup/logo.png'))
        self.setStyleSheet(back)
        self.tagik = name
        self.commandLinkButton.clicked.connect(self.back)
        self.db_client = DBClient()
        self.namelabel.setText(name)
        result = self.db_client.execute_query("SELECT tag FROM study_plans WHERE namelc = ?", (name.lower(),))
        self.textBrowser.setText(result[0][0])
        self.commandLinkButton2.clicked.connect(self.tries)

    def tries(self):
        self.ti = Test(self.tagik)
        self.ti.show()
        self.hide()

    def back(self):
        self.hide()


class Test(QMainWindow):
    def __init__(self, tagik):
        super().__init__()
        self.image = QLabel(self)
        self.setStyleSheet(back)
        self.k = 1
        self.c = 0
        self.konec1, self.konec2, self.konec3, self.konec4, self.konec5 = None, None, None, None, None
        self.tries(tagik)
        self.show_photo()


    def tries(self, tagik):
        self.otv1, self.otv2, self.otv3, self.otv4, self.otv5 = "", "", "", "", ""
        self.xxx1, self.xxx2, self.xxx3, self.xxx4, self.xxx5, self.xxx6, self.xxx7, self.xxx8, self.xxx9, \
            self.xxx10 = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        self.tagik = tagik
        uic.loadUi('ui/try1.ui',self)
        self.num.setText(f"Задача №{self.k}")
        self.setWindowTitle("ChessTraining")
        self.setWindowIcon(QIcon('sup/logo.png'))
        self.pb.setValue(self.c)
        self.commandLinkButton4.hide()
        self.commandLinkButton3.hide()
        self.db_client = DBClient()
        result = self.db_client.execute_query("SELECT * FROM study_plans WHERE namelc = ?", (self.tagik.lower(),))
        self.namelabel.setText(self.tagik)
        self.ans = [a for a in result[0] if a != None]
        picts = self.db_client.execute_query("SELECT * FROM study_plans WHERE namelc = ?", (self.tagik.lower(),))[0]
        self.picts = [picts[3], picts[5], picts[7], picts[9], picts[11]]
        self.q1, self.q2, self.q3, self.q4, self.q5 = self.ans[4].split(", "), self.ans[6].split(", "), self.ans[8].split(", "), \
            self.ans[10].split(", "), self.ans[12].split(", ")
        self.commandLinkButton.clicked.connect(self.back)
        self.commandLinkButton2.clicked.connect(self.straight)
        self.rulesbtn.clicked.connect(self.rul)
        self.savebtn.clicked.connect(self.save)
        self.commandLinkButton3.clicked.connect(self.end)
        self.commandLinkButton4.clicked.connect(self.exit)

    def exit(self):
        self.hide()

    def end(self):
        self.flag = True
        self.itog = True
        if not self.konec1:
            self.flag = False
        if not self.konec2:
            self.flag = False
        if not self.konec3:
            self.flag = False
        if not self.konec4:
            self.flag = False
        if not self.konec5:
            self.flag = False
        if self.flag:
            self.c = 0
            if self.konec1 == self.ans[4]:
                self.c += 1
            if self.konec2 == self.ans[6]:
                self.c += 1
            if self.konec3 == self.ans[8]:
                self.c += 1
            if self.konec4 == self.ans[10]:
                self.c += 1
            if self.konec5 == self.ans[12]:
                self.c += 1
            self.pb.setValue(self.c)
            if self.konec1 != self.ans[4] or self.konec2 != self.ans[6] or self.konec3 != self.ans[8] or\
                    self.konec4 != self.ans[10] or self.konec5 != self.ans[12]:
                self.itog = False
            if self.itog:
                self.poditog()

    def poditog(self):
        self.labelit.setText("Поздравляем, вы прошли этот урок!")
        self.commandLinkButton3.hide()
        self.commandLinkButton4.show()


    def save(self):
        if self.xxx1 == 1:
            self.x1 = self.xod1.text()
        else:
            self.x1 = ''
        if self.xxx2 == 1:
            self.x2 = self.xod2.text()
        else:
            self.x2 = ''
        if self.xxx3 == 1:
            self.x3 = self.xod3.text()
        else:
            self.x3 = ''
        if self.xxx4 == 1:
            self.x4 = self.xod4.text()
        else:
            self.x4 = ''
        if self.xxx5 == 1:
            self.x5 = self.xod5.text()
        else:
            self.x5 = ''
        if self.xxx6 == 1:
            self.x6 = self.xod6.text()
        else:
            self.x6 = ''
        if self.xxx7 == 1:
            self.x7 = self.xod7.text()
        else:
            self.x7 = ''
        if self.xxx8 == 1:
            self.x8 = self.xod8.text()
        else:
            self.x8 = ''
        if self.xxx9 == 1:
            self.x9 = self.xod9.text()
        else:
            self.x9 = ''
        if self.xxx10 == 1:
            self.x10 = self.xod10.text()
        else:
            self.x10 = ''
        s = [self.x1, self.x2, self.x3, self.x4, self.x5, self.x6, self.x7, self.x8, self.x9, self.x10]
        s = [a for a in s if a != '']
        if self.k == 1:
            self.otv1 = ", ".join(s).lstrip().rstrip()
            self.konec1 = self.otv1
        if self.k == 2:
            self.otv2 = ", ".join(s)
            self.konec2 = self.otv2
        if self.k == 3:
            self.otv3 = ", ".join(s)
            self.konec3 = self.otv3
        if self.k == 4:
            self.otv4 = ", ".join(s)
            self.konec4 = self.otv4
        if self.k == 5:
            self.otv5 = ", ".join(s)
            self.konec5 = self.otv5

    def show_photo(self):
        if self.picts is not None:
            self.image.clear()
            a = "img/" + self.picts[self.k - 1]
            pic = self.compress_photo(a)
            self.pixmap = QPixmap(pic)
            self.image.move(50, 100)
            self.image.resize(400, 400)
            self.image.setPixmap(self.pixmap)
            if self.k == 1:
                self.r1 = self.prov(self.q1)
            if self.k == 2:
                self.r2 = self.prov(self.q2)
            if self.k == 3:
                self.r3 = self.prov(self.q3)
            if self.k == 4:
                self.r4 = self.prov(self.q4)
            if self.k == 5:
                self.r5 = self.prov(self.q5)

    def rul(self):
        self.rup = Rule()
        self.rup.show()

    def straight(self):
        if 0 < self.k < 5:
            self.tries(self.tagik)
            self.k += 1
            self.num.setText(f"Задача №{self.k}")
            self.commandLinkButton2.show()
            self.commandLinkButton3.hide()
        elif self.k <= 0:
            self.hide()
        if self.k == 5:
            self.commandLinkButton2.hide()
            self.commandLinkButton3.show()
        self.show_photo()

    def prov(self, arg):
        self.xod10.show()
        if len(arg) < 10:
            self.xxx10 = 0
            self.xod10.hide()
        self.xod9.show()
        if len(arg) < 9:
            self.xxx9 = 0
            self.xod9.hide()
        self.xod8.show()
        if len(arg) < 8:
            self.xxx8 = 0
            self.xod8.hide()
        self.xod7.show()
        if len(arg) < 7:
            self.xxx7 = 0
            self.xod7.hide()
        self.xod6.show()
        if len(arg) < 6:
            self.xxx6 = 0
            self.xod6.hide()
        self.xod5.show()
        if len(arg) < 5:
            self.xxx5 = 0
            self.xod5.hide()
        self.xod4.show()
        if len(arg) < 4:
            self.xxx4 = 0
            self.xod4.hide()
        self.xod3.show()
        if len(arg) < 3:
            self.xxx3 = 0
            self.xod3.hide()
        self.xod2.show()
        if len(arg) < 2:
            self.xxx2 = 0
            self.xod2.hide()
        self.xod1.show()
        if len(arg) < 1:
            self.xxx1 = 0
            self.xod1.hide()
            return 0
        return len(arg)

    def compress_photo(self, pict):
        im = Image.open(pict)
        im2 = im.resize((400, 400))
        im2.save(pict)
        return pict

    def back(self):
        self.k -= 1
        if 0 < self.k < 5:
            self.tries(self.tagik)
            self.num.setText(f"Задача №{self.k}")
            self.commandLinkButton2.show()
            self.commandLinkButton3.hide()
        elif self.k <= 0:
            self.hide()
        self.show_photo()


class Rule(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ru()

    def ru(self):
        uic.loadUi("ui/rules.ui", self)
        self.setWindowTitle("ChessTraining")
        self.setWindowIcon(QIcon('sup/logo.png'))
        self.commandLinkButton.clicked.connect(self.back)

    def back(self):
        self.hide()


class Sprav(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_client = DBClient()
        self.setStyleSheet(back)
        self.windowmain()
        self.findtem()

    def windowmain(self):
        uic.loadUi("ui/spravo4ka.ui", self)
        self.setWindowTitle("ChessTraining")
        self.setWindowIcon(QIcon('sup/logo.png'))
        self.send = self.sender()
        self.commandLinkButton.clicked.connect(self.back)
        self.addtem.clicked.connect(self.addtems)
        self.poisktem.clicked.connect(self.findtem)
        self.db_client = DBClient()
        self.modified = {}
        self.titles = None
        self.opentem.clicked.connect(self.open_temy)
        self.tableWidget.doubleClicked.connect(self.open_less_on_double_click)

    def open_less_on_double_click(self, index):
        """Вызывается при двойном клике на таблицу."""
        self.open_temy()

    def open_temy(self):
        if self.tableWidget.currentItem():
            title = self.tableWidget.currentItem().text()
            self.viewR = ViewTem(title)
            self.viewR.show()
            self.le = Sprav()
            self.le.hide()

    def findtem(self):
        self.wenty = self.temline.text()
        if self.wenty:
            result = self.db_client.execute_query("SELECT name FROM tems WHERE name LIKE ?",
                                 (self.temline.text() + "%",))
        else:
            result = self.db_client.execute_query("SELECT name FROM tems")
        self.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage("")
        self.tableWidget.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def addtems(self):
        self.addtemwin = AddTems()
        self.addtemwin.show()
        self.sprik = Sprav()
        self.sprik.hide()

    def back(self):
        if self.send.objectName() == 'spravka':
            self.backStudy = Choosemenu()
            self.backStudy.show()
            self.hide()
        elif self.send.objectName() == 'spravkat':
            self.backteachstudy = TeacherChooseMenu()
            self.backteachstudy.show()
            self.hide()


class Sprav_Teach(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_client = DBClient()
        self.setStyleSheet(back)
        self.windowmain()


    def windowmain(self):
        uic.loadUi("ui/spravo4ka_teach.ui", self)
        self.setWindowTitle("ChessTraining")
        self.setWindowIcon(QIcon('sup/logo.png'))
        self.send = self.sender()
        self.commandLinkButton.clicked.connect(self.back)
        self.addtem.clicked.connect(self.addtems)
        self.poisktem.clicked.connect(self.findtem)
        self.db_client = DBClient()
        self.modified = {}
        self.titles = None
        self.opentem.clicked.connect(self.open_temy)
        self.deltem.clicked.connect(self.delete_elem)
        self.tableWidget.doubleClicked.connect(self.open_less_on_double_click)
        self.findtem()


    def open_less_on_double_click(self, index):
        """Вызывается при двойном клике на таблицу."""
        self.open_temy()

    def delete_elem(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        valid = QMessageBox.question(
            self, '', "Действительно удалить элементы с id " + ",".join(ids),
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            result = self.db_client.execute_query("DELETE FROM tems WHERE name = ?",
                                                   (self.tableWidget.currentItem().text(), ))
            self.findtem()

    def open_temy(self):
        if self.tableWidget.currentItem():
            title = self.tableWidget.currentItem().text()
            self.viewR = ViewTem(title)
            self.viewR.show()
            self.le = Sprav_Teach()
            self.le.hide()

    def findtem(self):
        self.wenty = self.temline.text()
        if self.wenty:
            result = self.db_client.execute_query("SELECT name FROM tems WHERE name LIKE ?",
                                 (self.temline.text() + "%",))
        else:
            result = self.db_client.execute_query("SELECT name FROM tems")
        if result != []:
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(len(result[0]))
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
            self.modified = {}
        else:
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(0)
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
            self.modified = {}

    def addtems(self):
        self.addtemwin = AddTems()
        self.addtemwin.show()
        self.sprik = Sprav()
        self.sprik.hide()


    def back(self):
        if self.send.objectName() == 'spravka':
            self.backStudy = Choosemenu()
            self.backStudy.show()
            self.hide()
        elif self.send.objectName() == 'spravkat':
            self.backteachstudy = TeacherChooseMenu()
            self.backteachstudy.show()
            self.hide()


class ViewTem(QMainWindow):
    def __init__(self, name):
        super().__init__()
        self.db_client = DBClient()
        self.setStyleSheet(back)
        self.mane(name)

    def mane(self, name):
        uic.loadUi('ui/Tematipo.ui', self)
        self.setWindowTitle("ChessTraining")
        self.setWindowIcon(QIcon('sup/logo.png'))
        self.commandLinkButton.clicked.connect(self.back)
        self.db_client = DBClient()
        self.namelabel.setText(name)
        result = self.db_client.execute_query("SELECT info FROM tems WHERE namelc = ?", (name.lower(),))
        self.textBrowser.setText(result[0][0])

    def back(self):
        #  self.l = Lessonsst()
        #  self.l.show()
        self.hide()


class AddTems(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(back)
        self.db_client = DBClient()
        self.mainw()

    def mainw(self):
        uic.loadUi("ui/addtem.ui", self)
        self.setWindowTitle("ChessTraining")
        self.setWindowIcon(QIcon('sup/logo.png'))
        self.commandLinkButton.clicked.connect(self.back)
        self.addbtn.clicked.connect(self.addtem)


    def addtem(self):
        self.name = self.temname.text()
        self.info = self.temtext.toPlainText()
        result = self.db_client.execute_query("INSERT INTO tems (name, info, namelc) VALUES (?, ?, ?)",
                                              (self.name, self.info, self.name.lower(),))
        self.hide()

    def back(self):
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Vxodtyt()
    ex.show()
    sys.exit(app.exec_())
