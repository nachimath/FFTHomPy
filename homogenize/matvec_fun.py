import numpy as np


def get_inverse(A):
    """
    It calculates the inverse of conductivity coefficients at grid points,
    i.e. of matrix A_GaNi

    Parameters
    ----------
    A : numpy.ndarray

    Returns
    -------
    invA : numpy.ndarray
    """
    B = np.copy(A)
    N = np.array(A.shape[2:])
    d = A.shape[0]
    if A.shape[0] != A.shape[1]:
        raise NotImplementedError("Non-square matrix!")

    invA = np.eye(d).tolist()
    for m in np.arange(d):
        Bdiag = np.copy(B[m][m])
        B[m][m] = np.ones(N)
        for n in np.arange(m+1, d):
            B[m][n] = B[m][n]/Bdiag
        for n in np.arange(d):
            invA[m][n] = invA[m][n]/Bdiag
        for k in np.arange(m+1, d):
            Bnull = np.copy(B[k][m])
            for l in np.arange(d):
                B[k][l] = B[k][l] - B[m][l]*Bnull
                invA[k][l] = invA[k][l] - invA[m][l]*Bnull
    for m in np.arange(d-1, -1, -1):
        for k in np.arange(m-1, -1, -1):
            Bnull = np.copy(B[k][m])
            for l in np.arange(d):
                B[k][l] = B[k][l] - B[m][l]*Bnull
                invA[k][l] = invA[k][l] - invA[m][l]*Bnull
    invA = np.array(invA)
    return invA


def enlarge(xN, M):
    """
    Enlarge an array of Fourier coefficients by zeros.

    Parameters
    ----------
    xN : numpy.ndarray of shape = N
        input array that is to be enlarged

    Returns
    -------
    xM : numpy.ndarray of shape = M
        output array that is enlarged
    M : array like
        number of grid points
    """
    xM = np.zeros(M, dtype=xN.dtype)
    M = np.array(M)
    N = np.array(np.shape(xN))
    if np.allclose(M, N):
        return xN
    dim = np.size(N)
    ibeg = (M-N+(N % 2))/2
    iend = (M+N+(N % 2))/2
    if dim == 2:
        xM[ibeg[0]:iend[0], ibeg[1]:iend[1]] = xN
    elif dim == 3:
        xM[ibeg[0]:iend[0], ibeg[1]:iend[1], ibeg[2]:iend[2]] = xN
    else:
        raise NotImplementedError()
    return xM

def restrict(xN, M):
    """
    Restrict an array making Fourier coefficients by zeros for high frequency.

    Parameters
    ----------
    xN : numpy.ndarray of shape = N
        input array that is to be restricted

    Returns
    -------
    xM : numpy.ndarray of shape = M
        output array that is restricted
    M : array like
        number of grid points
    """
    xM = np.zeros(M, dtype=xN.dtype)
    M = np.array(M)
    N = np.array(np.shape(xN))
    if np.allclose(M, N):
        return xN
    dim = np.size(N)
    ibeg = (N-M+(M % 2))/2
    iend = (N+M+(M % 2))/2
    if dim == 2:
        xM = xN[ibeg[0]:iend[0], ibeg[1]:iend[1]]
    elif dim == 3:
        xN = xM[ibeg[0]:iend[0], ibeg[1]:iend[1], ibeg[2]:iend[2]]
    else:
        raise NotImplementedError()
    return xM

def enlarge_M(xN, M):
    """
    Matrix representation of enlarge function.

    Parameters
    ----------
    xN : numpy.ndarray of shape = (dim, dim) + N
        input matrix that is to be enlarged

    Returns
    -------
    xM : numpy.ndarray of shape = (dim, dim) + M
        output matrix that is enlarged
    M : array like
        number of grid points
    """
    M = np.array(M, dtype=np.int32)
    N = np.array(xN.shape[2:])
    if np.allclose(M, N):
        return xN
    xM = np.zeros(np.hstack([xN.shape[0], xN.shape[1], M]))
    for m in np.arange(xN.shape[0]):
        for n in np.arange(xN.shape[1]):
            xM[m][n] = enlarge(xN[m][n], M)
    return xM


def decrease(xN, M):
    """
    Decreases an array of Fourier coefficients by omitting the highest
    frequencies.

    Parameters
    ----------
    xN : numpy.ndarray of shape = N
        input array that is to be enlarged

    Returns
    -------
    xM : numpy.ndarray of shape = M
        output array that is enlarged
    M : array like
        number of grid points
    """
    M = np.array(M, dtype=np.int32)
    N = np.array(xN.shape, dtype=np.int32)
    dim = N.size
    ibeg = (N-M+(M % 2))/2
    iend = (N+M+(M % 2))/2
    if dim == 2:
        xM = xN[ibeg[0]:iend[0], ibeg[1]:iend[1]]
    elif dim == 3:
        xM = xN[ibeg[0]:iend[0], ibeg[1]:iend[1], ibeg[2]:iend[2]]
    return xM


def get_Nodd(N):
    Nodd = N - ((N + 1) % 2)
    return Nodd
