# This program gathers user-entered information and then writes
# a comma-separated line containing the fields entered by the user
# to a file.  The file that was written to is then opened and read
# with the results being printed to the screen.

# The filename validation documentation and examples came from
# https://pypi.org/project/pathvalidate/#validate-a-filename
import sys
from pathvalidate import ValidationError, validate_filename


# Obtain the name of the file to read and write.  Call the function
# which prompts the user to enter information about themselves.
def main():

  # Prompt the user for a file name and then validate the entered
  # file name using pathvalidate.
  try:
    file_name_prompt = "Please enter a name for your file or type "
    file_name_prompt += "'q' to quit:\n"

    file_name = str(input(file_name_prompt)).strip()
    validate_filename(file_name)
  except ValidationError as e:
    print(f"{e}\n", file=sys.stderr)
    main()
  else:
    if file_name.lower() != 'q':
      file_text = get_user_info()

      try:
        with open(file_name, "w") as write_file_handle:
          write_file_handle.write(file_text)

        with open(file_name, "r") as read_file_handle:
          data = read_file_handle.read()

        print(data)
      except FileNotFoundError:
        print(f"Sorry, the file '{file_name}' does not exist.")


# This function prompts the user for various pieces of information
# in order to write to a file.
def get_user_info():
  ask = True
  user_name = ""
  address = ""
  phone = ""

  while ask:
    if not validate_input_data(user_name):
      name_prompt = "Please enter your name without commas:\n"
      user_name = str(input(name_prompt)).strip()

    if not validate_input_data(address):
      address_prompt = "Please enter your street address "
      address_prompt += "without commas:\n"
      address = str(input(address_prompt)).strip()

    if not validate_phone(phone):
      phone_prompt = "Please enter your phone number including "
      phone_prompt += "area code.\nDo not use commas.:\n"
      phone = str(input(phone_prompt)).strip()

    if validate_input_data(user_name) and validate_input_data(
        address) and validate_phone(phone):
      ask = False
    else:
      #print("Please supply the missing information.")
      ask = True

  return user_name + "," + address + "," + phone


# This function will test to make sure that the user-entered data
# is not blank and does not contain commas.  We do not want commas
# as we are writing the data so as to be comma-separated.
def validate_input_data(data):
  if len(data) != 0 and "," not in data:
    return True
  else:
    return False


# This function will validate a phone number to ensure it is all
# numbers and 10 digits long including area code.
def validate_phone(phone_num):
  stripped_phone = phone_num.replace("-", "")
  if stripped_phone.isnumeric() and len(
      str(stripped_phone)) == 10 and  \
      validate_input_data(stripped_phone):
    return True
  else:
    return False


# Call the main function.
main()
