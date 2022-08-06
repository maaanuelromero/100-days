import requests


def check_username(username):
    url = "https://www.instagram.com/" + username
    x = requests.get(url)
    if x.status_code == 404:
        return False
    else:
        return True


def main():
    user = input("Type the username: ")
    if check_username(user):
        print(f"The username {user} already exists")
    else:
        print(f"{user} available")


if __name__ == "__main__":
    main()
