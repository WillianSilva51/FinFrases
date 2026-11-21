from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe


def expiration_midnight() -> int:
    """Retorna a quantidade de segundos restantes até a próxima meia-noite UTC.

    A função calcula a diferença entre o instante atual em UTC e o início do
    próximo dia em UTC, retornando o valor em segundos inteiros.

    Returns:
        int: Quantidade de segundos restantes até a próxima meia-noite.
    """
    now = datetime.now(UTC)
    midnight = (now + timedelta(1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return int((midnight - now).total_seconds())


def mask_email(email: str) -> str:
    """
    Máscara um endereço de e-mail, ocultando parte do nome local.

    Args:
        email (str): O endereço de e-mail a ser mascarado.

    Returns:
        str: O endereço de e-mail mascarado, com parte do nome local substituída por asteriscos.
    """
    local, domain = email.split("@", 1)
    if len(local) <= 2:
        return f"{local[0]}***@{domain}"
    return f"{local[:2]}***@{domain}"


def get_token_generator() -> Callable[[int], str]:
    """
    Retorna uma função que gera tokens seguros de URL com base no tamanho especificado.

    Returns:
        Callable[[int], str]: Uma função que aceita um tamanho inteiro e retorna um token seguro de URL.
    """
    return token_urlsafe
