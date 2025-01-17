#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)
"""Implements matrix profile transformation."""

__author__ = ["Markus Löning"]
__all__ = ["MatrixProfileTransformer"]

import pandas as pd
from sktime.transformations.base import _SeriesToSeriesTransformer
from sktime.utils.validation.series import check_series
from sktime.utils.validation._dependencies import _check_soft_dependencies

_check_soft_dependencies("stumpy")

import stumpy  # noqa: E402

# noqa: E501


class MatrixProfileTransformer(_SeriesToSeriesTransformer):
    """Calculate the matrix profile of a time series.

    Takes as input a single time series dataset and returns the matrix profile
    for that time series dataset.

    Parameters
    ----------
    window_length : int

    Examples
    --------
    >>> from sktime.transformations.series.matrix_profile import \
    MatrixProfileTransformer
    >>> from sktime.datasets import load_airline
    >>> y = load_airline()
    >>> transformer = MatrixProfileTransformer()
    >>> y_hat = transformer.fit_transform(y)
    """

    _tags = {"univariate-only": True, "fit-in-transform": True}  # for unit test cases

    def __init__(self, window_length=3):
        self.window_length = window_length
        super(MatrixProfileTransformer, self).__init__()

    def transform(self, Z, X=None):
        """Tranform data.

        Parameters
        ----------
        Z: pandas.Series
            Time series dataset(lets say of length=n)

        Returns
        -------
        Z: pandas.Series
            Matrix Profile of time series as output with length as (n-window_length+1)
        """
        self.check_is_fitted()
        Z = check_series(Z, enforce_univariate=True)
        Z = stumpy.stump(Z, self.window_length)
        return pd.Series(Z[:, 0])
