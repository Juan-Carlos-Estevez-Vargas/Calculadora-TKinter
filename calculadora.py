from tkinter import *
from math import sin, cos, tan, asin, acos, atan
import os


ventana = Tk()

# Ventana principal
ventana.geometry("340x490")
ventana.title("Calculadora Cientifica")
ventana.resizable(0, 0)  # No se puede redimensionar
ventana.attributes('-fullscreen', False)
ventana.configure(bg="#202020")

historial = StringVar()
historial.set(" ")

Hist = Label(ventana, textvariable=historial, width=30, justify='right',
             bg="#202020", foreground='white', font=('arial', 10, 'bold'), bd=4)
Hist.grid(row=0, column=2, columnspan=10)

input_text = StringVar()

grados = StringVar()
grados.set("grau")

RG = Button(ventana, highlightbackground="blue", highlightthickness=2,
            bd=4, textvariable=grados, width=8, height=1, font=("arial", 8))
RG.grid(row=0, column=1)

# Entrada de datos suministrada por el usuario
entrada = Entry(ventana, text=input_text, width=20, justify='right',
                bg="#202020", font=('arial', 22, "bold"), bd=5, foreground="white")
entrada.grid(row=1, column=0, columnspan=8, padx=5, pady=15, ipady=5)

# Matriz con la disposición de los botones
key_matrix = [["sin", "cos", "tan", "C", "<--"],
              ["2ªf", "Pi", "x!", "x<>y", "Hex"],
              ["m-", "mc", "mr", "m+", "/"],
              ["a/b", "7", "8", "9", "*"],
              ["1/x", "4", "5", "6", "-"],
              ["x²", "1", "2", "3", "+"],
              [u"\u221Ax", "(", "0", ".", "="]]

btn_dict = {}  # dicionario para montar Botones
respuesta = 0  # opcion usada para respuestas
mc = 0  # contenido memoria mr
p = ""  # numero en str de parentesis abiertos
last = ""  # ultimo contenido del visor
last_err = ""
last_ant = []  # Historico anterior Lista
Pi = 3.1415926535897932
f2 = 0  # 2ª función ativada=1 , desactivada=0


if os.name == "posix":  # (Android ou linux)
    w = 2  # largura botones para Android
else:
    w = 6  # largura botones para Windows

# Calcula la raiz cuadrada de un número


def R2(num):
    return num**.5

# Calcula la raiz cúbica de un número


def R3(num):
    return num**(1/3)

# Calculo seno con grados


def senx(x):
    global Pi
    return sin(Pi*x/180)

# Calculo arcoseno en grados


def asenx(x):
    global Pi
    return asin(x)*180/Pi

# Calculo coseno en grados


def cosx(x):
    global Pi
    return cos(Pi*x/180)

# Calculo arcoseno en grados


def acosx(x):
    global Pi
    return acos(x)*180/Pi

# Calculo tangente en grados


def tanx(x):
    global Pi
    return tan(Pi*x/180)

# Calculo arcotangente en grados


def atanx(x):
    global Pi
    return atan(x)*180/Pi

# TriABC Triángulo de lados A , B , C


