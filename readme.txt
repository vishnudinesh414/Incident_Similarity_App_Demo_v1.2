
------------------------------------------------------------------------------------------------------------------------

Setting Up the app

1. Extract the folder where ever you want

---Backend---
1. Open CMD in the backend folder position

Create Environment
-----------------------
2. Go to automate_python folder using "cd automate_python"
3. run the command "python automate_setup.py"

    This will create a dedicated environment and install necessary packages and libraries

4. Once done go to environment and activate it (You may need to go back to the base folder using "cd .." and give command "python_env\Scripts\activate")

Train and create our Custom model
-------------------------------------
6. Once activate run the command "python app_training.py"
(if nltk issue is there give this "python -m nltk.downloader stopwords" and start from step 1)
7. Once done you can run the app using "python app.py" and you are good to go

(Use postman to inspect payload and output)


---Frontend---
1. Open the root folder preferably in vscode open terminal
2. Navigate to frontend folder using "cd frontend"
3. run "npm install" to install node modules
4. run "npm run build" and create build


---nginx.config---
1. Copy absolute path of build folder from app frontend
2. Replace root in nginx.conf with absolute path (You need to change backward slash to forward slash) and save it
    eg, 
        "C:\Incident Similarity Analysis\frontend\build"  --->  "C:/Incident Similarity Analysis/frontend/build" (use your absolute path)

-------------------------------------------------------------------------------------------------------------------------


Installation of Nginx

---nginx---
1. download nginx from this link https://nginx.org/download/nginx-1.26.2.zip
2. Once download extract the folder into C drive and rename the  nginx-1.26.2 folder to nginx only
3. Copy nginx.conf file from app root directory
4. Paste and Replace the file to C:\nginx\conf folder
5. Open cmd in nginx directory and type "start nginx"
    now server is Up

-------------------------------------------------------------------------------------------------------------------------

now go to http://localhost:9000/

-------------------------------------------------------------------------------------------------------------------------

##### HAPPY CODING ######

