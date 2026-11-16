
import tkinter as tk
from tkinter import messagebox
from datetime import date


# Student information
STUDENT_NAME = "Wilmer Jose Gomez Ospino"
APP_NAME = "Fase4WilmerGomez"


# This class represents each node of the tree
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


root_node = None


# Add a number to the binary search tree
def insert_node(current, value, level=1):

    if current is None:
        return TreeNode(value), "added"

    if value == current.value:
        return current, "duplicate"

    if value < current.value:

        if current.left is None:
            if level == 4:
                return current, "level"

            current.left = TreeNode(value)
            return current, "added"

        current.left, result = insert_node(
            current.left, value, level + 1
        )
        return current, result

    else:

        if current.right is None:
            if level == 4:
                return current, "level"

            current.right = TreeNode(value)
            return current, "added"

        current.right, result = insert_node(
            current.right, value, level + 1
        )
        return current, result


# Search for a number in the tree
def search_node(current, value):

    if current is None:
        return False

    if current.value == value:
        return True

    if value < current.value:
        return search_node(current.left, value)

    return search_node(current.right, value)


# Preorder traversal: Root, Left, Right
def preorder(current, result):

    if current is not None:
        result.append(current.value)
        preorder(current.left, result)
        preorder(current.right, result)


# Inorder traversal: Left, Root, Right
def inorder(current, result):

    if current is not None:
        inorder(current.left, result)
        result.append(current.value)
        inorder(current.right, result)


# Postorder traversal: Left, Right, Root
def postorder(current, result):

    if current is not None:
        postorder(current.left, result)
        postorder(current.right, result)
        result.append(current.value)


# Draw the binary tree on the screen
def draw_tree(canvas, current, x, y, space):

    if current is None:
        return

    next_y = y + 55
    next_space = space / 2

    if current.left is not None:
        left_x = x - space
        canvas.create_line(x, y, left_x, next_y)

        draw_tree(
            canvas, current.left,
            left_x, next_y, next_space
        )

    if current.right is not None:
        right_x = x + space
        canvas.create_line(x, y, right_x, next_y)

        draw_tree(
            canvas, current.right,
            right_x, next_y, next_space
        )

    canvas.create_oval(
        x - 17, y - 17,
        x + 17, y + 17,
        fill="lightblue",
        outline="black"
    )

    canvas.create_text(
        x, y,
        text=str(current.value),
        font=("Arial", 10, "bold")
    )


# Show the tree
def show_tree():

    tree_canvas.delete("all")

    if root_node is None:
        tree_canvas.create_text(
            280, 110,
            text="El arbol esta vacio",
            font=("Arial", 12)
        )
    else:
        draw_tree(
            tree_canvas,
            root_node,
            280, 30, 140
        )


# Show the numbers of each traversal
def show_traversal(canvas, values):

    canvas.delete("all")

    if len(values) == 0:
        canvas.create_text(
            280, 40,
            text="Sin datos por mostrar",
            font=("Arial", 12)
        )
        return

    x = 15

    for value in values:

        canvas.create_rectangle(
            x, 25, x + 30, 55,
            fill="lightgreen",
            outline="black"
        )

        canvas.create_text(
            x + 15, 40,
            text=str(value),
            font=("Arial", 9, "bold")
        )

        x = x + 36


# Update all four panels
def update_panels():

    show_tree()

    preorder_values = []
    inorder_values = []
    postorder_values = []

    preorder(root_node, preorder_values)
    inorder(root_node, inorder_values)
    postorder(root_node, postorder_values)

    show_traversal(preorder_canvas, preorder_values)
    show_traversal(inorder_canvas, inorder_values)
    show_traversal(postorder_canvas, postorder_values)


# Add a new node
def add_node():

    global root_node

    text = number_entry.get()

    try:
        value = int(text)
    except ValueError:
        messagebox.showerror(
            "Dato incorrecto",
            "Por favor, ingresa un numero entero."
        )
        return

    root_node, result = insert_node(root_node, value)

    if result == "duplicate":
        messagebox.showwarning(
            "Aviso",
            "Ese numero ya se encuentra en el arbol."
        )
        return

    if result == "level":
        messagebox.showerror(
            "Limite alcanzado",
            "No se pueden agregar mas de cuatro niveles."
        )
        return

    number_entry.delete(0, tk.END)
    update_panels()

    messagebox.showinfo(
        "Registro exitoso",
        "El numero se agrego correctamente."
    )


# Search for a node
def find_node():

    text = number_entry.get()

    try:
        value = int(text)
    except ValueError:
        messagebox.showerror(
            "Dato incorrecto",
            "Por favor, ingresa un numero entero."
        )
        return

    if search_node(root_node, value):
        messagebox.showinfo(
            "Busqueda",
            "El numero si se encuentra en el arbol."
        )
    else:
        messagebox.showwarning(
            "Busqueda",
            "No encontramos ese numero en el arbol."
        )


