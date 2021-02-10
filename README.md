# Online Project Tracking System
This system tracks the status of any project. The system will keep all the information of
client and their projects. It will track the current status of projects. By
this system admin or project manager can assign project to specific department. Then department
head will divide the project into some modules and distribute those among some
created team. Team leader can divide module into
several tasks and assign to team members. Team member will submit the assigned task
to a tester after completion. If the tester get any bug in the task then he will send the
task to the member again to solve the bug. If the tester give approval of the task then
only the team member can submit the task to the team leader. If all the task under a
module is completed then only the module will be shown as completed.

## Requirements
To run this project following are required.

- [Python 3.7](https://www.python.org/)
- [Django 3.1.1](https://www.djangoproject.com/)

## Quickstart

A step by step series of examples that tell you how to get a development environment running and start the project.

## Setup

### Create Virtual Environment:
```bash
virtualenv venv
```
### Activate Virtual Environment:
Go to venv/Scripts/ and run
```bash
activate
```
### Install Packages:
```bash
pip install -r requirements.txt
```

### Perform database migration:
```bash
python manage.py check
python manage.py migrate
```

## Run Development Server

```bash
python manage.py runserver
```
Public endpoint is at http://localhost:8000

Admin endpoint is at http://127.0.0.1:8000/admin/,

## Author

* **Md. Golam Moazzem Naim** 
 

## License

This project is licensed under the MIT License.
