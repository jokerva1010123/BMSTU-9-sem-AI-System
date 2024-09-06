def flat_map(f, xs):
    return [y for ys in xs for y in f(ys)]
