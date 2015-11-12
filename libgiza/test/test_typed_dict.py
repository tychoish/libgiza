"""
A collection of tests of the TypedDict specialized dictionary type which allows
us to specify types for of the the keys and values of a dictionary along with
validation methods to validate input on creation.

These tests ensure that TypedDicts behave as expected, which is to say, like
"vanilla" dicts, but that they also enforce their validation requirements (when
implemented.) and type checking (always.)
"""
import datetime
import itertools
import sys
import unittest

import libgiza.typed_dict

if sys.version_info >= (3, 0):
    basestring = str


class TestTypedDictionaryObjectCreation(unittest.TestCase):
    def test_object_creation_returns_correctly_typed_values(self):
        d = libgiza.typed_dict.TypedDict(key_type=basestring,
                                         value_type=bool)

        self.assertIsInstance(d, libgiza.typed_dict.TypedDict)

        d = libgiza.typed_dict.TypedDict(key_type=basestring,
                                         value_type=bool)

        self.assertIsInstance(d, libgiza.typed_dict.TypedDict)

    def test_object_initialization_with_invalid_inputs(self):
        with self.assertRaises(TypeError):
            libgiza.typed_dict.TypedDict()

        with self.assertRaises(TypeError):
            libgiza.typed_dict.TypedDict("1", 2)

        with self.assertRaises(TypeError):
            libgiza.typed_dict.TypedDict(bool, 2)

        with self.assertRaises(TypeError):
            libgiza.typed_dict.TypedDict(2, bool)

        with self.assertRaises(TypeError):
            libgiza.typed_dict.TypedDict({})

        with self.assertRaises(TypeError):
            libgiza.typed_dict.TypedDict("1", 2, {})

        with self.assertRaises(TypeError):
            libgiza.typed_dict.TypedDict(bool, 2, {})

        with self.assertRaises(TypeError):
            libgiza.typed_dict.TypedDict(2, bool, {})

    def test_check_persistence_of_values_set_after_creation(self):
        d = libgiza.typed_dict.TypedDict(basestring, bool)
        d["foo"] = True
        self.assertEquals(True, d["foo"])

    def test_abc_implementations_return_correctly_typed_values(self):
        d = libgiza.typed_dict.TypedDict(basestring, bool)

        self.assertIsInstance(d.check_key("foo"), list)
        self.assertIsInstance(d.check_value(True), list)
        self.assertIsInstance(d.check_pair("foo", True), list)

    def test_creation_of_objects_works_correctly_with_input_base_object(self):
        for base in [{"foo": True, "bar": False}, [("foo", True), ("bar", False)],
                     {"baz": False}, [("baz", False)], {}, [], tuple()]:
            d = libgiza.typed_dict.TypedDict(basestring, bool)
            d.ingest(base)
            self.assertTrue(len(d) == len(base))


class Fake(object):
    def __init__(self, left, right):
        self.value = (left, right)
        self.validate_results = []

    def validate(self):
        return self.validate_results


class FakeTypedDict(libgiza.typed_dict.TypedDict):
    def __init__(self, *args):
        super(FakeTypedDict, self).__init__(key_type=Fake,
                                            value_type=Fake)
        self.ingest(args)
        self.pair_results = []

    def check_key(self, key):
        return key.validate()

    def check_value(self, value):
        return value.validate()

    def check_pair(self, key, value):
        return self.pair_results


class TestTypedDictionaryOperations(unittest.TestCase):
    def setUp(self):
        self.d = FakeTypedDict()
        self.key = Fake(1, 2)
        self.value = Fake(2, 3)

    def test_fake_object_exists_with_correct_types(self):
        self.assertIsInstance(self.d, FakeTypedDict)
        self.assertIsInstance(self.d, libgiza.typed_dict.TypedDict)
        self.assertIsInstance(self.d, dict)

    def test_setting_object_invalid_types_raises_type_errors(self):
        self.assertTrue(len(self.d) == 0)

        pairs = [
            (1, 1),
            (True, False),
            (1, True),
            (False, 0),
            (None, True),
            (False, None),
            ("string value", 3),
            (4, "string value"),
            (Fake(1, 2), 3),
            (Fake(2, 3), "3"),
            (Fake(4, 5), True),
            (3, Fake(5, 6)),
            ("4", Fake(6, 7)),
            (None, Fake(7, 8))
        ]

        for k, v in pairs:
            with self.assertRaises(TypeError):
                self.d[k] = v

        self.assertTrue(len(self.d) == 0)

    def test_setting_object_valid_data_allows_recall(self):
        self.d[self.key] = self.value

        self.assertIs(self.value, self.d[self.key])
        self.assertTrue(len(self.d) == 1)

    def test_setting_object_with_invalid_key_raises_value_error(self):
        self.key.validate_results.append("key has an error")

        with self.assertRaises(ValueError):
            self.d[self.key] = self.value

    def test_setting_object_with_invalid_value_raises_value_error(self):
        self.value.validate_results.append("value has an error")

        with self.assertRaises(ValueError):
            self.d[self.key] = self.value

    def test_setting_object_with_invalid_value_and_key_raises_value_error(self):
        self.key.validate_results.append("key has an error")
        self.value.validate_results.append("value has an error")

        with self.assertRaises(ValueError):
            self.d[self.key] = self.value

    def test_setting_with_invalid_pair_raises_value_error(self):
        self.d.pair_results.append("an object has errors")

        with self.assertRaises(ValueError):
            self.d[self.key] = self.value

    def test_abc_implementations_of_checks_return_list_values(self):
        self.assertIsInstance(self.d.check_key(self.key), list)
        self.assertIsInstance(self.d.check_value(self.value), list)
        self.assertIsInstance(self.d.check_pair(self.key, self.value), list)

    def test_check_functions_raise_exception(self):
        def bad_pair_validator(self, key, value):
            raise AttributeError("error")

        self.d.check_pair = bad_pair_validator

        with self.assertRaises(ValueError):
            self.d[self.key] = self.value


