from typing import List, Tuple

# -------------------------
# Funciones de similitud Kendall (conteo de inversiones)
# -------------------------
def merge_and_count(A: List[int], B: List[int]) -> Tuple[int, List[int]]:
    count, merged = 0, []
    i, j = 0, 0
    while i < len(A) and j < len(B):
        if A[i] <= B[j]:
            merged.append(A[i])
            i += 1
        else:
            merged.append(B[j])
            count += len(A) - i
            j += 1
    merged.extend(A[i:])
    merged.extend(B[j:])
    return count, merged

def sort_and_count(L: List[int]) -> Tuple[int, List[int]]:
    if len(L) == 1:
        return 0, L
    else:
        rA, A = sort_and_count(L[:len(L) // 2])
        rB, B = sort_and_count(L[len(L) // 2:])
        r, merged = merge_and_count(A, B)
        count = rA + rB + r
        return count, merged

def are_valid(A: List, B: List) -> bool:
    if len(A) != len(B):
        return False
    elements = set(A)
    for b in B:
        if b not in elements:
            return False
    return True

def kendall_similarity(A: List[str], B: List[str]) -> float:
    assert are_valid(A, B)
    position_in_B = {value: index + 1 for index, value in enumerate(B)}
    A_mapped_in_B = [position_in_B[val] for val in A]
    count, _ = sort_and_count(A_mapped_in_B)
    max_inversions = len(A) * (len(A) - 1) / 2
    similarity = 1 - count / max_inversions
    return similarity

# -------------------------
# Agregación de rankings con Borda
# -------------------------
def agregar_rankings_borda(rankings: List[List[str]]) -> List[str]:
    n = len(rankings[0])
    puntajes = {}
    for ranking in rankings:
        for pos, item in enumerate(ranking):
            puntajes[item] = puntajes.get(item, 0) + (n - pos)
    ordenado = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)
    return [item for item, _ in ordenado]

# -------------------------
# Algoritmo FAST-CR modificado para rankings
# -------------------------
def fast_cr(E: List[str], rankings_expertos: List[List[str]], tau: float, eta: int):
    m = len(E)
    ronda = 0
    consenso = 0
    consenso_alcanzado = False
    peliculas = rankings_expertos[0]

    while ronda < eta and not consenso_alcanzado:
        ronda += 1
        print(f"\n--- RONDA {ronda} ---")

        # Ranking agregado
        ranking_colectivo = agregar_rankings_borda(rankings_expertos)
        print(f"Ranking colectivo (Borda): {ranking_colectivo}")

        # Calcular similitudes
        similitudes = []
        for i in range(m):
            sim = kendall_similarity(ranking_colectivo, rankings_expertos[i])
            similitudes.append(sim)
            print(f"Similitud de {E[i]} con el colectivo: {sim:.4f}")

        consenso = sum(similitudes) / m
        print(f"Nivel de consenso actual τ* = {consenso:.4f}")

        if consenso < tau:
            print("\nSugerencias para mejorar consenso:")
            for i in range(m):
                print(f"\n- Para {E[i]}:")
                for peli in peliculas:
                    delta = ranking_colectivo.index(peli) - rankings_expertos[i].index(peli)
                    if delta < 0:
                        print(f"  Sugerencia: Subir prioridad de '{peli}'")
                    elif delta > 0:
                        print(f"  Sugerencia: Bajar prioridad de '{peli}'")
        else:
            consenso_alcanzado = True

    print("\n--- RESULTADO FINAL ---")
    print(f"Ranking final: {ranking_colectivo}")
    print(f"Consenso alcanzado: {consenso_alcanzado} (τ* = {consenso:.4f}, τ requerido = {tau})")

# -------------------------
# Ejecución de prueba de escritorio
# -------------------------
if __name__ == "__main__":
    E = ["José", "Leonardo", "Sebastián", "Antony"]
    ranking_jose = ["Superman", "Los 4 fantásticos", "El viaje de Chihiro", "Formula 1", "El exorcismo"]
    ranking_leonardo = ["Superman", "El viaje de Chihiro", "Formula 1", "Los 4 fantásticos", "El exorcismo"]
    ranking_sebastian = ["El viaje de Chihiro", "Superman", "Los 4 fantásticos", "Formula 1", "El exorcismo"]
    ranking_antony = ["Superman", "El exorcismo", "El viaje de Chihiro", "Formula 1", "Los 4 fantásticos"]

    rankings = [ranking_jose, ranking_leonardo, ranking_sebastian, ranking_antony]
    fast_cr(E, rankings, tau=0.85, eta=3)
