Add server ips in `/etc/ansible/hosts`
```bash
[dev]
172.16.9.71

[local]
127.0.0.1	ansible_connection=local
```
# Install python module via pip

Download package on internet machine `pip download isort` into current dir

Run playbook with verbose
```bash
ansible-playbook playbook-install-package.yml -u user -i hosts --extra-vars "package_file=isort-4.3.4-py3-none-any.whl" -vvv
```



# Install .deb package

Download .deb with dependences
```bash
$ mkdir package_name
$ sudo apt install apt-rdepends
$ apt-get download $(apt-rdepends toilet|grep -v "^ ")
```



Run playbook, send package filename as argument
```bash
ansible-playbook playbook-install-deb.yml -u user -i hosts --extra-vars "package_name=toilet dir=toilet}" -vvv -sudo
```