def TriLabc(a=0, b=0, c=0):
    global last
    ok = ""

    # Si los lados son 0 o no se suministraron
    if a == b == c == 0:
        ok = "Sin LADOS a b c !!!"
        return ok

    # Si si se suministraron todos los lados y ninguno es 0
    elif a != 0 and b != 0 and c != 0:
        # Si a + b es mayor a c estamos frente a dos posibles casos
        if a + b > c:
            ok = "Triángulo."
            if round((a**2+b**2)**.5, 4) == round((c**2)**.5, 4):
                ok += " Rectángulo."
                if a == int(a) and b == int(b) and c == int(c):
                    ok += " Pitagórico"
            else:
                pass
        else:
            ok = "Triângulo no existe"

    # Si tenemos el lado c igual a 0 debemos calcular ese lado con pitágoras
    elif c == 0 and a != 0 and b != 0:
        c1 = a**2 + b**2
        c = c1**.5
        if c == int(c):
            c = int(c)
        else:
            c = f"R2({c1})"
        ok = f"Triángulo. Rectángulo= {a}, {b}, {c}"

    # Si hay dos lados iguales
    elif a == b == 0 and c != 0:
        cat1 = c**2/2
        if cat1 == int(cat1):
            cat1 = int(cat1)
        a = b = (cat1)**.5
        if a == int(a):
            a = b = int(a)
        else:
            a = b = f"R2({cat1})"
        ok = f"Triâng.Ret={a},{b},{c}"
        # return ok
    elif a == 0 and b != 0 and c != 0:
        a1 = c**2-b**2
        a = (a1)**.5
        if a == int(a):
            a = int(a)
        else:
            a = f"R2({a1})"
        ok = f"Triâng.Ret= {a},{b},{c}"
    elif b == 0 and a != 0 and c != 0:
        b1 = c**2-a**2
        b = (b1)**.5
        if b == int(b):
            b = int(b)
        else:
            b = f"R2({b1})"
        ok = f"Triâng.Ret= {a},{b},{c}"
    last_ant.append(last)
    last = last + f" R= {(eval(str(a))+eval(str(b))-eval(str(c)))/2}"
    return ok

# Activa las segundas funciones


def f2_operation(operation=""):
    global f2

    if operation == "D":
        f2 = 1  # activa para Desativar
    elif operation == "A":
        f2 = 0  # desativa para Activar

    codigo = u"\u221Ax"
    tecla_raiz = f'btn_{codigo}'

    if f2 == 1:
        btn_dict["btn_2ªf"].configure(bg="light grey")
        btn_dict[tecla_raiz].configure(text=codigo)
        btn_dict["btn_."].configure(text=f".")
        btn_dict["btn_("].configure(text=f"{p}(")
        btn_dict["btn_sin"].configure(text="sin")
        btn_dict["btn_cos"].configure(text="cos")
        btn_dict["btn_tan"].configure(text="tan")
        btn_dict["btn_Hex"].configure(text="Hex")
        btn_dict["btn_Pi"].configure(text="Pi")
        f2 = 0
    else:
        btn_dict["btn_2ªf"].configure(bg="cyan")
        btn_dict[tecla_raiz].configure(text=f"R2(")
        btn_dict["btn_."].configure(text=f",")
        btn_dict["btn_("].configure(text=f"{p})")
        btn_dict["btn_sin"].configure(text="asin")
        btn_dict["btn_cos"].configure(text="acos")
        btn_dict["btn_tan"].configure(text="atan")
        btn_dict["btn_Hex"].configure(text="Rom")
        btn_dict["btn_Pi"].configure(text="Tri")
        f2 = 1


def decima(num):
    n_int = int(num)

    # Si el número es entero devolvemos su representación en string
    if num == n_int:
        return str(num)

    fs = str(num+1*(num < .0001))[str(num+1).find(".")+1:]

    for x in range(len(fs)):
        a = fs[x:(x+1+fs[x+1:].find(fs[x]))]
        rep, decima = (fs.count(a), a)

        if len(decima) > 0 and fs.count(decima*rep) > 0 and rep > (11/len(decima)) and a != "0":
            break

    np = fs[:x]
    denominador = int((len(decima) == 0)*"10"+len(decima)*"9")*10**len(np)
    numerador = int(str(n_int)+np+decima) - int(str(n_int)+np) + \
        int(str(n_int)+fs)*(len(decima) == 0)
    return f"({numerador}/{denominador})"

# Calcula a entre b


