from setuptools import setup
from setuptools.command.install import install
import subprocess

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        try:
            subprocess.check_call(['playwright', 'install'])
            subprocess.check_call(['playwright', 'install-deps'])
        except subprocess.CalledProcessError as e:
            print(f"Playwright browser installation failed: {e}")

setup(
    cmdclass={
        'install': PostInstallCommand,
    }
)
