from cx_Freeze import setup, Executable

include_files = [ 'templates', 'static']
includes = []
excludes = []

setup(
    name='Job Generator',
    version='1.0',
    description='Генератор заданий',
    options = {'build_exe':   {'excludes':excludes,'include_files':include_files, 'includes':includes}},
    executables = [Executable('app.py')]
)