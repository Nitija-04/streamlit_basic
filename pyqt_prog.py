from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

def on_click():
    window.config(bg=color)

app = QApplication([])
window = QWidget()
window.setWindowTitle("Signal and Slot")

button = QPushButton("Dil mein mere hain", window)
button.clicked.connect(on_click)
button.move(100,100) #x=100, y=100

window.resize(300,200)
window.show()

app.exec_()