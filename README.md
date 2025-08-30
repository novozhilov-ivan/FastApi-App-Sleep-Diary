# FastApi-App-Sleep-Diary

![Python](https://img.shields.io/badge/python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)

![Docker Build](https://img.shields.io/github/actions/workflow/status/novozhilov-ivan/FastApi-App-Sleep-Diary/build.yaml?branch=master&label=Docker%20Build&style=for-the-badge&logo=docker&logoColor=white)

![Pytest](https://img.shields.io/github/actions/workflow/status/novozhilov-ivan/FastApi-App-Sleep-Diary/tests.yaml?branch=master&label=Pytest&style=for-the-badge&logo=pytest&logoColor=white&color=6610f2)

![Pre-commit](https://img.shields.io/github/actions/workflow/status/novozhilov-ivan/FastApi-App-Sleep-Diary/pre-commit.yaml?branch=master&label=Pre-commit&style=for-the-badge&logo=git&logoColor=white&color=22863a)

![Ruff](https://img.shields.io/github/actions/workflow/status/novozhilov-ivan/FastApi-App-Sleep-Diary/pre-commit.yaml?branch=master&label=Ruff&style=for-the-badge&logo=python&logoColor=white&color=f0a500)

# FastApi + PostgreSQL Application


## Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)
- [OpenSSL](https://openssl-library.org/source/gitrepo/)

## How to Use

1. **Clone the repository:**

   ```shell
   git clone https://github.com/novozhilov-ivan/FastApi-App-Sleep-Diary
   ```
   ```shell
   cd FastApi-App-Sleep-Diary
   ```

2. **Create Secret Keys:**
    ```bash
    openssl genrsa -out jwt-private.pem 2048
    openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
    ```
