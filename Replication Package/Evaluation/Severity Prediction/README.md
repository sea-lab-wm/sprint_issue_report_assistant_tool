### Severity Prediction

This is the README.md file for replicating the fine-tuning for severity prediction of the RepresentThemAll model. All the credits for the dataset and the model fine-tuning code go to them. We just adjusted some things and replicated their work.

```bash
bash run_severity_pred_fine_tune.sh
```

Note that you should replace the input of the following three parameters with the path that you store the [dataset](https://drive.google.com/drive/folders/1gPnZbgOO4XiBBsyF27jS--XwhHaInxlQ):

- --train_file
- --validation_file
- --test_file

### Results
We ran the fine-tuned RTA model on their test dataset and got the following evaluation results:


### Test Data Overview

| Metric                         | Value                                        |
|--------------------------------|----------------------------------------------|
| **Number of Test Data**        | 15,510                                       |
| **Classification Labels**      | Trivial, Minor, Major, Critical, Blocker     |

### Evaluation Results

| Metric       | Value     |
|--------------|-----------|
| **Accuracy** | 65.5899%  |
| **Precision**| 66.2795%  |
| **Recall**   | 65.5899%  |



If you want to fine-tune RTA with multiple GPUs, you can use the following command:
```python
CUDA_LAUNCH_BLOCKING=1 python run_br_pred.py \
  --model_name_or_path Colorful/RTA \
  --train_file ./dataset/priority_train.csv \
  --validation_file ./dataset/priority_valid.csv \
  --test_file ./dataset/priority_test.csv \
  --cache_dir ./cache_dir \
  --do_train \
  --do_eval \
  --do_predict \
  --max_seq_length 256 \
  --per_device_train_batch_size 32 \
  --learning_rate 5e-6 \
  --num_train_epochs 10 \
  --save_steps 10000 \
  --output_dir ./results_priority
```