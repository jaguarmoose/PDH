from pdh import adnod


def build_nodes(max_i=5, max_j=4, max_k=29, root="1"):
    """Create a tree of nodes under the given root string."""
    i = 0
    while i < max_i:
        i += 1
        ns = f"{root}:{i}"
        adnod.adnod(ns)
        print(ns)
        j = 0
        while j < max_j:
            j += 1
            ns = f"{root}:{i}:{j}"
            print(ns)
            adnod.adnod(ns)
            k = 0
            while k < max_k:
                k += 1
                ns = f"{root}:{i}:{j}:{k}"
                print(ns)
                adnod.adnod(ns)


def main():
    """Run the node creation with default parameters."""
    build_nodes()


if __name__ == "__main__":
    main()
