"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import google.protobuf.timestamp_pb2
import metisfl.proto.model_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class Task(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    LEARNER_ID_FIELD_NUMBER: builtins.int
    SENT_AT_FIELD_NUMBER: builtins.int
    RECEIVED_AT_FIELD_NUMBER: builtins.int
    COMPLETED_AT_FIELD_NUMBER: builtins.int
    id: builtins.str
    learner_id: builtins.str
    @property
    def sent_at(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    @property
    def received_at(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    @property
    def completed_at(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    def __init__(
        self,
        *,
        id: builtins.str = ...,
        learner_id: builtins.str = ...,
        sent_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        received_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        completed_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["completed_at", b"completed_at", "received_at", b"received_at", "sent_at", b"sent_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["completed_at", b"completed_at", "id", b"id", "learner_id", b"learner_id", "received_at", b"received_at", "sent_at", b"sent_at"]) -> None: ...

global___Task = Task

@typing_extensions.final
class TrainRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TASK_FIELD_NUMBER: builtins.int
    MODEL_FIELD_NUMBER: builtins.int
    PARAMS_FIELD_NUMBER: builtins.int
    @property
    def task(self) -> global___Task: ...
    @property
    def model(self) -> metisfl.proto.model_pb2.Model: ...
    @property
    def params(self) -> global___TrainParams: ...
    def __init__(
        self,
        *,
        task: global___Task | None = ...,
        model: metisfl.proto.model_pb2.Model | None = ...,
        params: global___TrainParams | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["model", b"model", "params", b"params", "task", b"task"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["model", b"model", "params", b"params", "task", b"task"]) -> None: ...

global___TrainRequest = TrainRequest

@typing_extensions.final
class TrainParams(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    BATCH_SIZE_FIELD_NUMBER: builtins.int
    EPOCHS_FIELD_NUMBER: builtins.int
    NUM_LOCAL_UPDATES_FIELD_NUMBER: builtins.int
    METRICS_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    batch_size: builtins.int
    epochs: builtins.int
    num_local_updates: builtins.int
    @property
    def metrics(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Metrics and metadata to be collected during training. Learner must return"""
    @property
    def metadata(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        batch_size: builtins.int = ...,
        epochs: builtins.int = ...,
        num_local_updates: builtins.int = ...,
        metrics: collections.abc.Iterable[builtins.str] | None = ...,
        metadata: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["batch_size", b"batch_size", "epochs", b"epochs", "metadata", b"metadata", "metrics", b"metrics", "num_local_updates", b"num_local_updates"]) -> None: ...

global___TrainParams = TrainParams

@typing_extensions.final
class EvaluateRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TASK_FIELD_NUMBER: builtins.int
    MODEL_FIELD_NUMBER: builtins.int
    PARAMS_FIELD_NUMBER: builtins.int
    @property
    def task(self) -> global___Task: ...
    @property
    def model(self) -> metisfl.proto.model_pb2.Model: ...
    @property
    def params(self) -> global___EvaluationParams: ...
    def __init__(
        self,
        *,
        task: global___Task | None = ...,
        model: metisfl.proto.model_pb2.Model | None = ...,
        params: global___EvaluationParams | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["model", b"model", "params", b"params", "task", b"task"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["model", b"model", "params", b"params", "task", b"task"]) -> None: ...

global___EvaluateRequest = EvaluateRequest

@typing_extensions.final
class EvaluationParams(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    BATCH_SIZE_FIELD_NUMBER: builtins.int
    METRICS_FIELD_NUMBER: builtins.int
    batch_size: builtins.int
    @property
    def metrics(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        batch_size: builtins.int = ...,
        metrics: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["batch_size", b"batch_size", "metrics", b"metrics"]) -> None: ...

global___EvaluationParams = EvaluationParams

@typing_extensions.final
class EvaluateResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TASK_FIELD_NUMBER: builtins.int
    RESULTS_FIELD_NUMBER: builtins.int
    @property
    def task(self) -> global___Task: ...
    @property
    def results(self) -> global___EvaluationResults: ...
    def __init__(
        self,
        *,
        task: global___Task | None = ...,
        results: global___EvaluationResults | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["results", b"results", "task", b"task"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["results", b"results", "task", b"task"]) -> None: ...

global___EvaluateResponse = EvaluateResponse

@typing_extensions.final
class EvaluationResults(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class MetricsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.float
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.float = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    METRICS_FIELD_NUMBER: builtins.int
    @property
    def metrics(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.float]: ...
    def __init__(
        self,
        *,
        metrics: collections.abc.Mapping[builtins.str, builtins.float] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["metrics", b"metrics"]) -> None: ...

global___EvaluationResults = EvaluationResults