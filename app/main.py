from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.utils.password import generate_password

# Configuração do nosso app
app = FastAPI(
    title = "Secure password generate",
    description = "An API to generate secure passwords",
    version = "1.2.0"
)

# Validar parâmetros de entrada
class PasswordRequest(BaseModel):
    length: int = Field(8, ge=8, le=12, description="Tamanho da senha (entre 8 e 12 caracteres)")
    include_uppercase: bool = Field(True, description="Incluir letras maiúsculas")
    include_lowercase: bool = Field(True, description="Incluir letras minúsculas")
    include_numbers: bool = Field(True, description="Incluir Números")
    include_symbols: bool = Field(True, description="Incluir símbolos")
    exclude_chars: str = Field("", description="Caracteres a serem excluídos da senha")

# Validar modelo de saida
class PasswordResponse(BaseModel):
    password: str = Field(..., description="Senha gerada com segurança.")

# endpoint para gerar senha
@app.post('/generate-password', response_model=PasswordResponse, summary="Gerar uma senha segura", description="Gera uma senha com base nos critérios definidos pelo usuário.")
async def create_password(request: PasswordRequest):
    password = generate_password(
        length = request.length,
        include_uppercase = request.include_uppercase,
        include_lowercase = request.include_lowercase,
        include_numbers = request.include_numbers,
        include_symbols = request.include_symbols,
        exclude_chars = request.exclude_chars
    )
    return PasswordResponse(password=password)  