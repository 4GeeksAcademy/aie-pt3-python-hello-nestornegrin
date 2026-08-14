import csv
import sys
from pathlib import Path

DATA_FILE = Path(__file__).with_name("todos.csv")
todos = []


def add_one_task(title):
    task = str(title).strip()
    if not task:
        raise ValueError("El titulo de la tarea no puede estar vacio.")
    todos.append(task)
    return task


def print_list():
    if not todos:
        print("No hay tareas pendientes.")
        return

    for index, task in enumerate(todos, start=1):
        print(f"{index}. {task}")


def delete_task(number_to_delete):
    if not isinstance(number_to_delete, int):
        raise ValueError("La posicion debe ser un numero entero.")
    if number_to_delete < 1 or number_to_delete > len(todos):
        raise IndexError(f"La posicion {number_to_delete} no existe en la lista.")

    task_removed = todos.pop(number_to_delete - 1)
    return task_removed


def save_todos(file_path=DATA_FILE):
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["title"])
        for task in todos:
            writer.writerow([task])


def load_todos(file_path=DATA_FILE):
    file_path = Path(file_path)
    global todos

    if not file_path.exists():
        todos = []
        return todos

    tasks = []
    with file_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if not row:
                continue
            title = row[0].strip()
            if not title or title.lower() == "title":
                continue
            tasks.append(title)

    todos = tasks
    return todos


def interactive_cli():
    load_todos()
    while True:
        print("\n=== Gestor de tareas ===")
        print("1. Agregar tarea")
        print("2. Ver tareas")
        print("3. Eliminar tarea")
        print("4. Guardar tareas")
        print("5. Cargar tareas")
        print("6. Salir")

        option = input("Selecciona una opcion: ").strip()

        if option == "1":
            title = input("Titulo de la tarea: ").strip()
            try:
                add_one_task(title)
                save_todos()
                print(f"Tarea agregada: {title}")
            except ValueError as exc:
                print(f"Error: {exc}")

        elif option == "2":
            print_list()

        elif option == "3":
            if not todos:
                print("No hay tareas para eliminar.")
                continue
            try:
                pos = int(input("Ingresa la posicion numerica a eliminar: ").strip())
                removed = delete_task(pos)
                save_todos()
                print(f"Tarea eliminada: {removed}")
            except (ValueError, IndexError) as exc:
                print(f"Error: {exc}")

        elif option == "4":
            save_todos()
            print("Tareas guardadas en todos.csv")

        elif option == "5":
            load_todos()
            print("Tareas cargadas desde todos.csv")

        elif option == "6":
            print("Hasta luego.")
            break

        else:
            print("Opcion no valida.")


def cli_dispatch(argv):
    load_todos()

    if not argv:
        interactive_cli()
        return 0

    command = argv[0].lower()

    if command == "add":
        title = " ".join(argv[1:]).strip()
        try:
            add_one_task(title)
            save_todos()
            print(f"Tarea agregada: {title}")
            return 0
        except ValueError as exc:
            print(f"Error: {exc}")
            return 1

    if command == "list":
        print_list()
        return 0

    if command == "delete":
        if len(argv) < 2:
            print("Uso: python main.py delete <posicion>")
            return 1
        try:
            position = int(argv[1])
            removed = delete_task(position)
            save_todos()
            print(f"Tarea eliminada: {removed}")
            return 0
        except (ValueError, IndexError) as exc:
            print(f"Error: {exc}")
            return 1

    if command == "save":
        save_todos()
        print("Tareas guardadas en todos.csv")
        return 0

    if command == "load":
        load_todos()
        print_list()
        return 0

    if command == "help":
        print("Comandos disponibles: add <titulo>, list, delete <posicion>, save, load, help")
        return 0

    print("Comando no reconocido. Usa 'help' para ver la lista.")
    return 1


if __name__ == "__main__":
    raise SystemExit(cli_dispatch(sys.argv[1:]))
