import csv

import main


def test_add_one_task_and_delete_task(tmp_path, monkeypatch):
    data_file = tmp_path / "todos.csv"
    monkeypatch.setattr(main, "DATA_FILE", data_file)
    monkeypatch.setattr(main, "todos", [])

    main.add_one_task("Revisar pedidos")
    main.add_one_task("Enviar inventario")
    assert main.todos == ["Revisar pedidos", "Enviar inventario"]

    deleted = main.delete_task(1)
    assert deleted == "Revisar pedidos"
    assert main.todos == ["Enviar inventario"]

    main.save_todos(data_file)
    main.load_todos(data_file)
    assert main.todos == ["Enviar inventario"]


def test_print_list_and_load_todos_from_csv(tmp_path, monkeypatch):
    data_file = tmp_path / "todos.csv"
    data_file.write_text("title\nRevisar almacén\nPreparar ruta\n", encoding="utf-8")
    monkeypatch.setattr(main, "DATA_FILE", data_file)
    monkeypatch.setattr(main, "todos", [])

    tasks = main.load_todos(data_file)
    assert tasks == ["Revisar almacén", "Preparar ruta"]
    assert main.todos == ["Revisar almacén", "Preparar ruta"]

    output = []
    original_print = print

    def fake_print(value):
        output.append(str(value))

    monkeypatch.setattr("builtins.print", fake_print)
    main.print_list()
    assert "1. Revisar almacén" in output
    assert "2. Preparar ruta" in output
    monkeypatch.setattr("builtins.print", original_print)
