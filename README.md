
# 🛡️ SlimShield · ![Python](https://img.shields.io/badge/python-3.10+-blue) ![License](https://img.shields.io/github/license/muthusethu/slimshield) ![Stars](https://img.shields.io/github/stars/muthusethu/slimshield?style=social)

> Docker security scanner + base image optimizer — built for DevSecOps pipelines

**SlimShield** is a powerful CLI tool by [ItsCloudHub](https://itscloudhub.com) that helps DevOps and platform engineers:

- ✅ Scan Dockerfiles or Docker images for security vulnerabilities and misconfigurations using [Trivy](https://github.com/aquasecurity/trivy)

- ✅ Suggest minimal base images (`slim`, `alpine`, etc.) to optimize container size and security

- ✅ Easily integrate into local dev workflows or CI/CD pipelines

---

## 🚀 Why SlimShield?

- 🐳 Containers often include bloated or insecure base images
- 🔐 Vulnerabilities go unnoticed in production Dockerfiles
- ⚙️ Devs forget best practices like adding `USER`, `HEALTHCHECK`, etc.

**SlimShield** helps you solve all that — right from your terminal.

---

## 🧰 Features

| Feature | Status |
|----------------------------|--------|
| Scan Dockerfile config | ✅ |
| Scan Docker image security | ✅ |
| Suggest slim base images | ✅ |
| Fast CLI UX | ✅ |
| CI/CD ready | 🔜 |
| Export reports (JSON/HTML) | 🔜 |

---

## 🛠️ Installation

1.  **Clone the repo**

```bash
git  clone  https://github.com/muthusethu/slimshield.git

cd  slimshield
```

2.  **Set  up  Python  environment**

```bash
python  -m  venv  venv

source  venv/Scripts/activate  # Windows Git Bash

# or

source  venv/bin/activate  # macOS/Linux
```

3.  **Install  dependencies**

```bash
pip  install  -r  requirements.txt
```  

4.  **Install  Trivy**

🔗  [Official  install  guide](https://trivy.dev/latest/getting-started/installation/)

```bash
choco  install  trivy  # Windows

brew  install  trivy  # macOS

sudo  apt  install  trivy  # Ubuntu
```  

🧪  **Usage**

🔍 **Scan  a  Dockerfile**

```bash
python  cli.py  --dockerfile  test_dockerfiles/sample.Dockerfile
``` 

🔍 **Scan a Dockerfile and generate JSON report**

```bash
python cli.py --dockerfile test_dockerfiles/sample.Dockerfile --format json
``` 

🔍 **Scan a Dockerfile and generate HTML report**

```bash
python cli.py --dockerfile test_dockerfiles/sample.Dockerfile --format html
``` 

🐳 **Scan  a  Docker  Image**

```
python  cli.py  --image  nginx:latest
```

🐳 **Scan a Docker image and export JSON report**

```
python cli.py --image nginx:latest --format json
``` 

🐳 **Scan a Docker image and export HTML report**

```
python cli.py --image nginx:latest --format html
``` 

📆 Reports will be saved under the reports/ folder with a timestamped filename.

📦  **Slim  Base  Image  Suggestions**

SlimShield  currently  detects  these  and  suggests  lighter  alternatives:

| **Original  Base** | **Recommended  Minimal  Versions** |
| ------------- | ---------------------------------------- |
| `python` | `python:3.10-slim`,  `python:3.10-alpine` |
| `node` | `node:18-slim`,  `node:18-alpine` |
| `ubuntu` | `ubuntu:20.04-minimal` |
| `debian` | `debian:bullseye-slim` |
| `golang` | `golang:1.18-alpine` |

📈  **Roadmap**

 - Add  Dockerfile  best  practice  linter
 - Export  scan  results  as  JSON/HTML
 - GitHub  Action  for  automatic  scan
 - Web-based  scan  UI
 - SaaS  dashboard (SlimShield Cloud)
 
👨‍💻  **Author**

**Muthu  Kumar  Murugaiyan**
Cloud & DevOps  @  [ItsCloudHub](www.itscloudhub.com)
Drop  a  ⭐  on  GitHub  if  you  find  this  useful!

📜  **License**
MIT  –  free  to  use,  modify,  and  contribute!