from app.controllers.gui_controller import GuiController
from app.views.gui_view import GuiView

# Este é o ponto de entrada (entry point) para a aplicação com interface gráfica (GUI).
if __name__ == "__main__":
    # 1. Instancia o Controller: O controller é o cérebro que se comunica com os models
    #    para buscar e manipular dados.
    controller = GuiController()
    
    # 2. Instancia a View: A view é a janela principal da aplicação.
    #    O controller é "injetado" na view para que os elementos da interface (botões, etc.)
    #    possam chamar as funções do controller.
    view = GuiView(controller)
    
    # 3. Inicia a aplicação: O método main() da view inicia o loop principal do Tkinter,
    #    que desenha a janela e a mantém aberta, aguardando a interação do usuário.
    view.main()