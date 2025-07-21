from fastapi import FastAPI, HTTPException
from pydantic import BaseModel      # Validação
import secrets
import string


app = FastAPI(
    title = "Generate secure pass",
    description = "An api to generate secure pass",
    version = "1.0.0"
)

# Validar parâmetros de entrada
class PasswordRequest(BaseModel):
    length: int = 12    # Comprimento padrão de senha
    include_uppercase: bool = True  # conter letra maiúscula
    include_lowercase: bool = True  # conter letra minúscula
    include_numbers: bool = True    # incluir números
    include_symbols: bool = True    # incluir símbolos

# Gerar senha
def generate_password(length: int, include_uppercase: bool, include_lowercase: bool, include_numbers: bool, include_symbols: bool) -> str:
    
    # validando comprimento
    if length < 8:
        raise HTTPException(status_code=400, detail="A senha deve conter 8 caracteres ou mais.")
    
    # conjunto de caracteres disponiveis
    uppercase = string.ascii_uppercase if include_uppercase else "" ##
    lowercase = string.ascii_lowercase if include_lowercase else ""
    numbers = string.digits if include_numbers else ""
    symbols = string.punctuation if include_symbols else ""

    # combinaçãodos caracteres permitidos
    characters = uppercase + lowercase + numbers + symbols

    # validando os caracteres
    if not characters:
        raise HTTPException(status_code=400, detail="Pelo menos 1 caractere deve ser selecionado.")

    # gerando senha com secrets
    password = "".join(secrets.choice(characters) for x in range(length)) ##

    # verificando a validação de caractere
    if include_uppercase and not any(c in uppercase for c in password):
        password = password[:-1] + secrets.choice(uppercase)
    if include_lowercase and not any(c in lowercase for c in password):
        password = password[:-1] + secrets.choice(lowercase)
    if include_numbers and not any(c in numbers for c in password):
        password = password[:-1] + secrets.choice(numbers)
    if include_symbols and not any(c in symbols for c in password):
        password = password[:-1] + secrets.choice(symbols)
    
    return password

# endpoint para gerar senha
@app.post('/generate-password', response_model=dict)
async def create_password(request: PasswordRequest):
    password = generate_password(
        length = request.length,
        include_uppercase = request.include_uppercase,
        include_lowercase = request.include_lowercase,
        include_numbers = request.include_numbers,
        include_symbols = request.include_symbols
    )
    return {"password": password}

#generate_password(10, True, True, True, True)