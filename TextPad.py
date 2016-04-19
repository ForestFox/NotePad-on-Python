# -*- coding: cp1251 -*-
import sys
from PyQt4 import QtGui, QtCore
import tkFileDialog
import sys
import charade
reload(sys)
sys.setdefaultencoding('utf8')

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, NewWindow = None, parent=None):
      
        self.fNewWind = NewWindow;                        #ФУНКЦІЯ СТВОРЕННЯ НОВОГО ВІКНА
        self.filename = ""                                #ІМ'Я ФАЙЛА
        
        QtGui.QMainWindow.__init__(self,parent)
        self.resize(600, 400)
        self.setWindowTitle(u'TextPad')
        self.setWindowIcon(QtGui.QIcon('Graphica\\tEditor.png'))     
        self.setToolTip(u"<b>It's TextPad..</b>")
        QtGui.QToolTip.setFont(QtGui.QFont('Times New Roman', 12))       
      
        self.textEdit = QtGui.QTextEdit(self)
        self.textEdit.setFont(QtGui.QFont('Calibri', 14))        
        self.setCentralWidget(self.textEdit)     

        self.dial = FindDialog(self.FindNext)            #ВІКНО ПОШУКУ    
        self.ReplaceDial = ReplaceDialog(self.ReplaceDo) #ВІКНО ЗАМІНИ  
        
        self.AddMenu()                                   #ФУНКЦІЯ ДОДАННЯ МЕНЮ
        self.ReadRecords()                               #ФУНКЦІЯ ОНОВЛЕННЯ ІСТОРІЇ ФАЙЛІВ(ВІДКРИТИХ)        
        
           
    def AddMenu(self):
      
        #######################################################################################################
        #МЕНЮ ЗАВАНТАЖЕННЯ,ЗБЕРЕЖЕННЯ, ТА ІНШЕ.....############################################################
        #######################################################################################################

        #НОВИЙ ФАЙЛ
        mn_act_New = QtGui.QAction(QtGui.QIcon('Graphica\\acNew.jpg'), u'New File', self)
        mn_act_New.setShortcut('Ctrl+N')
        mn_act_New.setStatusTip('Create new file...')
        self.connect(mn_act_New, QtCore.SIGNAL('triggered()'), self.New)
        
        #НОВЕ ВІКНО
        mn_act_NewWindow = QtGui.QAction(QtGui.QIcon('Graphica\\newwindow.png'), u'New Window', self)
        mn_act_NewWindow.setShortcut('Ctrl+Shift+N')
        mn_act_NewWindow.setStatusTip('Create new window...')
        self.connect(mn_act_NewWindow, QtCore.SIGNAL('triggered()'), self.fNewWind)

        #ВІДКРИТИ ФАЙЛ
        mn_act_Load = QtGui.QAction(QtGui.QIcon('Graphica\\acLoad.png'), u'Open', self)
        mn_act_Load.setShortcut('Ctrl+O')
        mn_act_Load.setStatusTip('Load existing file...')
        self.connect(mn_act_Load, QtCore.SIGNAL('triggered()'), self.LoadFile)
        
        #ПЕРЕВІДКРИТИ ФАЙЛ
        mn_act_Reload = QtGui.QAction(QtGui.QIcon('Graphica\\reload.jpg'), u'Reload', self)
        mn_act_Reload.setShortcut('F5')
        mn_act_Reload.setStatusTip('Reload file...')
        self.connect(mn_act_Reload, QtCore.SIGNAL('triggered()'), self.Reload)

        #ЗБЕРЕГТИ
        mn_act_Save = QtGui.QAction(QtGui.QIcon('Graphica\\acSave.png'), u'Save', self)
        mn_act_Save.setShortcut('Ctrl+S')
        mn_act_Save.setStatusTip('Save...')
        self.connect(mn_act_Save, QtCore.SIGNAL('triggered()'), self.Save)

        #ЗБЕРЕГТИ В ОКРЕМИЙ ФАЙЛ
        mn_act_SaveAs = QtGui.QAction(QtGui.QIcon('Graphica\\saveas.png'), u'Save as', self)
        mn_act_SaveAs.setShortcut('Ctrl+Shift+S')
        mn_act_SaveAs.setStatusTip('Save to other file...')
        self.connect(mn_act_SaveAs, QtCore.SIGNAL('triggered()'), self.SaveAs)

        #ЗАКРИТИ РЕДАКТОР
        mn_act_Exit = QtGui.QAction(QtGui.QIcon('Graphica\\acExit.png'), u'Close', self)
        mn_act_Exit.setShortcut('Alt+F4')
        mn_act_Exit.setStatusTip('Close file redactor...')
        self.connect(mn_act_Exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        #ЗАПОВНЕННЯ МЕНЮ
        menubar = self.menuBar()
        mnFile = menubar.addMenu(u'&File')
        mnFile.addAction(mn_act_New)
        mnFile.addAction(mn_act_NewWindow)
        mnFile.addAction(mn_act_Load)
        mnFile.addAction(mn_act_Reload)
        mnFile.addSeparator()
        mnFile.addAction(mn_act_Save)
        mnFile.addAction(mn_act_SaveAs)
        mnFile.addSeparator()
        self.menuLast = mnFile.addMenu(QtGui.QIcon('Graphica\\lastfiles.png'),"Last files") #РОЗКРИВНЕ МЕНЮ
        mnFile.addSeparator()
        mnFile.addAction(mn_act_Exit)        
        
        ###################################################################################################
        #МЕНЮ ПАРАМЕТРІВ...################################################################################
        ###################################################################################################
        
        mnSettings = menubar.addMenu(u'&Settings')
        
        mn_act_BackColor = QtGui.QAction(QtGui.QIcon('Graphica\\brush.png'), u'Background', self)        
        self.connect(mn_act_BackColor, QtCore.SIGNAL('triggered()'), self.EditBack)
        mnSettings.addAction(mn_act_BackColor)
        
        mn_act_Font = QtGui.QAction(QtGui.QIcon('Graphica\\fontatr.jpg'), u'Fount', self)
        self.connect(mn_act_Font,QtCore.SIGNAL('triggered()'), self.FontAtr)
        mnSettings.addAction(mn_act_Font)

        mn_act_FontColor = QtGui.QAction(QtGui.QIcon('Graphica\\fcolor.jpg'), u'Fount color', self)
        self.connect(mn_act_FontColor,QtCore.SIGNAL('triggered()'), self.FontColor)
        mnSettings.addAction(mn_act_FontColor)

        mn_act_WrapMode = QtGui.QAction(QtGui.QIcon('Graphica\\wrap.jpg'), u'Дозволити перенос слів', self)
        self.connect(mn_act_WrapMode, QtCore.SIGNAL('triggered()'), self.Wrap )
        mn_act_WrapMode.setCheckable(True)
        mnSettings.addAction(mn_act_WrapMode)


        ###################################################################################################
        #МЕНЮ РЕДАГУВАННЯ...###############################################################################
        ###################################################################################################      

        mnEdit = menubar.addMenu(u'&Edit')

        mn_act_Copy = QtGui.QAction(QtGui.QIcon('Graphica\\copy.png'), u'&Копіювати', self)
        mn_act_Copy.setShortcut('Ctrl+C')
        self.connect(mn_act_Copy, QtCore.SIGNAL('triggered()'), self.Copy)
        mnEdit.addAction(mn_act_Copy)
        
        mn_act_Cut = QtGui.QAction(QtGui.QIcon('Graphica\\cut.png'), u'&Вирізати', self)
        mn_act_Cut.setShortcut('Ctrl+X')
        self.connect(mn_act_Cut, QtCore.SIGNAL('triggered()'), self.Cut)
        mnEdit.addAction(mn_act_Cut)        

        mn_act_Paste = QtGui.QAction(QtGui.QIcon('Graphica\\paste.jpg'), u'&Вставити', self)
        mn_act_Paste.setShortcut('Ctrl+V')
        self.connect(mn_act_Paste, QtCore.SIGNAL('triggered()'), self.Paste)
        mnEdit.addAction(mn_act_Paste)

        mn_act_Delete = QtGui.QAction(QtGui.QIcon('Graphica\\delete.png'), u'&Видалити', self)
        mn_act_Delete.setShortcut('Del')
        self.connect(mn_act_Delete, QtCore.SIGNAL('triggered()'), self.Delete)
        mnEdit.addAction(mn_act_Delete)

        mn_act_Find = QtGui.QAction(QtGui.QIcon('Graphica\\find.png'), u'&Знайти', self)
        mn_act_Find.setShortcut('Ctrl+F')
        self.connect(mn_act_Find, QtCore.SIGNAL('triggered()'), self.Find)
        mnEdit.addAction(mn_act_Find)

        mn_act_Replace = QtGui.QAction(QtGui.QIcon('Graphica\\replace.gif'), u'&Замінити', self)
        mn_act_Replace.setShortcut('Ctrl+H')
        self.connect(mn_act_Replace, QtCore.SIGNAL('triggered()'), self.Replace)
        mnEdit.addAction(mn_act_Replace)

        mn_act_Select = QtGui.QAction(QtGui.QIcon('Graphica\\choose.png'), u'&Виділити все', self)
        mn_act_Select.setShortcut('Ctrl+A')
        self.connect(mn_act_Select, QtCore.SIGNAL('triggered()'), self.Select)
        mnEdit.addAction(mn_act_Select)

        ###################################################################################################
        #МЕНЮ КОДУВАНЬ...##################################################################################
        ###################################################################################################
        
        mnCoding = menubar.addMenu(u'&Coding')

        #ЗАВАНТАЖЕННЯ В ПЕВНОМУ КОДУВАННІ
        
        mn_act_LWinCode = QtGui.QAction(u'Open as Windows - 1251', self)
        mn_act_LWinCode.setShortcut('Alt+W')
        self.connect(mn_act_LWinCode, QtCore.SIGNAL('triggered()'), self.LCodingWin)        

        mn_act_LDosCode = QtGui.QAction(u'Open as DOS - 866', self)
        mn_act_LDosCode.setShortcut('Alt+D')
        self.connect(mn_act_LDosCode, QtCore.SIGNAL('triggered()'), self.LCodingDos)        

        mn_act_LKONCode = QtGui.QAction(u'Open as KOИ8 - p', self)
        mn_act_LKONCode.setShortcut('Alt+K')
        self.connect(mn_act_LKONCode, QtCore.SIGNAL('triggered()'), self.LCodingKON)        
        
        mnCoding.addAction(mn_act_LWinCode)
        mnCoding.addAction(mn_act_LDosCode)
        mnCoding.addAction(mn_act_LKONCode)

        #ПІДМЕНЮ......................................................................................
        
        mnLUnicods = mnCoding.addMenu("Open as Unicode")

        mn_act_LUnicode_UCS2_l = QtGui.QAction(u'UCS-2 little endian(standart)', self)
        mn_act_LUnicode_UCS2_l.setShortcut('Alt+L')
        self.connect(mn_act_LUnicode_UCS2_l, QtCore.SIGNAL('triggered()'), self.LCodingUCS2_l)

        mn_act_LUnicode_UCS2_b = QtGui.QAction(u'UCS-2 big endian', self)
        mn_act_LUnicode_UCS2_b.setShortcut('Alt+B')
        self.connect(mn_act_LUnicode_UCS2_b, QtCore.SIGNAL('triggered()'), self.LCodingUCS2_b)

        mn_act_LUnicode_UTF_8 = QtGui.QAction(u'UTF - 8', self)
        mn_act_LUnicode_UTF_8.setShortcut('Alt+U')
        self.connect(mn_act_LUnicode_UTF_8, QtCore.SIGNAL('triggered()'), self.LCodingUTF_8)

        
        mnLUnicods.addAction(mn_act_LUnicode_UCS2_l)
        mnLUnicods.addAction(mn_act_LUnicode_UCS2_b)
        mnLUnicods.addAction(mn_act_LUnicode_UTF_8)

        #.............................................................................................
        
        mnCoding.addSeparator()
        
        #ЗБЕРЕЖЕННЯ В ПЕВНОМУ КОДУВАННІ
        
        mn_act_SWinCode = QtGui.QAction(u'Save to Windows - 1251', self)
        mn_act_SWinCode.setShortcut('Ctrl+Alt+W')
        self.connect(mn_act_SWinCode, QtCore.SIGNAL('triggered()'), self.SCodingWin)        

        mn_act_SDosCode = QtGui.QAction(u'Save to DOS - 866', self)
        mn_act_SDosCode.setShortcut('Ctrl+Alt+D')
        self.connect(mn_act_SDosCode, QtCore.SIGNAL('triggered()'), self.SCodingDos)        

        mn_act_SKONCode = QtGui.QAction(u'Save to KOИ8 - p', self)
        mn_act_SKONCode.setShortcut('Ctrl+Alt+K')
        self.connect(mn_act_SKONCode, QtCore.SIGNAL('triggered()'), self.SCodingKON)        
        
        mnCoding.addAction(mn_act_SWinCode)
        mnCoding.addAction(mn_act_SDosCode)
        mnCoding.addAction(mn_act_SKONCode)

        #ПІДМЕНЮ......................................................................................
        
        mnSUnicods = mnCoding.addMenu("Save to Unicode")

        mn_act_SUnicode_UCS2_l = QtGui.QAction(u'UCS-2 little endian(standart)', self)
        mn_act_SUnicode_UCS2_l.setShortcut('Ctrl+Alt+L')
        self.connect(mn_act_SUnicode_UCS2_l, QtCore.SIGNAL('triggered()'), self.SCodingUCS2_l)

        mn_act_SUnicode_UCS2_b = QtGui.QAction(u'UCS-2 big endian', self)
        mn_act_SUnicode_UCS2_b.setShortcut('Ctrl+Alt+B')
        self.connect(mn_act_SUnicode_UCS2_b, QtCore.SIGNAL('triggered()'), self.SCodingUCS2_b)

        mn_act_SUnicode_UTF_8 = QtGui.QAction(u'UTF - 8', self)
        mn_act_SUnicode_UTF_8.setShortcut('Ctrl+Alt+U')
        self.connect(mn_act_SUnicode_UTF_8, QtCore.SIGNAL('triggered()'), self.SCodingUTF_8)
        
        mnSUnicods.addAction(mn_act_SUnicode_UCS2_l)
        mnSUnicods.addAction(mn_act_SUnicode_UCS2_b)
        mnSUnicods.addAction(mn_act_SUnicode_UTF_8)

        #.............................................................................................
        
        mnCoding.addSeparator()

        #ВИЗНАЧЕННЯ КОДУВАННЯ ТЕКСТУ

        mn_act_DetermCode = QtGui.QAction(u'Determine the coding', self)
        self.connect(mn_act_DetermCode, QtCore.SIGNAL('triggered()'), self.CodingDetermine)
        mnCoding.addAction(mn_act_DetermCode)

        
    #############################################################
    #ФУНКЦІЇ МЕНЮ "ФАЙЛ"...######################################################################
    #############################################################################################
        
    #............................................................................................
    def New(self):
      
        "ОЧИСТИТИ ПОЛЕ ТЕКСТУ"
        
        ExMess = QtGui.QMessageBox.question(self, u'Warning!', u"You can lost your data. Are you shure to create new file?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if ExMess == QtGui.QMessageBox.Yes:
            self.textEdit.setText("")
        else:
            event.ignore()
            
    #............................................................................................   
    def LoadFile(self,coding = "cp1251"):

        "ЗАВАНТАЖИТИ ФАЙЛ"        
        
        filename = QtGui.QFileDialog.getOpenFileName(self, u'Відкрити файл')        
        file = open(filename, 'r')
        data = file.read().decode(coding)
        self.textEdit.setText(data)
        self.filename = filename
        file.close()

    #............................................................................................    
    def Reload(self):

        "ПЕРЕЗАВАНТАЖИТИ ФАЙЛ"
        
        file = open(self.filename, 'r')
        data = file.read().decode('cp1251')
        self.textEdit.setText(data)     
        file.close()

    #............................................................................................   
    def Save(self):

        "ЗБЕРЕГТИ ФАЙЛ"
        
        if self.filename == "":
            self.SaveAs()
        else:
            file = open(self.filename,'w').write(self.textEdit.toPlainText())            
            file.close()          
                
    #............................................................................................       
    def SaveAs(self,coding = "cp1251"):

        "ЗБЕРЕГТИ ЯК"
        
        filename = QtGui.QFileDialog.getSaveFileName(self, u'Зберегти файл')
        file = open(filename,'w').write(self.textEdit.toPlainText().encode(coding))
        self.filename = filename
        self.AddRecord(filename)
        self.ReadRecords()
        file.close()

    #............................................................................................
    def AddRecord(self,record):

        "ДОДАТИ ЗАПИС В ІСТОРІЮ"
        
        file  = open('lastfiles.txt','a')
        file.write(record+'\n')
        file.close()
    
    def ReadRecords(self):

        "ОТРИМАТИ ЗАПИСИ З ІСТОРІЇ"
        
        file  = open('lastfiles.txt','r')
        text = file.readlines()
        file.close()
        text.reverse()
        for line in text:
            if text.index(line)==5:
                return
            fLast = QtGui.QAction(line.decode('cp1251'), self)
            self.connect(fLast, QtCore.SIGNAL('triggered()'), self.LoadFile)
            self.menuLast.addAction(fLast)

    #............................................................................................
    def closeEvent(self, event):

        "ЗАКРИТТЯ ФАЙЛУ"
        
        ExMess = QtGui.QMessageBox.question(self, u'Увага!', u"Ви впевнені, що хочете вийти?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if ExMess == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
        
    #############################################################################################
    #ФУНКЦІЇ МЕНЮ РЕДАГУВАННЯ...#################################################################
    #############################################################################################
      
                
    def EditBack(self):
        color = QtGui.QColorDialog.getColor()
        self.textEdit.setStyleSheet("QWidget { background-color: %s }" % color.name())

    def FontAtr(self):
        font, ok = QtGui.QFontDialog.getFont()
        if ok:
           self.textEdit.setFont(font)

    def FontColor(self):
        color = QtGui.QColorDialog.getColor()
        self.textEdit.setTextColor(color)          
            
    def Wrap(self):
        if self.textEdit.wordWrapMode() == QtGui.QTextOption.NoWrap:
            self.textEdit.setWordWrapMode(QtGui.QTextOption.WordWrap)
        elif self.textEdit.wordWrapMode() == QtGui.QTextOption.WordWrap:
            self.textEdit.setWordWrapMode(QtGui.QTextOption.NoWrap)

    def Cut(self):
        self.textEdit.cut()

    def Copy(self):
        self.textEdit.copy()

    def Paste(self):
        self.textEdit.paste()

    def Delete(self):
        self.textEdit.cut()

    def Find(self):
        self.dial.show()

    def FindNext(self):
        if self.dial.Backwards() == True:
            self.textEdit.find(self.dial.GetString(), QtGui.QTextDocument.FindBackward)
        else:
            self.textEdit.find(self.dial.GetString())
            
    def Replace(self):
        self.ReplaceDial.show()

    def ReplaceDo(self):
        while self.textEdit.find(self.ReplaceDial.GetSrs(), QtGui.QTextDocument.FindBackward):
            pass
        self.textEdit.textCursor().insertText(self.ReplaceDial.GetDest())
        while self.textEdit.find(self.ReplaceDial.GetSrs()):
            self.textEdit.textCursor().insertText(self.ReplaceDial.GetDest())

    def Select(self):
        self.textEdit.selectAll()

    #############################################################################################
    #ФУНКЦІЇ МЕНЮ КОДУВАНЬ...####################################################################
    #############################################################################################

    def LCodingWin(self):
        self.LoadFile('CP1251')

    def LCodingDos(self):
        self.LoadFile('CP866')

    def LCodingKON(self):
        self.LoadFile('KOI8-R')

    def LCodingUCS2_l(self):
        self.LoadFile('UTF-16LE')

    def LCodingUCS2_b(self):
        self.LoadFile('UTF-16BE')

    def LCodingUTF_8(self):
        self.LoadFile('UTF8')      

    def SCodingWin(self):
        self.SaveAs('CP1251')

    def SCodingDos(self):
        self.SaveAs('CP866')

    def SCodingKON(self):
        self.SaveAs('KOI8-R')

    def SCodingUCS2_l(self):
        self.SaveAs('UTF-16LE')

    def SCodingUCS2_b(self):
        self.SaveAs('UTF-16BE')

    def SCodingUTF_8(self):
        self.SaveAs('UTF8')

    def CodingDetermine(self):
        
        coding = charade.detect(self.textEdit.toPlainText())
        ExMess = QtGui.QMessageBox.question(self, u'Coding!', str(coding.items()), QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        


    
#ДІАЛОГОВЕ ВІКНО РЕДАГУВАННЯ(ЗАМІНИ) В ТЕКСТІ

class ReplaceDialog(QtGui.QWidget):
    def __init__(self,  FuncFind = None, parent=None,):

        QtGui.QWidget.__init__(self, parent,)
        self.BACK = False;
        self.setGeometry(300, 300, 200, 100)
        self.setWindowTitle(u'Пошук в тексті..')
        self.button = QtGui.QPushButton(u'Замінити всюди', self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.move(20, 20)
        self.connect(self.button, QtCore.SIGNAL('clicked()'), FuncFind)
        self.setFocus()

        self.labelSrc = QtGui.QLineEdit(self)
        self.labelSrc.move(20, 50)
        self.labelDest = QtGui.QLineEdit(self)
        self.labelDest.move(20, 70)

    def GetSrs(self):
        return self.labelSrc.text()

    def GetDest(self):
        return self.labelDest.text()

#ДІАЛОГОВЕ ВІКНО РЕДАГУВАННЯ(ПОШУК) В ТЕКСТІ
      
class FindDialog(QtGui.QWidget):
   def __init__(self,  FuncFind = None, parent=None,):

       QtGui.QWidget.__init__(self, parent, )
       self.BACK = True;
       self.setGeometry(300, 300, 250, 50)
       self.setWindowTitle(u'Пошук..')
       self.button = QtGui.QPushButton(u'Знайти', self)
       self.button.setFocusPolicy(QtCore.Qt.NoFocus)
       self.button.move(10, 10)
       self.connect(self.button, QtCore.SIGNAL('clicked()'), FuncFind)
       self.setFocus()
       self.label = QtGui.QLineEdit(self)
       self.label.move(100, 12)

   def GetString(self):
       return self.label.text()

   def Backwards(self):
        return self.BACK

#ГОЛОВНИЙ КЛАС ЗАПУСКУ ПРОГРАМИ
      
class Program:
   def __init__(self):
      self.WindowList = [] 
      app = QtGui.QApplication(sys.argv)
      main = MainWindow(self.NewWindow)        
      main.show()
      self.WindowList.append(main)           
      sys.exit(app.exec_())
   def NewWindow(self):      
      main = MainWindow(self.NewWindow)
      main.show()
      self.WindowList.append(main)
      

Program()
