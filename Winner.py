import thorpy
import Menu


def wingui():
    # global value
    application = thorpy.Application((800, 600), "You Win!")

    clickable = thorpy.make_button("Play again?", func=at_pressed)
    thorpy.makeup.add_basic_help(clickable, "Press to play again")

    title_element = thorpy.make_text("You Win!", 22, (255, 0, 0))

    elements = [clickable]
    central_box = thorpy.Box(elements=elements)
    central_box.fit_children(margins=(30,30))  # we want big margins
    central_box.center()  # center on screen
    central_box.set_main_color((220, 220, 220, 180))  # set box color and opacity

    background = thorpy.Background(image="winner_img.png", elements=[title_element, central_box])
    thorpy.store(background)

    menu = thorpy.Menu(background)

    menu.play()
    application.quit()


def at_pressed():
    menu = Menu.MenuGui()
    menu_gui = menu.menugui()
