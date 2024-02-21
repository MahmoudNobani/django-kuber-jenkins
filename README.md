# OVERVIEW
This project aims to build an indoor restaurant system that tackles the problems a normal restaurant faces using django technology and routers.

# GOALS
This software will provide a database for all the available meals, employees and orders, while performing the needed operation of (add, remove, update) while checking the capacity, prices and performing some analytics.

# SPECIFICATIONS
The database we will support are as specified in the ER-diagram here:
---
views are documented in docstrings in files views.py

the code was also built as a docker image and deployed on minikube using kuberenetes with 2 microservices (django app and a postgresql db), then a CI-CD pipline was made to automate the whole process using jenkins


python manage.py spectacular --file schema.yml
pip install drf-spectacular        
