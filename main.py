import sys
import requests
import json
from errorhandling import Error
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QLineEdit,
    QTextEdit
)


class MyApplication(QWidget):
	def __init__(self):
		super().__init__()

		global config_data
		config_data = self.load_config_data()

		self.build_window()

	def load_config_data(self):		
		try:
			config_handle = open( "config/config.json", "r" )
			config_data = json.load(config_handle)
			return config_data

		except:
			config_error = Error("False")
			config_error.new_error("Invalid Config Data","It seems there was an error loading the config data.","False")
			

	def get_messages(self, message_box):
		try:	
			for addr in config_data['config']:
				message_request = requests.get( addr['get_addr'] )

				if message_request.status_code == 200:
					message_dict = json.loads(message_request.text)
					full_message_text = ""

					for message in message_dict['messages']:
						full_message_text = full_message_text + message['name'] + ": " + message['message_text'] + "\n\n"

					message_box.setText(full_message_text)
					message_box.moveCursor(QTextCursor.End)
		except:
			request_error = Error("False")
			request_error.new_error("Invalid Server Response", "It seems there was an error fetching and parsing the json data.", "True")

	def post_message(self, username, message_to_post_text, text_area, message_box):
		try:	
			#post the message
			print("Message sent...")	
		except:
			post_message_error = Error("False")
			post_message_error.new_error("Post Error", "An error occured while sending the message. Please try again...")

		self.text_area.setText("")
		message_box.setText("")
		self.get_messages(message_box)

	def build_window(self):		
		#Window UI controls
		self.setWindowTitle("ChatWindow")
		self.setGeometry(300,300,750,250)
		layout = QVBoxLayout()
		layout.addStretch()

		message_box = QTextEdit()
		message_box.setReadOnly(True)
		self.get_messages(message_box)
		self.text_area = QLineEdit(self)
		self.text_area.returnPressed.connect( lambda: self.post_message( config_data, self.text_area.text(), self.text_area, message_box ) )

		sendButton = QPushButton("Send Message")
		sendButton.setFixedWidth(100)

		#push button will run the post_message method
		sendButton.clicked.connect( lambda: self.post_message( config_data, self.text_area.text(), self.text_area, message_box ) )

		#add the widgets to the layout, create the GUI
		layout.addWidget(message_box)
		layout.addWidget( self.text_area )
		layout.addWidget(sendButton)
		self.setLayout(layout)

app = QApplication(sys.argv)
window = MyApplication()
window.show()

sys.exit(app.exec_())