def a_b(numero):
    aux = 1

    if numero < 0:
        aux = -1
        numero = abs(numero)

    numero_entero = int(numero)
    fraccion = numero-numero_entero

    if fraccion == 0:
        btn_dict["btn_<--"].configure(bg="green")
        return "Sin parte Decimal, ERROR"
    elif fraccion > 1e-6:
        fraccion = round(fraccion, 15)

    lista = []
    exponencial = 0
    for exp in range(16, 3, -1):
        if str(1+fraccion).count("0"*exp) == 1 and fraccion < 1e-5:
            exponencial = exp-1
            break
    fraccion *= 10**exponencial
    while fraccion > 1e-8 and len(lista) < 22:
        a = 1/fraccion  # sem arredondamento
        b = int(a)
        if len(str(b)) > 4 and len(lista) > 2:  # Limites
            break
        lista.append(b)
        fraccion = a-b

    if len(lista) % 2:
        impar = lista[-1]
        par = 0
        lista = lista+[0, 0, 0]
    else:
        par = lista[-1]
        impar = 0
        lista = lista+[0, 0]

    numerador = lista[-1]
    denominador = lista[-2]*numerador+1*(lista[-1] > 0)

    for i in range(3, len(lista)+1, 2):
        numerador = lista[-i]*denominador+1*(lista[-i+1] > 0)*(
            lista[-i+2] == 0)+numerador*(lista[-i+2] > 0)+par*(lista[-i+2] == 0)
        denominador = lista[-i-1]*numerador+1*(lista[-i] > 0)*(
            lista[-i+1] == 0)+denominador*(lista[-i+1] > 0)+impar*(lista[-i+1] == 0)

    denominador *= 10**exponencial
    numer2 = numerador+1*(lista[0] > 0)*(lista[1] == 0)
    numerador = (numer2 + numero_entero*denominador)*aux
    return f"({numerador}/{denominador})"

# Función para convertir entero en romano


def roman(num):
    # tabela em Dicionarios dos simbolos usados
    tabla_romanos = {1: {"1": "I", "4": "IV", "5": "V", "9": "IX"}, 2: {"1": "X", "4": "XL", "5": "L", "9": "XC"}, 3: {"1": "C", "4": "CD", "5": "D", "9": "CM"}, 4: {
        "1": "M", "4": "iv", "5": "v", "9": "ix"}, 5: {"1": "x", "4": "xl", "5": "l", "9": "xc"}, 6: {"1": "c", "4": "cd", "5": "d", "9": "cm"}, 7: {"1": "m"}}
    longitud_numero = len(num)

    if longitud_numero == 0:
        return ""
    if num.isdecimal():
        num = int(num)
        if num > 3999999:
            return ""
        return "".join([tabla_romanos[longitud_numero-i][n] if tabla_romanos[longitud_numero-i].get(n) else (tabla_romanos[longitud_numero-i]["5"]+(int(n)-5)*(tabla_romanos[longitud_numero-i]["1"]) if n > "5" else (int(n))*(tabla_romanos[longitud_numero-i]["1"])) for i, n in enumerate(str(num))])
    else:
        letras = "IVXLCDMivxlcdm "
        num = num + " "
        ok = [i for i in num if i not in letras]

        if len(ok):
            print("letras en Romano no disponibles: ", ok)
            return ""
        tabla_romanos2 = {" ": 0, "I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000,
                          "i": 1000, "v": 5000, "x": 10000, "l": 50000, "c": 100000, "d": 500000, "m": 1000000}

        return str(sum([a if (a := tabla_romanos2[num[longitud_numero-i]]) >= tabla_romanos2[num[longitud_numero-i+1]] else -a for i in range(1, longitud_numero+1)]))

# Botón memoria mr


def cor_mem():
    global mc

    if mc < 0:
        btn_dict["btn_mr"].configure(bg="magenta")
    elif mc > 0:
        btn_dict["btn_mr"].configure(bg="green")
    elif mc == 0:
        btn_dict["btn_mr"].configure(bg="light grey")

# Botón para intercambiar entre radianes y grados


def grau(self):
    global grados
    if grados.get() == "rad":
        grados.set("grad")
    else:
        grados.set("rad")


def cop_yx(e):
    global input_text, historial, last_ant
    input_text.set(historial.get())  # actualiza 2º visor como 1º visor
    if len(last_ant) > 0:
        historial.set(last_ant.pop())


# executa funçión grad al clicar con botón nª1 del mouse
RG.bind("<Button-1>", grau)
Hist.bind("<Button-1>", cop_yx)  # executa funçión cop_xy

# Calcula una operación según sea la tecla presionada por el usuario


