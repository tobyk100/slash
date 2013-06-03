import itertools
import shakedown
from .utils import TestCase
from .utils import run_tests_assert_success
from .utils.event_recorder import EventRecorder

_recorder = None

class _SampleContextBase(shakedown.TestContext):
    def before(self):
        self._record("before")
    def after(self):
        self._record("after")
    def before_case(self):
        self._record("before_case")
    def after_case(self):
        self._record("after_case")
    def _record(self, event_name):
        event_name = "{0}.{1}".format(type(self).__name__, event_name)
        if "_case" in event_name:
            test = shakedown.context.test
            event_name += "({0}.{1})".format(
                type(test).__name__,
                test._test_method_name,
            )
        _recorder.record(event_name)

class Context1(_SampleContextBase):
    pass

class Context2(_SampleContextBase):
    pass

class EventRecordingTest(TestCase):
    def setUp(self):
        super(EventRecordingTest, self).setUp()
        global _recorder
        self._events = EventRecorder()
        _recorder = self._events
    def tearDown(self):
        global _recorder
        _recorder = None
        super(EventRecordingTest, self).tearDown()

class MultipleContextsTest(EventRecordingTest):
    def test_multiple_contexts(self):
        @shakedown.with_context(Context1)
        @shakedown.with_context(Context2)
        class Test1(shakedown.Test):
            def test_1(self):
                assert _recorder["Context1.before_case(Test1.test_1)"].timestamp < \
                       _recorder["Context2.before_case(Test1.test_1)"].timestamp, "Context1 did not happen before Context2"

        @shakedown.with_context(Context2)
        class Test2(shakedown.Test):
            def test_1(self):
                assert "Context1.before_case(Test2.test_1)" not in _recorder.events, "Context1 unexpectedly called"
                assert _recorder.events["Context2.before_case(Test2.test_1)"].happened

        run_tests_assert_success(itertools.chain(Test1.generate_tests(), Test2.generate_tests()))
