from googlevoicesms import Voice
import getpass

def main():
    voice = Voice()
    email = input("email: ")
    password = getpass.getpass() # input("password: ")
    number = input("phone number to send sms to: ")
    voice.login(email, password)
    voice.send_sms(number, "pygooglevoice-sms")
    voice.logout()


main()
