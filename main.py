from ui.interfaz_principal import InterfazPrincipal
from controladores.sistema_biblioteca import SistemaBiblioteca

if __name__ == "__main__":
    sistema = SistemaBiblioteca()
    app = InterfazPrincipal(sistema)   
    sistema.interfaz = app
    app.ejecutar()                     
