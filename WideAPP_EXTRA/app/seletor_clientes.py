# -*- coding: utf-8 -*-
"""Resumo de selecao antes de gerar relatorios."""


def resumir_selecao(registros):
    sem_contrato = [r for r in registros if r.get("contrato") != "Encontrado"]
    divergentes = [r for r in registros if r.get("divergencias")]
    pendentes = [r for r in registros if "pendente" in (r.get("status", "").lower())]
    linhas = [
        f"Quantidade selecionada: {len(registros)}",
        "",
        "Clientes/lotes:",
    ]
    for item in registros:
        linhas.append(
            f"- {item.get('cliente')} | Lote {item.get('lote')} | "
            f"Contrato: {item.get('contrato')} | Status: {item.get('status')}"
        )
    linhas.extend(
        [
            "",
            f"Pendentes: {len(pendentes)}",
            f"Sem contrato confirmado: {len(sem_contrato)}",
            f"Com divergencia: {len(divergentes)}",
        ]
    )
    return "\n".join(linhas)
