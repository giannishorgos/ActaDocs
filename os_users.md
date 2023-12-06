# Restore Users on the new OS
## Steps

- Create user:
```bash
sudo useradd -c "Full Name" <username>
```
- Create password:
```bash
sudo passwd <username>
```
- Make it sudoer:
```bash
sudo usermod -aG wheel <username> 
```
- Copy the old home directory of the user to the directory:
```bash
sudo cp -r /opt/os_backup/users_backup/home/<username>/. /home/<username>/
```
- Change permission of directory:
```bash
sudo chown -R <username>:<username> <username>/
```

- Or all together with a python script...:
```python
import subprocess

def create_user(username, full_name):
    # Step 1: Create user
    subprocess.run(["sudo", "useradd", "-c", full_name, username])

def set_password(username):
    # Step 2: Create password
    subprocess.run(["sudo", "passwd", username])

def make_sudoer(username):
    # Step 3: Make it sudoer
    subprocess.run(["sudo", "usermod", "-aG", "wheel", username])

def copy_home_directory(username):
    # Step 4: Copy old home directory
    subprocess.run(["sudo", "cp", "-r", f"/opt/os_backup/users_backup/home/{username}/.", f"/home/{username}/"])

def change_directory_permission(username):
    # Step 5: Change permission of directory
    subprocess.run(["sudo", "chown", "-R", f"{username}:{username}", f"/home/{username}/"])

def decompress_backup(username):
    # Step 6: Decompress Backup
    subprocess.run(["sudo", "gzip", "-d", f"/opt/os_backup/users_backup/{username}.tar.gz"])
    subprocess.run(["sudo", "tar", "-xvf", f"/opt/os_backup/users_backup/{username}.tar"])

def main():
    # Input: Get username and full name
    username = input("Enter username: ")
    full_name = input("Enter full name: ")

    # Execute steps
    create_user(username, full_name)
    # set_password(username)
    make_sudoer(username)
    decompress_backup(username)
    copy_home_directory(username)
    change_directory_permission(username)

if __name__ == "__main__":
    main()

```
