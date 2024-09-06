from typing import List

from io_util.read_until import read_until


def read_natural_or_zero_number_of(what: str, maximum: int) -> int:
    def f(inp: str):
        try:
            n = int(inp)
        except ValueError:
            return False
        return 0 <= n <= maximum

    return int(
        read_until(
            f'Input number of {what}: ',
            f'There is no such number of products (available: {maximum})',
            f
        )
    )


def read_product(product_number: str, products: List[str]) -> str:
    return read_until(
        f'Input {product_number} product: ',
        'There is no such product',
        lambda product:
            product in products
    )


def read_products(of_what: str, products: List[str]) -> List[str]:
    return [
        read_product(f'{i + 1}', products)
        for i in range(
            read_natural_or_zero_number_of(of_what, len(products))
        )
    ]
