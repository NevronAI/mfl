// MIT License
//
// Copyright (c) 2021 Project Metis
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#include "projectmetis/controller/controller.h"

#include <memory>

#include <gtest/gtest.h>

namespace projectmetis::controller {
namespace {

class ControllerTest : public ::testing::Test {
public:
  static std::unique_ptr<Controller> CreateEmptyController() {
    // A controller with no registered learner.
    return Controller::New(ControllerParams());
  }

  static std::unique_ptr<Controller> CreateController() {
    // A controller with a single registered learner.
    auto controller = Controller::New(ControllerParams());

    auto learner = ServerEntity();
    learner.set_hostname("localhost");
    learner.set_port(1991);

    auto dataset = LocalDatasetSpec();
    dataset.set_num_training_examples(1);
    dataset.set_num_validation_examples(1);
    dataset.set_num_test_examples(1);

    EXPECT_TRUE(controller->AddLearner(learner, dataset).ok());

    return controller;
  }
};

TEST_F(ControllerTest, GetParamsNotEmpty) /* NOLINT */ {
  auto controller = CreateEmptyController();

  const auto params = controller->GetParams();
  EXPECT_TRUE(params.IsInitialized());
}

TEST_F(ControllerTest, GetLearnersEmpty) /* NOLINT */ {
  auto controller = CreateEmptyController();

  const auto learners = controller->GetLearners();
  EXPECT_TRUE(learners.empty());
}

TEST_F(ControllerTest, GetLearnersNotEmpty) /* NOLINT */ {
  auto controller = CreateController();

  const auto learners = controller->GetLearners();
  EXPECT_FALSE(learners.empty());
}

TEST_F(ControllerTest, AddLearnerNewEntity) /* NOLINT */ {
  auto controller = CreateEmptyController();

  auto learner = ServerEntity();
  learner.set_hostname("localhost");
  learner.set_port(1991);

  auto dataset = LocalDatasetSpec();
  dataset.set_num_training_examples(1);
  dataset.set_num_validation_examples(1);
  dataset.set_num_test_examples(1);

  auto status = controller->AddLearner(learner, dataset);

  EXPECT_TRUE(status.ok());
}

TEST_F(ControllerTest, AddLearnerExistingEntity) /* NOLINT */ {
  auto controller = CreateController();

  auto learner = ServerEntity();
  learner.set_hostname("localhost");
  learner.set_port(1991);

  auto dataset = LocalDatasetSpec();
  dataset.set_num_training_examples(1);
  dataset.set_num_validation_examples(1);
  dataset.set_num_test_examples(1);

  auto status = controller->AddLearner(learner, dataset);

  EXPECT_FALSE(status.ok());
}

TEST_F(ControllerTest, AddLearnerEmptyFields) /* NOLINT */ {
  auto controller = CreateController();

  auto status = controller->AddLearner(ServerEntity(), LocalDatasetSpec());
  EXPECT_FALSE(status.ok());
}

TEST_F(ControllerTest, RemoveLearnerExistingEntity) /* NOLINT */ {
  auto controller = CreateController();
  auto learners = controller->GetLearners();

  // We already know that the Controller is initialized with a single learner
  // therefore the 0 index on the returned vector.
  auto status = controller->RemoveLearner(learners[0].learner_id(),
                                          learners[0].auth_token());
  EXPECT_TRUE(status.ok());
}

TEST_F(ControllerTest, RemoveLearnerExistingEntityWrongToken) /* NOLINT */ {
  auto controller = CreateController();
  auto learners = controller->GetLearners();

  // We already know that the Controller is initialized with a single learner
  // therefore the 0 index on the returned vector.
  auto status = controller->RemoveLearner(learners[0].learner_id(),
                                          "foobar");
  EXPECT_FALSE(status.ok());
}

TEST_F(ControllerTest, RemoveLearnerNotExistingEntity) /* NOLINT */ {
  auto controller = CreateEmptyController();

  auto status = controller->RemoveLearner("foo", "bar");
  EXPECT_FALSE(status.ok());
}

TEST_F(ControllerTest, RemoveLearnerEmptyFields) /* NOLINT */ {
  auto controller = CreateEmptyController();

  auto status = controller->RemoveLearner(std::string(), std::string());
  EXPECT_FALSE(status.ok());

  status = controller->RemoveLearner("foobar", std::string());
  EXPECT_FALSE(status.ok());

  status = controller->RemoveLearner(std::string(), "foobar");
  EXPECT_FALSE(status.ok());
}

} // namespace
} // namespace projectmetis::controller