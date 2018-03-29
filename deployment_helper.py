import os
import sys


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def prepare_requirements():
    '''
    Creates requirements.txt with pip freeze and adds "django-extensions"
    and "gunicorn" in as well. Best done once project is finished and ready
    for deployment. BE SURE IN your virtual environment before you run
    this command.
    '''
    os.system("pip freeze --local > requirements.txt")
    os.system("echo 'django-extenstions' >> requirements.txt")
    os.system("echo 'gunicorn' >> requirements.txt")
    os.system("git add . && git commit -m 'added requirements.txt'")
    print("Finished Building 'requirements.txt'\n")


def git_init():
    '''
    Initializes a local git repo and performs the inital commit.
    '''
    os.system("echo '*.pyc' > .gitignore")
    os.system("echo '/home/ubuntu/django_env/' >> .gitignore")
    os.system("git init")
    os.system("git add .")
    os.system("git commit -m 'initial commit'")


def update_apt():
    os.system("sudo apt-get update")


def build_py_env():
    '''
    Installs pip, python-dev, nginx, git, virtualenv. Run this command once
    on a brand new server.
    '''
    update_apt()
    os.system("sudo apt-get install python-pip python-dev nginx git")
    update_apt()
    os.system("sudo -H pip install virtualenv")
    update_apt()


def load_venv():
    '''
    Installs all packages in requirements.txt
    BE IN YOUR VENV FIRST
    '''
    os.system("pip install -r requirements.txt")
    os.system("pip freeze")
    print("Completed loadenv Command")


def perpare_server_for_app():
    '''
    Build the neccessary nginx, and gunicorn files, as well as setup settings.py
    with the proper changes it needs to communicate with gunicorn.
    '''
    REPO_PATH = os.getcwd()
    REPO_NAME = REPO_PATH.split("/")[-1]
    # public_ip = raw_input(" Enter your yourEC2.public.ip: ")
    PUBLIC_IP = '18.221.207.53'
    dir_list = list(enumerate(os.listdir(".")))
    choices = {}
    for num, directory in dir_list:
        choices[str(num)] = directory
    print("Select the location of your Project Dir (must contain settings.py)")
    for key, value in choices.items():
        print("{}. --> {}".format(key, value))
    choice = raw_input("Enter the number of your choice: ")
    clear()
    PROJ_NAME = choices[choice]
    
    to_change_settings_py = raw_input("Would you like to edit Settings.py? y/N").upper()
    if to_change_settings_py == Y:
        os.chdir(PROJ_NAME)
        os.system("echo '' >> settings.py ")
        os.system("echo '#{}' >> settings.py".format(PUBLIC_IP))
        print("Your about to enter 'settings.py'\n")
        print("\tCopy and paste at the bottom of the file:\n\n\tSTATIC_ROOT = os.path.join(BASE_DIR, 'static/')\n")
        print("\tFirst thing after pasting is to set DEBUG = FALSE\n")
        print("\tMove commented out ip address at the base of the file into ALLOWED_HOSTS")
        wait = raw_input("\nPress ENTER to continue")
        os.system("vim settings.py")

        os.chdir("..")
        os.system("python manage.py collectstatic")

    placeholders = {"repoName": REPO_NAME, "projectName": PROJ_NAME, "public_ip": PUBLIC_IP}
    gunicorn_service = '''
    [Unit]
    Description=gunicorn daemon
    After=network.target
    [Service]
    User=ubuntu
    Group=www-data
    WorkingDirectory=/home/ubuntu/{repoName}
    ExecStart=/home/ubuntu/{repoName}/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/{repoName}/{projectName}.sock {projectName}.wsgi:application
    [Install]
    WantedBy=multi-user.target
    '''.format(**placeholders)
    os.system("sudo echo '{}' > /etc/systemd/system/gunicorn.service".format(gunicorn_service))
    os.system("sudo systemctl daemon-reload")
    os.system("sudo systemctl start gunicorn")
    os.system("sudo systemctl enable gunicorn")
    os.system("sudo service gunicorn status")

    nginx_file = "server {\n\tlisten 80;\n"
    nginx_file += "\tserver_name {};\n".format(PUBLIC_IP)
    nginx_file += "\tlocation = /favicon.ico { access_log off; log_not_found off; }\n"
    nginx_file += "\tlocation /static/ {\n"
    nginx_file += "\t\troot /home/ubuntu/{};\n".format(REPO_NAME)
    nginx_file += "\t}\n\tlocation / {\n\t\tinclude proxy_params;\n"
    nginx_file += "\t\tproxy_pass http://unix:/home/ubuntu/{repoName}/{projectName}.sock;\n".format(**placeholders)
    nginx_file += "\t}\n}"
    os.system("sudo echo '{}' >> /etc/nginx/sites-available/{}".format(nginx_file, PROJ_NAME))

    os.system("sudo ln -s /etc/nginx/sites-available/{} /etc/nginx/sites-enabled".format(PROJ_NAME))
    os.system("sudo nginx -t")
    os.system("sudo rm /etc/nginx/sites-enabled/default")
    os.system("sudo service nginx restart")
    os.system("sudo service nginx status")
    print("Completed serverconfig")


def build_venv():
    os.system("virtualenv venv")


def main():
    try:
        if sys.argv[1] == "requirements":
            prepare_requirements()
        elif sys.argv[1] == "serverconfig":
            perpare_server_for_app()
        elif sys.argv[1] == "gitinit":
            git_init()
        elif sys.argv[1] == "loadvenv":
            load_venv()
        elif sys.argv[1] == "pyenv":
            build_py_env()
        elif sys.argv[1] == 'buildvenv':
            build_venv()

    except IndexError:
        print("Possible Args:\n")
        print("---------- Local Machine ----------")
        print("'gitinit{}".format(git_init.__doc__))
        print("'requirements'{}".format(prepare_requirements.__doc__))
        print("---------- Remote Machine ----------")
        print("'pyenv'{}".format(build_py_env.__doc__))
        print("'buildvenv'{}".format(build_venv.__doc__))
        print("'loadenv'{}".format(load_venv.__doc__))
        print("'serverconfig'{}".format(perpare_server_for_app.__doc__))


if __name__ == '__main__':
    clear()
    print("WELCOME TO DEPLOYMENT HELPER\n")
    main()
