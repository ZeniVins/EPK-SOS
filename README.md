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
7. install pip >= 9.0.1 on your computer
8. install virtualenv: `pip install virtualenv`
9. Access to the python project, and create a folder named `.env`, this folder will contain your dependencies
   Go into your .env folder and execute: virtualenv elastic 
10. access to your .env/elastic/Scrips and execute activate.bash (or : `source activate` for mac) yo are now under the elastic python environment.
11. with the same cmd/terminal access to the root project folder and execute: `pip install -r requirements.txt`
12. copy your log file into the folder logs (the name of your index will be the name of your file)
13. execute the script with : python main.py `path to my logs folder` (if not specified, default folder will be `logs` in your project)


*********Run the Python script when everything is already installed*********

10. access to your .env/elastic/Scrips and execute activate.bash (or : `source activate` for mac) yo are now under the elastic python environment.
11. with the same cmd/terminal access to the root project folder and execute: pip install -r requirement.txt
12. copy your log file into the folder logs (the name of your index will be the name of your file)
13. execute the script with:  python main.py `path to my logs folder` (if not specified, default folder will be `logs` in your project)
