from MainWindow import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QApplication
import sys

class MainWindowController(QMainWindow, Ui_MainWindow):
    
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        #self.instrucciones = ""
        #self.modo = ""

    def obtener_configuracion_usuario(self):
    # Obtener instrucciones
        instrucciones = self.ui.txtedtInstructions.toPlainText()

    # Modo de ejecución
        if self.ui.rbtnStepByStep.isChecked():
            modo = "paso_a_paso"
        elif self.ui.rbtnCiclesPerSecond.isChecked():
            modo = "por_ciclos"
        elif self.ui.rbtnCompleteExecution.isChecked():
            modo = "completo"
        else:
            modo = None

        # Unidad de riesgos / predicción
        if self.ui.rbtnWithoutHazards.isChecked():
            riesgos = "sin_unidad"
        elif self.ui.rbtnWithHazards.isChecked():
            riesgos = "con_unidad"
        elif self.ui.rbtnMode.isChecked():
            riesgos = "con_prediccion"
        else:
            riesgos = None
        print(instrucciones)
        print("*****************")
        print(modo)
        print("*****************")
        print(riesgos)
        return instrucciones, modo, riesgos



