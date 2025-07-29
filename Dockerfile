# Imagem base com suporte a Python e dependências nativas
FROM python:3.12-slim

# Evita prompts interativos na instalação
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    rustc \
    cargo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório da aplicação
WORKDIR /app

# Copia os arquivos para dentro da imagem
COPY . .

# Instala dependências
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Expõe a porta usada pelo Uvicorn (ajustável)
EXPOSE 8000

# Comando de execução do servidor FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]