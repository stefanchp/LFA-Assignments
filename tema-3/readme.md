# Context-Free Grammar (CFG) Processor - LFA Homework 3

Acest proiect implementează diverse funcționalități legate de Gramaticile Libere de Context (CFG). Scriptul este scris în Python și se concentrează pe gramatica `S -> aSb | ε` și pe limbajul `L = {a^n b^n c^n | n >= 1}`.

## Obiective Principale și Implementare

Conform cerințelor din PDF, proiectul abordează următoarele:

*   **Implementarea unui parser pentru CFG:**
    *   Realizat prin funcția recursivă `_parse_recursive` și metoda publică `get_derivation_and_membership`.
*   **Realizarea derivațiilor programatice:**
    *   Codul implementează și afișează **derivații stângi** pentru șirurile membre (Task 3).
    *   *Notă:* Obiectivul din PDF menționa și derivații drepte, care **nu sunt implementate** în versiunea curentă a codului. Parserul utilizează o strategie de derivare stângă.
*   **Generarea de șiruri dintr-o CFG:**
    *   Realizată de funcția `generate_strings` (Task 2).
*   **Testarea apartenenței unui șir la limbajul definit de o CFG:**
    *   Realizată de funcția `get_derivation_and_membership` (Task 4).

## Funcționalități Detaliate

1.  **Task 1: Definirea unei CFG (S -> aSb | ε)**
    *   Gramatica `S -> aSb | ε` este definită programatic prin instanța `cfg_S_aSb_eps`.
    *   Non-terminalele (`S`), terminalele (`a`, `b`), simbolul de start (`S`) și regulile de producție (`S -> aSb`, `S -> ε`) sunt specificate conform cerinței.

2.  **Task 2: Generator de Șiruri**
    *   Funcția `generate_strings(num_strings, max_length, max_recursion_depth)` generează aleatoriu șiruri din CFG-ul `S -> aSb | ε`.
    *   Generează implicit (în `main`) până la 10 șiruri.
    *   Limitează implicit (în `main`) lungimea șirurilor la maxim 10 caractere.
    *   Utilizează funcția ajutătoare `_generate_recursive_string` cu o limită de adâncime a recursivității.

3.  **Task 3: Afișarea Derivației (Stângi)**
    *   Funcția `get_derivation_and_membership(target_string, max_deriv_steps)` returnează calea de **derivație stângă** dacă șirul `target_string` aparține limbajului CFG-ului.
    *   Derivația este prezentată ca o listă de forme sentențiale.

4.  **Task 4: Testarea Apartenenței**
    *   Funcția `get_derivation_and_membership(target_string, max_deriv_steps)` returnează `True` dacă șirul aparține limbajului și `False` în caz contrar.
    *   Funcționează corect pentru șiruri de lungime până la 12 caractere, conform testelor din `main`.

5.  **Task 5: Bonus - Limbajul L = {a^n b^n c^n | n ≥ 1}**
    *   **Clarificare conceptuală:** Limbajul L = {a<sup>n</sup>b<sup>n</sup>c<sup>n</sup> | n ≥ 1} **nu este liber de context**. Acest lucru se demonstrează cu Lema de Pompare pentru Limbaje Libere de Context. O CFG nu poate gestiona cele două dependențe de numărare necesare (numărul de 'b' egal cu 'a', ȘI numărul de 'c' egal cu 'a'/'b'). Prin urmare, **nu se poate scrie o CFG** care să genereze acest limbaj.
    *   **Implementare Recognizer:** În conformitate cu cerința de a "implementa un recognizer", a fost creată funcția `recognize_anbncn(s)`. Aceasta verifică direct dacă un șir de intrare respectă structura a<sup>n</sup>b<sup>n</sup>c<sup>n</sup> (cu n ≥ 1).
    *   Explicația de ce limbajul nu este liber de context este inclusă atât în comentariile din cod, cât și în outputul funcției `main`.

## Cerințe Tehnice

*   Python 3.x
*   Modulul `random` (standard, inclus în Python)
*   Nu sunt utilizate biblioteci externe de parsare.

## Cum se Rulează Programul

1.  Salvați codul furnizat într-un fișier Python (de ex., `LFA-Assignment3.py`).
2.  Deschideți un terminal sau o linie de comandă.
3.  Navigați în directorul unde ați salvat fișierul.
4.  Rulați scriptul folosind comanda:
    ```bash
    python LFA-Assignment3.py
    ```
    Scriptul va executa funcția `main()` și va afișa rezultatele pentru fiecare task în consolă.

## Exemplu de Output

```
--- Task 1: CFG Definition (S -> aSb | ε) ---
Non-terminals: {'S'}
Terminals: {'a', 'b'}  (Ordinea poate varia)
Start Symbol: S
Productions:
  S -> aSb
  S -> ε
----------------------------------------

--- Task 2: String Generator (for S -> aSb | ε) ---
Generated up to 10 strings (max length 10): ['', 'ab', 'aabb', 'aaabbb', 'aaaabbbb', 'aaaaabbbbb']
(Notă: Lista exactă de șiruri generate poate diferi ușor din cauza aleatorietății)
----------------------------------------

--- Task 3 & 4: Derivation and Membership (for S -> aSb | ε) ---

Testing string: '' (length 0)
  Belongs to L(G) (S -> aSb | ε): True
  Derivation: S -> ε

Testing string: 'aabb' (length 4)
  Belongs to L(G) (S -> aSb | ε): True
  Derivation: S -> aSb -> aaSbb -> aabb

Testing string: 'aab' (length 3)
  Belongs to L(G) (S -> aSb | ε): False

Testing string: 'aaaaaabbbbbb' (length 12)
  Belongs to L(G) (S -> aSb | ε): True
  Derivation: S -> aSb -> aaSbb -> aaaSbbb -> aaaaSbbbb -> aaaaaSbbbbb -> aaaaaaSbbbbbb -> aaaaaabbbbbb
(Vor fi afișate și alte cazuri de test pentru Task 3 & 4)
----------------------------------------

--- Task 5: Bonus - Recognizer for L = {a^n b^n c^n | n >= 1} ---
This language L = {a^n b^n c^n | n >= 1} is NOT context-free.
This can be proven using the Pumping Lemma for Context-Free Languages.
A CFG essentially has one 'stack' or counter, but this language requires two linked counts
(the number of 'b's must match 'a's, AND 'c's must match 'a's/'b's).
The following is a direct recognizer, not based on a (non-existent) CFG for this language.
String 'abc': Belongs to L = {a^n b^n c^n | n >= 1}: True
String 'aabbcc': Belongs to L = {a^n b^n c^n | n >= 1}: True
String 'aaabbbccc': Belongs to L = {a^n b^n c^n | n >= 1}: True
String '': Belongs to L = {a^n b^n c^n | n >= 1}: False
String 'aabbc': Belongs to L = {a^n b^n c^n | n >= 1}: False
(Vor fi afișate și alte cazuri de test pentru Task 5)
----------------------------------------
```

## Structura Generală a Codului

*   **Clasa `CFG`**: Conține logica pentru definirea, generarea de șiruri și parsarea CFG-urilor.
    *   `__init__(...)`: Constructor.
    *   `generate_strings(...)` și `_generate_recursive_string(...)`: Pentru Task 2.
    *   `get_derivation_and_membership(...)` și `_parse_recursive(...)`: Pentru Task 3 și Task 4.
*   **`cfg_S_aSb_eps`**: Instanța CFG pentru Task 1.
*   **`recognize_anbncn(s)`**: Funcția pentru Task 5 (Bonus).
*   **`main()`**: Punctul de intrare care demonstrează toate funcționalitățile.
