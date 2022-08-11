def regresion_lineal_simple(x, y):
    """
    Parametros:
    x = lista numerica con valores en x
    y = lista numerica con valores en y
    Regresa
    a = coeficiente de a
    b = coeficiente de b
    esto en la funcion a + bx
    ssr = SSR
    sse = SSE
    sst = SST
    fisher = la formula de fisher
    """
    import numpy as np

    x = np.array(x)
    X = np.array([np.ones(x.shape[0]), x])
    n = len(x)
    A = np.matmul(X, X.T)
    A_inv = np.linalg.inv(A)
    ab = np.matmul(np.matmul(A_inv, X), y)
    a, b = ab[0], ab[1]

    yp = a + np.array(b) * x
    y_bar = np.mean(y)
    ssr = ((yp - y_bar) ** 2).sum()
    sse = ((y - yp) ** 2).sum()
    sst = ((y - y_bar) ** 2).sum()

    fisher = ssr / (sse / (n - 2))
    print(
        f"""
        ------------------------
        RESULTADOS
        funcion = {a:.2f} + {b:.2f}x
        ssr = {ssr:.2f}
        sse = {sse:.2f}
        sst = {sst:.2f}
        fisher = {fisher:.2f}
        ------------------------
        """
    )
    return a, b, ssr, sse, sst, fisher
