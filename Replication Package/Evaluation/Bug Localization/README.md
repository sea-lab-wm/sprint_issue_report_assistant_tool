### Bug Localization

This is the README.md file for replicating approach applied in the Long Code Arena paper. All the credit for the dataset goes to them. 

We cloned and ran the baseline scripts from [this](https://github.com/JetBrains-Research/lca-baselines/tree/main/bug_localization) repository. All the instructions for running the project and the baseline scripts are provided here.

### Results
We ran the fine-tuned **Llama-2-7b-chat** model on Long Code Arena test dataset. We ran the model 3 times for each issue since prompt-based LLM outputs slightly differ each time and we took only the results that were common in all 3 executions. We got the following evaluation results on their test dataset issues:


### Test Data Overview

| Metric                        | Value                                        |
|--------------------------------|----------------------------------------------|
| **Number of Test Issues**        | 150                                       |

### Evaluation Results

| Metric       | Value     |
|--------------|-----------|
| **Accuracy** | 34%  |
| **Recall@2**| 20%  |
| **Precision@2**   | 31%  |