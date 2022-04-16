# Mini-Amazon
This is a group final project for Duke COMPSCI 516 course.   
[Demo Link](http://vcm.tinchun.top:5001).  
[Demo Video](https://youtu.be/QWuk3q39c80)

All passwords and tokens in the history commits have been removed and revoked. All new passwords and tokens are randomly generated.  

# Team Members
- Tianjun Mo (tm326): Account and Purchases
- Zheng Zhang (zz277): Products and Cart
- Dingzhou Wang (dw299): Inventory and Order Fulfillment
- Enmiao Feng (ef141): Feedback and Messaging
# Development Workflow
1. Develop: Update master branch, checkout a new branch from master branch and named as dev_{name}\_{feature}. eg.: dev_tm326_login
1. Switch to the new branch
1. Develop new features on the new branch and test on the local machine (connected to a remote database)
1. After fully tested, push your code to GitHub and create a Pull Request. After reviewing (diffing) the code, merge it to master branch and delete the development branch.
1. Automatically deploy to server via CI/CD workflow.

# Development
0. Rename template.env as .env and modify it to store sensitive passwords and secrets.

1. Create and activate venv:
```bash
$ python3 -m venv ./venv
$ source ./venv/bin/activate
```
2. Install dependencies:
```bash
$ make install
```

3. Run server:
```bash
$ make run
```

# Deployment
The Docker-compose will automatically deploy this Mini-Amazon service, Postgres Database, MinIO Object Storage and load a bunch of fake data into it.   

0. Rename template.env as .env and modify it to store sensitive passwords and secrets.

1. Check [docker-compose.yaml](./docker-compose.yaml), and modify it if you want.

2. Deploy with Docker-compose
    ```bash
    $ docker-compose up -d
    ```
    PS: If this is not able to init the database, try it again!


[Original Readme](./Desc.md)
