"""
Tabla hash y sus principales operaciones
CS2023 - Algoritmos y Estructuras de Datos (UTEC)
Autores: Estefano Zárate, Ignacio Álvarez

Preview rápido:    manim -pql hash_table.py HashTableVideo
Render (1080p60):  manim -qh  hash_table.py HashTableVideo
Render (4K):       manim -qk  hash_table.py HashTableVideo

No requiere LaTeX: todo el texto usa Text (Pango).
"""

import math
from manim import *

# ---------------------------------------------------------------- estilo
BG = "#0F1117"
C_KEY = "#FFB454"    # claves
C_IDX = "#7FDBFF"    # índices
C_HASH = "#C792EA"   # funciones hash
C_OK = "#A5E075"     # éxito
C_BAD = "#FF6B6B"    # colisión / error
C_CELL = "#3B4252"   # celdas
C_DEL = "#6C7086"    # tombstone
MONO = "Monospace"   # en Windows puedes cambiarlo por "Consolas"

CODE = 202612345      # código de alumno de ejemplo (AÑO-xx-xxx)


def T(s, size=30, color=WHITE, **kw):
    return Text(s, font_size=size, color=color, **kw)


def M(s, size=26, color=WHITE, **kw):
    return Text(s, font_size=size, color=color, font=MONO, **kw)


def cell(w=0.95, h=0.8):
    return Rectangle(width=w, height=h, stroke_color=GREY_B, stroke_width=2,
                     fill_color=C_CELL, fill_opacity=0.35)


def make_row(n, w=0.95, h=0.8):
    boxes = VGroup(*[cell(w, h) for _ in range(n)]).arrange(RIGHT, buff=0)
    idx = VGroup(*[T(str(i), 20, C_IDX).next_to(b, DOWN, 0.12)
                   for i, b in enumerate(boxes)])
    return boxes, idx


def make_col(n, w=0.8, h=0.62):
    boxes = VGroup(*[cell(w, h) for _ in range(n)]).arrange(DOWN, buff=0)
    idx = VGroup(*[T(str(i), 20, C_IDX).next_to(b, LEFT, 0.15)
                   for i, b in enumerate(boxes)])
    return boxes, idx


