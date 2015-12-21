import os

my_path = os.getcwd()


def find_and_rename():
    file_list = os.listdir(r"/Users/sergei.miroshnikov/Downloads/test-kro")
    print(file_list)
    os.chdir(r'/Users/sergei.miroshnikov/Downloads/test-kro')
    for file_name in file_list:
        print("Old name - " + file_name)
        print("New name - " + file_name.translate(None, "0123456789"))
        os.rename(file_name, file_name.translate(None, "0123456789"))  # WOW!
    os.chdir(my_path)


print(my_path)
find_and_rename()
