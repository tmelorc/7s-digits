import json
import os

CONFIG_FILE = "config.json"


class Translator:
    def __init__(self, default_language='en'):
        self.supported_languages = ['en', 'pt', 'it']
        self.translations = {
            'en': {
                'Theme': 'Theme',
                'Options': 'Options',
                'Game': 'Main',
                'keep_lenght_checkbutton': 'Keep the number of digits',
                'keep_parity_checkbutton': 'Keep the number\'s parity',
                'leading_zero_checkbutton': 'Allow leading zeros',
                'fix_initial_number_checkbutton': 'Set initial number',
                'max_num_moviments_label': 'Maximum number of moves:\n(Game II)',
                'exact_moviments_label': 'Precise number of moves:\n(Game III)',
                'choose_game_label': 'Choose a Game',
                'Game I': 'Game I',
                'Game II': 'Game II',
                'Game III': 'Game III',
                'new_game_button': 'New Game',
                'button_repeat_game': 'Reset Game',
                'button_check_solution': 'Check Solution',
                'Time': 'Time',
                'Moviments': 'Moviments',
                'Initial Number': 'Initial Number',
                'display_frame': 'Digital Display',
                'author_label': 'Author',
                'Version': 'Version',
                'Perfect': 'Perfect',
                'Correct': 'Correct',
                'But too many moviments': 'But too many moviments',
                'Not Yet. Try again!': 'Not Yet. Try again!',
                'Sorry. Too many moviments!': 'Sorry. Too many moviments!',
                'Maximum allowed': 'Maximum allowed',
                'Sorry. You must move exactly': 'Sorry. You must move exactly',
                'segments': 'segments',
                'language': 'Language',
                'english': 'English',
                'portuguese': 'Portuguese',
                'italian': 'Italian',
                'file': 'File',
                'exit': 'Exit',
                "Help I": (
                    "Minimize the initial number only by moving segments, i.e., keeping the same number of segments.\n"
                    " - Use the 'Keep the number of digits' option to maintain the number of digits, i.e., deleting digits is not allowed.\n"
                    " - Use the 'Keep the number's parity' option so that the solution has the same parity as the initial number.\n"
                    " - Use the 'Allow leading zeros' option to permit leading zeros."
                ),
                "Help II": (
                    "Minimize the initial number by moving at most 'Maximum number of moves' segments.\n"
                    " - Use the 'Keep the number of digits' option to maintain the number of digits, i.e., deleting digits is not allowed.\n"
                    " - Use the 'Keep the number's parity' option so that the solution has the same parity as the initial number.\n"
                    " - Use the 'Allow leading zeros' option to permit leading zeros."
                ),
                "Help III": (
                    "Minimize the initial number by moving exactly 'Precise number of moves' segments.\n"
                    " - Use the 'Keep the number of digits' option to maintain the number of digits, i.e., deleting digits is not allowed.\n"
                    " - Use the 'Keep the number's parity' option so that the solution has the same parity as the initial number.\n"
                    " - Use the 'Allow leading zeros' option to permit leading zeros."
                )
            },
            'pt': {
                'Theme': 'Tema',
                'Options': 'Opções',
                'Game': 'Principal',
                'keep_lenght_checkbutton': 'Manter quantidade de dígitos',
                'keep_parity_checkbutton': 'Manter paridade do número',
                'leading_zero_checkbutton': 'Permitir zeros à esquerda',
                'fix_initial_number_checkbutton': 'Fixar número inicial',
                'max_num_moviments_label': 'Número máximo de movimentos:\n(Jogo II)',
                'exact_moviments_label': 'Número exato de movimentos:\n(Jogo III)',
                'choose_game_label': 'Escolha um jogo',
                'Game I': 'Jogo I',
                'Game II': 'Jogo II',
                'Game III': 'Jogo III',
                'new_game_button': 'Novo Jogo',
                'button_repeat_game': 'Reiniciar Jogo',
                'button_check_solution': 'Verificar Solução',
                'Time': 'Tempo',
                'Moviments': 'Movimentos',
                'Initial Number': 'Número Inicial',
                'display_frame': 'Painel Digital',
                'author_label': 'Autor',
                'Version': 'Versão',
                'Perfect': 'Perfeito',
                'Correct': 'Correto',
                'But too many moviments': 'Mas com muitos movimentos',
                'Not Yet. Try again!': 'Ainda não. Tente novamente!',
                'Sorry. Too many moviments!': 'Desculpe. Muitos movimentos!',
                'Maximum allowed': 'Máximo permitido',
                'Sorry. You must move exactly': 'Desculpe. Você deve mover exatamente',
                'segments': 'segmentos',
                'language': 'Idioma',
                'english': 'Inglês',
                'portuguese': 'Português',
                'italian': 'Italiano',
                'file': 'Arquivo',
                'exit': 'Sair',
                "Help I": (
                            "Minimizar o número inicial apenas movendo segmentos, ou seja, mantendo a quantidade de segmentos.\n"
                            " - Utilize a opção {txt} para manter a quantia de dígitos, ou seja, não será permitido apagar dígitos.\n"
                            " - Utilize a opção 'Keep the number's parity' para que a solução tenha a mesma paridade que o número inicial.\n - Utilize a opção 'Allow leading zeros' para permitir zeros à esquerda."
                ),
                "Help II": (
                    "Minimizar o número inicial movendo no máximo {txt} segmentos.\n"
                    " - Utilize a opção {txt} para manter a quantia de dígitos, ou seja, não será permitido apagar dígitos.\n"
                    " - Utilize a opção {txt} para que a solução tenha a mesma paridade que o número inicial.\n"
                    " - Utilize a opção {txt} para permitir zeros à esquerda."
                ),
                "Help III": (
                    "Minimizar o número inicial movendo exatamente {txt} segmentos.\n"
                    " - Utilize a opção {txt} para manter a quantia de dígitos, ou seja, não será permitido apagar dígitos.\n"
                    " - Utilize a opção {txt} para que a solução tenha a mesma paridade que o número inicial.\n"
                    " - Utilize a opção {txt} para permitir zeros à esquerda."
                )
            },
            'it': {
                'Theme': 'Tema',
                'Options': 'Opzioni',
                'Game': 'Principale',
                'keep_lenght_checkbutton': 'Mantieni il numero di cifre',
                'keep_parity_checkbutton': 'Mantieni la parità del numero',
                'leading_zero_checkbutton': 'Permetti zeri iniziali',
                'fix_initial_number_checkbutton': 'Imposta numero iniziale',
                'max_num_moviments_label': 'Numero massimo di mosse:\n(Gioco II)',
                'exact_moviments_label': 'Numero preciso di mosse:\n(Gioco III)',
                'choose_game_label': 'Scegli un Gioco',
                'Game I': 'Gioco I',
                'Game II': 'Gioco II',
                'Game III': 'Gioco III',
                'new_game_button': 'Nuovo Gioco',
                'button_repeat_game': 'Resetta Gioco',
                'button_check_solution': 'Controlla Soluzione',
                'Time': 'Tempo',
                'Moviments': 'Mosse',
                'Initial Number': 'Numero Iniziale',
                'display_frame': 'Pannello digitale',
                'author_label': 'Autore',
                'Version': 'Versione',
                'Perfect': 'Perfetto',
                'Correct': 'Corretto',
                'But too many moviments': 'Ma troppe mosse',
                'Not Yet. Try again!': 'Non ancora. Riprova!',
                'Sorry. Too many moviments!': 'Spiacente. Troppe mosse!',
                'Maximum allowed': 'Massimo consentito',
                'Sorry. You must move exactly': 'Spiacente. Devi muovere esattamente',
                'segments': 'segmenti',
                'language': 'Lingua',
                'english': 'Inglese',
                'italian': 'Italiano',
                'portuguese': 'Portoghese',
                'file': 'File',
                'exit': 'Esci',
                "Help I": (
                    "Minimizza il numero iniziale spostando solo i segmenti, cioè mantenendo lo stesso numero di segmenti.\n"
                    " - Usa l'opzione 'Mantieni il numero di cifre' per mantenere il numero di cifre, cioè non è permesso cancellare cifre.\n"
                    " - Usa l'opzione 'Mantieni la parità del numero' affinché la soluzione abbia la stessa parità del numero iniziale.\n"
                    " - Usa l'opzione 'Permetti zeri iniziali' per consentire zeri iniziali."
                ),
                "Help II": (
                    "Minimizza il numero iniziale spostando al massimo 'Numero massimo di mosse' segmenti.\n"
                    " - Usa l'opzione 'Mantieni il numero di cifre' per mantenere il numero di cifre, cioè non è permesso cancellare cifre.\n"
                    " - Usa l'opzione 'Mantieni la parità del numero' affinché la soluzione abbia la stessa parità del numero iniziale.\n"
                    " - Usa l'opzione 'Permetti zeri iniziali' per consentire zeri iniziali."
                ),
                "Help III": (
                    "Minimizza il numero iniziale spostando esattamente 'Numero preciso di mosse' segmenti.\n"
                    " - Usa l'opzione 'Mantieni il numero di cifre' per mantenere il numero di cifre, cioè non è permesso cancellare cifre.\n"
                    " - Usa l'opzione 'Mantieni la parità del numero' affinché la soluzione abbia la stessa parità del numero iniziale.\n"
                    " - Usa l'opzione 'Permetti zeri iniziali' per consentire zeri iniziali."
                ),
            }
        }

        self.current_language = self.load_language(default_language)

    def translate(self, key, **kwargs):
        text = self.translations[self.current_language][key]
        if kwargs:
            return text.format(**kwargs)
        return text
        # return self.translations[self.current_language].get(key, key)

    def set_language(self, lang):
        if lang in self.supported_languages:
            self.current_language = lang
            self.save_language(lang)
            print(f'** Idioma alterado para: {lang}')

    def save_language(self, lang):
        with open(CONFIG_FILE, 'w') as f:
            json.dump({'language': lang}, f)

    def load_language(self, fallback):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                if 'language' in data and data['language'] in self.supported_languages:
                    return data['language']
        return fallback


if __name__ == "__main__":
    None
