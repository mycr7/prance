# -*- coding: utf-8 -*-
"""Test suite focusing on validation backend features."""

__author__ = 'Jens Finkhaeuser'
__copyright__ = 'Copyright (c) 2018 Jens Finkhaeuser'
__license__ = 'MIT +no-false-attribs'
__all__ = ()

import pytest

from prance import BaseParser
from prance import ValidationError
from prance.util import validation_backends

from . import run_if_present

def test_bad_backend():
  with pytest.raises(ValueError):
    BaseParser('tests/specs/petstore.yaml', backend = 'does_not_exist')


@run_if_present('flex')
def test_flex_issue_5_integer_keys():
  # Must succeed with default (flex) parser; note the parser does not stringify the response code
  parser = BaseParser('tests/specs/issue_5.yaml', backend = 'flex')
  assert 200 in parser.specification['paths']['/test']['post']['responses']


@run_if_present('flex')
def test_flex_validate_success():
  parser = BaseParser('tests/specs/petstore.yaml', backend = 'flex')


@run_if_present('flex')
def test_flex_validate_failure():
  with pytest.raises(ValidationError):
    parser = BaseParser('tests/specs/missing_reference.yaml', backend = 'flex')


@run_if_present('swagger_spec_validator')
def test_swagger_spec_validator_issue_5_integer_keys():
  # Must fail in implicit strict mode.
  with pytest.raises(ValidationError):
    BaseParser('tests/specs/issue_5.yaml', backend = 'swagger-spec-validator')

  # Must fail in explicit strict mode.
  with pytest.raises(ValidationError):
    BaseParser('tests/specs/issue_5.yaml', backend = 'swagger-spec-validator', strict = True)

  # Must succeed in non-strict/lenient mode
  parser = BaseParser('tests/specs/issue_5.yaml', backend = 'swagger-spec-validator', strict = False)
  assert '200' in parser.specification['paths']['/test']['post']['responses']


@run_if_present('swagger_spec_validator')
def test_swagger_spec_validator_validate_success():
  parser = BaseParser('tests/specs/petstore.yaml', backend = 'swagger-spec-validator')


@run_if_present('swagger_spec_validator')
def test_swagger_spec_validator_validate_failure():
  with pytest.raises(ValidationError):
    parser = BaseParser('tests/specs/missing_reference.yaml', backend = 'swagger-spec-validator')


@run_if_present('openapi_spec_validator')
def test_openapi_spec_validator_issue_5_integer_keys():
  # Must fail in implicit strict mode.
  with pytest.raises(ValidationError):
    BaseParser('tests/specs/issue_5.yaml', backend = 'openapi-spec-validator')

  # Must fail in explicit strict mode.
  with pytest.raises(ValidationError):
    BaseParser('tests/specs/issue_5.yaml', backend = 'openapi-spec-validator', strict = True)

  # Must succeed in non-strict/lenient mode
  parser = BaseParser('tests/specs/issue_5.yaml', backend = 'openapi-spec-validator', strict = False)
  assert '200' in parser.specification['paths']['/test']['post']['responses']


@run_if_present('openapi_spec_validator')
def test_openapi_spec_validator_validate_success():
  parser = BaseParser('tests/specs/petstore.yaml', backend = 'openapi-spec-validator')


@run_if_present('openapi_spec_validator')
def test_openapi_spec_validator_validate_failure():
  with pytest.raises(ValidationError):
    parser = BaseParser('tests/specs/missing_reference.yaml', backend = 'openapi-spec-validator')


@run_if_present('openapi_spec_validator')
def test_openapi_spec_validator_issue_20_spec_version_handling():
  # The spec is OpenAPI 3, but broken. Need to set 'strict' to False to stringify keys
  with pytest.raises(ValidationError):
    parser = BaseParser('tests/specs/issue_20.yaml', backend = 'openapi-spec-validator', strict = False)

  # Lazy parsing should let us validate what's happening
  parser = BaseParser('tests/specs/issue_20.yaml', backend = 'openapi-spec-validator', strict = False, lazy = True)
  assert not parser.valid
  assert parser.version_parsed == ()

  with pytest.raises(ValidationError):
    parser.parse()

  # After parsing, the specs are not valid, but the correct version is
  # detected.
  assert not parser.valid
  assert parser.version_parsed == (3, 0, 0)
