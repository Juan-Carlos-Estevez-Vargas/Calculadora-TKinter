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

Hist = Label(ventana, textvariable=historial, width=30, justify='right', bg="#202020", foreground='white', font=('arial', 10, 'bold'), bd=4)
Hist.grid(row=0, column=2, columnspan=10)

inputText = StringVar()

grados = StringVar()
grados.set("grau")

RG = Button(ventana, highlightbackground="blue", highlightthickness=2, bd=4, textvariable=grados, width=8, height=1, font=("arial", 8))
RG.grid(row=0, column=1)

# Entrada de datos suministrada por el usuario
entrada = Entry(ventana, text=inputText, width=20, justify='right', bg="#202020", font=('arial', 22, "bold"), bd=5, foreground="white")
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
resp = 0  # opcion usada para respuestas
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

    if num == n_int:
        return str(num)
    
    fs = str(num+1*(num < .0001))[str(num+1).find(".")+1:]

    for x in range(len(fs)):
        a = fs[x:(x+1+fs[x+1:].find(fs[x]))]
        rep, dizima = (fs.count(a), a)
        if len(dizima) > 0 and fs.count(dizima*rep) > 0 and rep > (11/len(dizima)) and a != "0":
            break
    np = fs[:x]
    denumer = int((len(dizima) == 0)*"10"+len(dizima)*"9")*10**len(np)
    numer = int(str(n_int)+np+dizima) - int(str(n_int)+np) + \
        int(str(n_int)+fs)*(len(dizima) == 0)
    return f"({numer}/{denumer})"

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

    lst = []
    exponencial = 0
    for exp in range(16, 3, -1):
        if str(1+fraccion).count("0"*exp) == 1 and fraccion < 1e-5:
            exponencial = exp-1
            break
    fraccion *= 10**exponencial
    while fraccion > 1e-8 and len(lst) < 22:
        a = 1/fraccion  # sem arredondamento
        b = int(a)
        if len(str(b)) > 4 and len(lst) > 2:  # Limites
            break
        lst.append(b)
        fraccion = a-b
    #print("Numeros encontrados",*lst)
    if len(lst) % 2:
        impar = lst[-1]
        par = 0
        lst = lst+[0, 0, 0]
    else:
        par = lst[-1]
        impar = 0
        lst = lst+[0, 0]
    numer = lst[-1]
    denumer = lst[-2]*numer+1*(lst[-1] > 0)
    for i in range(3, len(lst)+1, 2):
        numer = lst[-i]*denumer+1*(lst[-i+1] > 0)*(lst[-i+2]
                                                   == 0)+numer*(lst[-i+2] > 0)+par*(lst[-i+2] == 0)
        denumer = lst[-i-1]*numer+1*(lst[-i] > 0)*(lst[-i+1]
                                                   == 0)+denumer*(lst[-i+1] > 0)+impar*(lst[-i+1] == 0)
    denumer *= 10**exponencial
    numer2 = numer+1*(lst[0] > 0)*(lst[1] == 0)
    numer = (numer2 + numero_entero*denumer)*aux
    return f"({numer}/{denumer})"

# Función para convertir entero en romano
def roman(num):
    # tabela em Dicionarios dos simbolos usados
    tablaRomanos = {1: {"1": "I", "4": "IV", "5": "V", "9": "IX"}, 2: {"1": "X", "4": "XL", "5": "L", "9": "XC"}, 3: {"1": "C", "4": "CD", "5": "D", "9": "CM"}, 4: {
        "1": "M", "4": "iv", "5": "v", "9": "ix"}, 5: {"1": "x", "4": "xl", "5": "l", "9": "xc"}, 6: {"1": "c", "4": "cd", "5": "d", "9": "cm"}, 7: {"1": "m"}}
    longitudNumero = len(num)
    if longitudNumero == 0:
        return ""
    if num.isdecimal():
        num = int(num)
        if num > 3999999:
            return ""
        return "".join([tablaRomanos[longitudNumero-i][n] if tablaRomanos[longitudNumero-i].get(n) else (tablaRomanos[longitudNumero-i]["5"]+(int(n)-5)*(tablaRomanos[longitudNumero-i]["1"]) if n > "5" else (int(n))*(tablaRomanos[longitudNumero-i]["1"])) for i, n in enumerate(str(num))])
    else:
        letras = "IVXLCDMivxlcdm "
        num = num + " "
        ok = [i for i in num if i not in letras]
        if len(ok):
            print("letras em Romano no disponibles: ", ok)
            return ""
        tablaRomanos2 = {" ": 0, "I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000,
                "i": 1000, "v": 5000, "x": 10000, "l": 50000, "c": 100000, "d": 500000, "m": 1000000}
        return str(sum([a if (a := tablaRomanos2[num[longitudNumero-i]]) >= tablaRomanos2[num[longitudNumero-i+1]] else -a for i in range(1, longitudNumero+1)]))


