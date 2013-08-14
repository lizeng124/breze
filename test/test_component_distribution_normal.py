# -*- coding: utf-8 -*-

import numpy as np
import theano
import theano.tensor as T

from breze.component.distributions import normal


def test_pdf_compare_logpdf():
    theano.config.compute_test_value = 'raise'
    sample = T.matrix()
    sample.tag.test_value = np.random.random((10, 5))
    mean = T.vector()
    mean.tag.test_value = np.empty(5)
    cov = T.matrix()
    cov.tag.test_value = np.random.random((5, 5))

    density = normal.pdf(sample, mean, cov)
    log_density = normal.logpdf(sample, mean, cov)

    f_density = theano.function([sample, mean, cov], density)
    f_logdensity = theano.function([sample, mean, cov], log_density)

    some_sample = np.random.random((20, 5))
    some_mean = np.array([1., 2., 3., 4., 5.])
    w = np.random.random((5, 5))
    some_cov = np.dot(w, w.T) + np.eye(5)

    d = f_density(some_sample, some_mean, some_cov)
    log_d = f_logdensity(some_sample, some_mean, some_cov)

    #print np.log(d), log_d
    #print  (np.log(d) - log_d).tolist()

    assert np.allclose(np.log(d), log_d)
