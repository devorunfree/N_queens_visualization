import thorpy
import Queengame


class MenuGui:
    def __init__(self):
        self.application = None
        self.inserter = None
        self.clickable = None
        self.title_element = None

    def menugui(self):
        self.application = thorpy.Application((800, 600), "N Queens by Devon Resendes")

        self.inserter = thorpy.Inserter(name="Enter Value for N: ")

        self.clickable = thorpy.make_button("Start Game", func=self.at_pressed)
        thorpy.makeup.add_basic_help(self.clickable, "Press to start game")

        self.title_element = thorpy.make_text("N Queens by Devon Resendes", 22, (255, 0, 0))

        elements = [self.inserter, self.clickable]
        central_box = thorpy.Box(elements=elements)
        central_box.fit_children(margins=(30, 30))  # we want big margins
        central_box.center()  # center on screen
        central_box.set_main_color((220, 220, 220, 180))  # set box color and opacity

        background = thorpy.Background(color=(255, 255, 255), elements=[self.title_element, central_box])
        thorpy.store(background)

        menu = thorpy.Menu(background)

        menu.play()

        self.application.quit()

    def ret_n(self):
        n = int(self.inserter.get_value())
        return n

    def at_pressed(self):  # starts the game and passes in n
        n = self.ret_n()
        print(n)
        lady_bug_game = Queengame.LadyBugGame(n)
        lady_bug_game.setup()
        lady_bug_game.update_ui()
        lady_bug_game.quit()
