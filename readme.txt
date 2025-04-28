# Machine-Translation-AI
This project focuses on building a Neural Machine Translation (NMT) system for translating text 
from English to Arabic using a fine-tuned mBART model. Includes a FastAPI backend for serving 
the model and a web app for real-time translation through a simple user interface.

How to Run the Project ?
Follow these steps to set up and run the project on your local machine:

1- Clone the github repo to your machine
    command : git clone <repository-url>
  
2- Open the project folder in the VScode or other code editor

3- Open a terminal (PowerShell or your terminal of choice)

4- Create a virtual enviroment:
    command: py -3.10 -m venv venv 
  
5- Activate the virtual enviroment:
    command: .venv\Scripts\activate 
    
6- Install project dependencies: 
    command: pip install -r requirements.txt 
    
7- Run the application using Uvicorn: 
    command: uvicorn main:app --reload 