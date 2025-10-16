from app.controllers.gui_controller import GuiController
from app.views.gui_view import GuiView

if __name__ == "__main__":
    # 1. Cria o controller (que tem acesso aos models)
    controller = GuiController()
    
    # 2. Cria a view e injeta o controller nela
    view = GuiView(controller)
    
    # 3. Inicia a aplicação
    view.main()