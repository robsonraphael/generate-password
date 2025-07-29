from fastapi import HTTPException
import secrets
import string
import re

# função para gerar senha
def generate_password(length: int, include_uppercase: bool, include_lowercase: bool, include_numbers: bool, include_symbols: bool, exclude_chars: str = "") -> str:

    # validando comprimento
    if length < 8:
        raise HTTPException(status_code=400, detail="A senha padrão deve conter 8 caracteres ou mais.")
    if length > 12:
        raise HTTPException(status_code=400, detail="A senha não pode conter mais de 12 caracteres.")
    
    # conjunto de caracteres disponiveis
    uppercase = string.ascii_uppercase if include_uppercase else "" 
    lowercase = string.ascii_lowercase if include_lowercase else ""
    numbers = string.digits if include_numbers else ""
    symbols = string.punctuation if include_symbols else ""

    # combinando caracteres permitidos
    characters = uppercase + lowercase + numbers + symbols
    
    # excluindo caracteres não permitidos
    if exclude_chars:
        characters = re.sub(f"[{re.escape(exclude_chars)}]", "", characters)

    # validando lista de caracteres
    if not characters:
        raise HTTPException(status_code=400, detail="Pelo menos 1 caractere deve ser adicionado.")

    # gerando senha com secrets
    password = "".join(secrets.choice(characters) for x in range(length)) 

    # Garantindo que contenha pelo menos um tipo
    if include_uppercase and not any(c in uppercase for c in password):
        password = password[:-1] + secrets.choice(uppercase)
    if include_lowercase and not any(c in lowercase for c in password):
        password = password[:-1] + secrets.choice(lowercase)
    if include_numbers and not any(c in numbers for c in password):
        password = password[:-1] + secrets.choice(numbers)
    if include_symbols and not any(c in symbols for c in password):
        password = password[:-1] + secrets.choice(symbols)
    
    return password
