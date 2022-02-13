# Import the modules for the GUI
from PyQt5.QtWidgets import *
from PyQt5 import uic
# Imports the moduels for the SMTP intergration
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
# Main Code
class MailClient(QMainWindow):

    def __init__(self):
        super(MailClient, self).__init__()
        uic.loadUi("mailgui.ui", self)
        self.show()

        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.attach_sth)
        self.pushButton_3.clicked.connect(self.send_mail)

    
    def login(self):
        try:
            self.server = smtplib.SMTP(self.lineEdit_3.text(), self.lineEdit_4.text())
            self.server.ehlo
            self.server.starttls()
            self.server.ehlo()
            self.server.login(self.lineEdit.text(), self.lineEdit_2.text())

            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.lineEdit_3.setEnabled(False)
            self.lineEdit_4.setEnabled(False)
            self.pushButton.setEnabled(False)

            self.lineEdit_5.setEnabled(True)
            self.lineEdit_6.setEnabled(True)
            self.lineEdit_7.setEnabled(True)
            self.textEdit.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)

            self.msg = MIMEMultipart()
        except smtplib.SMTPAuthenticationError:
            message_box = QMessageBox()
            message_box.setText("Invalid Email or password. Please make sure you typed it correctly and, for Gmail users, go to the less secure apps and enable it. Google your email provider and then less secure apps for other mail clients.")
            message_box.exec()
        except:
            message_box = QMessageBox()
            message_box.setText("An problem occured while logging in. It might be that you misspelld the SMTP server or the port, or it might be that the server of the email client is down. Whatever the case is, it might be an issue from our end. You can submit an issue through Github and we will help you. ")
            message_box.exec()

    def attach_sth(self):
        options = QFileDialog.Options()
        filenames, _ = QFileDialog.getOpenFileNames(self, "Attach", "", "All Files (*.*)", options=options)
        if filenames != []:
            for filename in filenames:
                attachement = open(filename, 'rb')

                
                p = MIMEBase('application', 'octet-stream')
                p.set_payload(attachement.read())
                encoders.encode_base64(p)
                p.add_header("Content-Disposition", f"attachement; filename={filename}")
                self.msg.attach(p)
    
    
    def send_mail(self):
        dialog = QMessageBox()
        dialog.setText("Do you want to send this mail?")
        dialog.addButton(QPushButton("Yes"), QMessageBox.YesRole) # 0
        dialog.addButton(QPushButton("No"), QMessageBox.NoRole) # 1

        if dialog.exec_() == 0:
            try:
                self.msg['From'] = self.lineEdit.text()
                self.msg['To'] = self.lineEdit_5.text()
                self.msg['Subject'] = self.lineEdit_6.text()
                self.msg.attach(MIMEText(self.textEdit.toPlainText(), 'plain'))
                text = self.msg.as_string()
                self.server.sendmail(self.lineEdit.text(), self.lineEdit_5.text(), text)
                message_box = QMessageBox()
                message_box.setText("The mail is sent.")
                message_box.exec()
            except:
                message_box = QMessageBox()
                message_box.setText("A problem occured while the mail was being sent.")
                message_box.exec()
                
            
            
            
# Show the GUI
app = QApplication([])
window = MailClient()
app.exec_()
