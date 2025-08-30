# FastApi-App-Sleep-Diary


![Python](https://img.shields.io/badge/python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)

![Docker Build](https://github.com/${{ github.repository }}/actions/workflows/build.yaml/badge.svg?branch=master)

![Pytest](https://github.com/${{ github.repository }}/actions/workflows/tests.yaml/badge.svg?branch=master)

![Pre-commit](https://github.com/${{ github.repository }}/actions/workflows/pre-commit.yaml/badge.svg?branch=master)

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
