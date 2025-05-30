![Tests](https://github.com/novozhilov-ivan/FastApi-App-Sleep-Diary/actions/workflows/run_tests.yml/badge.svg)
# Sleep Diary
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
