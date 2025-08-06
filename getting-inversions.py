from typing import List, Tuple


type Inversion = tuple[int, int]


def merge_and_count(A: List, B: List) -> Tuple[List[Inversion], List[int]]:
    i, j = 0, 0
    inversions, merged = [], []

    while i < len(A) and j < len(B):
        if A[i] <= B[j]:
            merged.append(A[i])
            i += 1
        else:
            merged.append(B[j])
            # inversions += len(A) - i
            inversions.extend([(A[k], B[j]) for k in range(i, len(A))])
            j += 1

    merged.extend(A[i:])
    merged.extend(B[j:])

    return inversions, merged


def sort_and_count(L: List) -> Tuple[List[Inversion], List[int]]:
    if len(L) == 1:
        return [], L
    else:
        inversionsL, left = sort_and_count(L[:len(L) // 2])
        inversionsR, right = sort_and_count(L[len(L) // 2:])
        inversionsM, merged = merge_and_count(left, right)
        return inversionsL + inversionsR + inversionsM, merged


def get_inversions(A: List, B: List) -> List[Inversion]:
    assert(len(A) == len(B))
    position_in_B = {val: i for i, val in enumerate(B)}
    A_in_B_space = [position_in_B[x] for x in A]
    inversion_pairs, _ = sort_and_count(A_in_B_space)
    inversions = []

    for i_pos, j_pos in inversion_pairs:
        # Find values in A that had these B-space positions
        i_val = A[[position_in_B[x] for x in A].index(i_pos)]
        j_val = A[[position_in_B[x] for x in A].index(j_pos)]
        inversions.append((i_val, j_val))

    return inversions


def main():
    A = [2, 4, 1, 3, 5] # preference list of A
    B = [1, 2, 3, 4, 5] # preference list of B

    inversions = get_inversions(A, B)
    similarity = 1 - len(inversions) / len(B)

    print(f'A = {A}')
    print(f'B = {B}')
    print('')
    print(f'inversions = {inversions}')
    print(f'similarity(A, B) = {similarity}')


if __name__ == "__main__":
    main()
