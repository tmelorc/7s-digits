import random
from typing import Tuple
from constantes import *


def euclid(n, k=7):
    return (n // k, n % k)


def random_number():
    return random.randint(initial_number_min, initial_number_max)


def update_vector(vector, idx):
    vector[idx] = (vector[idx] + 1) % 2
    return vector


def vec_to_digit(vector):
    ''' Returns the digit value represented by the vector. '''
    for digit, vec in vectors.items():
        if vec == vector:
            return digit
    return None


def digit_to_vec(value: int):
    ''' Returns the vector representation of the digit value. '''
    if value not in range(10):
        print(f'** Invalid value: {value}. Should be single digit.')
        return None
    return vectors[value]


def num_to_vec(N):
    ''' Returns the vector representation of the number N. '''
    v = []
    for digit in str(N):
        v += digit_to_vec(int(digit))
    return v


def norm(N: int):
    tmp = 0
    for d in str(N):
        tmp += sum(digit_to_vec(int(d)))
    return tmp


def expand_vec(vector, delta=0):
    ''' Add leading zeros to the vector representation of a number. '''
    return 7 * delta * [0] + vector


def seconds_to_time(seconds):
    hours, rest = divmod(seconds, 3600)
    minutes, seconds = divmod(rest, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def solver_I(N: int, *args, **kwargs) -> Tuple[int, int]:
    ''' Minimize the initial number only by moving segments, i.e., keeping the same number of segments. '''
    keep_lenght = kwargs.get('keep_lenght', False)
    keep_parity = kwargs.get('keep_parity', False)
    segments = norm(N)

    if keep_lenght:
        Nmin = 10**(len(str(N))-1)
    else:
        Nmin = 0

    if keep_parity:
        while norm(Nmin) != segments or (N - Nmin) % 2 != 0:
            Nmin += 1
    else:
        while norm(Nmin) != segments:
            Nmin += 1

    delta = len(str(N)) - len(str(Nmin))
    min_moviments = sum([x != y for x, y in zip(
        num_to_vec(N), expand_vec(num_to_vec(Nmin), delta))]) // 2

    return Nmin, min_moviments


def solver_II(N: int, *args, **kwargs) -> Tuple[int, int]:
    ''' Minimize the initial number by moving at most 'Maximal number of moviments' segments. '''
    keep_lenght = kwargs.get('keep_lenght', False)
    keep_parity = kwargs.get('keep_parity', False)
    max_num_moviments = kwargs.get('max_num_moviments', 5)

    if keep_lenght:
        Nmin = 10**(len(str(N))-1)
    else:
        Nmin = 0

    for k in range(Nmin, N+1):
        if keep_parity:
            if norm(k) != norm(N) or (N - k) % 2 != 0:
                continue
            else:
                delta = len(str(N)) - len(str(k))
                min_moviments = sum([x != y for x, y in zip(
                    num_to_vec(N), expand_vec(num_to_vec(k), delta))]) // 2
                if min_moviments > max_num_moviments:
                    continue
                return k, min_moviments
        else:
            if norm(k) != norm(N):
                continue
            else:
                delta = len(str(N)) - len(str(k))
                min_moviments = sum([x != y for x, y in zip(
                    num_to_vec(N), expand_vec(num_to_vec(k), delta))]) // 2
                if min_moviments > max_num_moviments:
                    continue
                return k, min_moviments


def solver_III(N: int, *args, **kwargs) -> int:
    ''' Minimize the initial number by moving exactly 'Precise number of moviments' segments. '''
    exact_moviments = kwargs.get('exact_moviments', 5)
    keep_lenght = kwargs.get('keep_lenght', False)
    keep_parity = kwargs.get('keep_parity', False)

    if keep_lenght:
        Nmin = 10**(len(str(N))-1)
    else:
        Nmin = 0

    for k in range(Nmin, N+1):
        if keep_parity:
            if norm(k) != norm(N) or (N - k) % 2 != 0:
                continue
            else:
                delta = len(str(N)) - len(str(k))
                min_moviments = sum([x != y for x, y in zip(
                    num_to_vec(N), expand_vec(num_to_vec(k), delta))]) // 2
                if min_moviments != exact_moviments:
                    continue
                return k, min_moviments
        else:
            if norm(k) != norm(N):
                continue
            else:
                delta = len(str(N)) - len(str(k))
                min_moviments = sum([x != y for x, y in zip(
                    num_to_vec(N), expand_vec(num_to_vec(k), delta))]) // 2
                if min_moviments != exact_moviments:
                    continue
                return k, min_moviments


solvers = {
    "Game I": solver_I,
    "Game II": solver_II,
    "Game III": solver_III,
}

solvers_help = {
    "pt": {
        "Game I": (
            f"Minimizar o número inicial apenas movendo segmentos, ou seja, mantendo a quantidade de segmentos.\n"
            f" - Utilize a opção 'Manter o número de dígitos' para manter a quantia de dígitos, ou seja, não será permitido apagar dígitos.\n"
            f" - Utilize a opção 'Manter paridade do número' para que a solução tenha a mesma paridade que o número inicial.\n"
            f" - Utilize a opção 'Permitir zeros à esquerda' para permitir zeros à esquerda."
        ),

        "Game II": (
            f"Minimizar o número inicial movendo no máximo 'Número máximo de movimentos' (definido pelo jogador) segmentos.\n"
            f" - Utilize a opção 'Manter o número de dígitos' para manter a quantia de dígitos, ou seja, não será permitido apagar dígitos.\n"
            f" - Utilize a opção 'Manter paridade do número' para que a solução tenha a mesma paridade que o número inicial.\n"
            f" - Utilize a opção 'Permitir zeros à esquerda' para permitir zeros à esquerda."
        ),

        "Game III": (
            f"Minimizar o número inicial movendo exatamente 'Número exato de movimentos' (definido pelo jogador) segmentos.\n"
            f" - Utilize a opção 'Manter o número de dígitos' para manter a quantia de dígitos, ou seja, não será permitido apagar dígitos.\n"
            f" - Utilize a opção 'Manter paridade do número' para que a solução tenha a mesma paridade que o número inicial.\n"
            f" - Utilize a opção 'Permitir zeros à esquerda' para permitir zeros à esquerda."
        )
    },
    "en": {
        "Game I": (
            "Minimize the initial number only by moving segments, i.e., keeping the same number of segments.\n"
            " - Use the 'Keep the number of digits' option to maintain the number of digits, i.e., deleting digits is not allowed.\n"
            " - Use the 'Keep the number's parity' option so that the solution has the same parity as the initial number.\n"
            " - Use the 'Allow leading zeros' option to permit leading zeros."
        ),
        "Game II": (
            "Minimize the initial number by moving at most 'Maximum number of moves' segments.\n"
            " - Use the 'Keep the number of digits' option to maintain the number of digits, i.e., deleting digits is not allowed.\n"
            " - Use the 'Keep the number's parity' option so that the solution has the same parity as the initial number.\n"
            " - Use the 'Allow leading zeros' option to permit leading zeros."
        ),
        "Game III": (
            "Minimize the initial number by moving exactly 'Precise number of moves' segments.\n"
            " - Use the 'Keep the number of digits' option to maintain the number of digits, i.e., deleting digits is not allowed.\n"
            " - Use the 'Keep the number's parity' option so that the solution has the same parity as the initial number.\n"
            " - Use the 'Allow leading zeros' option to permit leading zeros."
        )
    },
    "it": {
        "Game I": (
            "Minimizza il numero iniziale spostando solo i segmenti, cioè mantenendo lo stesso numero di segmenti.\n"
            " - Usa l'opzione 'Mantieni il numero di cifre' per mantenere il numero di cifre, cioè non è permesso cancellare cifre.\n"
            " - Usa l'opzione 'Mantieni la parità del numero' affinché la soluzione abbia la stessa parità del numero iniziale.\n"
            " - Usa l'opzione 'Permetti zeri iniziali' per consentire zeri iniziali."
        ),
        "Game II": (
            "Minimizza il numero iniziale spostando al massimo 'Numero massimo di mosse' segmenti.\n"
            " - Usa l'opzione 'Mantieni il numero di cifre' per mantenere il numero di cifre, cioè non è permesso cancellare cifre.\n"
            " - Usa l'opzione 'Mantieni la parità del numero' affinché la soluzione abbia la stessa parità del numero iniziale.\n"
            " - Usa l'opzione 'Permetti zeri iniziali' per consentire zeri iniziali."
        ),
        "Game III": (
            "Minimizza il numero iniziale spostando esattamente 'Numero preciso di mosse' segmenti.\n"
            " - Usa l'opzione 'Mantieni il numero di cifre' per mantenere il numero di cifre, cioè non è permesso cancellare cifre.\n"
            " - Usa l'opzione 'Mantieni la parità del numero' affinché la soluzione abbia la stessa parità del numero iniziale.\n"
            " - Usa l'opzione 'Permetti zeri iniziali' per consentire zeri iniziali."
        ),
    }
}


if __name__ == '__main__':
    solver_III(123, exact_num_moviments=3)
    None
