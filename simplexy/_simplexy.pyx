from __future__ import division

cimport cython
from libc.stdlib cimport malloc, free

import numpy as np
cimport numpy as np
np.import_array()

DTYPE = np.float32
ctypedef np.float32_t DTYPE_t

cdef extern from "simplexy.h":
    cdef float NUM_INT_TIME
    cdef float SIMPLEXY_DEFAULT_DPSF
    cdef float SIMPLEXY_DEFAULT_PLIM
    cdef float SIMPLEXY_DEFAULT_DLIM
    cdef float SIMPLEXY_DEFAULT_SADDLE
    cdef int SIMPLEXY_DEFAULT_MAXPER
    cdef int SIMPLEXY_DEFAULT_MAXNPEAKS
    cdef int SIMPLEXY_DEFAULT_MAXSIZE
    cdef int SIMPLEXY_DEFAULT_HALFBOX

    struct simplexy_t:
        #
        #  INPUTS
        #
        float *image
        unsigned char* image_u8
        int nx
        int ny
        # gaussian psf width (sigma, not FWHM) */
        float dpsf
        # significance to keep */
        float plim
        # closest two peaks can be */
        float dlim
        # saddle difference (in sig) */
        float saddle
        # maximum number of peaks per object */
        int maxper
        # maximum number of peaks total */
        int maxnpeaks
        # maximum size for extended objects */
        int maxsize
        # size for sliding sky estimation box */
        int halfbox

        # (boolean) don't do background subtraction.
        int nobgsub

        # global background.
        float globalbg

        # (boolean) invert the image before processing (for black-on-white images)
        int invert

        # If set to non-zero, the given sigma value will be used
        # otherwise a value will be estimated.
        float sigma

        #
        #  OUTPUTS
        #
        float *x
        float *y
        float *flux
        float *background
        int npeaks

        # Lanczos-interpolated flux and backgrounds
        # measured if Lorder > 0.
        int Lorder
        float* fluxL
        float* backgroundL

        #
        #  DEBUG
        #

        # The filename for saving the background-subtracted FITS image.
        const char* bgimgfn
        const char* maskimgfn
        const char* blobimgfn
        const char* bgsubimgfn
        const char* smoothimgfn
    ctypedef simplexy_t simplexy_t

    cdef void simplexy_set_defaults(simplexy_t* s)
    cdef void simplexy_free_contents(simplexy_t* s)
    cdef int simplexy_run(simplexy_t* s)


def simplexy(np.ndarray[DTYPE_t, ndim=2, mode="c"] img not None,
             float dpsf=SIMPLEXY_DEFAULT_DPSF,
             float plim=SIMPLEXY_DEFAULT_PLIM,
             float dlim=SIMPLEXY_DEFAULT_DLIM,
             float saddle=SIMPLEXY_DEFAULT_SADDLE,
             int maxper=SIMPLEXY_DEFAULT_MAXPER,
             int maxnpeaks=SIMPLEXY_DEFAULT_MAXNPEAKS,
             int maxsize=SIMPLEXY_DEFAULT_MAXSIZE,
             int halfbox=SIMPLEXY_DEFAULT_HALFBOX):
    cdef simplexy_t* s = <simplexy_t*>malloc(sizeof(simplexy_t))
    simplexy_set_defaults(s)

    # Set up the solver.
    s.image = <float*>img.data
    s.nx = img.shape[1]
    s.ny = img.shape[0]
    s.dpsf = dpsf
    s.plim = plim
    s.dlim = dlim
    s.saddle = saddle
    s.maxper = maxper
    s.maxsize = maxsize
    s.maxnpeaks = maxnpeaks
    s.halfbox = halfbox

    # Run simplexy.
    cdef int flag = simplexy_run(s)

    # Build the results.
    cdef int i
    cdef np.ndarray[DTYPE_t, ndim=2, mode="c"] results = \
            np.empty((s.npeaks, 4), dtype=DTYPE)
    for i in range(s.npeaks):
        results[i, 0] = s.x[i]
        results[i, 1] = s.y[i]
        results[i, 2] = s.flux[i]
        results[i, 3] = s.background[i]

    # Don't deallocate the image pointer.
    s.image = NULL

    # Clean up.
    simplexy_free_contents(s)
    free(s)

    if not flag:
        raise RuntimeError("simplexy_run failed")

    return results
