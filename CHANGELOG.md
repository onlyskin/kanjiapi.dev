# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

- canonicalise api data
    - enables easier partial updates to the live API bucket
    - the response data returned on all API endpoints is now canonicalised,
      meaning all dicts are recursively sorted by key and then by value, and
      most lists are also recursively sorted
    - the lists of glosses under the `/words` endpoints are not sorted as these
      are in rough order of importance in the source data

## [v1]
