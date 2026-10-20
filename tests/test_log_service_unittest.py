import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from log_service import gravar_log, ler_logs


class TestLogService(unittest.TestCase):

    def test_criar_primeiro_log(self):
        with TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "teste.log"

            registro = gravar_log(
                "INFO",
                "Cadastro concluído.",
                caminho=caminho
            )


            self.assertTrue(caminho.is_file())

            self.assertEqual(
                registro,
                "[INFO] Cadastro concluído."
            )

            self.assertEqual(
                caminho.read_text(encoding="utf-8"),
                "[INFO] Cadastro concluído.\n"
            )


    def test_gravar_duas_mensagens(self):
        with TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "teste.log"

            gravar_log("INFO", "Cadastro realizado.", caminho=caminho)
            gravar_log("ERROR", "Falha no login.", caminho=caminho)

            logs = ler_logs(caminho=caminho)

            self.assertEqual(
                logs,
                [
                    "[INFO] Cadastro realizado.",
                    "[ERROR] Falha no login."
                ]
            )        


    def test_mensagens_duplicadas(self):
        with TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "teste.log"

            gravar_log("INFO", "Cadastro realizado.", caminho=caminho)
            gravar_log("INFO", "Cadastro realizado.", caminho=caminho)

            logs = ler_logs(caminho=caminho)

            self.assertEqual(len(logs), 2)

            self.assertEqual(
                logs,
                [
                    "[INFO] Cadastro realizado.",
                    "[INFO] Cadastro realizado."
                ]
            )


    def test_arquivo_inexistente_ou_vazio(self):
        with TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "teste.log"

            # Primeiro: arquivo ainda não existe
            logs = ler_logs(caminho=caminho)

            self.assertEqual(logs, [])
            self.assertFalse(caminho.exists())

            # Segundo: arquivo existe, mas está vazio
            caminho.write_text("", encoding="utf-8")

            logs = ler_logs(caminho=caminho)

            self.assertEqual(logs, [])


    def test_mensagem_com_caracteres_especiais(self):
        with TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "teste.log"

            mensagem = 'Não foi possível concluir, pedido "urgente".'

            gravar_log("WARNING", mensagem, caminho=caminho)

            logs = ler_logs(caminho=caminho)

            self.assertEqual(
                logs,
                ['[WARNING] Não foi possível concluir, pedido "urgente".']
            )

    def test_persistencia_dos_logs(self):
        with TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "teste.log"

            gravar_log("INFO", "Primeiro registro.", caminho=caminho)
            gravar_log("ERROR", "Segundo registro.", caminho=caminho)

            # Abrir novamente o arquivo para conferir os dados
            with open(caminho, "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read().splitlines()

            self.assertEqual(
                conteudo,
                [
                    "[INFO] Primeiro registro.",
                    "[ERROR] Segundo registro."
                ]
            )

            # Verificar se a função também recupera os registros
            logs = ler_logs(caminho=caminho)

            self.assertEqual(logs, conteudo)

    def test_falha_ao_gravar_log(self):
        with TemporaryDirectory() as pasta:
            caminho = Path(pasta)

            with self.assertRaises(OSError):
                gravar_log(
                    "ERROR",
                    "Falha ao realizar login.",
                    caminho=caminho
                )

    def test_falha_ao_ler_log(self):
        with TemporaryDirectory() as pasta:
            caminho = Path(pasta)

            with self.assertRaises(OSError):
                ler_logs(caminho=caminho)            