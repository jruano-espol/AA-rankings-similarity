from typing import List, Tuple


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

    merged.extend(A[i:]); merged.extend(B[j:])

    return count, merged


def sort_and_count(L: List[int]) -> int:
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


def get_inversion_count(A: List[str], B: List[str]) -> int:
    assert are_valid(A, B)

    position_in_B = {}
    for index, value in enumerate(B):
        position_in_B[value] = index + 1

    A_mapped_in_B = [0] * len(A)
    for i in range(len(A)):
        A_mapped_in_B[i] = position_in_B[A[i]]

    count, _ = sort_and_count(A_mapped_in_B)
    return count


def main():
    ranking_mio    = ["Superman", "Exorcismo el ritual", "El viaje de Chihiro", "F1", "4 Fantásticos"]
    ranking_modelo = ["F1", "Superman", "El viaje de Chihiro", "4 Fantásticos", "Exorcismo el ritual"]

    count = get_inversion_count(ranking_mio, ranking_modelo)
    similarity = 1 - count / len(ranking_modelo)

    print(f'similitud = {similarity}')


if __name__ == "__main__":
    main()