# Clear the complete tree
def clear_tree():

    global root_node

    root_node = None
    number_entry.delete(0, tk.END)

    update_panels()

    messagebox.showinfo(
        "Arbol limpio",
        "Se han eliminado todos los nodos."
    )


# Close the application
def exit_application():

    main_window.destroy()


# Open the main application window
def open_main_window():

    global main_window
    global number_entry
    global tree_canvas
    global preorder_canvas
    global inorder_canvas
    global postorder_canvas

    login_window.destroy()

    main_window = tk.Tk()
    main_window.title("Arbol Binario de Busqueda")
    main_window.geometry("1200x750")
    main_window.resizable(False, False)

    title = tk.Label(
        main_window,
        text="ARBOL BINARIO DE BUSQUEDA",
        font=("Arial", 20, "bold")
    )
    title.pack(pady=10)

    # Number input
    input_frame = tk.Frame(main_window)
    input_frame.pack(pady=10)

    tk.Label(
        input_frame,
        text="Ingresa un numero:"
    ).grid(row=0, column=0, padx=5)

    number_entry = tk.Entry(
        input_frame,
        width=20
    )
    number_entry.grid(row=0, column=1, padx=5)

    # Application buttons
    tk.Button(
        input_frame,
        text="Agregar Nodo",
        width=13,
        command=add_node
    ).grid(row=0, column=2, padx=5)

    tk.Button(
        input_frame,
        text="Buscar Nodo",
        width=13,
        command=find_node
    ).grid(row=0, column=3, padx=5)

    tk.Button(
        input_frame,
        text="Limpiar",
        width=13,
        command=clear_tree
    ).grid(row=0, column=4, padx=5)

    tk.Button(
        input_frame,
        text="Salir",
        width=13,
        command=exit_application
    ).grid(row=0, column=5, padx=5)

    # Tree panel
    tree_frame = tk.LabelFrame(
        main_window,
        text="ARBOL",
        font=("Arial", 11, "bold"),
        width=570,
        height=280
    )
    tree_frame.place(x=15, y=110)
    tree_frame.pack_propagate(False)

    tree_canvas = tk.Canvas(
        tree_frame,
        width=560,
        height=240,
        bg="white"
    )
    tree_canvas.pack()

    # Preorder panel
    preorder_frame = tk.LabelFrame(
        main_window,
        text="PREORDEN",
        font=("Arial", 11, "bold"),
        width=570,
        height=230
    )
    preorder_frame.place(x=610, y=110)
    preorder_frame.pack_propagate(False)

    preorder_canvas = tk.Canvas(
        preorder_frame,
        width=560,
        height=190,
        bg="white"
    )
    preorder_canvas.pack()

    # Inorder panel
    inorder_frame = tk.LabelFrame(
        main_window,
        text="INORDEN",
        font=("Arial", 11, "bold"),
        width=570,
        height=230
    )
    inorder_frame.place(x=15, y=420)
    inorder_frame.pack_propagate(False)

    inorder_canvas = tk.Canvas(
        inorder_frame,
        width=560,
        height=190,
        bg="white"
    )
    inorder_canvas.pack()

    # Postorder panel
    postorder_frame = tk.LabelFrame(
        main_window,
        text="POSORDEN",
        font=("Arial", 11, "bold"),
        width=570,
        height=230
    )
    postorder_frame.place(x=610, y=420)
    postorder_frame.pack_propagate(False)

    postorder_canvas = tk.Canvas(
        postorder_frame,
        width=560,
        height=190,
        bg="white"
    )
    postorder_canvas.pack()

    update_panels()

    main_window.mainloop()


# Check the access password
def check_password():

    password = password_entry.get()

    if password == "UNAD":
        open_main_window()
    else:
        messagebox.showerror(
            "Acceso denegado",
            "La contrasena ingresada no es correcta."
        )


# Login window
login_window = tk.Tk()
login_window.title("Acceso a la aplicacion")
login_window.geometry("430x350")
login_window.resizable(False, False)

tk.Label(
    login_window,
    text=APP_NAME,
    font=("Arial", 18, "bold")
).pack(pady=15)

tk.Label(
    login_window,
    text="Estudiante: " + STUDENT_NAME,
    font=("Arial", 11)
).pack(pady=5)

tk.Label(
    login_window,
    text="Fecha: " + date.today().strftime("%d/%m/%Y"),
    font=("Arial", 11)
).pack(pady=5)

tk.Label(
    login_window,
    text="Ingresa la contrasena:",
    font=("Arial", 11)
).pack(pady=15)

password_entry = tk.Entry(
    login_window,
    show="*",
    width=25
)
password_entry.pack(pady=5)

tk.Button(
    login_window,
    text="INGRESAR",
    width=15,
    command=check_password
).pack(pady=20)

login_window.mainloop()