def cor_mem():  # cor do botao memoria mr
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
        grados.set("grau")
    else:
        grados.set("rad")


def cop_yx(e):
    global inputText, historial, last_ant
    inputText.set(historial.get())  # atualiza 2º visor com o 1º visor
    if len(last_ant) > 0:
        historial.set(last_ant.pop())


# executa função grau se clicar com botao nª1 do mouse
RG.bind("<Button-1>", grau)
Hist.bind("<Button-1>", cop_yx)  # executa função cop_xy

# Calcula una operación según sea la tecla presionada por el usuario
def Calcula(event):
    global Pi, last, mc, f2, p, historial, last_ant, last_err
    botonPresionado = event.widget.cget("text")
    global key_matrix, inputText, resp

    try:
        if botonPresionado == u"\u221Ax":
            if float(eval(inputText.get())) < 0:
                last = inputText.get()
                inputText.set("Numero Negativo, ERROR")
                btn_dict["btn_<--"].configure(bg="green")
                return
            last_ant.append(last)
            last = inputText.get()
            resp = float(eval(inputText.get())**(0.5))
            inputText.set(str(resp))

        elif botonPresionado == "R2(":
            p = str(int("0"+p) + 1)
            inputText.set(inputText.get()+"R2(")

        elif botonPresionado == "1/x":
            last_ant.append(last)
            last = inputText.get()
            resp = 1/float(eval(inputText.get()))
            inputText.set(str(resp))
        elif botonPresionado == "Hex":
            num = int(float(inputText.get()))
            tab = ["0", "1", "2", "3", "4", "5", "6", "7",
                   "8", "9", "A", "B", "C", "D", "E", "F"]
            hex = ""
            while num > 0:
                r = num % 16
                hex = tab[r]+hex
                num = num//16
            last_ant.append(last)
            last = inputText.get()
            inputText.set(hex)
        elif botonPresionado == "x²":
            last_ant.append(last)
            last = inputText.get()
            resp = float(eval(inputText.get()))**2
            inputText.set(str(resp))
        elif botonPresionado == " Pi":
            last_ant.append(last)
            last = inputText.get()
            inputText.set(inputText.get()+"Pi")
        elif botonPresionado == "Tri":
            inputText.set("TriLabc(")
            p = str(int("0"+p) + 1)
        elif botonPresionado == "x<>y":
            trc = inputText.get()
            inputText.set(last)
            last = trc
        elif botonPresionado == "a/b":
            if "ERROU" in inputText.get():
                return
            num = float(eval(inputText.get()))
            last_ant.append(last)
            last = inputText.get()
            historial.set(decima(num))
            inputText.set(a_b(num))
        elif botonPresionado == "Rom":
            resp = roman(inputText.get())
            if len(resp) > 0:
                last_ant.append(last)
                last = inputText.get()
                inputText.set(resp)
        elif botonPresionado == "2ªf":
            f2_operation()  # desativa f2 ou ativa
        elif botonPresionado[-1] == "(" or botonPresionado[-1] == ")":
            pc = int("0"+p)
            if f2 == 0:
                p = str(pc + 1)
                inputText.set(inputText.get() + "(")
                btn_dict["btn_("].configure(text=f"{p}(")
            else:
                if pc > 0:
                    p = str(pc - 1)
                    if pc == 1:
                        p = ""
                    inputText.set(inputText.get() + ")")
                    btn_dict["btn_("].configure(text=f"{p})")
        elif botonPresionado == "C":
            if inputText.get() == "":
                historial.set("")
            p = ""
            f2_operation("D")  # Desativa 2ª função
            inputText.set("")
            btn_dict["btn_<--"].configure(bg="light grey")
        elif botonPresionado == "x!":
            def fact(n): return 1 if n == 0 else n*fact(n-1)
            num = fact(int(inputText.get()))
            last_ant.append(last)
            last = inputText.get()
            inputText.set(str(num))
        elif botonPresionado == "<--":
            resp = inputText.get()
            if "ERROU" in resp:
                inputText.set(last_err)
                btn_dict["btn_<--"].configure(bg="light grey")
            else:
                if resp[-1] == "(":
                    p = str(int("0"+p) - 1)
                    if p == "0":
                        p = " "
                    btn_dict["btn_("].configure(text=f"{p}{resp[-1]}")
                    f2_operation("D")  # Desativa 2ª função
                if resp[-1] == ")":
                    p = str(int("0"+p) + 1)
                    btn_dict["btn_("].configure(text=f"{p}{resp[-1]}")
                    f2_operation("A")  # Ativa 2ª função
                inputText.set(resp[:-1])
        elif botonPresionado[-3:] == "sin":
            p = str(int("0"+p) + 1)
            if grados.get() == "rad":
                if f2 == 0:
                    inputText.set(inputText.get()+"sin(")
                else:
                    inputText.set(inputText.get()+"asin(")
            else:
                if f2 == 0:
                    inputText.set(inputText.get()+"senx(")
                else:
                    inputText.set(inputText.get()+"asenx(")
            f2_operation("D")  # zera 2ª função
        elif botonPresionado[-3:] == "cos":
            p = str(int("0"+p) + 1)
            if grados.get() == "rad":
                if f2 == 0:
                    inputText.set(inputText.get()+"cos(")
                else:
                    inputText.set(inputText.get()+"acos(")
            else:
                if f2 == 0:
                    inputText.set(inputText.get()+"cosx(")
                else:
                    inputText.set(inputText.get()+"acosx(")
            f2_operation("D")  # Zera 2ª função
        elif botonPresionado[-3:] == "tan":
            p = str(int("0"+p) + 1)
            if grados.get() == "rad":
                if f2 == 0:
                    inputText.set(inputText.get()+"tan(")
                else:
                    inputText.set(inputText.get()+"atan(")
            else:
                if f2 == 0:
                    inputText.set(inputText.get()+"tanx(")
                else:
                    inputText.set(inputText.get()+"atanx(")
            f2_operation("D")  # zera 2ª função
        elif botonPresionado == "mc":
            mc = 0
            cor_mem()
        elif botonPresionado == "mr":
            if inputText.get() == "":
                inputText.set("("+str(mc)+")")
            else:
                if inputText.get()[-1] in "1234567890":
                    inputText.set("("+str(mc)+")")
                else:
                    last = inputText.get()
                    inputText.set(inputText.get()+"("+str(mc)+")")
        elif botonPresionado == "m+":
            pass
            mc += float(inputText.get())
            cor_mem()
        elif botonPresionado == "m-":
            pass
            mc -= float(inputText.get())
            cor_mem()
        elif botonPresionado == ",":
            resp = inputText.get()
            if len(resp) > 2:
                inputText.set(resp+",")

        elif botonPresionado == ".":
            resp = inputText.get()
            if resp == "":
                inputText.set(resp+".")
            elif resp[-1] != ".":
                if len(resp) > 2:
                    if resp[-2] != ".":
                        inputText.set(resp+".")
                else:
                    inputText.set(resp+".")
        elif botonPresionado == "=":
            if "ERROU" in inputText.get():
                inputText.set(last_err)
                btn_dict["btn_<--"].configure(bg="light grey")
            else:
                last_ant.append(last)
                last = inputText.get().split()[-1]
                while last[:2] == "00":
                    last = last[1:]
                c0 = last[last.find("."):].count("0")
                c9 = last[last.find("."):].count("9")
                if c9 > 8 or c0 > 8:
                    last = str(round(float(last), max(c0, c9)-1))
                resp = eval(last)
                if type(resp) != type("A"):
                    if resp > .1:
                        resp = str(round(resp, 16))
                    else:
                        resp = str(resp)
                    if len(resp) > 24:
                        resp = str(float(resp))
                if resp == last:
                    last = last_ant.pop()
                inputText.set(resp)
                historial.set(last)
                f2_operation("D")  # zera 2ª função
        else:
            inputText.set(inputText.get()+str(botonPresionado.strip()))
            cor_mem()
    except:
        last_err = inputText.get()
        inputText.set("ERROU")
        btn_dict["btn_<--"].configure(bg="green")

# Construyendo los botones en la ventana
for i in range(len(key_matrix)):
    for j in range(len(key_matrix[i])):
        btn_dict["btn_"+str(key_matrix[i][j])] = Button(ventana, bd=4, text=str(key_matrix[i][j]), width=w, height=2, font=("arial", 11, "bold"), foreground='white', background="#3b3b3b")
        btn_dict["btn_"+str(key_matrix[i][j])].grid(row=i+2, column=j+1)
        btn_dict["btn_"+str(key_matrix[i][j])].bind('<Button-1>', Calcula)

btn_dict["btn_sin"].configure(highlightbackground="blue", highlightthickness=2, bd=2)
btn_dict["btn_cos"].configure(highlightbackground="blue", highlightthickness=2, bd=2)
btn_dict["btn_tan"].configure(highlightbackground="blue", highlightthickness=2, bd=2)

ventana.mainloop()
