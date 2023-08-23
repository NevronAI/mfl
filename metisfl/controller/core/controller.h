
#ifndef METISFL_METISFL_CONTROLLER_CORE_CONTROLLER_H_
#define METISFL_METISFL_CONTROLLER_CORE_CONTROLLER_H_

#include <glog/logging.h>
#include <google/protobuf/util/time_util.h>
#include <grpcpp/client_context.h>
#include <grpcpp/completion_queue.h>
#include <grpcpp/create_channel.h>
#include <grpcpp/impl/codegen/async_unary_call.h>

#include <mutex>
#include <string>
#include <thread>
#include <utility>
#include <vector>

#include "absl/container/flat_hash_map.h"
#include "absl/memory/memory.h"
#include "absl/status/statusor.h"
#include "metisfl/controller/common/bs_thread_pool.h"
#include "metisfl/controller/common/macros.h"
#include "metisfl/controller/common/proto_tensor_serde.h"
#include "metisfl/controller/core/controller_utils.h"
#include "metisfl/controller/core/model_manager.h"

namespace metisfl::controller {

class Controller {
 public:
  virtual ~Controller() = default;

  virtual const ServerParams &GetServerParams() const = 0;

  virtual std::vector<std::string> GetLearnerIds() const = 0;

  virtual uint32_t GetNumLearners() const = 0;

  virtual const FederatedModel &CommunityModel() const = 0;

  virtual absl::Status SetInitialModel(const Model &model) = 0;

  virtual absl::StatusOr<std::string> AddLearner(
      const LearnerDescriptor &learner) = 0;

  virtual absl::Status StartTraining() = 0;

  virtual absl::Status RemoveLearner(const std::string &learner_id) = 0;

  virtual absl::Status TrainDone(const TrainDoneRequest &task) = 0;

  virtual TrainingMetadataMap GetTrainingMetadata() = 0;

  virtual EvaluationMetadataMap GetEvaluationMetadata() = 0;

  virtual RuntimeMetadataMap GetRuntimeMetadata() = 0;

  virtual std::string GenerateTaskId() = 0;

  virtual void Shutdown() = 0;

 private:
  std::unique_ptr<ModelManager> model_manager_;

  GlobalTrainParams global_train_params_;

  std::mutex learners_mutex_;
  BS::thread_pool scheduling_pool_;
  LearnersMap learners_;
  LearnerStubMap learners_stub_;
  TrainParamsMap learners_train_params_;
  EvaluationParamsMap learners_eval_params_;

  TaskLearnerMap task_learner_map_;
  TrainingMetadataMap training_metadata_;
  EvaluationMetadataMap evaluation_metadata_;

  grpc::CompletionQueue run_tasks_cq_;
  grpc::CompletionQueue eval_tasks_cq_;

 public:
  static std::unique_ptr<Controller> New(
      const GlobalTrainParams &global_train_params,
      const ModelStoreParams &model_store_params);
};

}  // namespace metisfl::controller

#endif  // METISFL_METISFL_CONTROLLER_CORE_CONTROLLER_H_
