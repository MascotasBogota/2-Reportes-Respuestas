# 2-Reportes-Respuestas

Service for the second module of PatitasBog application: Reportes y respuestas

## Setup

Clone repository

```bash
git clone https://github.com/MascotasBogota/2-Reportes-Respuestas.git
```

If you already have a local copy of the repository make sure you are up to date
with the `main` branch before working.

```bash
git pull origin main
```

Create a branch to work on.

```bash
git checkout -b <my-branch>
```

### Venv

Create a Python virtual environment before going forward.

```bash
python -m venv venv
```

After creating the venv, you have to activate it.

```bash
 venv/Scripts/activate
```

#### Caution:

When using venv, you ought to change the python interpreter in VScode. In order
to do this, do `Ctrl + Shift + P` and then in the bar at the top write
`>Python:Select Interpreter`. Here you have to select the interpreter that has
the venv route. For example `.\venv\Scripts\python.exe`

Another thing to look out for, is to use `python` instead of `python3` if you
execute a file from the terminal. This is because python3 calls directly the
python interpreter in the machine. This can lead to dependecy problems (speaking
from experience)

### .env file

You have to create a .env file that contains:

```
FLASK_APP=app.py
FLASK_ENV=development
MONGO_URI=mongodb+srv://<username>:<password>@reportes-respuestas.ntzkwtx.mongodb.net/?retryWrites=true&w=majority&appName=reportes-respuestas
JWT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkq...\n-----END PUBLIC KEY-----"
DEV_MODE=True
```

### initalizing without docker

#### installing dependencies

A `requirements.txt` file should exitst among the files. Just use

```bash
pip install -r requirements.txt
```

#### running the app

Once all of the above is done, go to the root directory and execute the `app.py`
file:

```bash
python app.py
```

### Using docker

> You have to install docker beforehand

Docker serves the purpose of running the application in a container. That is, a
minimalist version of an operating system is created and the application runs on
top of it. This is to avoid issues with hardware and operating system
environment in each of the team member's PC (it works in my machine! issue).

There is a dockerfile that defines layer by layer the configuration of the
container, and a docker-compose.yml that automatizes the process.

To start the docker container just do:

```bash
docker compose up
```
