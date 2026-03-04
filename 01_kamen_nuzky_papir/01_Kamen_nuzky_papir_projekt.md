# Kámen, nůžky, papír – Technická dokumentace

Tento dokument slouží jako podrobný průvodce kódem a strukturou projektu „Kámen, nůžky, papír“ s grafickým rozhraním v Pythonu.

## 1. Popis a cíl projektu
Cílem bylo vytvořit moderní verzi klasické hry s využitím knihovny **Pygame**. Program je navržen tak, aby byl vizuálně atraktivní, intuitivně ovladatelný a technicky správně strukturovaný podle standardů studentské práce.

## 2. Architektura programu
Program využívá **objektově orientované programování (OOP)**. Celá hra je zapouzdřena ve třídě `Game`, což zajišťuje přehlednost a snadnou správu stavu hry (skóre, herní volby).

### Použité technologie:
- **Python 3.14+**: Nejnovější verze interpretu.
- **Pygame-ce**: Komunitní edice knihovny Pygame pro vykreslování grafiky a zpracování událostí.
- **Modul `random`**: Pro generování náhodných tahů počítače.
- **Modul `os`**: Pro bezpečnou práci s cestami k souborům (ikony v `assets`).

---

## 3. Rozbor klíčových částí kódu

### 3.1 Inicializace a nastavení (`__init__`)
V této části nastavujeme okno, fonty a základní proměnné.
```python
def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((800, 600))
    # Definice tlačítek pomocí seznamu slovníků pro snadnou iteraci při vykreslování
    self.buttons = [
        {"id": "rock", "rect": pygame.Rect(100, 420, 180, 140)},
        {"id": "paper", "rect": pygame.Rect(310, 420, 180, 140)},
        {"id": "scissors", "rect": pygame.Rect(520, 420, 180, 140)}
    ]
```
*Proč toto řešení?* Použití `pygame.Rect` nám později umožňuje velmi jednoduše detekovat kolizi myši s tlačítkem.

### 3.2 Herní logika (`play`)
Tato funkce je srdcem hry. Spustí se pokaždé, když hráč klikne na tlačítko.
```python
def play(self, player_choice):
    self.last_player_choice = player_choice
    self.last_computer_choice = random.choice(self.choices)
    
    # Logika vyhodnocení vítěze
    if self.last_player_choice == self.last_computer_choice:
        self.result_text = "Je to remíza!"
    elif (self.last_player_choice == "rock" and self.last_computer_choice == "scissors") or \
         (self.last_player_choice == "paper" and self.last_computer_choice == "rock") or \
         (self.last_player_choice == "scissors" and self.last_computer_choice == "paper"):
        self.result_text = "Vyhrál jsi!"
        self.player_score += 1
    else:
        self.result_text = "Počítač vyhrál!"
        self.computer_score += 1
```
*Vysvětlení:* Počítač si náhodně vybere z listu `["rock", "paper", "scissors"]`. Následně porovnáme volby pomocí podmínek, které pokrývají všechny tři možnosti výhry hráče. V ostatních případech (kromě remízy) vyhrává počítač.

### 3.3 Vykreslovací smyčka (`draw`)
Zde vytváříme grafické rozhraní. Aplikujeme zde tzv. **double buffering** (funkce `pygame.display.flip()`), který zabraňuje blikání obrazu.
- **Zpracování barev**: Používáme moderní hexadecimální převody do RGB (např. tmavé pozadí `(20, 24, 35)`).
- **Hover efekt**: 
```python
is_hovered = btn["rect"].collidepoint(mouse_pos)
color = (ACCENT[0]+20, ACCENT[1]+20, ACCENT[2]+20) if is_hovered else CARD_BG
```
*Vysvětlení:* Pokud se souřadnice myši nacházejí uvnitř obdélníku tlačítka, barva se mírně zesvětlí, což dává uživateli zpětnou vazbu.

---

## 4. Uživatelská příručka
1. **Spuštění**: Spusťte skript `main.py` ve složce projektu.
2. **Průběh**: Uvidíte tři velká tlačítka s ikonami. Kliknutím levým tlačítkem myši provedete svůj tah.
3. **Cíl**: Získejte co nejvyšší skóre. Skóre se ukládá po dobu běhu programu.
4. **Ukončení**: Zavřete okno křížkem v horním rohu.

## 5. Správa aktiv
Obrázky jsou uloženy v podsložce `assets`. Pokud by soubor chyběl (např. smazání uživatelem), kód obsahuje **fallback mechanismus**:
```python
if os.path.exists(path):
    # Načtení reálného obrázku
else:
    # Dynamické vytvoření barevného kruhu jako náhrady
```
To zajišťuje, že program nespadne s chybou `FileNotFoundError`, ale zůstane funkční i v omezeném režimu.
