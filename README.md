
# 🛡️ SlimShield · ![Python](https://img.shields.io/badge/python-3.10+-blue) ![License](https://img.shields.io/github/license/muthusethu/slimshield) ![Stars](https://img.shields.io/github/stars/muthusethu/slimshield?style=social)

> Docker security scanner + base image optimizer — built for DevSecOps pipelines

**SlimShield** is a powerful CLI tool by [ItsCloudHub](https://itscloudhub.com) that helps DevOps and platform engineers:

- ✅ Scan Dockerfiles or Docker images for security vulnerabilities and misconfigurations using [Trivy](https://github.com/aquasecurity/trivy)
- ✅ Suggest minimal base images (`slim`, `alpine`, etc.) to optimize container size and security
- ✅ Detect hardcoded secrets and sensitive ENV variables
- ✅ Generate detailed JSON/HTML reports for audits
- ✅ Fail builds if secrets are found (for CI/CD)
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
| Scan Dockerfiles | ✅ |
| Scan Docker images | ✅ |
| Suggest slim base images | ✅ |
| Detect secrets (ENV, tokens, etc.) | ✅ |
| Fail build on secret detection | ✅ |
| Export reports (JSON / HTML) | ✅ |
| Quiet CLI mode | ✅ |
| CI/CD friendly | ✅ |

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

🔍 **Quiet Mode**

```bash
python cli.py --dockerfile test_dockerfiles/sample.Dockerfile --quiet
``` 

🔍 **Fail Build If Secrets Are Found**

```bash
python cli.py --dockerfile test_dockerfiles/secret.Dockerfile --fail-on-secrets
``` 

🐳 **Scan  a  Docker  Image**

```bash
python  cli.py  --image  nginx:latest
```

🐳 **Scan a Docker image and export JSON report**

```bash
python cli.py --image nginx:latest --format json
``` 

🐳 **Scan a Docker image and export HTML report**

```bash
python cli.py --image nginx:latest --format html
``` 

🐳 **Fail Build If Secrets Are Found**

```bash
python cli.py --image nginx:latest --fail-on-secrets
``` 

📆 Reports will be saved under the reports/ folder with a timestamped filename.

🧪 **Secret Detection Example Output**

When secrets are found:

```YAML
❌ Secrets detected in test_dockerfiles/secret.Dockerfile

🔑 ENV variable: SECRET_KEY
📍 Line: 4
🔒 Value (redacted): super-****-token
💡 Tip: Avoid storing secrets in Dockerfile. Use external secret managers like HashiCorp Vault, AWS Secrets Manager, or Docker BuildKit secrets.
``` 

Use --fail-on-secrets in CI/CD pipelines to block the deployment if secrets are detected.

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

| Feature                                 | Status      |
| --------------------------------------- | ----------- |
| ✅ Trivy Scan HTML/JSON export           | Completed   |
| ✅ Secret detection in Dockerfiles       | Completed   |
| ✅ Fail on secrets flag                  | Completed   |
| ✅ Docker image scan support             | Completed   |
| 🔄 Detect secrets inside Docker images  | In Progress |
| 🔄 Best practice linter for Dockerfiles | Planned     |
| 🔄 Multi-stage build detection          | Planned     |
| 🔄 GitHub Action for CI scans           | Planned     |
| 🔄 SaaS dashboard (SlimShield Cloud)    | Planned     |
| 🔄 Image Size Analyzer                  | Planned     |

👨‍💻  **Author**

**Muthu  Kumar  Murugaiyan**
Cloud & DevOps  @  [ItsCloudHub](www.itscloudhub.com)
Drop  a  ⭐  on  GitHub  if  you  find  this  useful!

📜  **License**
MIT  –  free  to  use,  modify,  and  contribute!