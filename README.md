# Mini-Amazon
This is a group final project for Duke COMPSCI 516 course.   
[Demo Link](http://vcm.tinchun.top:5000)

All passwords and tokens in the history commits have been removed and revoked. All new passwords and tokens are randomly generated.  
# Development Workflow：
1. Develop: Update master branch, checkout a new branch from master branch and named as dev_{name}\_{feature}. eg.: dev_tm326_login
1. Switch to the new branch
1. Develop new features on the new branch and test on the local machine (connected to a remote database)
1. After fully tested, push your code to GitHub and create a Pull Request. After reviewing (diffing) the code, merge it to master branch and delete the development branch.
1. Automatically deploy to server via CI/CD workflow.

# Development：

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

[Original Readme](./Desc.md)