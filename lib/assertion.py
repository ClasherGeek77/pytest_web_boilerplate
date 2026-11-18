import logging

logger = logging.getLogger(__name__)


# the only place with bare assert, every check is logged as a step
class Assertion:
    def assert_status(self, actual_status, expected_status, detail=""):
        logger.info(
            f"checking HTTP status: got {actual_status}, expected {expected_status}"
        )
        assert actual_status == expected_status, (
            f"HTTP status: actual {actual_status!r} is not equal to expected "
            f"{expected_status!r} {detail}"
        )

    def assert_equal(self, actual_result, expected_result, *, label="value", detail=""):
        logger.info(
            f"checking {label}: got {actual_result}, expected {expected_result}"
        )
        assert actual_result == expected_result, (
            f"{label}: actual {actual_result!r} is not equal to expected "
            f"{expected_result!r} {detail}"
        )

    def assert_is_none(self, actual_result, *, label="value"):
        logger.info(f"checking {label}: got {actual_result}, expected none")
        assert actual_result is None, f"{label}: actual {actual_result!r} is not None"

    # for values the server makes up, like an id or a token, that we cannot predict
    def assert_not_empty(self, actual_result, *, label="value"):
        logger.info(f"checking {label}: got {actual_result}, expected something")
        assert actual_result, f"{label}: actual {actual_result!r} is empty"

    def assert_length(self, actual_array, expected_length, *, label="list"):
        actual_length = len(actual_array)
        logger.info(
            f"checking {label}: got {actual_length}, expected {expected_length}"
        )
        assert (
            actual_length == expected_length
        ), f"{label}: length {actual_length} is not {expected_length}: {actual_array!r}"
