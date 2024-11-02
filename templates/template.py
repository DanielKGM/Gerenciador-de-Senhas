import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from model.password import Password
from views.password_views import FernetHasher

if __name__ == '__main__':
    action = input('Digite 1 para salvar uma nova senha ou 2 para ver uma senha salva: ')

    match action:
        case '1':
            if len(Password.get()) == 0:
                key, path = FernetHasher.create_key(archive = True)
                if path:
                    print('Chave salva no arquivo, lembre-se de remover o arquivo após o transferir de local')
                    print(f'Caminho: {path}')
                domain = input('Dominio: ')
                password = input('Senha: ')
                fernet = FernetHasher(key)
                p1 = Password(domain=domain, password=fernet.encrypt(password).decode('utf-8'))
                p1.save()
            else:
                key = input('Digite sua chave usada para criptografia, use sempre a mesma chave: ')

        case '2':
            domain = input('Domínio: ')
            key = input('Key: ')
            fernet = FernetHasher(key)
            data = Password.get()
            password = ''
            for i in data:
                if domain in i['domain']:
                    password = fernet.decrypt(i['password'])

            if password:
                print(f'Sua senha: {password}')
            else:
                print('Nenhuma senha encontrada para esse domínio.')
