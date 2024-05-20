prompts = {
    "tutorial": "tut"
}

tutorials = {
    "variablen_operatoren": 
    """
🌟 **Operatoren und Variablen**

📋 **Die wichtigsten Konzepte**  
*Variablen* - Was ist das?  
Variablen sind wie kleine Boxen, in denen du Informationen speichern kannst.
Beispiel: x = 5 speichert die Zahl 5 in der Variable x.  

**Datentypen**  
- Zahlen: int (Ganze Zahlen), float (Dezimalzahlen)
- Text: str (Zeichenketten oder Strings)
- Wahrheitswerte: bool (True oder False)  

**Operatoren**  
- Arithmetisch: +, -, *, / (Addition, Subtraktion, Multiplikation, Division)
- Vergleich: ==, !=, >, <, >=, <= (Gleich, Ungleich, Größer als, Kleiner als, usw.)

🛠️ **Beispiele**  
1) Ausgabe einer Zeichenkette (Datentyp str). Denke hier an die Anführungszeichen!
```python
# Ein Wort in einer Variable ablegen 
name = "Lisa" 
print(name)
# Ausgabe: Lisa
```

2) Erstellen von Variablen mit Zahlen (Datentyp int) und Ausgabe der Additions
```python
# Zwei Zahlen speichern - Datentyp int
a = 2
b = 3

# Die Zahlen addieren
summe = a + b
# Ausgabe: 5

# Das Ergebnis ausgeben
print("Die Summe ist:", summe)
```

3) Vergleiche 2 Zahlen und gib das Ergebnis aus:
```python
a = 50
b = 2

print(a > b)
# Ausgabe: True
```

📚 **Nützliche Ressourcen**  
- [W3Schools](https://www.w3schools.com/python/python_variables.asp) bietet eine Einführung in Python-Variablen und Operatoren.  
""",
    "if_else" : 
    """
🌟 **If/Else-Anweisungen in Python**

📋 **Die wichtigsten Konzepte**  
*If/Else-Anweisungen* - Was ist das?  
If/Else-Anweisungen sind wie Wegweiser in deinem Code. Sie helfen deinem Programm zu entscheiden, welchen Weg es nehmen soll, basierend auf bestimmten Bedingungen.

**Syntax von If/Else-Anweisungen**  
- `if` - Überprüft, ob eine Bedingung wahr ist.
- `else` - Führt einen Block aus, wenn keine der vorherigen Bedingungen wahr ist.
- `elif` - (kurz für "else if") Überprüft eine neue Bedingung, falls die vorherige Bedingung falsch war.

**Schlüsselwörter und Konzepte**
- `if`-Bedingung: Beginnt eine bedingte Anweisung.
- `else`: Wird ausgeführt, wenn die `if`-Bedingung nicht erfüllt ist.
- `elif`: Ermöglicht zusätzliche Bedingungen.

🛠️ **Beispiele**

1) Einfache If-Anweisung
```python
# Einfache Bedingung prüfen
x = 10

if x > 5:
    print("x ist größer als 5")
# Ausgabe: x ist größer als 5
```
2) If/Else-Anweisung
```python
# Bedingung prüfen und 
# alternative Aktion ausführen
x = 4

if x > 5:
    print("x ist größer als 5")
else:
    print("x ist nicht größer als 5")
# Ausgabe: x ist nicht größer 
# als 5
```
3) If/Elif/Else-Anweisung
```python
# Mehrere Bedingungen prüfen
x = 7

if x > 10:
    print("x ist größer als 10")
elif x == 7:
    print("x ist genau 7")
else:
    print("x ist 10 oder kleiner, aber nicht 7")
# Ausgabe: x ist genau 7
```
4) Verschachtelte If-Anweisung
```python
# Bedingung innerhalb einer Bedingung prüfen
x = 15

if x > 10:
    print("x ist größer als 10")
    if x > 20:
        print("x ist auch größer als 20")
    else:
        print("x ist aber nicht größer als 20")
# Ausgabe: 
# x ist größer als 10
# x ist aber nicht größer als 20
```
📚 **Nützliche Ressourcen**

[W3Schools If Else](https://www.w3schools.com/python/python_conditions.asp) bietet eine Einführung in If/Else-Anweisungen in Python.
"""
}