# ================================================================ escena
class HashTableVideo(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.intro()
        self.motivacion()
        self.estructura()
        self.funciones_hash()
        self.encadenamiento()
        self.open_addressing()
        self.costos()
        self.rehashing()
        self.grafica_sondeos()
        self.creditos()

    # ---------------------------------------------------------- helpers
    def clear_all(self, rt=0.6):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=rt)

    def header(self, text):
        h = T(text, 34, WHITE, weight=BOLD).to_edge(UP, buff=0.35)
        line = Line(LEFT * 6.6, RIGHT * 6.6, stroke_width=2, color=C_HASH)
        line.next_to(h, DOWN, 0.15)
        self.play(FadeIn(h, shift=DOWN * 0.2), Create(line), run_time=0.6)
        return VGroup(h, line)

    def slide(self, group, hold=2.0):
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in group],
                              lag_ratio=0.3), run_time=0.6 + 0.25 * len(group))
        self.wait(hold)

    # ----------------------------------------------------------- 1 intro
    def intro(self):
        boxes, _ = make_row(8, 0.6, 0.6)
        boxes.set_stroke(C_HASH, 2).to_edge(UP, buff=1.0)
        t1 = T("Tabla hash", 76, C_KEY, weight=BOLD)
        t2 = T("y sus principales operaciones", 40)
        authors = T("Estefano Zárate  ·  Ignacio Álvarez", 32, C_IDX)
        course = T("CS2023 · Algoritmos y Estructuras de Datos · UTEC", 24, GREY_B)
        VGroup(t1, t2, authors, course).arrange(DOWN, buff=0.4).shift(DOWN * 0.4)
        authors.shift(DOWN * 0.3)
        course.shift(DOWN * 0.3)

        self.play(LaggedStart(*[GrowFromCenter(b) for b in boxes], lag_ratio=0.08),
                  run_time=0.8)
        self.play(Write(t1), run_time=1.2)
        self.play(FadeIn(t2, shift=UP * 0.3), FadeIn(authors), FadeIn(course))
        self.wait(2.5)
        self.clear_all()

    # ------------------------------------------------------- 2 motivación
    def motivacion(self):
        self.header("¿Por qué una tabla hash?")
        vals = [202641190, 202687678, 202627094, 202681333, 202689157,
                202611725, 202680906, CODE]
        boxes, idx = make_row(len(vals), 1.6, 0.8)
        VGroup(boxes, idx).move_to(UP * 1.3)
        nums = VGroup(*[T(str(v), 17).move_to(b) for v, b in zip(vals, boxes)])
        self.play(FadeIn(boxes), FadeIn(idx), FadeIn(nums), run_time=0.6)

        ptr = SurroundingRectangle(boxes[0], color=C_KEY, buff=0.04)
        lin = T(f"buscar al alumno {CODE} recorriendo el array: O(n)", 26, C_BAD)
        lin.next_to(boxes, DOWN, 0.7)
        self.play(Create(ptr), FadeIn(lin), run_time=0.4)
        for b in boxes[1:]:
            self.play(ptr.animate.move_to(b), run_time=0.15)
        self.play(boxes[-1].animate.set_fill(C_BAD, 0.4), FadeOut(ptr), run_time=0.3)

        key = T(str(CODE), 30, C_KEY)
        fbox = RoundedRectangle(corner_radius=0.15, width=1.6, height=0.9, color=C_HASH)
        ftxt = M("h(k)", 28, C_HASH).move_to(fbox)
        res = T("índice 7", 30, C_IDX)
        pipe = VGroup(key, VGroup(fbox, ftxt), res).arrange(RIGHT, buff=1.0)
        pipe.move_to(DOWN * 1.4)
        a1 = Arrow(key.get_right(), fbox.get_left(), buff=0.15)
        a2 = Arrow(fbox.get_right(), res.get_left(), buff=0.15)
        self.play(FadeIn(key), Create(fbox), Write(ftxt), run_time=0.6)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(res), run_time=0.6)
        jump = CurvedArrow(res.get_top(), boxes[7].get_bottom() + DOWN * 0.35,
                           angle=-PI / 3, color=C_OK)
        o1 = T("calcular la posición: O(1) en promedio", 28, C_OK)
        o1.to_edge(DOWN, buff=0.45)
        self.play(FadeOut(lin), run_time=0.3)
        self.play(Create(jump), boxes[-1].animate.set_fill(C_OK, 0.6), Write(o1))
        self.wait(2)
        self.clear_all()

    # ------------------------------------------------------ 3 estructura
    def estructura(self):
        self.header("Estructura de la tabla")
        m = 7
        boxes, idx = make_row(m, 1.8, 1.0)
        VGroup(boxes, idx).move_to(UP * 0.6)
        br = Brace(boxes, UP)
        brt = T("array de m = 7 buckets, índices 0 … m − 1", 24).next_to(br, UP, 0.1)
        self.play(LaggedStart(*[GrowFromCenter(b) for b in boxes], lag_ratio=0.08),
                  FadeIn(idx), GrowFromCenter(br), FadeIn(brt), run_time=1.0)

        formula = None
        for k, v in [(CODE, "Estefano"), (202641190, "Ignacio")]:
            i = k % m
            f = M(f"h({k}) = {k} mod {m} = {i}", 26, C_KEY).move_to(DOWN * 1.5)
            item = VGroup(T(str(k), 19), T(v, 17, GREY_B)).arrange(DOWN, buff=0.08)
            item.move_to(DOWN * 2.4)
            if formula is None:
                formula = f
                self.play(Write(f), FadeIn(item), run_time=0.6)
            else:
                self.play(Transform(formula, f), FadeIn(item), run_time=0.5)
            self.play(item.animate.move_to(boxes[i]),
                      boxes[i].animate.set_fill(C_OK, 0.35), run_time=0.7)
            self.wait(0.4)

        alpha = VGroup(
            M("factor de carga  α = n / m = 2 / 7", 28, C_HASH),
            T("más lleno ⇒ más colisiones", 24, GREY_B),
        ).arrange(DOWN, buff=0.2).next_to(formula, DOWN, 0.4)
        self.slide(alpha, 2.0)
        self.clear_all()

    # --------------------------------------------------- 4 funciones hash
    def funciones_hash(self):
        hdr = self.header("Funciones hash")
        cur = VGroup()

        def show(group, hold=2.5):
            nonlocal cur
            if len(cur):
                self.play(FadeOut(cur), run_time=0.4)
            group.next_to(hdr, DOWN, 0.5)
            self.slide(group, hold)
            cur = group

        # división
        k = CODE
        bits = format(k, "b")
        brow = VGroup(*[M(b, 24, C_BAD if j >= len(bits) - 3 else GREY_A)
                        for j, b in enumerate(bits)]).arrange(RIGHT, buff=0.06)
        bline = VGroup(M(f"{k} = ", 24), brow).arrange(RIGHT)
        g = VGroup(
            T("1. División", 32, C_KEY),
            M("h(k) = k mod m", 34, C_HASH),
            M(f"h({k}) = {k} mod 7 = {k % 7}", 28, C_OK),
            bline,
            T(f"con m = 8: k mod 8 = {k & 7} → solo usa los 3 bits bajos ⇒ m primo",
              24, C_BAD),
        ).arrange(DOWN, buff=0.35)
        show(g, 3.5)

        # ¿y si solo usamos el año?
        sample = [CODE, 202641190, 202687678]
        rows = VGroup()
        for c in sample:
            sc = str(c)
            r = VGroup(M(sc[:4], 30, C_BAD), M(sc[4:], 30, GREY_D)).arrange(RIGHT, buff=0.05)
            rows.add(r)
        rows.arrange(DOWN, buff=0.3)
        target = VGroup(
            M(f"h = 2026 mod 7 = {2026 % 7}", 28, C_BAD),
            T(f"¡todos al bucket {2026 % 7}!", 28, C_BAD),
        ).arrange(DOWN, buff=0.2)
        body = VGroup(rows, target).arrange(RIGHT, buff=2.2)
        g = VGroup(T("Error común: usar solo el año del código", 32, C_KEY), body,
                   T("Todos los alumnos 2026 colisionan ⇒ la función debe usar TODA la clave",
                     24, GREY_B)).arrange(DOWN, buff=0.5)
        self.play(FadeOut(cur), run_time=0.4)
        g.next_to(hdr, DOWN, 0.5)
        self.play(FadeIn(g[0]), FadeIn(rows), run_time=0.6)
        arrs = VGroup(*[Arrow(r.get_right(), target.get_left(), buff=0.2, stroke_width=3,
                              color=C_BAD) for r in rows])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.2),
                  FadeIn(target), run_time=0.9)
        self.play(FadeIn(g[2]), run_time=0.4)
        self.wait(2.5)
        cur = VGroup(g, arrs)

        # Knuth + Fibonacci
        A = (math.sqrt(5) - 1) / 2
        m = 16
        fr = (k * A) % 1
        h = math.floor(m * fr)
        C = 2654435769
        prod = (k * C) & 0xFFFFFFFF
        hf = prod >> 28
        g = VGroup(
            T("2. Multiplicativo de Knuth", 32, C_KEY),
            M("h(k) = ⌊ m · frac(k · A) ⌋ ,   A = (√5 − 1)/2 ≈ 0.618", 26, C_HASH),
            M(f"h({k}) = ⌊16 · {fr:.4f}⌋ = {h}", 26, C_OK),
            T("Versión entera (Fibonacci hashing), m = 2ᵖ:", 26, C_KEY),
            M("h(k) = (k · 2654435769 mod 2³²) >> (32 − p)", 26, C_HASH),
            M(f"h({k}) = {hf}   (p = 4)   ·   2654435769 ≈ 2³² / φ", 24, C_OK),
            T("Sin divisiones: 1 multiplicación + 1 shift", 24, GREY_B),
        ).arrange(DOWN, buff=0.28)
        show(g, 4.5)

        # industria (visual)
        self.play(FadeOut(cur), run_time=0.4)
        title = T("3. En la industria", 32, C_KEY).next_to(hdr, DOWN, 0.45)
        key = VGroup(RoundedRectangle(corner_radius=0.15, width=1.8, height=0.9,
                                      color=C_KEY, fill_color=C_KEY, fill_opacity=0.12),
                     M("clave k", 26, C_KEY))
        key[1].move_to(key[0])
        key.move_to(LEFT * 5 + DOWN * 0.7)
        specs = [
            ("PostgreSQL", "hash_any()", "lookup3 (Bob Jenkins)"),
            ("Java HashMap", "h ^ (h >>> 16)", "mezcla bits altos y bajos"),
            ("C++ unordered_map", "std::hash<int>(k) = k", "índice = k mod m (m primo)"),
        ]
        boxes = VGroup()
        for name, fn, note in specs:
            r = RoundedRectangle(corner_radius=0.15, width=4.2, height=1.05,
                                 color=C_HASH)
            t1 = T(name, 24, WHITE, weight=BOLD)
            t2 = M(fn, 20, C_HASH)
            VGroup(t1, t2).arrange(DOWN, buff=0.1).move_to(r)
            n = T(note, 22, GREY_B).next_to(r, RIGHT, 0.45)
            boxes.add(VGroup(r, t1, t2, n))
        boxes.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 1.3 + DOWN * 0.7)
        arrows = VGroup(*[Arrow(key.get_right(), b[0].get_left(), buff=0.15,
                                stroke_width=3, color=GREY_A) for b in boxes])
        self.play(FadeIn(title), FadeIn(key, scale=0.8), run_time=0.5)
        for a, b in zip(arrows, boxes):
            self.play(GrowArrow(a), FadeIn(b[:3]), run_time=0.5)
            self.play(FadeIn(b[3], shift=LEFT * 0.2), run_time=0.35)
        self.wait(3.5)
        self.clear_all()

    # ------------------------------------------------- 5 encadenamiento
    def encadenamiento(self):
        hdr = self.header("Colisiones (1): encadenamiento")
        m = 7
        boxes, idx = make_col(m)
        VGroup(boxes, idx).to_edge(LEFT, buff=1.0).shift(DOWN * 0.4)
        nulls = VGroup(*[M("∅", 20, GREY_D).move_to(b) for b in boxes])
        self.play(FadeIn(boxes), FadeIn(idx), FadeIn(nulls), run_time=0.6)

        def pos(i, j):
            b = boxes[i]
            return np.array([b.get_right()[0] + 1.05 + j * 1.85, b.get_center()[1], 0])

        NW = 1.5

        def node(k):
            r = RoundedRectangle(corner_radius=0.1, width=NW, height=0.5,
                                 color=C_KEY, fill_color=C_KEY, fill_opacity=0.15)
            return VGroup(r, T(str(k), 18))

        chains = {i: [] for i in range(m)}
        arrows = {i: VGroup() for i in range(m)}

        def build_arrows(i):
            ar = VGroup()
            prev = boxes[i].get_right()
            for j, _ in enumerate(chains[i]):
                p = pos(i, j)
                ar.add(Arrow(prev, p + LEFT * NW / 2, buff=0.05, stroke_width=3,
                             max_tip_length_to_length_ratio=0.3, color=GREY_A))
                prev = p + RIGHT * NW / 2
            return ar

        sub = T("Dos claves distintas pueden caer en el mismo bucket", 24, GREY_B)
        sub.next_to(hdr, DOWN, 0.3)
        self.play(FadeIn(sub), run_time=0.4)

        formula = None
        for k in [CODE, 202681333, 202627094, 202687678, 202672135]:
            i = k % m
            f = M(f"{k} mod 7 = {i}", 26, C_KEY)
            f.move_to(RIGHT * 3.6 + UP * 1.3)
            if formula is None:
                formula = f
                self.play(Write(f), run_time=0.4)
            else:
                self.play(Transform(formula, f), run_time=0.35)
            nd = node(k).move_to(pos(i, 0))
            anims = [n.animate.move_to(pos(i, j + 1)) for j, n in enumerate(chains[i])]
            if len(arrows[i]):
                anims.append(FadeOut(arrows[i]))
            if not chains[i]:
                anims.append(FadeOut(nulls[i]))
            collide = bool(chains[i])
            chains[i].insert(0, nd)
            self.play(Indicate(boxes[i], color=C_BAD if collide else C_KEY),
                      run_time=0.35)
            new_ar = build_arrows(i)
            self.play(*anims, FadeIn(nd, shift=LEFT * 0.3), run_time=0.5)
            self.play(Create(new_ar), run_time=0.3)
            arrows[i] = new_ar
            if collide:
                col = T("¡colisión! → se inserta al inicio de la lista", 22, C_BAD)
                col.next_to(formula, DOWN, 0.25)
                self.play(FadeIn(col), run_time=0.3)
                self.wait(0.5)
                self.play(FadeOut(col), run_time=0.25)

        side = VGroup(
            T("Insertar (al inicio): O(1)", 26, C_OK),
            T("Buscar / eliminar: O(1 + α)", 26, C_KEY),
            T("α = longitud media de cada lista", 22, GREY_B),
            T("Así funciona std::unordered_map (C++)", 22, C_IDX),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.6 + DOWN * 0.6)
        self.slide(side, 2.5)
        self.clear_all()

    # ------------------------------------------------ 6 open addressing
    def open_addressing(self):
        self.header("Colisiones (2): direccionamiento abierto")
        m = 10
        boxes, idx = make_row(m, 1.25, 0.85)
        VGroup(boxes, idx).move_to(UP * 1.2)
        f = M("Sondeo lineal:  h(k, i) = (h(k) + i) mod m", 28, C_HASH)
        f.next_to(boxes, UP, 0.5)
        self.play(FadeIn(boxes), FadeIn(idx), Write(f), run_time=0.7)

        table = [None] * m
        texts = [None] * m
        ptr = SurroundingRectangle(boxes[0], color=C_KEY, buff=0.04)
        info = T("", 26).move_to(DOWN * 0.5)
        first = True
        for k in [CODE, 202672135, 202611725, 202680906]:
            ni = T(f"insertar {k}:  h = {k % m}", 26, C_KEY).move_to(DOWN * 0.5)
            self.play(Transform(info, ni), run_time=0.3)
            i = 0
            while True:
                j = (k % m + i) % m
                if first:
                    ptr.move_to(boxes[j])
                    self.play(Create(ptr), run_time=0.25)
                    first = False
                else:
                    self.play(ptr.animate.move_to(boxes[j]), run_time=0.25)
                if table[j] is None:
                    t = T(str(k), 13).move_to(boxes[j])
                    table[j], texts[j] = k, t
                    self.play(FadeIn(t, scale=0.7),
                              boxes[j].animate.set_fill(C_OK, 0.35), run_time=0.35)
                    break
                self.play(boxes[j].animate.set_fill(C_BAD, 0.7),
                          rate_func=there_and_back, run_time=0.3)
                i += 1
        self.play(FadeOut(ptr), FadeOut(info), run_time=0.3)

        br = Brace(VGroup(*boxes[5:9]), DOWN, buff=0.45)
        brt = T("cluster primario: 202680906 tenía h = 6 y terminó en 8", 22, C_BAD)
        brt.next_to(br, DOWN, 0.1).align_to(boxes, RIGHT)
        alt = VGroup(
            M("Cuadrático:    (h(k) + i²) mod m", 22, C_HASH),
            M("Doble hashing: (h₁(k) + i·h₂(k)) mod m", 22, C_HASH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        altt = T("→ reducen el clustering", 22, GREY_B).next_to(alt, RIGHT, 0.3)
        VGroup(alt, altt).next_to(brt, DOWN, 0.45).set_x(0)
        self.play(GrowFromCenter(br), FadeIn(brt), run_time=0.5)
        self.wait(1.2)
        self.play(FadeIn(alt), FadeIn(altt), run_time=0.5)
        self.wait(2.5)
        self.play(FadeOut(VGroup(br, brt, alt, altt)), run_time=0.4)

        # eliminar con tombstone
        f2 = T("Eliminar: no se vacía la celda, se marca un tombstone (DEL)",
               26, C_KEY).move_to(f)
        self.play(Transform(f, f2), run_time=0.5)
        dl = M("DEL", 22).move_to(boxes[6])
        self.play(Transform(texts[6], dl), boxes[6].animate.set_fill(C_DEL, 0.8),
                  run_time=0.5)
        ptr = SurroundingRectangle(boxes[5], color=C_IDX, buff=0.04)
        info = T("buscar(202611725):  5 → 6 (DEL, continuar) → 7 ✔", 26, C_IDX)
        info.move_to(DOWN * 0.5)
        self.play(Create(ptr), FadeIn(info), run_time=0.4)
        self.play(ptr.animate.move_to(boxes[6]), run_time=0.4)
        self.play(ptr.animate.move_to(boxes[7]), run_time=0.4)
        self.play(boxes[7].animate.set_fill(C_OK, 0.8), ptr.animate.set_color(C_OK),
                  run_time=0.3)
        why = T("Si la celda 6 quedara vacía, la búsqueda se detendría ahí ✘", 24, C_BAD)
        why.move_to(DOWN * 1.6)
        self.play(FadeIn(why), run_time=0.4)
        self.wait(2.5)
        self.clear_all()

    # --------------------------------------------------------- 7 costos
    def costos(self):
        hdr = self.header("Costo de las operaciones")
        data = [
            ["Operación", "Promedio", "Peor caso"],
            ["Insertar", "O(1)", "O(n)"],
            ["Buscar", "O(1 + α)", "O(n)"],
            ["Eliminar", "O(1 + α)", "O(n)"],
        ]
        colw = [3.0, 3.0, 2.6]
        rh = 0.75
        grid = VGroup()
        y0 = 1.3
        for r, row in enumerate(data):
            x = -sum(colw) / 2
            for c, txt in enumerate(row):
                color = WHITE if r == 0 else [WHITE, C_OK, C_BAD][c]
                cr = Rectangle(width=colw[c], height=rh, stroke_color=GREY_D,
                               stroke_width=1.5,
                               fill_color=C_HASH if r == 0 else C_CELL,
                               fill_opacity=0.35 if r == 0 else 0.15)
                cr.move_to([x + colw[c] / 2, y0 - r * rh, 0])
                t = T(txt, 28, color, weight=BOLD if r == 0 else NORMAL).move_to(cr)
                grid.add(VGroup(cr, t))
                x += colw[c]
        self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.06),
                  run_time=1.5)
        foot = T("Peor caso: todas las claves en el mismo bucket (hash malo o ataque)",
                 24, C_BAD).next_to(grid, DOWN, 0.5)
        self.play(FadeIn(foot), run_time=0.4)
        self.wait(3)
        self.clear_all()

    # --------------------------------------------------- 8 rehashing
    def rehashing(self):
        self.header("Rehashing: crecer cuando α supera el máximo")
        m_old, m_new = 5, 11
        old, oidx = make_row(m_old, 1.3, 0.75)
        VGroup(old, oidx).move_to(UP * 1.35 + LEFT * 3.1)
        ol = T(f"m = {m_old}", 22, GREY_B).next_to(old, UP, 0.15).align_to(old, LEFT)
        keys = [CODE, 202687678, 202627094, 202689157, 202687476]
        ktx = [T(str(k), 13).move_to(old[k % m_old]) for k in keys]
        a1 = VGroup(
            M("α = 5/5 = 1.0", 26, C_KEY),
            M("C++: max_load_factor() = 1.0", 22, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(old, RIGHT, 0.6)
        self.play(FadeIn(old), FadeIn(oidx), FadeIn(ol), *[FadeIn(t) for t in ktx],
                  FadeIn(a1), run_time=0.8)
        new_key = 202641190
        ins = T(f"insertar {new_key} → α = 6/5 > 1.0  ⇒  rehash: m = primo ≥ 2m = 11",
                24, C_BAD).move_to(UP * 0.1)
        self.play(Write(ins), run_time=0.8)

        new, nidx = make_row(m_new, 1.17, 0.75)
        VGroup(new, nidx).move_to(DOWN * 1.35)
        nl = T(f"m = {m_new}", 22, GREY_B).next_to(new, UP, 0.15).align_to(new, LEFT)
        self.play(FadeIn(new), FadeIn(nidx), FadeIn(nl), run_time=0.5)
        self.play(*[t.copy().animate.move_to(new[k % m_new]) for k, t in zip(keys, ktx)],
                  *[new[k % m_new].animate.set_fill(C_OK, 0.3) for k in keys],
                  run_time=1.0)
        tn = T(str(new_key), 13, C_KEY).move_to(new[new_key % m_new])
        self.play(FadeIn(tn, scale=0.6), new[new_key % m_new].animate.set_fill(C_KEY, 0.35),
                  run_time=0.4)
        am = T("Cuesta O(n), pero ocurre pocas veces ⇒ O(1) amortizado por inserción",
               24, C_HASH).next_to(nidx, DOWN, 0.5)
        self.play(FadeIn(am), run_time=0.4)
        self.wait(2.5)
        self.clear_all()

    # --------------------------------------------- 9 gráfica sondeos
    def grafica_sondeos(self):
        hdr = self.header("¿Cuál conviene? Sondeos esperados vs α")
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 12, 4], x_length=7.5,
                  y_length=4.4, tips=False, axis_config={"color": GREY_B})
        ax.next_to(hdr, DOWN, 0.6).shift(LEFT * 2.0)
        xl = VGroup(*[T(f"{x:g}", 18, GREY_B).next_to(ax.c2p(x, 0), DOWN, 0.15)
                      for x in [0, 0.25, 0.5, 0.75, 1]])
        yl = VGroup(*[T(str(y), 18, GREY_B).next_to(ax.c2p(0, y), LEFT, 0.15)
                      for y in [0, 4, 8, 12]])
        xt = T("factor de carga α", 20).next_to(ax, DOWN, 0.5)
        yt = T("sondeos (búsqueda fallida)", 20).next_to(ax, UP, 0.1).align_to(ax, LEFT)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(xt), FadeIn(yt),
                  run_time=0.8)

        c_chain = ax.plot(lambda a: 1 + a, x_range=[0, 0.99], color=C_OK,
                          stroke_width=4)
        c_lin = ax.plot(lambda a: 0.5 * (1 + 1 / (1 - a) ** 2), x_range=[0, 0.79],
                        color=C_BAD, stroke_width=4)
        legend = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=C_OK, stroke_width=5),
                   T("Encadenamiento: 1 + α", 22)),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=C_BAD, stroke_width=5),
                   T("Sondeo lineal: ½(1 + 1/(1−α)²)", 22)),
        )
        for l in legend:
            l.arrange(RIGHT, buff=0.2)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        legend.shift(UP * 0.8)
        for c, l in zip([c_chain, c_lin], legend):
            self.play(Create(c), FadeIn(l), run_time=1.1)
        v = DashedLine(ax.c2p(0.75, 0), ax.c2p(0.75, 12), color=C_KEY)
        vt = T("α = 0.75", 20, C_KEY).next_to(v, UP, 0.1)
        self.play(Create(v), FadeIn(vt), run_time=0.5)
        concl = VGroup(
            T("Open addressing: más rápido", 22, C_KEY),
            T("en caché, pero exige α bajo", 22, C_KEY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(legend, DOWN, 0.6)
        concl.align_to(legend, LEFT)
        self.play(FadeIn(concl), run_time=0.4)
        self.wait(2.5)
        self.clear_all()

    # --------------------------------------------------- 10 créditos
    def creditos(self):
        credits = VGroup(
            T("Tabla hash y sus principales operaciones", 40, C_KEY, weight=BOLD),
            T("Autores", 26, GREY_B),
            T("Estefano Zárate", 34, C_IDX),
            T("Ignacio Álvarez", 34, C_IDX),
            T("CS2023 · Algoritmos y Estructuras de Datos · UTEC · 2026", 22, GREY_B),
            T("Animado con Manim Community", 22, C_HASH),
        ).arrange(DOWN, buff=0.35)
        self.slide(credits, 2.5)
        self.play(FadeOut(credits), run_time=0.8)
