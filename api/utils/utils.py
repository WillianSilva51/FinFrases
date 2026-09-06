from datetime import UTC, datetime, timedelta


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
