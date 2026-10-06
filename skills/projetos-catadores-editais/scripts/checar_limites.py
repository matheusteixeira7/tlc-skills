#!/usr/bin/env python3
"""
Confere o limite de caracteres de cada seção (## Título) de um projeto em Markdown.

Uso:
    python3 checar_limites.py projeto.md limites.json
    python3 checar_limites.py projeto.md limites.json --sem-espacos
    python3 checar_limites.py projeto.md            # só mostra a contagem

limites.json: {"Justificativa": 2000, "Objetivos": 1000}

A contagem ignora a marcação Markdown (**, *, #, |, marcadores de lista)
para refletir o que o avaliador vê no formulário.

Saída: 0 = tudo dentro do limite; 1 = alguma seção estourou ou não foi encontrada.
"""

import json
import re
import sys


def secoes(texto: str) -> dict[str, str]:
    resultado: dict[str, str] = {}
    atual = None
    linhas: list[str] = []
    for linha in texto.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", linha)
        if m and not linha.startswith("###"):
            if atual is not None:
                resultado[atual] = "\n".join(linhas).strip()
            atual = m.group(1).strip()
            linhas = []
        elif atual is not None:
            linhas.append(linha)
    if atual is not None:
        resultado[atual] = "\n".join(linhas).strip()
    return resultado


def limpar(texto: str) -> str:
    texto = re.sub(r"^\s*\|?\s*:?-{3,}.*$", "", texto, flags=re.M)  # separador de tabela
    texto = re.sub(r"^#{1,6}\s+", "", texto, flags=re.M)
    texto = re.sub(r"^\s*([-*+]|\d+\.)\s+", "", texto, flags=re.M)
    texto = texto.replace("**", "").replace("__", "")
    texto = re.sub(r"(?<!\w)[*_](.+?)[*_](?!\w)", r"\1", texto)
    texto = texto.replace("|", " ")
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"\n{2,}", "\n", texto)
    return texto.strip()


def contar(texto: str, sem_espacos: bool) -> int:
    t = limpar(texto)
    if sem_espacos:
        t = re.sub(r"\s", "", t)
    return len(t)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sem_espacos = "--sem-espacos" in sys.argv
    if not args:
        print(__doc__)
        return 1

    with open(args[0], encoding="utf-8") as f:
        partes = secoes(f.read())

    limites: dict[str, int] = {}
    if len(args) > 1:
        with open(args[1], encoding="utf-8") as f:
            limites = json.load(f)

    modo = "sem espaços" if sem_espacos else "com espaços"
    print(f"Contagem de caracteres ({modo})\n")
    falhou = False

    for nome, conteudo in partes.items():
        n = contar(conteudo, sem_espacos)
        if nome in limites:
            lim = limites[nome]
            status = "OK" if n <= lim else f"ESTOUROU em {n - lim}"
            falhou |= n > lim
            print(f"[{status}] {nome}: {n}/{lim}")
        else:
            print(f"[--] {nome}: {n}")

    for nome in limites:
        if nome not in partes:
            falhou = True
            print(f"[FALTA] Seção '{nome}' não encontrada no Markdown (confira o título ##)")

    return 1 if falhou else 0


if __name__ == "__main__":
    sys.exit(main())
