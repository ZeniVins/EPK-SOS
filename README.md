# EPK-SOS

*********Elastic and kibana setup*********

1. Download Elastic version 6.6.0 : https://www.elastic.co/downloads/past-releases/elasticsearch-6-6-0
Download Kibana version 6.6.0 : https://www.elastic.co/downloads/past-releases/kibana-6-6-0

2. Make sure you installed java JDK 8 on your computer, in order to check you can execute : `java -version`
3. Make sure you JAVA_HOME is set : https://docs.oracle.com/cd/E19182-01/820-7851/inst_cli_jdk_javahome_t/ , in order to check you can execute in you cmd or terminal `echo %JAVA_HOME%` (windows)

4. Go into your elasticsearch folder: elasticsearch-6.6.0\bin and execute elasticsearch.sh (linux or mac) elasticsearch.batch (windows)
   Your data will be stored in the folder elasticsearch-6.6.0\data
   You can tune the memory allocate to the JVM (memory used by elasticsearch) by configuring the file elasticsearch-6.6.0\config\jvm.options : default is -Xms1g
 -Xmx1g (1 giga)
5. Go into kibana folder kibana-6.6.0-windows-x86_64\bin and exucute kibana.bach (same logic for the linux/mac version) and then access to you kibana interface : http://localhost:5601

*********Python script setup*********


6. install python version >= 3.6.0 to check if python is installed you can execute in you cmd or terminal: `python --version`
   If you have a previous version of python, make sure to uninstall it first 
7. install pip >= 9.0.1 on your computer
8. install virtualenv: `pip install virtualenv`
9. Clone the python script with `git clone https://github.com/ZeniVins/EPK-SOS.git` (require git installed : https://git-scm.com/downloads)
10. Access to the previous python project downloaded (EPK-SOS), and create a folder named `.env`, this folder will contain your dependencies
   Go into your .env folder and execute: `virtualenv elastic` 
11. access to your .env/elastic/Scrips and execute activate.bash (or : `source activate` for mac) yo are now under the elastic python environment.
12. with the same cmd/terminal access to the root project folder and execute: `pip install -r requirements.txt`
13. copy your log file into the folder logs (the name of your index will be the name of your file)
14. execute the script with : python main.py `path to my logs folder` (if not specified, default folder will be `logs` in your project)


*********Run the Python script when everything is already installed*********

11. access to your .env/elastic/Scrips and execute activate.bash (or : `source activate` for mac) yo are now under the elastic python environment.
12. make sure your Elastic and Kibana instances are running, if not re-execute the step 4 and 5   
13. copy your log file into the folder logs (the name of your index will be the name of your file)
14. execute the script with:  python main.py `path to my logs folder` (if not specified, default folder will be `logs` in your project)

*********Alternative installation for the python script*********

If you have hard time with python, pip, and virtualenv, you can directly download Pycharm community version : https://www.jetbrains.com/pycharm/
You still have to install python version >= 3.6.0

1. Clone the python script with `git clone https://github.com/ZeniVins/EPK-SOS.git` (require git installed : https://git-scm.com/downloads)
2. Open the previous python project downloaded (EPK-SOS) with pycharm
3. Click on File > Settings, Go into the section Project: EPK-SOS and click on Project interpreter
4. (still on the same view of the precedent step) In the section with `Project interpreter` (the one with a path), click on the gear and then click on `Add...`
5. Click on VirtualEnv Environment, select new environment, in `Location:` select a empty environment folder (can be any empty folder), preferably select your .env folder (EPK-SOS/.env) you can remove the readme.md if needed
6. On `Base interpreter` select your python (version >= 3.6.0), and then click on `Ok`
7. Click on button `Add Configuration` (top right of pycharm), and click on the plus button (+), select `python`
8. In `Script file` select the main.py python script (`EPK-SOS\main.py`) in the root folder of the project
9. In the `Parameters` you can specify your logs folder, but it's optional, your default logs folder will be EPK-SOS\logs in your project folder
10. Specify in `Python interpreter` the environment your previously created on step 5, click on apply and ok
11. Click on the tab `Terminal` (bottom left of the pycharm windows) and execute : `pip install -r requirements.txt`
12. click on the green button play to start your script, or directly in the pycharm terminal : python main.py `path to my logs folder` (if not specified, default folder will be `logs` in your project)