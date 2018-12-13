# Installation guide for flo Backend 2.0

## Requirements
- Python 3.5
- postgres


## 1 Getting project
Go to the specified folder and run (for ex `cd /var/opt`)

`git clone -b 'v2.0.1' http://git-server.gmail.com/second-lab/flo-backend.git`

## 2 Prepare environment

### 2.1 Create python environment
Go to `cd flo-backend` and create python virtual environment 

`virtualenv -p python3.5 --no-download venvpy35`

### 2.2 Activate env
`source venvpy35/bin/activate`

### 2.3 Install all modules from requirements.txt 
`export PIP_INDEX_URL=http://172.16.9.160:8888/simple`

`source /etc/enviroment`

[How work with local pypi server](have a look http://git-server.gmail.com/second-lab/Common/wikis/%D0%9A%D0%B0%D0%BA-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D1%82%D1%8C-c-%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%BC-pypi-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%BE%D0%BC) 

`./scripts/pip-tusted-host-req-install.sh requirements.txt`


## 2 Create and setup database
### 2.1 Create database
From root of project run:
`sudo -u postgres psql -f scripts/create-db-user.sql`


### 2.2 Setup database
Fill in the correct data: IP, database name, user and password in `backend/settings.py`


### 2.3 Check database connection
Run: 
`./manage.py dbshell`


## 3 Install models and load initial data
### 3.1 Install models
Run:
`./manage.py migrate`


### 3.2 Create user 
Run:
`./manage.py createsuperuser` (usually admin)


### 3.3 Load initial data
Run:
```commandline
./manage.py loaddata scripts/initial_data/01_attribute_mappingtype.json 
./manage.py loaddata scripts/initial_data/02_entity_attributes.json 
./manage.py loaddata scripts/initial_data/03_graph_model_drawing.json 
./manage.py loaddata scripts/initial_data/04_model_templates.json 
./manage.py loaddata scripts/initial_data/05_relation_templates.json
```


### 3.4 Start and test server
Check `backend/settings.py`

```commandline
ALLOWED_HOSTS = [ %YOUR_HOST%
                 '127.0.0.1']
```
Run:

`./manage.py runserver %YOUR_HOST%:8000`

### 3.5 Loading attributes from ES and mapping it
Load data from ES:
```commandline
http://172.16.9.71:8001/attribute/attribute_reload_mapped_attributes_list
```
Then it's needed define entity attribute for every attribute (from search system)
Make it here

`http://172.16.9.71:8001/admin/attribute/attribute/`
