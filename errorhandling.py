from datetime import date

class Error:

	#global variables for errora location
	error_file_name = "error.log"
	error_file_location = "./logs/"
	runtime_error_storage = []

	def __init__(self, debug):
		self.debug = debug

	def get_date(self):
		current_date =date.today()
		return current_date.strftime("%d/%m/%y")

	#create and store and new error
	def new_error(self, error_type, error_information, return_error):
		todays_date = self.get_date()
		create_error_string = "[ " + error_type.upper() + " ] " + error_information + " - " + todays_date + "\n"
		error_address = self.error_file_location + self.error_file_name

		try:
			error_log_handle = open( error_address, "a+" )
			error_log_handle.write( create_error_string )
			error_log_handle.close()
		except:
			print("Error writing to the error log.")

		if self.debug == "True":
			error_array = [ error_type, error_information, todays_date]
			self.runtime_error_storage.append( error_array )

		if return_error == "True":
			return create_error_string
				
	def errors_count(self):
		if self.debug == "True":
			return self.runtime_error_storage.len()
		else:
			print("Error debugging must be enabled, maybe try enabling it with \"Error('True')\"")
