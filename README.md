# E-Healthcare Management System

!Remember to clone this repo in the HOME directory.

To install the environment:  
```
conda env create -f env.yml
```

Generate the dependencies:
```
make dep all clean
```

To run the doctor interface:  
```
python linebot/main.py
```

To run the linebot on server (the token needs to be filled in):
```
python linebot/app.py
```
Note that the patient can use linebot to access the medical records.
