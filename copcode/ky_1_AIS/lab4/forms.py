from PyQt5 import QtGui, QtCore, QtWidgets

def define_form_palette():
	palette = QtGui.QPalette()

	brush = QtGui.QBrush(QtGui.QColor(239, 239, 239))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
	brush = QtGui.QBrush(QtGui.QColor(239, 239, 239))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
	brush = QtGui.QBrush(QtGui.QColor(239, 239, 239))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
	brush.setStyle(QtCore.Qt.SolidPattern)

	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
	return palette

def define_name_palette():
	palette = QtGui.QPalette()
	brush = QtGui.QBrush(QtGui.QColor(84, 88, 133))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
	brush = QtGui.QBrush(QtGui.QColor(84, 88, 133))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
	brush = QtGui.QBrush(QtGui.QColor(84, 88, 133, 128))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
	brush = QtGui.QBrush(QtGui.QColor(84, 88, 133))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
	brush = QtGui.QBrush(QtGui.QColor(84, 88, 133))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
	brush = QtGui.QBrush(QtGui.QColor(84, 88, 133, 128))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
	brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
	brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
	brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
	brush.setStyle(QtCore.Qt.SolidPattern)

	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
	return palette

def define_property_palette():
	palette = QtGui.QPalette()
	brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
	brush = QtGui.QBrush(QtGui.QColor(127, 144, 196))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
	brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
	brush = QtGui.QBrush(QtGui.QColor(127, 144, 196))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
	brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
	brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
	brush = QtGui.QBrush(QtGui.QColor(127, 144, 196))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
	brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
	brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
	brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
	brush.setStyle(QtCore.Qt.SolidPattern)
	palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)

	return palette


def add_name(frame_city, idx):
	name = QtWidgets.QLabel(frame_city)
	name.setGeometry(QtCore.QRect(10, 10, 281, 41))

	palette = define_name_palette()
	name.setPalette(palette)

	font = QtGui.QFont()
	font.setPointSize(13)
	font.setBold(True)
	font.setWeight(75)
	name.setFont(font)
	name.setLayoutDirection(QtCore.Qt.LeftToRight)
	name.setFrameShape(QtWidgets.QFrame.StyledPanel)
	name.setLineWidth(2)
	name.setText("")
	name.setAlignment(QtCore.Qt.AlignCenter)
	name.setObjectName("name_" + str(idx))

	return name

def add_properties(frame_city, idx):
	properties = QtWidgets.QTextBrowser(frame_city)
	properties.setGeometry(QtCore.QRect(10, 70, 281, 131))

	palette = define_name_palette()
	properties.setPalette(palette)
	font = QtGui.QFont()
	font.setPointSize(13)
	properties.setFont(font)
	properties.setObjectName("properties_" + str(idx))

	return properties

def add_btn_like(frame_city, idx):
	btn_like = QtWidgets.QPushButton(frame_city)
	btn_like.setGeometry(QtCore.QRect(20, 220, 121, 31))

	palette = define_property_palette()
	btn_like.setPalette(palette)
	font = QtGui.QFont()
	font.setPointSize(13)
	font.setStyleStrategy(QtGui.QFont.PreferDefault)
	btn_like.setFont(font)
	btn_like.setObjectName("btn_like_" + str(idx))

	return btn_like

def add_btn_dislike(frame_city, idx):
	btn_dislike = QtWidgets.QPushButton(frame_city)
	btn_dislike.setGeometry(QtCore.QRect(150, 220, 121, 31))

	palette = define_property_palette()	
	btn_dislike.setPalette(palette)
	font = QtGui.QFont()
	font.setPointSize(13)
	font.setStyleStrategy(QtGui.QFont.PreferDefault)
	btn_dislike.setFont(font)
	btn_dislike.setObjectName("btn_dislike_" + str(idx))

	return btn_dislike

def add_frame(scrollArea, idx):
	frame_city = QtWidgets.QFrame(scrollArea)

	sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
	sizePolicy.setHorizontalStretch(0)
	sizePolicy.setVerticalStretch(0)
	sizePolicy.setHeightForWidth(frame_city.sizePolicy().hasHeightForWidth())
	frame_city.setSizePolicy(sizePolicy)
	frame_city.setMinimumSize(QtCore.QSize(301, 271))

	palette = define_form_palette()
	frame_city.setPalette(palette)
	frame_city.setAutoFillBackground(True)
	frame_city.setFrameShape(QtWidgets.QFrame.StyledPanel)
	frame_city.setFrameShadow(QtWidgets.QFrame.Raised)
	frame_city.setObjectName("frame_city_" + str(idx))

	name = add_name(frame_city, idx)
	properties = add_properties(frame_city, idx)
	
	btn_like = add_btn_like(frame_city, idx)
	btn_dislike = add_btn_dislike(frame_city, idx)
	
	_translate = QtCore.QCoreApplication.translate
	btn_like.setText(_translate("MainWindow", "Нравится"))
	btn_dislike.setText(_translate("MainWindow", "Не нравится")) 
	
	return frame_city, name, properties, btn_like, btn_dislike