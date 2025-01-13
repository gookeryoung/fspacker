import logging
import platform
import subprocess
import typing

__all__ = ["commands"]


class Commands:

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Commands()

        return cls._instance

    @staticmethod
    def pip(args: typing.List[str]) -> typing.Tuple[typing.Optional[str], str]:
        python_executor = "python.exe" if platform.system() == "Windows" else "python3"
        try:
            cmds = [python_executor, "-m", "pip", *args]
            logging.info(f"Calling command: {cmds}.")
            cid = subprocess.call(
                cmds,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            return cid
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the script: {e}")
            return -1


commands = Commands.get_instance()
