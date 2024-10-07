### Duplicate bug report detection

This is the README.md file for replicating the fine-tuning for dup br detection of the RepresentThemAll model. All the credit for the dataset and the model fine-tuning code go to them. We just adjusted some things and replicated their work.

```bash
bash run_dup_br_detection.sh
```

Note that you should replace the input of the following three parameters with the path that you store the [dataset](https://drive.google.com/drive/folders/1gPnZbgOO4XiBBsyF27jS--XwhHaInxlQ):

- --train_file
- --validation_file
- --test_file

### Results
We ran the fine-tuned RTA model on their test dataset and got the following evaluation results:

### Test Data Overview

| Metric                         | Value  |
|---------------------------------|--------|
| **Number of Test Data**         | 15,288 |
| **Number of Duplicates**        | 11,088 |
| **Number of Non-duplicates**    | 4,200  |

### Evaluation Results

| Metric      | Value     |
|-------------|-----------|
| **Accuracy**| 97.3051%  |
| **Precision**| 97.4576% |
| **Recall**  | 98.8637%  |




If you want to fine-tune RTA with multiple GPUs, you can use the following command:
```python
CUDA_LAUNCH_BLOCKING=1 python -m torch.distributed.launch \
  --nproc_per_node 4 run_dup_br_detection.py \
  --model_name_or_path Colorful/RTA \
  --train_file ./open_office/train.csv \
  --validation_file ./open_office/valid.csv \
  --test_file ./open_office/test.csv \
  --cache_dir ./cache_dir \
  --do_train \
  --do_eval \
  --do_predict \
  --max_seq_length 256 \
  --per_device_train_batch_size 32 \
  --learning_rate 5e-6 \
  --num_train_epochs 10 \
  --save_steps 10000 \
  --output_dir ./openoffice_results
```


