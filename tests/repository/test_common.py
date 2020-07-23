# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name
"""Tests for the :mod:`aiida.repository.common` module."""
import pytest

from aiida.repository import FileObject, FileType


@pytest.fixture
def file_object() -> FileObject:
    """Test fixture to create and return a ``FileObject`` instance."""
    name = 'relative'
    file_type = FileType.DIRECTORY
    key = None
    objects = {'sub': FileObject('sub', file_type=FileType.FILE, key='abcdef')}
    return FileObject(name, file_type, key, objects)


def test_constructor():
    """Test the constructor defaults."""
    file_object = FileObject()
    assert file_object.name == ''
    assert file_object.file_type == FileType.DIRECTORY
    assert file_object.key is None
    assert file_object.objects == {}


def test_constructor_kwargs(file_object: FileObject):
    """Test the constructor specifying specific keyword arguments."""
    name = 'relative'
    file_type = FileType.DIRECTORY
    key = None
    objects = {'sub': FileObject()}
    file_object = FileObject(name, file_type, key, objects)

    assert file_object.name == name
    assert file_object.file_type == file_type
    assert file_object.key == key
    assert file_object.objects == objects

    name = 'relative'
    file_type = FileType.FILE
    key = 'abcdef'
    objects = None
    file_object = FileObject(name, file_type, key, objects)

    assert file_object.name == name
    assert file_object.file_type == file_type
    assert file_object.key == key
    assert file_object.objects == {}


def test_constructor_kwargs_invalid():
    """Test the constructor specifying invalid keyword arguments."""
    name = 'relative'
    file_type = FileType.FILE
    key = 'abcdef'
    objects = {'sub': FileObject()}

    with pytest.raises(TypeError):
        FileObject(None, file_type, key, objects)

    with pytest.raises(TypeError):
        FileObject(name, None, key, objects)

    with pytest.raises(TypeError):
        FileObject(name, file_type, 123, objects)

    with pytest.raises(ValueError, match=r'an object of type `FileType.FILE` cannot define any objects.'):
        FileObject(name, FileType.FILE, key, {})

    with pytest.raises(ValueError, match=r'an object of type `FileType.DIRECTORY` cannot define a key.'):
        FileObject(name, FileType.DIRECTORY, key, {})


def test_serialize():
    """Test the ``FileObject.serialize`` method."""
    objects = {
        'empty': FileObject('empty', file_type=FileType.DIRECTORY),
        'file.txt': FileObject('file.txt', file_type=FileType.FILE, key='abcdef'),
    }
    file_object = FileObject(file_type=FileType.DIRECTORY, objects=objects)

    expected = {
        'o': {
            'empty': {},
            'file.txt': {
                'k': 'abcdef',
            }
        }
    }

    assert file_object.serialize() == expected


def test_serialize_roundtrip(file_object: FileObject):
    """Test the serialization round trip."""
    serialized = file_object.serialize()
    reconstructed = FileObject.from_serialized(serialized, file_object.name)

    assert isinstance(reconstructed, FileObject)
    assert file_object == reconstructed


def test_eq():
    """Test the ``FileObject.__eq__`` method."""
    file_object = FileObject()

    # Identity operation
    assert file_object == file_object  # pylint: disable=comparison-with-itself

    # Identical default copy
    assert file_object == FileObject()

    # Identical copy with different arguments
    assert FileObject(name='custom', file_type=FileType.FILE) == FileObject(name='custom', file_type=FileType.FILE)

    # Identical copies with nested objects
    assert FileObject(objects={'sub': FileObject()}) == FileObject(objects={'sub': FileObject()})

    assert file_object != FileObject(name='custom')
    assert file_object != FileObject(file_type=FileType.FILE)
    assert file_object != FileObject(key='123456', file_type=FileType.FILE)
    assert file_object != FileObject(objects={'sub': FileObject()})

    # Test ordering of nested files:
    objects = {
        'empty': FileObject('empty', file_type=FileType.DIRECTORY),
        'file.txt': FileObject('file.txt', file_type=FileType.FILE, key='abcdef'),
    }
    file_object_a = FileObject(file_type=FileType.DIRECTORY, objects=objects)
    objects = {
        'file.txt': FileObject('file.txt', file_type=FileType.FILE, key='abcdef'),
        'empty': FileObject('empty', file_type=FileType.DIRECTORY),
    }
    file_object_b = FileObject(file_type=FileType.DIRECTORY, objects=objects)

    assert file_object_a == file_object_b