class LatestReleaseDownloads(libgiza.typed_dict.TypedDict):
    def __init__(self, *args):
        super(LatestReleaseDownloads, self).__init__(key_type=basestring,
                                                     value_type=basestring)
        self.ingest(args)

    def check_key(self, key):
        return []

    def check_value(self, value):
        errors = []

        if "win" in value:
            if not value.endswith(".zip"):
                errors.append("windows binaries must end with .zip, not: " + value)
        else:
            if not value.endswith(".tgz"):
                errors.append("unix-like packages should end with .tgz: " + value)

        return errors

    def check_pair(self, key, value):
        errors = []

        if key.replace("_", "-", 1) not in value:
            errors.append("key '{0}' is not in value '{1}'".format(key, value))

        return errors


class LatestReleaseDict(libgiza.typed_dict.TypedDict):
    def __init__(self, *args):
        super(LatestReleaseDict, self).__init__(key_type=basestring,
                                                value_type=LatestReleaseDocument)
        self.ingest(args)

    def check_key(self, key):
        return []

    def check_value(self, value):
        if value.validate():
            return []
        else:
            return ["latest release does not validate: " + str(value)]

    def check_pair(self, key, value):
        return []


class LatestReleaseDocument(libgiza.config.ConfigurationBase):
    _option_registry = ["major", "minor", "maintenance"]

    @property
    def version(self):
        return self.state["version"]

    @version.setter
    def version(self, value):
        self.state["version"] = value

    @property
    def date(self):
        return self.state["date"]

    @date.setter
    def date(self, value):
        date_format = "%m/%d/%Y"
        if isinstance(value, datetime.datetime):
            self.state["date"] = value.strftime(date_format)
        elif isinstance(value, basestring):
            # pass through a datetime time object to make sure its valid and
            # well formed.
            self.state["date"] = datetime.datetime.strptime(value,
                                                            date_format).strftime(date_format)
        else:
            raise TypeError("invalid date value: {0}".format(value))

    @property
    def rc(self):
        if "rc" not in self.state:
            return False
        else:
            return self.state["rc"]

    @rc.setter
    def rc(self, value):
        if isinstance(value, bool):
            self.state["rc"] = value
        else:
            raise TypeError("{0} is not a valid 'rc' value".format(value))

    @property
    def downloads(self):
        if "downloads" not in self.state:
            self.state["downloads"] = LatestReleaseDownloads()

        return self.state["downloads"]

    @downloads.setter
    def downloads(self, value):
        self.state["downloads"] = LatestReleaseDownloads(value)

    def validate(self):
        errors = 0
        for key in ("rc", "version", "major", "minor", "maintenance", "date", "downloads"):
            if key not in self.state:
                errors += 1

        for platform, url in self.downloads.items():
            for i in itertools.chain(self.downloads.check_pair(platform, url),
                                     self.downloads.check_key(platform),
                                     self.downloads.check_value(url)):
                errors += 1

            if self.version not in url:
                errors += 1

        if errors > 0:
            return False
        else:
            return True


class TestLatestReleaseTypedDict(unittest.TestCase):
    def setUp(self):
        self.d = LatestReleaseDict()
        self.value = LatestReleaseDocument()
        self.value.version = "2.2.2"
        self.value.major = 2
        self.value.minor = 2
        self.value.maintenance = 2
        self.value.rc = False
        self.value.date = "1/16/2014"
        self.value.downloads = {"foo": "https://fastdl.mongodb.org/foo/mongodb-2.2.2-foo.tgz"}

    def test_adding_version(self):
        self.d["2.2"] = self.value
        self.assertIs(self.value, self.d["2.2"])

    def test_creation_from_existing_object(self):
        self.d["2.2"] = self.value

        o = LatestReleaseDict(self.d)
        self.assertEquals(o["2.2"], self.d["2.2"])

    def test_adding_version_with_missing_value(self):
        del self.value.state["date"]

        with self.assertRaises(ValueError):
            self.d["2.2"] = self.value
