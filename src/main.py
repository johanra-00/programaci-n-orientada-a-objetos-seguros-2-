
from menus.menu_usuario import solicitar_login, menu_privado


def main():
    while True:
        usuario_actual = solicitar_login()

        if usuario_actual is None:
            opcion = input("Enter para reintentar o 0 para salir: ")

            if opcion == "0":
                break

            continue

        opcion = menu_privado(usuario_actual)

        if opcion == "0":
            break

        print("Sesión cerrada. Ingrese nuevamente.")


if __name__ == "__main__":
    main()
