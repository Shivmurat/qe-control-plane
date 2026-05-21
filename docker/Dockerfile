FROM python:3.12-slim
LABEL authors="shivmuratsharma"

WORKDIR /app

RUN apt-get update && \
    apt-get install -y default-jre wget unzip && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/allure-framework/allure2/releases/download/2.29.0/allure-2.29.0.zip && \
    unzip allure-2.29.0.zip && \
    mv allure-2.29.0 /opt/allure && \
    ln -s /opt/allure/bin/allure /usr/bin/allure && \
    rm allure-2.29.0.zip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "scripts.execution.run_tests"]