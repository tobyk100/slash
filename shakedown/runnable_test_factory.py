from .metadata import ensure_shakedown_metadata

class RunnableTestFactory(object):

    @classmethod
    def generate_tests(cls):
        """
        Generates :class:`.RunnableTest` instances to run

        Do not override this method directly. Use :func:`.RunnableTestFactory._generate_tests` instead.
        """
        for test in cls._generate_tests():
            ensure_shakedown_metadata(test).factory = cls
            yield test

    @classmethod
    def _generate_tests(cls):
        raise NotImplementedError() # pragma: no cover

    __shakedown_needed_contexts__ = None

