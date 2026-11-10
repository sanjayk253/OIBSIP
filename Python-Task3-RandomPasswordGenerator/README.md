# ***Secure Random Password Generator***



##### **Project Overview**

The Secure Random Password Generator is a Python-based desktop application developed using Tkinter. It generates strong, random passwords based on user-selected character types and password length.



##### **Features**

* Generate secure random passwords.
* Customize password length (8–128 characters).
* Include uppercase letters, lowercase letters, numbers, and symbols.
* Exclude ambiguous characters.
* Automatically copy generated passwords to the clipboard.
* Manually copy passwords using the Copy button.
* Display password strength (Weak, Medium, Strong).
* Maintain a history of the five most recently generated passwords.
* Validate password length and character selections.



##### **Technologies Used**

\- Python

\- Tkinter

\- Secrets module

\- String module

\- Pyperclip



##### **Installation**

1\. Install Python 3.

2\. Clone or download this repository.

3\. Open the project folder in VS Code or a terminal.

4\. Install the required package:



&#x20;  `pip install -r requirements.txt`



##### **How to Run**

Execute the following command:

`python main.py`



**Project Structure**

```text

Python-Task3-RandomPasswordGenerator/

│

├── main.py

├── README.md

├── requirements.txt

└── screenshots/

```



##### **Security**

The application uses Python's `secrets` module to generate cryptographically secure random passwords.

Password history is stored temporarily in memory and is cleared when the application closes.



###### **Internship**

*Organization:* Oasis Infobyte  

*Track:* Python Programming Internship  

*Task:* Task 3 – Random Password Generator



**Author**

Sanjay K

