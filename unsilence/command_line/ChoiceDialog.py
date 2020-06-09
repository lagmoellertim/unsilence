from rich.console import Console


def choice_dialog(console: Console, message: str, default: bool = None):
    """
    A simple yes/no console dialog option
    :param console: rich.Console Instance
    :param message: Message should be asked
    :param default: Default value when enter is pressed without an input (None, True, False)
    :return: Answer (True, False)
    """
    yes = "y" if default is not True else "[green]Y[/green]"
    no = "n" if default is not False else "[red]N[/red]"

    result = None
    while result is None:
        choice = console.input(f"[[[green]?[/green]]] {message} ({yes}/{no}) ").lower()
        if choice in ["yes", "y"]:
            result = True
        elif choice in ["no", "n"]:
            result = False
        elif choice == "":
            if default is not None:
                result = default

        if result is None:
            console.print("[red]Invalid input, please try again[/red]")

    return result
