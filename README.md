# Shopify_Backend
This is a CRUD web app created for the Shopify Backend Intern application for summer of 2022. The problem statement offered by Shopify is https://docs.google.com/document/d/1z9LZ_kZBUbg-O2MhZVVSqTmvDko5IJWHtuFmIu_Xg1A/edit


SETUP:
------
First, download the zip file from git hub and extract it.
In the folder that you extrated from the zip open a terminal/comand prompt
Then download python version 3.9.10, it should work on any version but that the one I used.
(check your python version using python --version or python3 --version (we ussually use python3 in mac))
Also download vertual environment using the command "pip install virtualenv"
then create your virtual environment by using the command "virtualenv __name of venv__"
then activate the environment using (for mac) "source venv/bin/activate" (for windows) "__name of venv__\Scripts\ativate.bat"
Download flask as well using "pip install flask" in the your virtual env
Then run the command “flask run” which should give you a link (make sure you are running this command in the folder where app.py is in)
Copy and paste the link into any browser 


ABOUT THIS WEB APP
------------------
This web app simulates a invontory whre it has the CRUD functionality, which means you can Creat, Review, Update, and Delete the items.
Here I already have some items in the database "logistics_comp.db" but you can create your own by clicking the create button.
In the create you can chose to cancel and go back to the main page or click submit after you fill in the data. If you click submit and it refreshes the page and does not take you back to the main page then you have left one of the boxes empty.
You can also choose to delete the item you just created by clicking the delte button next to it and a warning messege will pop up to confirm.
You can also choose to edit the data in a certain item by just clicking the edit button next to it. 
You will see that it is a very similar layout to the create page. Unfotunately I did not have time to implement the feature where it autofills the boxes with the data alreafy in the db, so you will HAVE to add in all the data again even if it is different in just one category. If you do not fill all the boxes it will not update in the database.

The Extra Feature I chose to include is the filtering feature. I chose to display it using 2 options: "Item Count (100+)" and "Company Size (Large)".

