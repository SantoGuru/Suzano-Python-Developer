from decimal import Decimal
import textwrap

def menu():
    menu = """\n
    ================= MENU =================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [lc]\tListar contas
    [nu]\tNovo Usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def sacar(*,saldo:Decimal,valor:Decimal,extrato:str,limite:Decimal,numero_saques:int,limite_saques:int)-> tuple[Decimal,str]:
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"\n=== Saque realizado com sucesso! Saldo atual: R$ {saldo:.2f} ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

def depositar(saldo:Decimal,valor:Decimal,extrato:str,/)-> tuple[Decimal,str]:
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"\n=== Depósito realizado com sucesso! Saldo atual: R$ {saldo:.2f} ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato

def exibir_extrato(extrato:str,/,*,saldo:Decimal)-> str:
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios:list):
    cpf = input("Informe o CPF (somente números): ").replace(",", ".","-","_"," ").strip()
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/sigla estado): ")

    usuario.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print(f"\n=== Usuário {nome} cadastrado com sucesso! ===")

def criar_conta(agencia:str,numero_conta:str,usuarios:list):
    cpf = input("Informe o CPF do usuário: ").replace(",", ".","-","_"," ").strip()
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

def listar_contas(contas:list):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("-" * 100)
        print(textwrap.dedent(linha))

def filtrar_usuario(cpf:str,usuarios:list) -> dict:
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = Decimal(0)
    limite = Decimal(500)
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()
        
        if opcao == "d":
            valor = Decimal(input("Informe o valor do depósito: ").replace(",", "."))
            valor,extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = Decimal(input("Informe o valor do saque: ").replace(",", "."))
            saldo, extrato = sacar(
                saldo=saldo, 
                valor=valor, 
                extrato=extrato, 
                limite=limite, 
                numero_saques=numero_saques, 
                limite_saques=LIMITE_SAQUES
            )  

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA,numero_conta,usuarios)

            if conta:
                contas.append(conta)
                print(f"Conta {numero_conta} criada com sucesso!")
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


main()