

import threading
from typing import Any, Dict, Tuple

import grpc
from google.protobuf.json_format import MessageToDict
from google.protobuf.timestamp_pb2 import Timestamp

from ..common.logger import MetisLogger
from ..common.server import get_server
from ..common.types import ServerParams
from ..proto import (learner_pb2, learner_pb2_grpc, model_pb2,
                     service_common_pb2)
from .controller_client import GRPCClient
from .learner import (Learner, try_call_evaluate, try_call_get_weights,
                      try_call_set_weights, try_call_train)
from .task_manager import TaskManager
from .message_helper import MessageHelper


class LearnerServer(learner_pb2_grpc.LearnerServiceServicer):

    def __init__(
        self,
        learner: Learner,
        client: GRPCClient,
        message_helper: MessageHelper,
        task_manager: TaskManager,
        server_params: ServerParams,
    ):
        """The Learner server. Impliments the LearnerServiceServicer endponits.

        Parameters
        ----------
        learner : Learner
            The Learner object. Must impliment the Learner interface.
        client : GRPCControllerClient
            The client object. Used to communicate with the controller.
        message_helper : MessageHelper
            The message helper object. Used to convert ProtoBuf objects
        task_manager : TaskManager
            The task manager object. Udse to run tasks in a pool of workers.
        server_params : ServerParams
            The server parameters of the Learner server.

        """
        self._learner = learner
        self._client = client
        self._message_helper = message_helper
        self._task_manager = task_manager

        self._status = service_common_pb2.ServingStatus.UNKNOWN
        self._shutdown_event = threading.Event()
        self._server_params = server_params

        self._server = get_server(
            server_params=server_params,
            servicer=self,
            add_servicer_to_server_fn=learner_pb2_grpc.add_LearnerServiceServicer_to_server,
        )

    def start(self):
        """Starts the server. This is a blocking call and will block until the server is shutdown."""

        self._server.start()

        if self._server:
            self._status = service_common_pb2.ServingStatus.SERVING
            MetisLogger.info("Learner server started. Listening on: {}:{}".format(
                self._server_params.hostname,
                self._server_params.port,
            ))
            self._shutdown_event.wait()
        else:
            # TODO: Should we raise an exception here?
            MetisLogger.error("Learner server failed to start.")

    def GetHealthStatus(self) -> service_common_pb2.HealthStatusResponse:
        """Returns the health status of the server."""

        return service_common_pb2.HealthStatusResponse(
            status=self._status,
        )

    def GetModel(
        self,
        _: service_common_pb2.Empty,
        context: Any
    ) -> model_pb2.Model:
        """Initializes the weights of the model.

        Parameters
        ----------
        _ : service_common_pb2.Empty
            An empty request. No parameters are needed.
        context : Any
            The gRPC context of the request.

        Returns
        -------
        model_pb2.Model
            The ProtoBuf object containing the model.

        """
        if not self._is_serving(context):
            return None

        weights = try_call_get_weights(
            learner=self._learner,
        )

        return self._message_helper.weights_to_model_proto(weights)

    def SetInitialModel(
        self,
        model: model_pb2.Model,
        context: Any
    ) -> service_common_pb2.Ack:
        """Sets the initial weights of the model.

        Parameters
        ----------
        request : model_pb2.Model
            The ProtoBuf object containing the model.
        context : Any
            The gRPC context of the request.

        Returns
        -------
        learner_pb2.SetInitialModelResponse
            The response containing the acknoledgement. The acknoledgement contains the status, i.e. True if the weights were set, False otherwise.
        """

        if not self._is_serving(context):
            return service_common_pb2.Ack(status=False)

        weights = self._message_helper.model_proto_to_weights(model)

        status = try_call_set_weights(
            learner=self._learner,
            weights=weights,
        )

        return service_common_pb2.Ack(
            status=status,
            timestamp=Timestamp().GetCurrentTime()
        )

    def Evaluate(
        self,
        request: learner_pb2.EvaluateRequest,
        context: Any
    ) -> learner_pb2.EvaluateResponse:
        """Evaluation endpoint. Evaluates the given model.

        Parameters
        ----------
        request : learner_pb2.EvaluateRequest
            The request containing the model and evaluation parameters.
        context : Any
            The gRPC context of the request.

        Returns
        -------
        learner_pb2.EvaluateResponse
            The response containing the evaluation metrics.
        """
        if not self._is_serving(context):
            return learner_pb2.EvaluateResponse(ack=None)

        weights = self._message_helper.model_proto_to_weights(request.model)
        params = MessageToDict(request.params)

        metrics = try_call_evaluate(
            learner=self._learner,
            weights=weights,
            params=params,
        )

        return learner_pb2.EvaluateResponse(
            task_id=request.task_id,
            results=learner_pb2.EvaluationResults(
                metrics=metrics,
            ),
        )

    def Train(
        self,
        request: learner_pb2.TrainRequest,
        context: Any
    ) -> service_common_pb2.Ack:
        """Training endpoint. Training happens asynchronously in a seperate process. 
            The Learner server responds with an acknoledgement after receiving the request.
            When training is done, the client calls the TrainDone Controller endpoint.

        Parameters
        ----------
        request : learner_pb2.TrainRequest
            The request containing the model and training parameters.
        context : Any
            The gRPC context of the request.

        Returns
        -------
        service_common_pb2.Ack
            The response containing the acknoledgement. 
            The acknoledgement contains the status, i.e. True if the training was started, False otherwise.

        """
        if not self._is_serving(context):
            return service_common_pb2.Ack(status=False)

        task_id: str = request.task_id
        weights = self._message_helper.model_proto_to_weights(request.model)
        params = MessageToDict(request.params)

        def train_out_to_callback_fn(train_out: Tuple[Any]) -> Tuple[Any]:
            return (
                task_id,
                train_out[0],  # weights
                train_out[1],  # metrics
                train_out[2],  # metadata
            )

        self._task_manager.run_task(
            task_fn=try_call_train,
            task_kwargs={
                'learner': self._learner,
                'weights': weights,
                'params': params,
            },
            callback=self._client.train_done,
            task_out_to_callback_fn=train_out_to_callback_fn,
        )

        return service_common_pb2.Ack(
            status=True,
            timestamp=Timestamp().GetCurrentTime(),
        )

    def ShutDown(self) -> service_common_pb2.Ack:
        """Shuts down the server."""

        self._status = service_common_pb2.ServingStatus.NOT_SERVING
        self._shutdown_event.set()

        return service_common_pb2.Ack(
            status=True,
            timestamp=Timestamp().GetCurrentTime(),
        )

    def _is_serving(self, context) -> bool:
        """Returns True if the server is serving, False otherwise."""

        if self._status != service_common_pb2.ServingStatus.SERVING:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            return False
        return True