def Calcula(event):
    global Pi, last, mc, f2, p, historial, last_ant, last_err
    botonPresionado = event.widget.cget("text")
    global key_matrix, input_text, respuesta

    try:
        if botonPresionado == u"\u221Ax":
            if float(eval(input_text.get())) < 0:
                last = input_text.get()
                input_text.set("Numero Negativo, ERROR")
                btn_dict["btn_<--"].configure(bg="green")
                return
            last_ant.append(last)
            last = input_text.get()
            respuesta = float(eval(input_text.get())**(0.5))
            input_text.set(str(respuesta))

        elif botonPresionado == "R2(":
            p = str(int("0"+p) + 1)
            input_text.set(input_text.get()+"R2(")

        elif botonPresionado == "1/x":
            last_ant.append(last)
            last = input_text.get()
            respuesta = 1/float(eval(input_text.get()))
            input_text.set(str(respuesta))

        elif botonPresionado == "Hex":
            num = int(float(input_text.get()))
            tab = ["0", "1", "2", "3", "4", "5", "6", "7",
                   "8", "9", "A", "B", "C", "D", "E", "F"]
            hex = ""

            while num > 0:
                r = num % 16
                hex = tab[r]+hex
                num = num//16

            last_ant.append(last)
            last = input_text.get()
            input_text.set(hex)

        elif botonPresionado == "x²":
            last_ant.append(last)
            last = input_text.get()
            respuesta = float(eval(input_text.get()))**2
            input_text.set(str(respuesta))

        elif botonPresionado == " Pi":
            last_ant.append(last)
            last = input_text.get()
            input_text.set(input_text.get()+"Pi")

        elif botonPresionado == "Tri":
            input_text.set("TriLabc(")
            p = str(int("0"+p) + 1)

        elif botonPresionado == "x<>y":
            trc = input_text.get()
            input_text.set(last)
            last = trc
        elif botonPresionado == "a/b":
            if "ERROR" in input_text.get():
                return

            num = float(eval(input_text.get()))
            last_ant.append(last)
            last = input_text.get()
            historial.set(decima(num))
            input_text.set(a_b(num))

        elif botonPresionado == "Rom":
            respuesta = roman(input_text.get())
            if len(respuesta) > 0:
                last_ant.append(last)
                last = input_text.get()
                input_text.set(respuesta)

        elif botonPresionado == "2ªf":
            f2_operation()  # desactiva o activa f2

        elif botonPresionado[-1] == "(" or botonPresionado[-1] == ")":
            pc = int("0"+p)

            if f2 == 0:
                p = str(pc + 1)
                input_text.set(input_text.get() + "(")
                btn_dict["btn_("].configure(text=f"{p}(")
            else:
                if pc > 0:
                    p = str(pc - 1)
                    if pc == 1:
                        p = ""
                    input_text.set(input_text.get() + ")")
                    btn_dict["btn_("].configure(text=f"{p})")

        elif botonPresionado == "C":
            if input_text.get() == "":
                historial.set("")

            p = ""
            f2_operation("D")  # Desactiva 2ª funçión
            input_text.set("")
            btn_dict["btn_<--"].configure(bg="light grey")

        elif botonPresionado == "x!":
            def fact(n): return 1 if n == 0 else n*fact(n-1)
            num = fact(int(input_text.get()))
            last_ant.append(last)
            last = input_text.get()
            input_text.set(str(num))

        elif botonPresionado == "<--":
            respuesta = input_text.get()
            if "ERROR" in respuesta:
                input_text.set(last_err)
                btn_dict["btn_<--"].configure(bg="light grey")
            else:
                if respuesta[-1] == "(":
                    p = str(int("0"+p) - 1)
                    if p == "0":
                        p = " "
                    btn_dict["btn_("].configure(text=f"{p}{respuesta[-1]}")
                    f2_operation("D")  # Desativa 2ª função
                if respuesta[-1] == ")":
                    p = str(int("0"+p) + 1)
                    btn_dict["btn_("].configure(text=f"{p}{respuesta[-1]}")
                    f2_operation("A")  # Ativa 2ª função
                input_text.set(respuesta[:-1])

        elif botonPresionado[-3:] == "sin":
            p = str(int("0"+p) + 1)

            if grados.get() == "rad":
                if f2 == 0:
                    input_text.set(input_text.get()+"sin(")
                else:
                    input_text.set(input_text.get()+"asin(")
            else:
                if f2 == 0:
                    input_text.set(input_text.get()+"senx(")
                else:
                    input_text.set(input_text.get()+"asenx(")
            f2_operation("D")

        elif botonPresionado[-3:] == "cos":
            p = str(int("0"+p) + 1)
            if grados.get() == "rad":
                if f2 == 0:
                    input_text.set(input_text.get()+"cos(")
                else:
                    input_text.set(input_text.get()+"acos(")
            else:
                if f2 == 0:
                    input_text.set(input_text.get()+"cosx(")
                else:
                    input_text.set(input_text.get()+"acosx(")
            f2_operation("D")

        elif botonPresionado[-3:] == "tan":
            p = str(int("0"+p) + 1)
            if grados.get() == "rad":
                if f2 == 0:
                    input_text.set(input_text.get()+"tan(")
                else:
                    input_text.set(input_text.get()+"atan(")
            else:
                if f2 == 0:
                    input_text.set(input_text.get()+"tanx(")
                else:
                    input_text.set(input_text.get()+"atanx(")
            f2_operation("D")

        elif botonPresionado == "mc":
            mc = 0
            cor_mem()

        elif botonPresionado == "mr":
            if input_text.get() == "":
                input_text.set("("+str(mc)+")")
            else:
                if input_text.get()[-1] in "1234567890":
                    input_text.set("("+str(mc)+")")
                else:
                    last = input_text.get()
                    input_text.set(input_text.get()+"("+str(mc)+")")

        elif botonPresionado == "m+":
            mc += float(input_text.get())
            cor_mem()

        elif botonPresionado == "m-":
            mc -= float(input_text.get())
            cor_mem()

        elif botonPresionado == ",":
            respuesta = input_text.get()
            if len(respuesta) > 2:
                input_text.set(respuesta+",")

        elif botonPresionado == ".":
            respuesta = input_text.get()
            if respuesta == "":
                input_text.set(respuesta+".")
            elif respuesta[-1] != ".":
                if len(respuesta) > 2:
                    if respuesta[-2] != ".":
                        input_text.set(respuesta+".")
                else:
                    input_text.set(respuesta+".")

        elif botonPresionado == "=":
            if "ERROR" in input_text.get():
                input_text.set(last_err)
                btn_dict["btn_<--"].configure(bg="light grey")
            else:
                last_ant.append(last)
                last = input_text.get().split()[-1]

                while last[:2] == "00":
                    last = last[1:]
                c0 = last[last.find("."):].count("0")
                c9 = last[last.find("."):].count("9")

                if c9 > 8 or c0 > 8:
                    last = str(round(float(last), max(c0, c9)-1))

                respuesta = eval(last)
                if type(respuesta) != type("A"):
                    if respuesta > .1:
                        respuesta = str(round(respuesta, 16))
                    else:
                        respuesta = str(respuesta)
                    if len(respuesta) > 24:
                        respuesta = str(float(respuesta))

                if respuesta == last:
                    last = last_ant.pop()
                input_text.set(respuesta)
                historial.set(last)
                f2_operation("D")  # zera 2ª função
        else:
            input_text.set(input_text.get()+str(botonPresionado.strip()))
            cor_mem()
    except:
        last_err = input_text.get()
        input_text.set("ERROU")
        btn_dict["btn_<--"].configure(bg="green")


# Construyendo los botones en la ventana
for i in range(len(key_matrix)):
    for j in range(len(key_matrix[i])):
        btn_dict["btn_"+str(key_matrix[i][j])] = Button(ventana, bd=4, text=str(key_matrix[i][j]),
                                                        width=w, height=2, font=("arial", 11, "bold"), foreground='white', background="#3b3b3b")
        btn_dict["btn_"+str(key_matrix[i][j])].grid(row=i+2, column=j+1)
        btn_dict["btn_"+str(key_matrix[i][j])].bind('<Button-1>', Calcula)

btn_dict["btn_sin"].configure(
    highlightbackground="blue", highlightthickness=2, bd=2)
btn_dict["btn_cos"].configure(
    highlightbackground="blue", highlightthickness=2, bd=2)
btn_dict["btn_tan"].configure(
    highlightbackground="blue", highlightthickness=2, bd=2)
btn_dict["btn_="].configure(bg="cyan")


ventana.mainloop()
